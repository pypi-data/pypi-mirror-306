from typing import Any

import pydantic

SYSTEM_ROLE = "system"
HUMAN_ROLE = "user"
ASSISTANT_ROLE = "assistant"


class ChatMessage(pydantic.BaseModel):
    role: str  # TODO: make this an enum
    message: str
    timestamp: float
    message_id: int | str | None = None


class BrowserObservation(pydantic.BaseModel, extra="forbid"):
    axtree_txt: str
    screenshot_som: str  # base64 encoded image
    url: str
    network_requests: str
    last_browser_error: str


class Observation(BrowserObservation, extra="forbid"):
    chat_messages: list[ChatMessage]
    # TODO: To make this class public we should rename some fields to be more general
    last_action_error: str


class LogsRequestModel(pydantic.BaseModel):
    filename: str
    content: bytes

    def model_dump(self, **kwargs) -> dict[str, Any]:
        return {"file": (self.filename, self.content)}
