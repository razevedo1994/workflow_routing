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

    def _fetch(self, url: str, timeout: int) -> str:
        response = httpx.get(
            url, headers=self.HEADERS, timeout=timeout, follow_redirects=True
        )
        response.raise_for_status()
        return response.text

    def _parse(self, html: str) -> tuple[str | None, str]:
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(self.NOISE_TAGS):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else None

        body = soup.find("article") or soup.find("main") or soup.find("body") or soup

        content = " ".join(body.get_text(separator=" ").split())

        return title, content

    @staticmethod
    def _error(url: str, message: str) -> WebFetchOutput:
        return WebFetchOutput(
            url=url,
            title=None,
            content="",
            word_count=0,
            success=False,
            error=message,
        )
