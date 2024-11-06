from typing import Optional

from pydantic import BaseModel

from wexample_prompt.const.types import LineDict
from wexample_prompt.enums.message_type import MessageType


class PromptResponseLine(BaseModel):
    message: str
    line_type: Optional[MessageType] = None

    @staticmethod
    def from_dict(line_dict: LineDict) -> 'PromptResponseLine':
        return PromptResponseLine(
            message=line_dict.get('message'),
            line_type=line_dict.get('type'),
        )

    @staticmethod
    def from_message(
        message: str,
        line_type: Optional[str] = None
    ) -> 'PromptResponseLine':
        return PromptResponseLine(
            message=message,
            line_type=line_type,
        )
