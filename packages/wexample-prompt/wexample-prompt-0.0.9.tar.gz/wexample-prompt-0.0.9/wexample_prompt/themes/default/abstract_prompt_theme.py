from abc import ABC, abstractmethod

from pydantic import BaseModel

from wexample_prompt.enums.message_type import MessageType


class AbstractPromptTheme(BaseModel, ABC):
    @abstractmethod
    def get_color(self, message_type: MessageType) -> str:
        pass
