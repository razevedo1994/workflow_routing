from schemas.router.routing import RoutingDecision
from services.api.claude_client import ClaudeClient


class Router:
    def __init__(self, claude: ClaudeClient):
        self.claude = claude

    def classify(self, user_input: str) -> RoutingDecision:
        response = self.claude.client.messages.parse(
            model=self.claude.model,
            max_tokens=self.claude.max_tokens,
            system="Classify the user's research intent. Be concise.",
            messages=[{"role": "user", "content": user_input}],
            output_format=RoutingDecision,
        )

        result = response.parsed_output

        return result
