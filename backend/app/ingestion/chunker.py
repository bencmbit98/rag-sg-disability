import hashlib
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.ingestion.scraper import ScrapedPage


@dataclass
class Chunk:
    id: str
    text: str
    source_label: str
    source_url: str
    seed_url: str
    page_title: str
    crawl_depth: int
    chunk_index: int
    char_count: int
    fetched_at: str


def chunk_pages(pages: list[ScrapedPage]) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
    )
    chunks: list[Chunk] = []
    for page in pages:
        texts = splitter.split_text(page.markdown)
        for i, text in enumerate(texts):
            uid = hashlib.md5(f"{page.source_url}::{i}".encode()).hexdigest()
            chunks.append(Chunk(
                id=uid,
                text=text,
                source_label=page.label,
                source_url=page.source_url,
                seed_url=page.seed_url,
                page_title=page.page_title,
                crawl_depth=page.crawl_depth,
                chunk_index=i,
                char_count=len(text),
                fetched_at=page.fetched_at,
            ))
    return chunks
