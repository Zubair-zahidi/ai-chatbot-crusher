# ai-chatbot-crusher
Crusher is an AI-powered chatbot built with Flask and OpenAI’s API. It understands natural language, generates intelligent responses, and can translate or speak back to users using integrated NLTK, Google Translate, and gTTS features.


AI Chatbot Crusher

AI Chatbot Crusher is a web-based AI chatbot application built with Python. It integrates various AI and NLP tools to allow users to interact naturally and get instant responses. This project is designed for developers, students, and enthusiasts to explore AI-driven conversational interfaces.

Features

Web-based AI chatbot interface

Text input and output

Integration with AI APIs (like OpenAI or other services)

Extensible for adding custom commands, APIs, or data sources

Easy deployment with virtual environments

Technologies Used

Python 3.x

Flask – Web framework

TextBlob – Natural language processing

SpeechRecognition – Speech-to-text

Requests – API requests

TQDM – Progress bars

Werkzeug – WSGI utilities

Pytz – Timezone handling

dotenv – Load environment variables

Regex – Text processing

SerpAPI – Optional search API integration

Installation

Clone the repository

git clone https://github.com/Zubair-zahidi/ai-chatbot-crusher.git
cd ai-chatbot-crusher


Create a virtual environment

python -m venv .venv


Activate the virtual environment

On Windows:

.venv\Scripts\activate


On macOS/Linux:

source .venv/bin/activate


Install dependencies

pip install -r requirements.txt

Configuration

Create a .env file in the root of the project:

OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here


Replace the keys with your actual API keys. You need an OpenAI API key for GPT integration and optionally a SerpAPI key for live searches.

Make sure .env is not committed to Git to keep your keys safe.

Running the App
python app.py


The app should be accessible at http://127.0.0.1:5000/

Enter your query in the input box and get responses from the AI

Usage

Type a question or command in the chat input

Press enter or click send

The AI will respond based on the configured API and logic
