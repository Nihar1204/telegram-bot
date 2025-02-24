# telegram-bot

🚀 AI-Powered Telegram Chatbot with Google Gemini, NER & Redis Caching
A smart Telegram chatbot powered by Google Gemini AI, featuring Named Entity Recognition (NER) using spaCy, Sentiment Analysis with NLTK, and Redis caching for optimized performance.

📌 Features
✅ Google Gemini AI Integration – Intelligent responses to user queries
✅ Named Entity Recognition (NER) – Extracts names, places, dates, and more
✅ Sentiment Analysis – Detects user mood (positive, neutral, negative)
✅ Redis Caching – Stores frequent responses to speed up replies
✅ Scalable & Efficient – Handles real-time queries with minimal latency

🔧 Tech Stack
Technology	Purpose
Python	Core language for bot logic
Telegram Bot API	Enables interaction with users
Google Gemini AI	Generates responses
spaCy	Extracts Named Entities (NER)
NLTK	Performs Sentiment Analysis
Redis	Caches responses for efficiency
python-dotenv	Manages environment variables


🚀 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/yourusername/telegram-gemini-bot.git
cd telegram-bot

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Download spaCy Model
python -m spacy download en_core_web_sm

4️⃣ Set Up Environment Variables
Create a .env file in the project root and add:


GEMINI_API_KEY=your-gemini-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
REDIS_HOST=localhost
REDIS_PORT=6379

5️⃣ Start Redis
For Windows (Using WSL)
redis-server.exe

6️⃣ Run the Bot
python telegram_gemini_bot.py

🤖 Your bot is now live! Try chatting with it on Telegram.

📌 Usage
🔹 Start the bot: /start
🔹 Get help: /help
🔹 Clear chat history: /clear
🔹 Ask anything: "Who is Elon Musk?"
🔹 Test NER: "I was born in New York on April 15, 1995."
🔹 Check sentiment: "I am feeling really sad today."

1️⃣ Cached Responses with Redis
User: "What is AI?"
Bot: "AI stands for Artificial Intelligence..."
User asks again: "What is AI?"
Bot: "✅ Retrieved from cache!"

🛠 Future Improvements
✅ We can add multilingual support
✅ We can train a custom NER model
✅ We can improve chatbot context awareness

🤝 Contribution
Fork this repository
Create a new branch:
git checkout -b feature-branch

Commit your changes:
git commit -m "Added feature XYZ"
Push to GitHub and create a pull request

✨ Star this repo if you found it useful! ⭐🚀
Let me know if you'd like to add anything else! 😊
