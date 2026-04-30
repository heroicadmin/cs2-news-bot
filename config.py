import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
DB_PATH = os.getenv("DB_PATH", "seen_items.db")
DEDUP_RETENTION_DAYS = 30

# Discord embed colors per source (decimal)
COLORS = {
    "HLTV":     0xF5A623,  # orange
    "Steam":    0x1B2838,  # steam dark blue
    "Reddit":   0xFF4500,  # reddit orange-red
    "Dust2":    0x8B5E3C,  # dust2 sand
    "Twitter":  0x1DA1F2,  # twitter/X blue
    "Dexerto":  0xE8272A,  # dexerto red
    "DotEsports": 0x00B4D8,  # dot esports blue
    "default":  0x7289DA,  # discord blurple
}

# Nitter instances tried in order — first one that returns entries wins.
# Public Nitter is unreliable; for guaranteed X coverage use rss.app (free tier):
#   1. Sign up at https://rss.app (free, no credit card)
#   2. Paste any x.com profile URL → copy the generated .xml feed URL
#   3. Add it directly to RSS_FEEDS below with color "Twitter"
NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.tiekoetter.com",
    "https://nitter.cz",
    "https://nitter.pussthecat.org",
]

# X accounts to monitor (handles only — the bot tries each Nitter instance)
TWITTER_ACCOUNTS = [
    # News & community
    ("Ozzny_CS2",      "X: @Ozzny_CS2"),
    ("CounterStrike",  "X: @CounterStrike"),
    ("HLTV_org",       "X: @HLTV_org"),
    # Tournaments & platforms
    ("ESL_CS",         "X: @ESL_CS"),
    ("FACEIT",         "X: @FACEIT"),
    # Teams
    ("NatusVincere",   "X: @NatusVincere"),
    ("FaZeClan",       "X: @FaZeClan"),
    ("G2esports",      "X: @G2esports"),
    ("TeamVitality",   "X: @TeamVitality"),
    ("BIG_CS",         "X: @BIG_CS"),
    ("Astralis",       "X: @Astralis"),
    ("mousesports",    "X: @mousesports"),
    # Weird / cultural news
    ("viewsceo",       "X: @viewsceo"),
    ("BoredPanda",     "X: @BoredPanda"),
    ("LADbible",       "X: @LADbible"),
    ("UberFacts",      "X: @UberFacts"),
    ("IFLScience",     "X: @IFLScience"),
    ("WeirdHistory",   "X: @WeirdHistory"),
]

RSS_FEEDS = [
    # ── News sites ────────────────────────────────────────────────────────
    {
        "name": "HLTV",
        "url": "https://www.hltv.org/rss/news",
        "color": "HLTV",
    },
    {
        "name": "Steam CS2",
        "url": "https://store.steampowered.com/feeds/news/app/730/",
        "color": "Steam",
    },
    {
        "name": "Dust2.us",
        "url": "https://dust2.us/rss",
        "color": "Dust2",
    },
    # ── News sites (additional) ───────────────────────────────────────────
    {
        "name": "Dot Esports",
        "url": "https://dotesports.com/feed",
        "color": "DotEsports",
        "keywords": ["CS2", "Counter-Strike", "CSGO", "cs2"],
    },
    {
        "name": "Dexerto CS2",
        "url": "https://www.dexerto.com/feed/?category=counter-strike",
        "color": "Dexerto",
        "keywords": ["CS2", "Counter-Strike", "CSGO", "cs2"],
    },
    # ── Reddit (CS2) ─────────────────────────────────────────────────────
    {
        "name": "r/GlobalOffensive",
        "url": "https://www.reddit.com/r/GlobalOffensive/new/.rss",
        "color": "Reddit",
    },
    {
        "name": "r/cs2",
        "url": "https://www.reddit.com/r/cs2/new/.rss",
        "color": "Reddit",
    },
    # ── Reddit (weird / cultural) ─────────────────────────────────────────
    {
        "name": "r/nottheonion",
        "url": "https://www.reddit.com/r/nottheonion/new/.rss",
        "color": "Reddit",
    },
    {
        "name": "r/interestingasfuck",
        "url": "https://www.reddit.com/r/interestingasfuck/new/.rss",
        "color": "Reddit",
    },
    {
        "name": "r/mildlyinteresting",
        "url": "https://www.reddit.com/r/mildlyinteresting/new/.rss",
        "color": "Reddit",
    },
    {
        "name": "r/Damnthatsinteresting",
        "url": "https://www.reddit.com/r/Damnthatsinteresting/new/.rss",
        "color": "Reddit",
    },
    {
        "name": "r/WeirdNews",
        "url": "https://www.reddit.com/r/WeirdNews/new/.rss",
        "color": "Reddit",
    },
    # ── X / Twitter (via rss.app — reliable, requires free account) ───────
    {
        "name": "X: @Ozzny_CS2",
        "url": "https://rss.app/feeds/VY7zKl7hjfy9WyF5.xml",
        "color": "Twitter",
    },
    {
        "name": "X: @CounterStrike",
        "url": "https://rss.app/feeds/FYosc6FjucGIRXdP.xml",
        "color": "Twitter",
    },
]
