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
import time


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
    3. 條列重構查詢：將重構後的查詢，條列成5個子問題，每個子問題都是一個可以在網路上搜尋到的具體問題。

    以下是使用者輸入的問題:
    {search_query}

    請使用以下 JSON 格式嚴格回應,只包含問題內容,不要使用 markdown 的語法:
    {{
        "questions":[
            "第1個子問題",
            "第2個子問題",
            ...
            "最後一個子問題"
        ]
    }}
""".format(
            search_query=search_query
        )

        model_name = "anthropic/claude-3-5-sonnet-20241022"
        response = litellm.completion(
            model=model_name,
            messages=[{"role": "user", "content": generate_questions_prompt}],
            api_key=get_api_key(model_name),
        )
        return json.loads(response.choices[0].message.content)["questions"]

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
        self, user_query: str, search_results: List[Dict[str, Any]]
    ) -> List[str]:
        """使用 LLM 選擇最相關的搜尋結果"""
        analyze_search_result_prompt = """請分析以下 Google 搜尋結果，參考 snippet 的內容，選出最相關的5個網頁連結，並且彼此內容的重覆性低。
請使用以下幾個優先權來選擇:
1. 如果有政府機關的網站，請優先選擇政府機關的網站
2. 標題跟使用者問題最相關的
3. 標題包含使用者問題關鍵字的
4. 內容包含使用者問題關鍵字的
5. 網頁連結的內容重覆性低

使用者問題: {question}
搜尋結果: {items}

請務必只使用以下 JSON 格式嚴格回應，不要加上 markdown 格式:
{{
    "urls":["url1", "url2", "url3", "url4", "url5"],
}}
"""
        items = []
        for result in search_results:
            if result["status"] == "success":
                items.extend(result["items"])

        model_name = "openai/gpt-4o-2024-08-06"
        response = litellm.completion(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to output JSON.",
                },
                {
                    "role": "user",
                    "content": analyze_search_result_prompt.format(
                        question=user_query,
                        items=json.dumps(items, ensure_ascii=False, indent=2),
                    ),
                },
            ],
            api_key=get_api_key(model_name),
        )

        try:
            selected_urls = json.loads(response.choices[0].message.content)["urls"]
            print(f"selected_urls: {selected_urls}")
            return selected_urls
        except Exception as e:
            print(f"Error parsing LLM response for URL selection: {str(e)}")
            return []

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
                # timeout=15,
            ) as response:
                if response.status == 200:
                    body = await response.json()
                    print(f"[scrape_single_url] url: {url}")
                    print(
                        f"[scrape_single_url] content: {body['data']['markdown'][:100]}"
                    )
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

    async def _scrape_urls(self, selected_urls: List[str]) -> List[Dict[str, Any]]:
        """並行抓取所有 URL 的內容"""
        async with aiohttp.ClientSession() as session:

            # 一次性創建所有 URL 的抓取任務
            scrape_tasks = [
                self._scrape_single_url(url, session) for url in selected_urls
            ]

            # 同時執行所有抓取任務
            scrape_results = await asyncio.gather(*scrape_tasks)
            scrape_results = [
                scrape_result
                for scrape_result in scrape_results
                if scrape_result["status"] == "success"
            ]

            # 轉換為原來的輸出格式
            return scrape_results

    async def _note_taking_single_result(
        self, user_query: str, scrape_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """對單個抓取結果進行筆記"""
        note_taker_prompt = """你是一位資料記錄者，請分析以下網頁內容是否與問題相關，相關的話會做出詳實記錄。

原本使用者問的問題: {user_query}
網頁URL: {url}
網頁標題: {title}
網頁內容: {markdown}

如果內容相關，請：
1. 去除不必要的 html 資料，
2. 去除與使用者問題無關的行銷內容
3. 去除看起來像是廣告的內容
4. 去除看起來像是header, footer, sidebar的內容
5. 去除看起來像是版權宣告的內容
你是記錄者，不能只摘錄重點，而是要詳實的記錄網頁內容的文字。
請使用以下 JSON 格式嚴格回應，不要附加任何其它文字，不要加上 markdown 的語法:
{{
    "url": "網頁URL",
    "title": "網頁標題",
    "note": "詳實的記錄內容"
}}

