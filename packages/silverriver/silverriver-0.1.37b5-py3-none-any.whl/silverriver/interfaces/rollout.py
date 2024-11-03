from pydantic import BaseModel


class RolloutRequest(BaseModel):
    start_urls: list[str]
    tos_level: str = "acceptable"


class RolloutResult(BaseModel):
    output: str
    error: str
