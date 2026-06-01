#!/usr/bin/env python3
"""Full ingestion pipeline: scrape → chunk → embed → store in ChromaDB."""
import asyncio
import logging
import os
import ssl
import sys
from pathlib import Path

# Allow `from app.x import y` when running as a script from backend/
sys.path.insert(0, str(Path(__file__).parent.parent))

# Bypass corporate SSL inspection (same as main.py)
if os.getenv("APP_ENV", "development") == "development":
    ssl._create_default_https_context = ssl._create_unverified_context
    import httpx
    try:
        import urllib3
        import requests
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        _orig_request = requests.Session.request
        def _patched_request(self, *args, **kwargs):
            kwargs.setdefault("verify", False)
            return _orig_request(self, *args, **kwargs)
        requests.Session.request = _patched_request
    except ImportError:
        pass
    _orig_client = httpx.Client.__init__
    def _patched_client(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_client(self, *args, **kwargs)
    httpx.Client.__init__ = _patched_client
    _orig_async_client = httpx.AsyncClient.__init__
    def _patched_async_client(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_async_client(self, *args, **kwargs)
    httpx.AsyncClient.__init__ = _patched_async_client

logging.basicConfig(level="INFO", format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

from app.config import CRAWL_SOURCES, settings  # noqa: E402
from app.ingestion.chunker import chunk_pages  # noqa: E402
from app.ingestion.embedder import embed_and_store  # noqa: E402
from app.ingestion.scraper import scrape_source  # noqa: E402

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


async def main() -> None:
    from sentence_transformers import SentenceTransformer

    logger.info("Loading embedding model: %s", settings.embedding_model)

    def _load_model():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return SentenceTransformer(settings.embedding_model)
        finally:
            loop.close()
            asyncio.set_event_loop(None)

    model = await asyncio.to_thread(_load_model)
    logger.info("Embedding model ready")

    summary = []
    for source in CRAWL_SOURCES:
        label = source["label"]
        logger.info("=== %s ===", label)
        pages = await scrape_source(source, RAW_DIR)
        chunks = chunk_pages(pages)
        stored = embed_and_store(chunks, model)
        summary.append({"label": label, "pages": len(pages), "chunks": len(chunks), "stored": stored})

    print("\n" + "=" * 60)
    print(f"{'Source':<25} {'Pages':>6} {'Chunks':>8} {'Stored':>8}")
    print("-" * 60)
    for row in summary:
        print(f"{row['label']:<25} {row['pages']:>6} {row['chunks']:>8} {row['stored']:>8}")
    print("=" * 60)
    print(f"Total chunks indexed: {sum(r['chunks'] for r in summary)}")


if __name__ == "__main__":
    asyncio.run(main())
