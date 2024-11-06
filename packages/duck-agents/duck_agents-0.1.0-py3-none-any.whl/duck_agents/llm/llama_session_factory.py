from llama import LlamaSession
from session_factory import SessionFactory
import logging

_logger = logging.getLogger(__name__)

class LlamaSessionFactory(SessionFactory):
    def __init__(self, url, model):
        self.url = url
        self.model = model

    def create_session(self, system_prompt):
        return LlamaSession(self.url, self.model, system_prompt)