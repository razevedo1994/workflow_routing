from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from schemas.agents.summarizer_agent import SummarizerInput, SummaryOutput
from schemas.router.content_type import ContentType
from schemas.tools.web_fetch import WebFetchInput
from services.api.claude_client import ClaudeClient
from tools.web_fetch import WebFetchTool

PROMPT_DIR = Path(__file__).parent.parent / "prompts"


class SummarizerAgent:
    """
    Receives raw content (URL text, PDF text, or plain text),
    calls Claude with a structured output schema,
    and returns a validated SummaryOutput.
    """

    def __init__(self, claude: ClaudeClient, web_fetch: WebFetchTool):
        self.claude = claude
        self._env = Environment(loader=FileSystemLoader(str(PROMPT_DIR)))
        self.web_fetch = web_fetch

    def run(self, input: SummarizerInput) -> SummaryOutput | None:
        content = self._resolve_content(input)
        system_prompt = self._render_prompt(input)

        response = self.claude.client.messages.parse(
            model=self.claude.model,
            max_tokens=self.claude.max_tokens,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            output_format=SummaryOutput,
        )

        return response.parsed_output

    def _render_prompt(self, input: SummarizerInput) -> str:
        template = self._env.get_template("summarizer.j2")
        return template.render(
            content_type=input.content_type.value,
            focus=input.focus,
            content=input.content[:500],
        )

    def _resolve_content(self, input: SummarizerInput) -> str:
        if input.content_type == ContentType.URL:
            fetched = self.web_fetch.run(WebFetchInput(url=input.content))
            if not fetched.success:
                raise RuntimeError(f"Webfetch failed: {fetched.error}")
            return fetched.content

        return input.content
