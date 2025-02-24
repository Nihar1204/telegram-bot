import logging
import os
import google.generativeai as genai
import redis
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Download required NLTK resources
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Load environment variables
load_dotenv()

# Set up API keys and Redis configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Validate API keys
if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ API keys not found! Check your .env file.")

# Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Connect to Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# Store user conversation history (optional)
user_conversations = {}

# Function to analyze sentiment using NLTK
def analyze_sentiment(text):
    sentiment_score = sia.polarity_scores(text)["compound"]
    if sentiment_score >= 0.5:
        return "positive 😊"
    elif sentiment_score <= -0.5:
        return "negative 😠"
    else:
        return "neutral 😐"

# Function to extract Named Entities using spaCy
def extract_entities(text):
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}  # Extract entities as a dictionary
    return entities if entities else None  # Return None if no entities are found

# Function to handle messages using Gemini AI with Redis caching and NER
async def chat_with_gemini(user_id, user_input):
    try:
        # Check if the response exists in Redis cache
        cached_response = redis_client.get(user_input)
        if cached_response:
            logging.info("✅ Retrieved response from Redis cache.")
            return cached_response

        # Maintain conversation history
        if user_id not in user_conversations:
            user_conversations[user_id] = []

        # Analyze user sentiment
        sentiment = analyze_sentiment(user_input)
        logging.info(f"📊 Sentiment Analysis: {sentiment}")

        # Extract Named Entities
        entities = extract_entities(user_input)
        if entities:
            logging.info(f"🔍 Extracted Named Entities: {entities}")

        # Generate AI response
        response = model.generate_content(user_input)

        # Validate response
        if not response.text:
            logging.warning("⚠ Gemini API returned an empty response.")
            return "⚠ Sorry, I couldn't generate a response."

        # Store AI response in Redis cache (expires in 1 hour)
        redis_client.setex(user_input, 3600, response.text)

        # Store AI response in history
        user_conversations[user_id].append({"role": "assistant", "content": response.text})

        # Append extracted NER information to response if applicable
        if entities:
            response.text += f"\n\n🔍 **Detected Entities:** {entities}"

        return response.text
    except Exception as e:
        logging.error(f"❌ Error in Gemini API: {e}")
        return "❌ Sorry, there was an issue processing your request."

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "🤖 Hello! I'm an AI chatbot powered by **Google Gemini AI**.\n"
        "You can chat with me by sending messages.\n\n"
        "Use **/help** to see available commands!"
    )

# Help command
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "**Available Commands:**\n"
        "✅ /start - Start the bot\n"
        "✅ /help - Get help and command list\n"
        "✅ /clear - Clear chat history\n\n"
        "Just type your message, and I'll respond! 😊"
    )

# Clear chat history command
async def clear_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id in user_conversations:
        del user_conversations[user_id]  # Clear conversation history
    await update.message.reply_text("✅ Chat history cleared! You can start fresh.")

# Message handler for user input
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_id = update.message.chat_id

    logging.info(f"📩 User ({user_id}) sent: {user_message}")

    bot_response = await chat_with_gemini(user_id, user_message)

    logging.info(f"🤖 Gemini Response: {bot_response}")

    await update.message.reply_text(bot_response)

# Main function to run the bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
