from pydantic import BaseModel


class UserSetting(BaseModel):
    user_id: str
    default_model: str = ""
    audio_reply: bool = False
