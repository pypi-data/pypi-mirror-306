import asyncio
from typing import Any

import google.api_core.exceptions

from duck_agents.llm.base_interface import BaseInterface, Role
import google.generativeai as genai

import logging
import re
import json

_logger = logging.getLogger(__name__)

_json_regex = re.compile(r"\{.*\}", re.DOTALL)

# TODO: try constraining output to json through model configuration(?)
# TODO: Play around with settings like temperature (degree of randomness)
class GeminiSession(BaseInterface):
    def __init__(self, model_name, system_prompt):
        super().__init__(system_prompt)
        self.model = genai.GenerativeModel(model_name, system_instruction=system_prompt)
        self.chat_session = self.model.start_chat()

    async def prompt(self, prompt: str, role=Role.USER) -> dict[str, any]:
        _logger.warning("Roles not yet implemented for Gemini Wrapper. Ignoring role.")

        try:
            response = await self.chat_session.send_message_async(prompt)
        except google.api_core.exceptions.ResourceExhausted:
            _logger.warning("Gemini API resource limit exhausted, retrying in one minute.")
            await asyncio.sleep(60)
            response = await self.chat_session.send_message_async(prompt)

        _logger.info(response.text)
        _logger.info(response.usage_metadata)
        _logger.info(response.parts)

        result = {}
        try:
            # handle responses like "json {...}" where the content of the curly braces is actually valid
            result = json.loads(_json_regex.search(response.text).group(0))
        except json.JSONDecodeError as e:
            logging.error(e.msg, e.doc)
        return result

    def clear_history(self) -> None:
        self.chat_session = self.model.start_chat()

    async def retry_last(self) -> dict[str, Any]:
        last_prompt = self.chat_session.rewind()
        last_prompt_text = ""
        for part in last_prompt[1].parts:
            if part.text:
                last_prompt_text = last_prompt_text + part.text
        return await self.prompt(last_prompt_text)
