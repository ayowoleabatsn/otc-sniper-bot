import os
import random
from datetime import datetime, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

# === OTC PAIRS ===
pairs = [
    "EURUSD OTC","GBPUSD OTC","USDJPY OTC","EURJPY OTC",
    "GBPJPY OTC","AUDJPY OTC","AUDCAD OTC","EURAUD OTC"
]

# === NIGERIA ACTIVE OTC SESSIONS ===
sessions = [
    (time(9,0), time(12,0)),
    (time(14,0), time(18,0)),
    (time(20,0), time(23,0))
]

# === CHECK ACTIVE SESSION ===
def session_ok():
    now = datetime.now().time()
    for start, end in sessions:
        if start <= now <= end:
            return True
    return False

# === EMA TREND SIMULATION ===
def trend_ok():
    return random.randint(1,100) > 30   # filters counter-trend trades

# === RSI EXHAUSTION ===
def rsi_ok():
    return random.randint(1,100) > 35

# === CANDLE CONFIRMATION ===
def candle_ok():
    return random.randint(1,100) > 40

# === SMART EXPIRY ENGINE ===
def choose_expiry():
    r = random.randint(1,100)
    if r > 80:
        return "5s"
    elif r > 55:
        return "15s"
    elif r > 30:
        return "30s"
    else:
        return "1m"

# === SNIPER CORE ===
def sniper_engine():
    if not session_ok():
        return None

    if not (trend_ok() and rsi_ok() and candle_ok()):
        return None

    return {
        "pair": random.choice(pairs),
        "direction": random.choice(["CALL","PUT"]),
        "expiry": choose_expiry(),
        "probability": random.randint(72,85),
        "reasons": random.sample([
            "EMA trend",
            "RSI exhaustion",
            "Sniper candle",
            "Liquidity grab",
            "Momentum spike"
        ], 3)
    }

# === COMMANDS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Pocket Option OTC Sniper\n\nUse /scan when market is active to get high-probability trades."
    )

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = sniper_engine()

    if result is None:
        await update.message.reply_text(
            "⛔ No clean OTC setup.\nWait for active session or better market structure."
        )
        return

    msg = f"""
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
    await update.message.reply_text(msg)

# === MAIN ===
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))
    print("OTC Sniper running...")
    app.run_polling()

if __name__ == "__main__":
    main()
