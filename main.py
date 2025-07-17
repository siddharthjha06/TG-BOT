import os
import logging
from io import BytesIO
from rembg import remove
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get token from environment variable
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info("Received photo")
        photo_file = await update.message.photo[-1].get_file()
        logger.info(f"File path: {photo_file.file_path}")
        photo_bytes = BytesIO()
        await photo_file.download_to_memory(out=photo_bytes)
        photo_bytes.seek(0)

        # Remove background
        output_bytes = remove(photo_bytes.getvalue(), force_return_bytes=True)
        logger.info("Background removed successfully")

        # Send the result
        await update.message.reply_photo(photo=BytesIO(output_bytes))
        logger.info("Replied with processed image")

    except Exception as e:
        logger.error(f"Error in handle_photo: {e}")
        await update.message.reply_text("An error occurred while processing the image.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    logger.info("Bot started")
    app.run_polling()

if __name__ == '__main__':
    main()
