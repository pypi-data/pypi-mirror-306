from wexample_prompt.const.colors import COLOR_GRAY, COLOR_DEFAULT
from wexample_prompt.enums.message_type import MessageType
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme


class DefaultPromptTheme(AbstractPromptTheme):
    def get_color(self, message_type: MessageType) -> str:
        return {
            MessageType.LOG: COLOR_GRAY
        }.get(message_type, COLOR_DEFAULT)
