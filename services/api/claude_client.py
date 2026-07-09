from anthropic import Anthropic

from config.settings import Settings


class ClaudeClient:
    def __init__(self, config: Settings):
        self.client = Anthropic(api_key=config.api_key)
        self.model = config.model
        self.max_tokens = config.max_tokens
