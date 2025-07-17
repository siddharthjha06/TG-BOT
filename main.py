import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
BG_REMOVER_API_KEY = 'YOUR_REMOVE_BG_API_KEY'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a photo, and I’ll remove its background!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo_file = await update.message.photo[-1].get_file()
        image_bytes_io = await photo_file.download_as_bytes()

        # Call background remover API
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': ('image.jpg', image_bytes_io)},
            data={'size': 'auto'},
            headers={'X-Api-Key': BG_REMOVER_API_KEY},
        )

        if response.status_code == 200:
            await update.message.reply_photo(photo=response.content)
        else:
            await update.message.reply_text(
                f"❌ Failed to remove background. Error: {response.status_code} - {response.text}"
            )
    except Exception as e:
        logging.error(f"Error in handle_photo: {e}")
        await update.message.reply_text("⚠️ An error occurred while processing your image.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