如果內容不相關，請回傳空值。
請使用以下 JSON 格式嚴格回應，不要附加任何其它文字，不要加上 markdown 的語法:
{{
    "url": "",
    "title": "",
    "note": ""
}}"""

        model_name = "openai/gpt-4o-2024-08-06"
        try:
            response = litellm.completion(
                model=model_name,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant designed to output JSON.",
                    },
                    {
                        "role": "user",
                        "content": note_taker_prompt.format(
                            user_query=user_query,
                            url=scrape_result["url"],
                            title=scrape_result["title"],
                            markdown=scrape_result["content"],
                        ),
                    },
                ],
                api_key=get_api_key(model_name),
            )

            result = json.loads(response.choices[0].message.content)
            print(f"[note_taking_single_result] url: {result['url']}")
            print(f"[note_taking_single_result] title: {result['title']}")
            print(f"[note_taking_single_result] note: {result['note']}")
            return result if result.get("note") else None

        except Exception as e:
            print(f"Error in note taking for URL {scrape_result['url']}: {str(e)}")
            return None

    async def _note_taking_scrape_results(
        self, user_query: str, scrape_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """並行處理所有抓取結果的筆記"""
        # 收集所有需要做筆記的任務
        note_tasks = []

        for scrape_result in scrape_results:
            note_tasks.append(
                self._note_taking_single_result(user_query, scrape_result)
            )

        # 一次性執行所有筆記任務
        notes = await asyncio.gather(*note_tasks)
        return [note for note in notes if note is not None and note["url"] != ""]
        # 組織結果

    async def run(
        self, variable_pool: Dict[str, Dict[str, Any]]
    ) -> AsyncGenerator[NodeEvent, None]:
        try:
            time_message = []
            time_1 = time.time()
            # 1. 生成搜尋問題
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在生成搜尋問題...\n",
                is_print=self.data.print_stream,
            )
            questions = await self._get_questions(
                self.replace_variables(self.data.search_query, variable_pool)
            )
            time_2 = time.time()
            time_message.append(f"生成搜尋問題: {time_2 - time_1:.2f} 秒")
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
                chunk=f"\n正在將問題交由 Google 搜尋...\n",
                is_print=self.data.print_stream,
            )
            async with aiohttp.ClientSession() as session:
                search_tasks = [
                    self._search_question(question, session) for question in questions
                ]
                search_results = await asyncio.gather(*search_tasks)
            time_3 = time.time()
            time_message.append(f"將問題交由 Google 搜尋: {time_3 - time_2:.2f} 秒")
            # 使用 asyncio.gather 同步執行所有分析任務
            selected_urls = await self._choose_related_results(
                self.replace_variables(self.data.search_query, variable_pool),
                search_results,
            )
            time_4 = time.time()
            time_message.append(f"選擇相關搜尋結果: {time_4 - time_3:.2f} 秒")
            # print(analyzed_search_results)

            # 3. 抓取網頁內容
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在抓取網頁內容...\n",
                is_print=self.data.print_stream,
            )
            scrape_results = await self._scrape_urls(selected_urls)
            time_5 = time.time()
            time_message.append(f"抓取網頁內容: {time_5 - time_4:.2f} 秒")
            # 4. 進行筆記
            yield NodeRunStreamEvent(
                node_id=self.data.id,
                node_title=self.data.title,
                node_type=self.data.type.value,
                chunk=f"\n正在分析有效內容...\n",
                is_print=self.data.print_stream,
            )

            note_taking_results = await self._note_taking_scrape_results(
                self.replace_variables(self.data.search_query, variable_pool),
                scrape_results,
            )
            time_6 = time.time()
            time_message.append(f"進行筆記: {time_6 - time_5:.2f} 秒")
            # for result in note_taking_results:
            #     yield NodeRunStreamEvent(
            #         node_id=self.data.id,
            #         node_title=self.data.title,
            #         node_type=self.data.type.value,
            #         chunk=f"完成筆記: {result['question']} ({len(result['note_taking_results'])} 個筆記)\n",
            #         is_print=self.data.print_stream,
            #     )
            for message in time_message:
                print(message)
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
