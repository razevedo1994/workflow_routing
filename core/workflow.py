from agents.summarizer_agent import SummarizerAgent
from schemas.agents.summarizer_agent import ContentType, SummarizerInput
from schemas.workflow.workflow import WorkflowResult


class Workflow:
    """
    Executes single-agent and multi-agent flows.
    """

    def __init__(self, summarizer: SummarizerAgent):
        self.summarizer = summarizer

    def run(
        self, intent: str, user_input: str, content_type: ContentType, focus: str | None = None
    ) -> WorkflowResult:
        runners = {
            "summarizer_agent" : self._run_summarizer,
        }

        runner = runners.get(intent)
        if not runner:
            return WorkflowResult(intent=intent, error=f"Unknow intent: {intent}")

        try:
            return runner(user_input, content_type, focus)
        except Exception as e:
            return WorkflowResult(intent=intent, error=str(e))

    def _run_summarizer(
        self, content: str, content_type: ContentType, focus: str | None = None
    ) -> WorkflowResult:
        result = WorkflowResult(intent="summarize")

        output= self.summarizer.run(
            SummarizerInput(content=content, content_type=content_type, focus=focus)
        )
        result.add("summarize", output)

        return result
