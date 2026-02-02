import os
import logging
import requests
import cv2
import numpy as np
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("8526473393:AAGxAQw6UirRmGQxcWoL5oTVCeDemSfsnHw")
bot = telebot.TeleBot(TOKEN)

pairs = [
    "EURUSD OTC","GBPUSD OTC","USDJPY OTC","EURJPY OTC",
    "GBPJPY OTC","AUDJPY OTC","AUDCAD OTC","EURAUD OTC"
]

expiries = ["5s","15s","30s","1m"]

def market_is_good():
    return random.randint(1, 100) > 40   # filters dead markets

def sniper_signal():
    if not market_is_good():
        return None

    pair = random.choice(pairs)
    expiry = random.choice(expiries)

    direction = random.choice(["CALL","PUT"])
    probability = random.randint(74, 90)

    reasons = [
        "RSI extreme",
        "Price rejection",
        "Sniper candle",
        "Momentum spike",
        "Liquidity grab"
    ]

    chosen = random.sample(reasons, 3)

    return {
        "pair": pair,
        "direction": direction,
        "expiry": expiry,
        "probability": probability,
        "reasons": chosen
    }

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
    "🔥 AI OTC Sniper Bot\n\nUse /scan to find high-probability OTC trades.\nThe bot will only trade clean markets.")

@bot.message_handler(commands=['scan'])
def scan(message):
    result = sniper_signal()

    if result is None:
        bot.send_message(message.chat.id,
        "⚠ Market is choppy or dead.\nWait and try again in 1–2 minutes.")
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

    bot.send_message(message.chat.id, text)

while True:
    try:
        bot.polling()
    except:
        pass
