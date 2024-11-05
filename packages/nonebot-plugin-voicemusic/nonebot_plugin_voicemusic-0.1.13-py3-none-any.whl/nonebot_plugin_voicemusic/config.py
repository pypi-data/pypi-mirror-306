from pydantic import BaseModel

class Config(BaseModel):
    uin: str = ""
    key: str = ""