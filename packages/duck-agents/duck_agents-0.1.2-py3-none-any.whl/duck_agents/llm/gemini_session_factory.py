from duck_agents.llm.gemini import GeminiSession
from duck_agents.llm.session_factory import SessionFactory
import google.generativeai as genai

class GeminiSessionFactory(SessionFactory):
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        genai.configure(api_key=api_key)

    def create_session(self, system_prompt):
        return GeminiSession(self.model_name, system_prompt)