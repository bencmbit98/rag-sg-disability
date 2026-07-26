import json
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


def load_pages_from_raw(source: dict, raw_dir: Path) -> list[ScrapedPage]:
    """Load pre-scraped pages from data/raw/<label>/ instead of hitting the network."""
    label = source["label"]
    out_dir = raw_dir / label
    pages = []
    for md_file in sorted(out_dir.glob("*.md")):
        json_file = md_file.with_suffix(".json")
        if not json_file.exists():
            logger.warning("[%s] no metadata for %s, skipping", label, md_file.name)
            continue
        try:
            meta = json.loads(json_file.read_text(encoding="utf-8"))
            markdown = md_file.read_text(encoding="utf-8")
            if markdown.strip():
                pages.append(ScrapedPage(
                    label=meta["label"],
                    seed_url=meta["seed_url"],
                    source_url=meta["source_url"],
                    page_title=meta["page_title"],
                    markdown=markdown,
                    crawl_depth=meta["crawl_depth"],
                    fetched_at=meta["fetched_at"],
                ))
        except Exception as exc:
            logger.warning("[%s] failed to load %s: %s", label, md_file.name, exc)
    logger.info("[%s] loaded %d pages from pre-scraped files", label, len(pages))
    return pages


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

            slug = _url_to_slug(url)
            (out_dir / f"{slug}.md").write_text(markdown, encoding="utf-8")
            (out_dir / f"{slug}.json").write_text(
                json.dumps({
                    "label": page.label,
                    "seed_url": page.seed_url,
                    "source_url": page.source_url,
                    "page_title": page.page_title,
                    "crawl_depth": page.crawl_depth,
                    "fetched_at": page.fetched_at,
                }),
                encoding="utf-8",
            )

            if depth < max_depth:
                for href in _extract_links(result, url):
                    norm = _normalize_url(href)
                    if _is_valid_url(norm, allowed_prefix) and norm not in visited:
                        queue.append((norm, depth + 1))

    logger.info("[%s] done — %d pages scraped", label, len(pages))
    return pages


def load_curated_pages(curated_dir: Path) -> list[ScrapedPage]:
    """Load manually curated markdown files as ScrapedPage objects.

    Each file may begin with a YAML-style front matter block:
        ---
        label: tp_sen
        url: https://...
        title: Page Title
        ---
    Fields not present default to safe fallbacks.
    """
    pages = []
    for md_file in sorted(curated_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        label = "curated"
        url = f"curated://{md_file.stem}"
        title = md_file.stem
        body = text

        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if fm_match:
            body = text[fm_match.end():]
            for line in fm_match.group(1).splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    key, val = key.strip(), val.strip()
                    if key == "label":
                        label = val
                    elif key == "url":
                        url = val
                    elif key == "title":
                        title = val

        if not body.strip():
            logger.warning("[curated] skipping empty file: %s", md_file.name)
            continue

        pages.append(ScrapedPage(
            label=label,
            seed_url=url,
            source_url=url,
            page_title=title,
            markdown=body,
            crawl_depth=0,
            fetched_at=datetime.now(timezone.utc).isoformat(),
        ))
        logger.info("[curated] loaded %s (%d chars)", md_file.name, len(body))

    return pages
