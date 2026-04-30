import logging
import time

import requests

from config import COLORS, DISCORD_WEBHOOK_URL
from feeds import FeedItem

logger = logging.getLogger(__name__)

_last_post_time: float = 0.0
_MIN_DELAY = 1.1  # seconds between posts to stay under Discord rate limits


def _throttle() -> None:
    global _last_post_time
    elapsed = time.monotonic() - _last_post_time
    if elapsed < _MIN_DELAY:
        time.sleep(_MIN_DELAY - elapsed)
    _last_post_time = time.monotonic()


def post_item(item: FeedItem) -> bool:
    if not DISCORD_WEBHOOK_URL:
        logger.error("DISCORD_WEBHOOK_URL is not set — cannot post.")
        return False

    color = COLORS.get(item.color, COLORS["default"])

    embed = {
        "title": item.title,
        "url": item.url,
        "color": color,
        "footer": {"text": item.source},
    }
    if item.summary:
        embed["description"] = item.summary

    payload = {"embeds": [embed]}

    _throttle()
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if resp.status_code == 204:
            return True
        # 429 = rate limited; back off and retry once
        if resp.status_code == 429:
            retry_after = resp.json().get("retry_after", 2)
            logger.warning("Discord rate-limited. Retrying after %ss.", retry_after)
            time.sleep(float(retry_after) + 0.5)
            resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
            return resp.status_code == 204
        logger.warning("Discord webhook returned %s: %s", resp.status_code, resp.text[:200])
        return False
    except requests.RequestException as exc:
        logger.error("Discord post failed: %s", exc)
        return False


def post_startup_message() -> None:
    if not DISCORD_WEBHOOK_URL:
        return
    payload = {
        "embeds": [
            {
                "title": "CS2 News Bot started",
                "description": "Now monitoring HLTV, Steam, Reddit, and more for CS2 news.",
                "color": COLORS["default"],
            }
        ]
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    except requests.RequestException:
        pass
