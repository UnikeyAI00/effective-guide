import logging
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.generativeai import generate_content, ImageGenerationConfig

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Google AI Studio API key
GEMINI_API_KEY = "your_google_ai_studio_api_key"

# Telegram bot token
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! Send me a text prompt and I will generate an image for you using Gemini 2.0 Flash.')

def generate_image(update: Update, context: CallbackContext) -> None:
    """Generate an image from a text prompt using Gemini 2.0 Flash."""
    user_prompt = update.message.text
    
    # Configure image generation
    generation_config = ImageGenerationConfig(
        model="gemini-2.0-flash-exp",
        prompt=user_prompt,
        aspect_ratio="1:1",
        quality="photo"
    )
    
    try:
        # Generate content using Gemini API
        content = generate_content(
            generation_config=generation_config,
            api_key=GEMINI_API_KEY
        )
        
        # Extract image data from response
        image_data = content.result().candidates[0].content
        image_bytes = image_data[0].inline_data.data
        
        # Send image to user
        update.message.reply_photo(photo=InputFile(image_bytes))
        
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        update.message.reply_text("Sorry, I encountered an error while generating your image.")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_BOT_TOKEN)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Register message handler for text prompts
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_image))
    
    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == "__main__":
    main()
