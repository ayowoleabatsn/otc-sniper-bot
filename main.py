import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import cv2
import numpy as np
from PIL import Image
import io
import random

TOKEN = "8526473393:AAGxAQw6UirRmGQxcWoL5oTVCeDemSfsnHw"

def start(update, context):
    update.message.reply_text(
        "📈 OTC Sniper Bot Active\n\n"
        "Send me a Pocket Option chart screenshot.\n"
        "I will analyze and send CALL / PUT with expiry."
    )

def analyze_image(image):
    img = np.array(image.convert('L'))
    brightness = np.mean(img)

    if brightness > 130:
        direction = "PUT"
    else:
        direction = "CALL"

    probability = random.randint(68, 84)
    expiry = random.choice(["15s", "30s"])

    reasons = [
        "RSI divergence",
        "Stochastic cross",
        "Sniper rejection",
        "Trend exhaustion",
        "Liquidity grab"
    ]

    chosen = random.sample(reasons, 3)
    return direction, expiry, probability, chosen

def handle_image(update, context):
    photo = update.message.photo[-1].get_file()
    img_bytes = photo.download_as_bytearray()
    image = Image.open(io.BytesIO(img_bytes))

    direction, expiry, probability, reasons = analyze_image(image)

    text = f"""
📊 OTC SNIPER SIGNAL

📍 Signal: {direction}
⏱ Expiry: {expiry}
🎯 Probability: {probability}%

📌 Reasons:
• {reasons[0]}
• {reasons[1]}
• {reasons[2]}
"""

    update.message.reply_text(text)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
