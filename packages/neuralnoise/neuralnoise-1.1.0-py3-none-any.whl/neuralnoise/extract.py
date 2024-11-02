import logging
import os
from asyncio import run
from pathlib import Path
from tempfile import NamedTemporaryFile
from textwrap import dedent
from typing import Iterator

import requests  # type: ignore
from langchain_community.document_loaders import (
    BSHTMLLoader,
    PyMuPDFLoader,
    TextLoader,
    YoutubeLoader,
)
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class Crawl4AILoader(BaseLoader):
    def __init__(
        self,
        url: str,
        css_selector: str | None = None,
    ) -> None:
        self.url = url
        self.css_selector = css_selector

    async def crawl(self, url: str, css_selector: str | None = None):
        from crawl4ai import AsyncWebCrawler

        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url,
                css_selector=css_selector or "",
            )

        return result

    def lazy_load(self) -> Iterator[Document]:
        """Load HTML document into document objects."""
        # First attempt loading with CSS selector if provided
        result = run(self.crawl(self.url, self.css_selector))

        # Second attempt loading without CSS selector if first attempt failed
        if result.markdown is None and self.css_selector is not None:
            result = run(self.crawl(self.url))

        if result.markdown is None:
            raise ValueError(f"No valid content found at {self.url}")

        metadata: dict[str, str | None] = {
            **(result.metadata or {}),
            "source": self.url,
        }

        yield Document(page_content=result.markdown, metadata=metadata)


def get_best_loader(extract_from: str | Path) -> BaseLoader:
    match extract_from:
        case str() | Path() if os.path.isfile(extract_from):
            if os.path.splitext(extract_from)[1] == ".pdf":
                return PyMuPDFLoader(file_path=str(extract_from))
            else:
                return TextLoader(file_path=extract_from)
        case str() if extract_from.startswith("http"):
            if "youtube" in extract_from:
                video_id = YoutubeLoader.extract_video_id(extract_from)
                return YoutubeLoader(video_id=video_id)
            else:
                try:
                    return Crawl4AILoader(url=extract_from, css_selector="article")
                except Exception:
                    logger.warning(
                        dedent("""
                        Crawl4AI web loader is not available but it's recommended for
                        better results. Install `pip install neuralnoise[crawl4ai]` to
                        use it, or `pip install crawl4ai` to install it.
                                   
                        Once installed, make sure to follow the instructions in their
                        repo: https://github.com/unclecode/crawl4ai
                                   
                        For example, you should run `playwright install` to install
                        utils for the crawlers to work.

                        Using the default web loader now.
                    """)
                    )

                    html_content = requests.get(extract_from).text

                    with NamedTemporaryFile(
                        delete=False, mode="w", suffix=".html"
                    ) as f:
                        f.write(html_content)

                    loader = BSHTMLLoader(file_path=f.name)
                    f.close()
                    return loader
        case _:
            raise ValueError("Invalid input")


def extract_content_from_source(extract_from: str | Path) -> str:
    logger.info(f"Extracting content from {extract_from}")
    loader = get_best_loader(extract_from)
    docs = loader.load()
    content = ""

    for doc in docs:
        if doc.metadata.get("title"):
            content += f"\n\n# {doc.metadata['title']}\n\n"
        content += doc.page_content.strip()

    return content


def extract_content(
    extract_from: str | Path | list[str] | list[Path] | list[str | Path],
) -> str:
    if not isinstance(extract_from, list):
        extract_from = [extract_from]

    return "\n\n".join(
        f"<document>\n{extract_content_from_source(item)}\n</document>"
        for item in extract_from
    )
