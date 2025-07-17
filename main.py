# main.py

import os
import logging
from io import BytesIO
from rembg import remove
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Get token from environment variable
TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a photo, and I’ll remove the background for you!")

# Handle photo messages
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()
    photo_bytes = await photo.download_as_bytearray()

    input_image = BytesIO(photo_bytes)
    output_image = remove(input_image)

    await update.message.reply_photo(photo=BytesIO(output_image), caption="Here is your image without background!")

# Main bot app
def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
