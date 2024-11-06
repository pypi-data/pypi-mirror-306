from json import JSONDecodeError
from typing import Any

import re
import requests
import json
import logging

from base_interface import BaseInterface, Role

_logger = logging.getLogger(__name__)

_json_regex = re.compile(r"\{.*\}", re.DOTALL)

class LlamaSession(BaseInterface):
    def __init__(self, url, model, system_prompt):
        super().__init__(system_prompt)
        self.url = url
        self.model = model
        self.history = [{
            "role": "system",
            "content": system_prompt
        }]

    async def prompt(self, prompt: str, role=Role.USER) -> dict[str, any]:
        llama_role = ""
        match role:
            case Role.USER:
                llama_role = "user"
            case Role.TOOL:
                llama_role = "ipython"
            case _:
                raise RuntimeError(f"Trying to prompt with invalid role {role}".format(role=role))

        new_message = {
            "role": llama_role,
            "content": prompt
        }

        self.history.append(new_message)

        data = {
            "model": self.model,
            "messages": self.history,
            "stream": False,
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self.url, headers=headers, json=data)
        response_content = response.json()["message"]["content"]

        self.history.append({
            "role": "assistant",
            "content": response_content
        })
        _logger.info(response_content)
        result = ""

        try:
            # handle responses like "json {...}" where the content of the curly braces is actually valid
            result = json.loads(_json_regex.search(response_content).group(0))
        except JSONDecodeError as e:
            logging.error(e.msg, e.doc)
        return result

    async def retry_last(self) -> dict[str, Any]:
        # discard last assistant prompt
        self.history.pop()
        last_prompt = self.history.pop()
        match last_prompt["role"]:
            case "user":
                role = Role.USER
            case "ipython":
                role = Role.TOOL
            case _:
                role = Role.USER
        return await self.prompt(last_prompt["content"], role)


    def clear_history(self) -> None:
        self.history = [{
            "role": "system",
            "content": self.system_prompt
        }]