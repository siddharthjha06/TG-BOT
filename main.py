import os
import logging
from io import BytesIO
from rembg import remove
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get your Telegram bot token from environment variable
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Handler for incoming photo messages
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    input_image = BytesIO(photo_bytes)

    # ✅ Fixed: Force return bytes from rembg
    output_image = remove(input_image, force_return_bytes=True)

    # Send processed image back
    await update.message.reply_photo(photo=BytesIO(output_image))

def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    # Add handler for photo
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
