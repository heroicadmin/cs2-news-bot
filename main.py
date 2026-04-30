import logging
import time

import schedule

from config import (
    NITTER_INSTANCES,
    POLL_INTERVAL_SECONDS,
    RSS_FEEDS,
    TWITTER_ACCOUNTS,
)
from dedup import is_seen, mark_seen, purge_old
from discord_bot import post_item, post_startup_message
from feeds import fetch_feed, fetch_twitter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def _all_feeds():
    """Yield (fetch_fn, args) for every configured source."""
    for feed_cfg in RSS_FEEDS:
        yield fetch_feed, (feed_cfg,)
    for handle, display_name in TWITTER_ACCOUNTS:
        yield fetch_twitter, (handle, display_name, NITTER_INSTANCES)


def poll_all_feeds() -> None:
    total_new = 0
    for fetch_fn, args in _all_feeds():
        items = fetch_fn(*args)
        new_items = [item for item in items if not is_seen(item.id)]
        if new_items:
            logger.info("[%s] %d new item(s)", new_items[0].source, len(new_items))
        for item in reversed(new_items):
            if post_item(item):
                mark_seen(item.id)
                logger.info("  Posted: %s", item.title[:80])
                total_new += 1
            else:
                logger.warning("  Failed to post: %s", item.title[:80])
    if total_new:
        logger.info("--- %d new item(s) posted this cycle ---", total_new)


def seed_seen_on_startup() -> None:
    logger.info("Seeding existing feed items so we don't flood Discord on first run...")
    seeded = 0
    for fetch_fn, args in _all_feeds():
        items = fetch_fn(*args)
        for item in items:
            if not is_seen(item.id):
                mark_seen(item.id)
                seeded += 1
    logger.info("Seeded %d item(s). Only new items will be posted going forward.", seeded)


def main() -> None:
    logger.info("CS2 News Bot starting up.")
    logger.info(
        "Poll interval: %ds | RSS feeds: %d | Twitter accounts: %d | Nitter instances: %d",
        POLL_INTERVAL_SECONDS, len(RSS_FEEDS), len(TWITTER_ACCOUNTS), len(NITTER_INSTANCES),
    )

    seed_seen_on_startup()
    post_startup_message()

    schedule.every(POLL_INTERVAL_SECONDS).seconds.do(poll_all_feeds)
    schedule.every(24).hours.do(purge_old)

    logger.info("Running. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == "__main__":
    main()
