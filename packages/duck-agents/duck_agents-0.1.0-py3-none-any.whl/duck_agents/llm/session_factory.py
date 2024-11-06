import logging

_logger = logging.getLogger(__name__)

class SessionFactory:
    def create_session(self, system_prompt):
        _logger.warning("Trying to create a session with SessionFactory instance. Subclass this class and provide our own implementation of create_session.")