import telebot
import time
import random
from datetime import datetime

TOKEN = "8526473393:AAGxAQw6UirRmGQxcWoL5oTVCeDemSfsnHw"
bot = telebot.TeleBot(TOKEN)

pairs = ["EURUSD OTC","GBPUSD OTC","USDJPY OTC","EURJPY OTC"]
timeframes = ["15s","30s"]

def generate_signal():
    pair = random.choice(pairs)
    tf = random.choice(timeframes)
    direction = random.choice(["CALL","PUT"])
    probability = random.randint(75,92)

    expiry = "15 seconds" if tf == "15s" else "30 seconds"

    reason = "RSI oversold + Sniper candle rejection"

    msg = f"""
🎯 *OTC SNIPER SIGNAL*

📊 Pair: {pair}
⏱ Timeframe: {tf}
📈 Direction: {direction}
⏳ Expiry: {expiry}
📊 Probability: {probability}%

📌 Reason:
{reason}

🕒 {datetime.now().strftime('%H:%M:%S')}
    """
    return msg

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"🔥 OTC Sniper Bot Activated!\nSend /signal to receive trades.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    bot.send_message(message.chat.id, generate_signal(), parse_mode="Markdown")

while True:
    try:
        bot.polling()
    except:
        time.sleep(5)
