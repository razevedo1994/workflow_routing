import httpx
from bs4 import BeautifulSoup

from schemas.tools.web_fetch import WebFetchInput, WebFetchOutput


class WebFetchTool:
    """
    Fetches a URL, strips HTML noise, and returns clean text.
    """

    HEADERS = {"User-Agent": ("Mozilla/5.0 (compatible; ResearchSummarizer/1.0)")}

    NOISE_TAGS = [
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside",
        "advertisement",
    ]

    def run(self, input: WebFetchInput) -> WebFetchOutput:
        try:
            raw_html = self._fetch(str(input.url), input.timeout_seconds)
            title, content = self._parse(raw_html)

            return WebFetchOutput(
                url=str(input.url),
                title=title,
                content=content,
                word_count=len(content.split()),
                success=True,
            )

        except httpx.TimeoutException:
            return self._error(str(input.url), "Request timed out")

        except httpx.HTTPStatusError as e:
            return self._error(str(input.url), f"HTTP {e.response.status_code}")

        except Exception as e:
            return self._error(str(input.url), str(e))
