import hashlib
import logging
import re
from dataclasses import dataclass
from typing import Optional

import feedparser
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Feedbin/2.0 (feed-parser)"}
TIMEOUT = 12


@dataclass
class FeedItem:
    id: str
    title: str
    url: str
    source: str
    color: str
    summary: Optional[str] = None


def _make_id(entry, feed_name: str) -> str:
    raw = getattr(entry, "id", None) or getattr(entry, "link", None) or ""
    if raw:
        return raw
    return hashlib.sha256(f"{feed_name}:{entry.get('title', '')}".encode()).hexdigest()


def _clean_summary(text: Optional[str], max_len: int = 200) -> Optional[str]:
    if not text:
        return None
    text = re.sub(r"<[^>]+>", "", text).strip()
    if len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0] + "…"
    return text or None


def _parse_url(url: str) -> list[FeedItem]:
    """Fetch one URL and return FeedItems. Returns [] on any failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False)
        resp.raise_for_status()
    except requests.RequestException:
        return []

    parsed = feedparser.parse(resp.content)
    if parsed.bozo and not parsed.entries:
        return []

    items = []
    for entry in parsed.entries:
        link = entry.get("link", "").strip()
        if not link:
            continue
        items.append(
            FeedItem(
                id=_make_id(entry, url),
                title=entry.get("title", "").strip() or "(no title)",
                url=link,
                source="",   # filled in by caller
                color="",
                summary=_clean_summary(entry.get("summary") or entry.get("description")),
            )
        )
    return items


def fetch_feed(feed_cfg: dict) -> list[FeedItem]:
    """Fetch a regular RSS feed."""
    items = _parse_url(feed_cfg["url"])
    for item in items:
        item.source = feed_cfg["name"]
        item.color = feed_cfg["color"]
    if not items:
        logger.warning("No items from %s (%s)", feed_cfg["name"], feed_cfg["url"])
    return items


def fetch_twitter(handle: str, display_name: str, instances: list[str]) -> list[FeedItem]:
    """
    Fetch a Twitter/X account via Nitter, trying each instance in order.
    Returns items from the first instance that responds with entries.
    """
    for base in instances:
        url = f"{base}/{handle}/rss"
        items = _parse_url(url)
        if items:
            for item in items:
                item.source = display_name
                item.color = "Twitter"
                # Rewrite nitter links back to x.com
                item.url = item.url.replace(base, "https://x.com")
            logger.debug("Twitter @%s: %d items via %s", handle, len(items), base)
            return items
        logger.debug("Twitter @%s: no items from %s", handle, base)

    logger.warning("Twitter @%s: all Nitter instances failed", handle)
    return []
