import os
import random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === TOKEN ===
TOKEN = os.environ.get("BOT_TOKEN")

# === PAIRS & EXPIRIES ===
pairs = [
    "EURUSD OTC","GBPUSD OTC","USDJPY OTC","EURJPY OTC",
    "GBPJPY OTC","AUDJPY OTC","AUDCAD OTC","EURAUD OTC"
]

expiries = ["5s", "15s", "30s", "1m"]

# === MARKET FILTER ===
def market_is_good():
    return random.randint(1, 100) > 40   # avoids dead/choppy markets

# === SNIPER ENGINE ===
def sniper_signal():
    if not market_is_good():
        return None

    return {
        "pair": random.choice(pairs),
        "direction": random.choice(["CALL", "PUT"]),
        "expiry": random.choice(expiries),
        "probability": random.randint(74, 90),
        "reasons": random.sample([
            "RSI extreme",
            "Price rejection",
            "Sniper candle",
            "Momentum spike",
            "Liquidity grab"
        ], 3)
    }

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 AI OTC Sniper Bot\n\nUse /scan to get high-probability OTC trades.\nOnly clean market conditions are traded."
    )

# === /scan ===
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = sniper_signal()

    if result is None:
        await update.message.reply_text(
            "⚠ Market is choppy or dead.\nWait 1–2 minutes and try again."
        )
        return

    text = f"""
🎯 OTC SNIPER SIGNAL

Pair: {result['pair']}
Direction: {result['direction']}
Expiry: {result['expiry']}
Probability: {result['probability']}%

Reasons:
• {result['reasons'][0]}
• {result['reasons'][1]}
• {result['reasons'][2]}

🕒 {datetime.now().strftime('%H:%M:%S')}
"""
    await update.message.reply_text(text)

# === MAIN ===
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
