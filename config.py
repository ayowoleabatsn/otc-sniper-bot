import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
TIMEFRAME = os.getenv("TIMEFRAME", "15s")
MARKET = os.getenv("MARKET", "OTC")
SIGNAL_MODE = os.getenv("SIGNAL_MODE", "A")
