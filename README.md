# CS2 News Bot

Polls CS2 news sources every 60 seconds and posts new items to a Discord channel via webhook.

## How it works

Monitors HLTV, Steam, Reddit, Dust2.us, and X/Twitter accounts simultaneously. Each item is deduplicated in a local SQLite database so nothing gets posted twice, even after restarts.

## Setup

```bash
cd cs2-news-bot
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

Create the webhook: **Discord channel → Edit Channel → Integrations → Webhooks → New Webhook → Copy URL**

```bash
python main.py
```

On first run the bot seeds all currently visible items as "already seen" so it doesn't flood your channel with old news. From then on only new items are posted.

## Sources monitored

| Source | Type | Status |
|---|---|---|
| HLTV news | RSS | ✅ Working |
| Steam CS2 updates | RSS | ✅ Working |
| Dust2.us | RSS | ✅ Working |
| Reddit r/GlobalOffensive | RSS | ✅ Working |
| Reddit r/cs2 | RSS | ✅ Working |
| X: @Ozzny_CS2 | Nitter RSS | ⚠️ See below |
| X: @CounterStrike | Nitter RSS | ⚠️ See below |
| X: @ESL_CS, @FACEIT, @NatusVincere, etc. | Nitter RSS | ⚠️ See below |

## Adding reliable X/Twitter feeds

Public Nitter instances (used for X feeds) are volunteer-run and go offline regularly. The bot tries 5 instances in order and logs a warning when all fail — RSS sources keep running normally.

For **guaranteed** X coverage, use [rss.app](https://rss.app) (free account, no credit card):

1. Sign up at https://rss.app
2. Go to **RSS Feeds → Create → X/Twitter**
3. Paste any X profile URL (e.g. `https://x.com/Ozzny_CS2`)
4. Copy the generated `https://rss.app/feeds/xxxx.xml` URL
5. Add it to `RSS_FEEDS` in `config.py`:

```python
{
    "name": "X: @Ozzny_CS2",
    "url": "https://rss.app/feeds/YOUR_ID.xml",
    "color": "Twitter",
},
```

Free tier allows 5 feeds. That covers the most important accounts.

## Configuration

All settings are in `config.py` and `.env`:

| Setting | Default | Description |
|---|---|---|
| `DISCORD_WEBHOOK_URL` | — | Your Discord webhook URL (required) |
| `POLL_INTERVAL_SECONDS` | 60 | How often to check feeds |
| `DB_PATH` | `seen_items.db` | Path to dedup database |

To add any RSS feed, append to `RSS_FEEDS` in `config.py`:
```python
{"name": "My Source", "url": "https://example.com/feed.xml", "color": "default"}
```

## Running as a background service

**Windows (Task Scheduler):**
Create a task that runs `python main.py` at startup with your project directory as the working dir.

**Linux/macOS (systemd or screen):**
```bash
screen -S cs2bot
python main.py
# Ctrl+A, D to detach
```
