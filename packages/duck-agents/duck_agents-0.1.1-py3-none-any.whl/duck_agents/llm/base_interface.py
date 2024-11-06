import logging
from typing import Any
from enum import Enum

_logger = logging.getLogger(__name__)

class Role(Enum):
    USER = "user"
    TOOL = "tool"
    ASSISTANT = "assistant"
    SYSTEM = "system"

# TODO: move function definitions to Interface API (e.g. to google's function calling api) ?
class BaseInterface:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt

    async def prompt(self, prompt : str, role=Role.USER) -> dict[str, Any]:
        _logger.warning(
            "Trying to prompt '%s' via BaseInterface Instance. Subclass this class and provide your own implementation for a specific (family of) model(s)."
            , prompt)
        return {}

    async def retry_last(self) -> dict[str, Any]:
        _logger.warning(
            "Trying to retry_last via BaseInterface Instance. Subclass this class and provide your own implementation for a specific (family of) model(s).")
        return {}

    def clear_history(self) -> None:
        _logger.warning("Trying to clear history on BaseInterface Instance. Subclass this class and provide your own implementation for a specific (family of) model(s).")


