import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

SKIP_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".zip"}


@dataclass
class ScrapedPage:
    label: str
    seed_url: str
    source_url: str
    page_title: str
    markdown: str
    crawl_depth: int
    fetched_at: str


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(fragment="").geturl().rstrip("/")


def _is_valid_url(url: str, allowed_prefix: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    if any(parsed.path.lower().endswith(ext) for ext in SKIP_EXTENSIONS):
        return False
    return url.startswith(allowed_prefix)


def _url_to_slug(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_")
    slug = re.sub(r"[^\w\-]", "_", path)
    return slug[:100] or "index"


def _extract_markdown(result) -> str:
    if hasattr(result, "markdown") and result.markdown:
        md = result.markdown
        if hasattr(md, "raw_markdown"):
            return md.raw_markdown or ""
        return str(md)
    return ""


def _extract_links(result, base_url: str) -> list[str]:
    if not hasattr(result, "links") or not result.links:
        return []
    internal = result.links.get("internal", [])
    hrefs = []
    for link in internal:
        href = link.get("href", "") if isinstance(link, dict) else str(link)
        if href:
            hrefs.append(urljoin(base_url, href))
    return hrefs


async def scrape_source(source: dict, raw_dir: Path) -> list[ScrapedPage]:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

    label = source["label"]
    seed_url = source["seed_url"]
    allowed_prefix = source["allowed_prefix"]
    max_depth = source["max_depth"]
    max_pages = source["max_pages"]

    out_dir = raw_dir / label
    out_dir.mkdir(parents=True, exist_ok=True)

    browser_cfg = BrowserConfig(headless=True, ignore_https_errors=True)
    crawl_cfg = CrawlerRunConfig(wait_until="networkidle", page_timeout=30000)

    visited: set[str] = set()
    queue: list[tuple[str, int]] = [(_normalize_url(seed_url), 0)]
    pages: list[ScrapedPage] = []

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        while queue and len(pages) < max_pages:
            url, depth = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)

            logger.info("[%s] depth=%d  %s", label, depth, url)
            try:
                result = await crawler.arun(url=url, config=crawl_cfg)
            except Exception as exc:
                logger.warning("[%s] failed %s: %s", label, url, exc)
                continue

            if not result.success:
                logger.warning("[%s] unsuccessful %s", label, url)
                continue

            markdown = _extract_markdown(result)
            if not markdown.strip():
                logger.warning("[%s] empty content %s", label, url)
                continue

            title = ""
            if hasattr(result, "metadata") and result.metadata:
                title = result.metadata.get("title", "")

            page = ScrapedPage(
                label=label,
                seed_url=seed_url,
                source_url=url,
                page_title=title,
                markdown=markdown,
                crawl_depth=depth,
                fetched_at=datetime.now(timezone.utc).isoformat(),
            )
            pages.append(page)
            (out_dir / f"{_url_to_slug(url)}.md").write_text(markdown, encoding="utf-8")

            if depth < max_depth:
                for href in _extract_links(result, url):
                    norm = _normalize_url(href)
                    if _is_valid_url(norm, allowed_prefix) and norm not in visited:
                        queue.append((norm, depth + 1))

    logger.info("[%s] done — %d pages scraped", label, len(pages))
    return pages
