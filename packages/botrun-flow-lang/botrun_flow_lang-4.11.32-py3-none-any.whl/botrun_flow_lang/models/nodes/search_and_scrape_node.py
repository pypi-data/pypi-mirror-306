from typing import Any, AsyncGenerator, Dict, List
from botrun_flow_lang.models.nodes.base_node import BaseNode, BaseNodeData, NodeType
from botrun_flow_lang.models.nodes.event import (
    NodeEvent,
    NodeRunCompletedEvent,
    NodeRunFailedEvent,
    NodeRunStreamEvent,
)
import litellm
import json
import aiohttp
import asyncio
from botrun_flow_lang.models.nodes.llm_node import get_api_key
from urllib.parse import quote

from botrun_flow_lang.models.variable import OutputVariable
from pydantic import Field


class SearchAndScrapeNodeData(BaseNodeData):
    """
    @param results: 筆記的結果, 會是一個 List[Dict[str, Any]], dict 長這樣{"question": "","url": "","title": "","note": ""}
    """

    type: NodeType = NodeType.SEARCH_AND_SCRAPE
    search_query: str
    output_variables: List[OutputVariable] = [OutputVariable(variable_name="results")]


class SearchAndScrapeNode(BaseNode):
    data: SearchAndScrapeNodeData

    async def _get_questions(self, search_query: str) -> List[str]:
        """使用 LLM 生成搜尋問題"""
        generate_questions_prompt = """
    你是一個專業的調查員，你會依據以下問題，去網路上搜尋相關資料，並且回答使用者。
    當使用者輸入一個問題時，你會
    1. 理解查詢：理解用戶輸入的查詢。這不僅僅是簡單的關鍵字匹配，而是深入分析查詢的上下文和意圖，以便更準確地理解用戶需求。
    2. 構建查詢：在理解查詢後，你會重構查詢以應其搜索和分析模型。這包括將用戶的自然語言問題轉換為可以在網路上有效搜索的訊息格式，從而提高搜索效率和結果的相關性。
    3. 條列重構查詢：將重構後的查詢，條列成多個子問題，每個子問題都是一個可以在網路上搜尋到的具體問題。

    以下是使用者輸入的問題:
    {search_query}

    請使用以下 JSON 格式嚴格回應,只包含問題內容:
    [
        "第1個子問題",
        "第2個子問題",
        "最後一個子問題"
    ]
""".format(
            search_query=search_query
        )

        model_name = "anthropic/claude-3-5-sonnet-20241022"
        response = litellm.completion(
            model=model_name,
            messages=[{"role": "user", "content": generate_questions_prompt}],
            api_key=get_api_key(model_name),
        )
        return json.loads(response.choices[0].message.content)

    async def _search_question(
        self, question: str, session: aiohttp.ClientSession
    ) -> Dict[str, Any]:
        """執行單個問題的搜尋"""
        url = "https://botrun-flow-lang-fastapi-prod-36186877499.asia-east1.run.app/api/search"
        try:
            async with session.post(
                url,
                json={"query": question, "num": 10},
                headers={"Content-Type": "application/json"},
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "question": question,
                        "status": "success",
                        "items": result["items"],
                    }
                else:
                    return {
                        "question": question,
                        "status": "error",
                        "error": f"Search failed with status {response.status}",
                    }
        except Exception as e:
            return {"question": question, "status": "error", "error": str(e)}

    async def _choose_related_results(
        self, search_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """使用 LLM 選擇最相關的搜尋結果"""
        analyze_search_result_prompt = """請分析以下 Google 搜尋結果，參考 snippet 的內容，選出最相關的三個網頁連結。
問題: {question}
搜尋結果: {items}

請務必使用以下 JSON 格式嚴格回應:["url1", "url2", "url3"]
"""

        model_name = "openai/gpt-4o-mini"
        response = litellm.completion(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": analyze_search_result_prompt.format(
                        question=search_result["question"],
                        items=json.dumps(
                            search_result["items"], ensure_ascii=False, indent=2
                        ),
                    ),
                }
            ],
            api_key=get_api_key(model_name),
        )

        try:
            selected_urls = json.loads(response.choices[0].message.content)
            return {
                "question": search_result["question"],
                "selected_urls": selected_urls,
            }
        except Exception as e:
            print(f"Error parsing LLM response for URL selection: {str(e)}")
            return {
                "question": search_result["question"],
                "selected_urls": [],
            }

    async def _scrape_single_url(
        self, url: str, session: aiohttp.ClientSession
    ) -> Dict[str, Any]:
        """抓取單個 URL 的內容"""
        try:
            quoted_url = quote(url, safe=":/")
            scrape_url = "https://botrun-crawler-fastapi-prod-36186877499.asia-east1.run.app/scrape"

            async with session.get(
                scrape_url,
                params={"url": quoted_url},
            ) as response:
                if response.status == 200:
                    body = await response.json()
                    return {
                        "url": url,
                        "title": body["data"]["metadata"]["title"],
                        "content": body["data"]["markdown"],
                        "status": "success",
                    }
                else:
                    return {
                        "url": url,
                        "status": "error",
                        "error": f"Scraping failed with status {response.status}",
                    }
        except Exception as e:
            return {"url": url, "status": "error", "error": str(e)}

    async def _scrape_urls(
        self, analyzed_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """並行抓取所有 URL 的內容"""
        async with aiohttp.ClientSession() as session:
            # 收集所有需要抓取的 URL，並記錄它們屬於哪個問題
            url_to_question = {}
            all_urls = []
            for result in analyzed_results:
                for url in result["selected_urls"]:
                    url_to_question[url] = result["question"]
                    all_urls.append(url)

            # 一次性創建所有 URL 的抓取任務
            scrape_tasks = [self._scrape_single_url(url, session) for url in all_urls]

            # 同時執行所有抓取任務
            scrape_results = await asyncio.gather(*scrape_tasks)

            # 按問題重新組織結果
            question_to_scrapes = {}
            for scrape_result in scrape_results:
                if scrape_result["status"] == "success":
                    url = scrape_result["url"]
                    question = url_to_question[url]
                    if question not in question_to_scrapes:
                        question_to_scrapes[question] = []
                    question_to_scrapes[question].append(
                        {
                            "url": scrape_result["url"],
                            "title": scrape_result["title"],
                            "content": scrape_result["content"],
                        }
                    )

            # 轉換為原來的輸出格式
            return [
                {"question": question, "scrape_results": scrapes}
                for question, scrapes in question_to_scrapes.items()
            ]

    async def _note_taking_single_result(
        self, question: str, scrape_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """對單個抓取結果進行筆記"""
        note_taker_prompt = """你是一位資料記錄者，請分析以下網頁內容是否與問題相關，並做出詳實記錄。

用來 Google 搜尋的問題: {question}
網頁URL: {url}
網頁標題: {title}
網頁內容: {markdown}

如果內容相關，請提取相關的重要資訊並做詳實記錄。
請使用以下 JSON 格式嚴格回應，不要附加任何其它文字:
{{
    "url": "網頁URL",
    "title": "網頁標題",
    "note": "詳實的記錄內容"
}}

如果內容不相關，請回傳空值。
請使用以下 JSON 格式嚴格回應，不要附加任何其它文字:
{{
    "url": "",
    "title": "",
    "note": ""
}}"""

        model_name = "openai/gpt-4o-mini"
        try:
            response = litellm.completion(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": note_taker_prompt.format(
                            question=question,
                            url=scrape_result["url"],
                            title=scrape_result["title"],
                            markdown=scrape_result["content"],
                        ),
                    }
                ],
                api_key=get_api_key(model_name),
            )

            result = json.loads(response.choices[0].message.content)
            return result if result.get("note") else None

        except Exception as e:
            print(f"Error in note taking for URL {scrape_result['url']}: {str(e)}")
            return None

    async def _note_taking_scrape_results(
        self, scrape_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """並行處理所有抓取結果的筆記"""
        # 收集所有需要做筆記的任務
        note_tasks = []
        scrape_info = []  # 用於保存每個任務的問題信息

        for result in scrape_results:
            question = result["question"]
            for scrape_result in result["scrape_results"]:
                note_tasks.append(
                    self._note_taking_single_result(question, scrape_result)
                )
                scrape_info.append({"question": question, "url": scrape_result["url"]})

        # 一次性執行所有筆記任務
        notes = await asyncio.gather(*note_tasks)

        # 組織結果
        all_note_taking_results = []
        for note, info in zip(notes, scrape_info):
            if note is not None:
                note["question"] = info["question"]
                all_note_taking_results.append(note)

        return all_note_taking_results

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        try:
            # 1. 生成搜尋問題
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n生成搜尋問題...\n",
                is_print=self.data.print_stream,
            )
            questions = await self._get_questions(
                self.replace_variables(self.data.search_query, variable_pool)
            )
            for question in questions:
                yield NodeRunStreamEvent(
                    node_id=self.data.id,
                    node_title=self.data.title,
                    node_type=self.data.type.value,
                    chunk=f"- {question}\n",
                    is_print=self.data.print_stream,
                )

            # 2. 執行搜尋
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n將問題交由 Google 搜尋...\n",
                is_print=self.data.print_stream,
            )
            async with aiohttp.ClientSession() as session:
                search_tasks = [
                    self._search_question(question, session) for question in questions
                ]
                search_results = await asyncio.gather(*search_tasks)

            # 使用 asyncio.gather 同步執行所有分析任務
            analysis_tasks = [
                self._choose_related_results(result)
                for result in search_results
                if result["status"] == "success"
            ]
            analyzed_search_results = await asyncio.gather(*analysis_tasks)
            # print(analyzed_search_results)

            # 3. 抓取網頁內容
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n抓取網頁內容...\n",
                is_print=self.data.print_stream,
            )

            scrape_results = await self._scrape_urls(analyzed_search_results)

            # 4. 進行筆記
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n進行分析有效內容...\n",
                is_print=self.data.print_stream,
            )

            note_taking_results = await self._note_taking_scrape_results(scrape_results)

            # for result in note_taking_results:
            #     yield NodeRunStreamEvent(
            #         node_id=self.data.id,
            #         node_title=self.data.title,
            #         node_type=self.data.type.value,
            #         chunk=f"完成筆記: {result['question']} ({len(result['note_taking_results'])} 個筆記)\n",
            #         is_print=self.data.print_stream,
            #     )

            # 5. 返回最終結果
            yield NodeRunCompletedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                outputs={
                    "results": note_taking_results,
                },
                is_print=self.data.print_complete,
            )

        except Exception as e:
            yield NodeRunFailedEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                error=str(e),
                is_print=True,
            )
            raise
