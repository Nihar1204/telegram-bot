# import logging
# import google.generativeai as genai
# from telegram import Update
# from dotenv import load_dotenv
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
# import os

# # Configure logging
# logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# load_dotenv()

# # Set up API keys
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# # Configure Google Gemini AI
# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel("gemini-pro")

# # Store user conversation history (optional)
# user_conversations = {}

# # Function to handle messages
# async def chat_with_gemini(user_id, user_input):
#     try:
#         # Maintain conversation history
#         if user_id not in user_conversations:
#             user_conversations[user_id] = []

#         # Add user message to history
#         user_conversations[user_id].append({"role": "user", "content": user_input})

#         # Generate AI response
#         response = model.generate_content(user_conversations[user_id])

#         # Store AI response in history
#         user_conversations[user_id].append({"role": "assistant", "content": response.text})

#         return response.text
#     except Exception as e:
#         logging.error(f"Error in Gemini API: {e}")
#         return "Sorry, I couldn't process that request."

# # Start command
# async def start(update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text(
#         "🤖 Hello! I'm a chatbot powered by **Google Gemini AI**.\n"
#         "You can chat with me by sending messages.\n\n"
#         "Use **/help** to see what I can do!"
#     )

# # Help command
# async def help_command(update: Update, context: CallbackContext) -> None:
#     await update.message.reply_text(
#         "**Available Commands:**\n"
#         "✅ /start - Start the bot\n"
#         "✅ /help - Get help and command list\n"
#         "✅ /clear - Clear chat history\n\n"
#         "Just type your message, and I'll respond! 😊"
#     )

# # Clear command
# async def clear_command(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.chat_id
#     if user_id in user_conversations:
#         del user_conversations[user_id]  # Clear conversation history
#     await update.message.reply_text("✅ Chat history cleared! You can start fresh.")

# # Message handler
# async def handle_message(update: Update, context: CallbackContext) -> None:
#     user_message = update.message.text
#     user_id = update.message.chat_id
#     bot_response = await chat_with_gemini(user_id, user_message)
#     await update.message.reply_text(bot_response)

# # Main function
# def main():
#     app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

#     # Add command handlers
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("help", help_command))
#     app.add_handler(CommandHandler("clear", clear_command))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

#     print("🤖 Bot is running...")
#     app.run_polling()

# if __name__ == "__main__":
#     main()

import logging
import os
import google.generativeai as genai
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Load environment variables
load_dotenv()

# Set up API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Validate API keys
if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ API keys not found! Check your .env file.")

# Configure Google Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Store user conversation history (optional)
user_conversations = {}

# Function to handle messages using Gemini AI
# async def chat_with_gemini(user_id, user_input):
#     try:
#         # Maintain conversation history
#         if user_id not in user_conversations:
#             user_conversations[user_id] = []

#         # Append user message to conversation history
#         user_conversations[user_id].append({"role": "user", "content": user_input})

#         # Generate AI response
#         response = model.generate_content(messages=[{"role": "user", "content": user_input}])

#         # Validate response
#         if not response.text:
#             logging.warning("⚠ Gemini API returned an empty response.")
#             return "⚠ Sorry, I couldn't generate a response."

#         # Store AI response in history
#         user_conversations[user_id].append({"role": "assistant", "content": response.text})

#         return response.text
#     except Exception as e:
#         logging.error(f"❌ Error in Gemini API: {e}")
#         return "❌ Sorry, there was an issue processing your request."

async def chat_with_gemini(user_id, user_input):
    try:
        # Generate AI response (passing user_input directly)
        response = model.generate_content(user_input)

        # Validate response
        if not response.text:
            logging.warning("⚠ Gemini API returned an empty response.")
            return "⚠ Sorry, I couldn't generate a response."

        return response.text
    except Exception as e:
        logging.error(f"❌ Error in Gemini API: {e}")
        return "❌ Sorry, there was an issue processing your request."


# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "🤖 Hello! I'm a chatbot powered by **Google Gemini AI**.\n"
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
