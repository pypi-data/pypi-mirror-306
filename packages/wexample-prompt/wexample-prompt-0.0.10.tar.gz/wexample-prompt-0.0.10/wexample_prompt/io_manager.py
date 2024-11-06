import shutil
from typing import Any, List

from pydantic import BaseModel, Field

from wexample_prompt.const.colors import COLOR_RESET
from wexample_prompt.mixins.with_indent import WithIndent
from wexample_prompt.themes.default.abstract_prompt_theme import AbstractPromptTheme
from wexample_prompt.themes.default.default_prompt_theme import DefaultPromptTheme
from wexample_prompt.utils.prompt_response import PromptResponse
from wexample_prompt.utils.prompt_response_line import PromptResponseLine


class IOManager(BaseModel, WithIndent):
    theme: AbstractPromptTheme = Field(
        default_factory=DefaultPromptTheme,
        description="Allow to customize colors")
    _tty_width: int = shutil.get_terminal_size().columns

    def print_responses(self, responses: List[PromptResponse]) -> None:
        for response in responses:
            self.print_response(response)

    def print_response(self, response: PromptResponse) -> None:
        for line in response.lines:
            self.print_response_line(line, response)

    def print_response_line(self, line: PromptResponseLine, response: PromptResponse) -> None:
        if line.line_type:
            color_type = line.line_type
        else:
            color_type = response.message_type

        self.print(f'{self.build_indent()}{self.theme.get_color(color_type)}{line.message}{COLOR_RESET}')

    @staticmethod
    def print(message: Any, **kwargs: Any) -> None:
        print(message, **kwargs)
