#!/usr/bin/env python3
"""Scrape tp.edu.sg SEN pages locally and save to data/raw/tp_sen/.
Run this once before deploying to bundle TP content with the deployment."""
import asyncio
import os
import ssl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

ssl._create_default_https_context = ssl._create_unverified_context

import httpx
_orig_client = httpx.Client.__init__
def _patch(self, *a, **kw): kw.setdefault("verify", False); _orig_client(self, *a, **kw)
httpx.Client.__init__ = _patch
_orig_async = httpx.AsyncClient.__init__
def _patch_async(self, *a, **kw): kw.setdefault("verify", False); _orig_async(self, *a, **kw)
httpx.AsyncClient.__init__ = _patch_async

import logging
logging.basicConfig(level="INFO", format="%(asctime)s %(levelname)s %(name)s: %(message)s")

from app.config import CRAWL_SOURCES
from app.ingestion.scraper import scrape_source

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


async def main():
    tp_source = next(s for s in CRAWL_SOURCES if s["label"] == "tp_sen")
    print(f"\nScraping TP SEN from: {tp_source['seed_url']}")
    print(f"Saving to: {RAW_DIR / 'tp_sen'}\n")
    pages = await scrape_source(tp_source, RAW_DIR)
    print(f"\nDone: {len(pages)} pages saved to data/raw/tp_sen/")
    for p in pages:
        print(f"  [{p.crawl_depth}] {p.source_url}")


if __name__ == "__main__":
    asyncio.run(main())
