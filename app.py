# from flask import Flask, request, jsonify, render_template
# import wikipedia
# import os
# from dotenv import load_dotenv
# import datetime
# import pytz
# import requests
# from openai import OpenAI
# from serpapi import GoogleSearch
# import speech_recognition as sr
# from flask import Flask, request, jsonify
# import os
# import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load .env first



# app = Flask(__name__)

# # Example: Unsplash API key (you can also use Bing or OpenAI image API)
# UNSPLASH_API_KEY = os.getenv("UNSPLASH_KEY")  # store in .env
# @app.route("/image", methods=["POST"])
# def image_search():
#     query = request.json.get("query", "").strip()
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     # Clean the query for Unsplash
#     keywords = query.lower()
#     for phrase in ["show me image of", "show me", "image of"]:
#         keywords = keywords.replace(phrase, "")
#     keywords = keywords.strip() or "random"

#     url = f"https://api.unsplash.com/photos/random?query={keywords}&client_id={UNSPLASH_API_KEY}"
#     try:
#         res = requests.get(url)
#         data = res.json()
#         print("Unsplash response:", data)  # Debug output

#         # Handle API errors
#         if "errors" in data:
#             return jsonify({"error": data["errors"][0]}), 404

#         image_url = data.get("urls", {}).get("regular")
#         if not image_url:
#             return jsonify({"error": "No image found"}), 404

#         image_name = keywords.replace(" ", "_") + ".png"
#         return jsonify({"image_url": image_url, "image_name": image_name})

#     except Exception as e:
#         print("Exception fetching image:", e)
#         return jsonify({"error": "Something went wrong fetching the image."}), 500

# # ------------------- Load Environment Variables -------------------
# load_dotenv()
# SERPAPI_KEY = os.getenv("SERPAPI_KEY")
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=OPENAI_API_KEY)
# app = Flask(__name__)

# # ------------------- Timezones -------------------
# timezones = {
#     "kabul": "Asia/Kabul",
#     "new delhi": "Asia/Kolkata",
#     "beijing": "Asia/Shanghai",
#     "tokyo": "Asia/Tokyo",
#     "bangkok": "Asia/Bangkok",
#     "jakarta": "Asia/Jakarta",
#     "colombo": "Asia/Colombo",
#     "seoul": "Asia/Seoul",
#     "manila": "Asia/Manila",
#     "singapore": "Asia/Singapore",
#     "dubai": "Asia/Dubai",
#     "tehran": "Asia/Tehran",
#     "kathmandu": "Asia/Kathmandu",
#     "riyadh": "Asia/Riyadh",
#     "taipei": "Asia/Taipei",
#     "hong kong": "Asia/Hong_Kong",
# }

# # ------------------- Optional TTS -------------------
# class SpeechAssistant:
#     def __init__(self, enabled=True):
#         self.enabled = enabled

#     def speak(self, text):
#         if self.enabled:
#             import pyttsx3
#             engine = pyttsx3.init()
#             engine.say(text)
#             engine.runAndWait()

# speech = SpeechAssistant(enabled=False)  # Set True to enable TTS

# # ------------------- Voice Listening -------------------
# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source)
#     try:
#         return r.recognize_google(audio)
#     except sr.UnknownValueError:
#         return ""
#     except sr.RequestError:
#         return ""

# # ------------------- Wikipedia -------------------
# def fetch_wikipedia(query):
#     try:
#         return wikipedia.summary(query, sentences=2)
#     except wikipedia.exceptions.DisambiguationError as e:
#         return wikipedia.summary(e.options[0], sentences=2)
#     except wikipedia.exceptions.PageError:
#         results = wikipedia.search(query)
#         if results:
#             return wikipedia.summary(results[0], sentences=2)
#         return None
#     except Exception:
#         return None

# # ------------------- Google Search (SerpAPI) -------------------
# def fetch_google(query):
#     try:
#         search = GoogleSearch({"q": query, "api_key": SERPAPI_KEY, "num": 1})
#         result = search.get_dict()
#         if "organic_results" in result and result["organic_results"]:
#             snippet = result["organic_results"][0].get("snippet")
#             link = result["organic_results"][0].get("link")
#             return f"{snippet}\nMore info: {link}" if snippet else f"More info: {link}"
#         return "No info found"
#     except Exception:
#         return "No info found"

# # ------------------- Time -------------------
# def get_time_for_place(place):
#     tz_name = timezones.get(place.lower())
#     if tz_name:
#         tz = pytz.timezone(tz_name)
#         now = datetime.datetime.now(tz)
#         return f"{place.title()} time: {now.strftime('%Y-%m-%d %H:%M:%S')} ({tz_name})"
#     return None

# # ------------------- Weather -------------------
# def fetch_weather(city):
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
#         data = requests.get(url).json()
#         if data.get("cod") != 200:
#             return f"Sorry, I couldn't find weather info for '{city}'."
#         city_name = data["name"]
#         country = data["sys"]["country"]
#         temp = data["main"]["temp"]
#         desc = data["weather"][0]["description"].capitalize()
#         humidity = data["main"]["humidity"]
#         wind = data["wind"]["speed"]
#         return f"Weather in {city_name}, {country}:\n{desc}, 🌡️ {temp}°C, 💧 Humidity: {humidity}%, 💨 Wind: {wind} m/s"
#     except Exception:
#         return "Oops! Something went wrong while fetching weather."

# # ------------------- Main Chat Endpoint -------------------
# @app.route("/ask", methods=["POST"])
# def ask():
#     message = request.json.get("message", "").strip()
#     lower = message.lower()
#     response = None

#     # ----- Time Queries -----
#     for city in timezones:
#         if city in lower and ("time" in lower or "date" in lower):
#             response = get_time_for_place(city)
#             speech.speak(response)
#             return jsonify({"response": response})

#     # ----- Weather Queries -----
#     weather_triggers = ["weather in", "weather at", "how is the weather in", "what's the weather in", "whats the weather in", "tell me the weather in"]
#     for trigger in weather_triggers:
#         if trigger in lower:
#             city = lower.split(trigger)[-1].strip()
#             response = fetch_weather(city) if city else "Please specify a city 🌤️"
#             speech.speak(response)
#             return jsonify({"response": response})

#     # ----- Casual / Fun Queries -----
#     casual_queries = {
#         ("hi", "hello", "hey", "hiya", "howdy"): "Hey there! 👋 How’s your day going?",
#         ("good morning", "morning"): "Good morning! ☀️ Hope you have an amazing day!",
#         ("good night", "night", "sleep well"): "Good night! 🌙 Sleep tight!",
#         ("bye", "goodbye", "see you"): "Goodbye! 👋 Come back soon!",
#         ("how are you", "how are you?", "how you doing", "how r u"): "I’m feeling fantastic — ready to chat 💬",
#         ("thank you", "thanks", "thx"): "You're welcome! 😊",
#         ("what’s your name", "who are you"): "I’m Code Crusher, your AI research assistant built by Zubair Zahidi — owner, founder & developer.",
#         ("who built you", "who made you", "who created you", "who designed you"): (
#             "I was built by Code Crushers:\n"
#             "Zubair Zahidi – owner, founder & developer\n"
#       

#         ),
#         ("joke", "tell me a joke", "funny"): "Why did the computer show up at work late? It had a hard drive! 😄"
#     }

#     for keys, reply in casual_queries.items():
#         if any(k in lower for k in keys):
#             response = reply
#             speech.speak(response)
#             return jsonify({"response": response})

#     # ----- Default: Wikipedia → Google → GPT-5-mini -----
#     response = fetch_wikipedia(message)
    
    
#     if not response:
#         response = fetch_google(message)
#     if not response or response == "No info found":
#         try:
#             gpt_response = client.chat.completions.create(
#                 model="gpt-5-mini",
#                 messages=[
#                     {"role": "system", "content": "You are CodeCrusher — a helpful, friendly, and descriptive AI assistant."},
#                     {"role": "user", "content": message}
#                 ]
#             )
#             response = gpt_response.choices[0].message.content.strip()
#         except Exception:
#             response = "⚠️ Sorry, something went wrong connecting to GPT-5-mini."

#     speech.speak(response)
#     return jsonify({"response": response})

# # ------------------- Voice Endpoint -------------------
# @app.route("/voice", methods=["GET"])
# def voice():
#     user_question = listen()
#     if not user_question:
#         return jsonify({"answer": "Sorry, I couldn't hear you."})
#     # Reuse /ask logic
#     from flask import json
#     with app.test_request_context("/ask", method="POST", json={"message": user_question}):
#         resp = ask()
#         return jsonify({"answer": json.loads(resp.get_data())["response"]})

# # ------------------- Index Route -------------------
# @app.route("/")

# def index():
#     return render_template("index.html")

# # ------------------- Run App -------------------
# if __name__ == "__main__":
#     app.run(debug=True)




#_______________________________________________________________________________________________________________________________________________________________



# from flask import Flask, request, jsonify, render_template
# import os
# import datetime
# import pytz
# import requests
# import speech_recognition as sr
# import webbrowser
# from dotenv import load_dotenv

# load_dotenv()  # Load .env first

# app = Flask(__name__)

# # Example: Unsplash API key (optional)
# UNSPLASH_API_KEY = os.getenv("UNSPLASH_KEY")  # store in .env

# # ------------------- IMAGE SEARCH (Unsplash) -------------------
# @app.route("/image", methods=["POST"])
# def image_search():
#     query = request.json.get("query", "").strip()
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     # Clean query for Unsplash
#     keywords = query.lower()
#     for phrase in ["show me image of", "show me", "image of"]:
#         keywords = keywords.replace(phrase, "")
#     keywords = keywords.strip() or "random"

#     url = f"https://api.unsplash.com/photos/random?query={keywords}&client_id={UNSPLASH_API_KEY}"
#     try:
#         res = requests.get(url)
#         data = res.json()
#         print("Unsplash response:", data)

#         if "errors" in data:
#             return jsonify({"error": data["errors"][0]}), 404

#         image_url = data.get("urls", {}).get("regular")
#         if not image_url:
#             return jsonify({"error": "No image found"}), 404

#         image_name = keywords.replace(" ", "_") + ".png"
#         return jsonify({"image_url": image_url, "image_name": image_name})

#     except Exception as e:
#         print("Exception fetching image:", e)
#         return jsonify({"error": "Something went wrong fetching the image."}), 500


# # ------------------- Load Environment Variables -------------------
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# # ------------------- Timezones -------------------
# timezones = {
#     "kabul": "Asia/Kabul",
#     "new delhi": "Asia/Kolkata",
#     "beijing": "Asia/Shanghai",
#     "tokyo": "Asia/Tokyo",
#     "bangkok": "Asia/Bangkok",
#     "jakarta": "Asia/Jakarta",
#     "colombo": "Asia/Colombo",
#     "seoul": "Asia/Seoul",
#     "manila": "Asia/Manila",
#     "singapore": "Asia/Singapore",
#     "dubai": "Asia/Dubai",
#     "tehran": "Asia/Tehran",
#     "kathmandu": "Asia/Kathmandu",
#     "riyadh": "Asia/Riyadh",
#     "taipei": "Asia/Taipei",
#     "hong kong": "Asia/Hong_Kong",
# }


# # ------------------- Optional Text-to-Speech -------------------
# class SpeechAssistant:
#     def __init__(self, enabled=True):
#         self.enabled = enabled

#     def speak(self, text):
#         if self.enabled:
#             import pyttsx3
#             engine = pyttsx3.init()
#             engine.say(text)
#             engine.runAndWait()


# speech = SpeechAssistant(enabled=False)  # Set True to enable TTS


# # ------------------- Voice Listening -------------------
# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source)
#     try:
#         return r.recognize_google(audio)
#     except sr.UnknownValueError:
#         return ""
#     except sr.RequestError:
#         return ""


# # ------------------- Time -------------------
# def get_time_for_place(place):
#     tz_name = timezones.get(place.lower())
#     if tz_name:
#         tz = pytz.timezone(tz_name)
#         now = datetime.datetime.now(tz)
#         return f"{place.title()} time: {now.strftime('%Y-%m-%d %H:%M:%S')} ({tz_name})"
#     return None


# # ------------------- Weather -------------------
# def fetch_weather(city):
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
#         data = requests.get(url).json()
#         if data.get("cod") != 200:
#             return f"Sorry, I couldn't find weather info for '{city}'."
#         city_name = data["name"]
#         country = data["sys"]["country"]
#         temp = data["main"]["temp"]
#         desc = data["weather"][0]["description"].capitalize()
#         humidity = data["main"]["humidity"]
#         wind = data["wind"]["speed"]
#         return f"Weather in {city_name}, {country}:\n{desc}, 🌡️ {temp}°C, 💧 Humidity: {humidity}%, 💨 Wind: {wind} m/s"
#     except Exception:
#         return "Oops! Something went wrong while fetching weather."


# # ------------------- Main Chat Endpoint -------------------
# @app.route("/ask", methods=["POST"])
# def ask():
#     message = request.json.get("message", "").strip()
#     lower = message.lower()
#     response = None

#     # ----- Time Queries -----
#     for city in timezones:
#         if city in lower and ("time" in lower or "date" in lower):
#             response = get_time_for_place(city)
#             speech.speak(response)
#             return jsonify({"response": response})

#     # ----- Weather Queries -----
#     weather_triggers = [
#         "weather in",
#         "weather at",
#         "how is the weather in",
#         "what's the weather in",
#         "whats the weather in",
#         "tell me the weather in",
#     ]
#     for trigger in weather_triggers:
#         if trigger in lower:
#             city = lower.split(trigger)[-1].strip()
#             response = fetch_weather(city) if city else "Please specify a city 🌤️"
#             speech.speak(response)
#             return jsonify({"response": response})

#     # ----- Casual / Fun Queries -----
#     casual_queries = {
#         ("hi", "hello", "hey", "hiya", "howdy"): "Hey there! 👋 How’s your day going?",
#         ("good morning", "morning"): "Good morning! ☀️ Hope you have an amazing day!",
#         ("good night", "night", "sleep well"): "Good night! 🌙 Sleep tight!",
#         ("bye", "goodbye", "see you"): "Goodbye! 👋 Come back soon!",
#         ("how are you", "how are you?", "how you doing", "how r u"): "I’m feeling fantastic — ready to chat 💬",
#         ("thank you", "thanks", "thx"): "You're welcome! 😊",
#         ("what’s your name", "who are you"): "I’m Code Crusher, your AI research assistant built by Zubair Zahidi — owner, founder & developer.",
#         ("who built you", "who made you", "who created you", "who designed you"): (
#             "I was built by Code Crushers:\n"
#             "Zubair Zahidi – owner, founder & developer\n"
#             "Abdul Raqib_Api 💻\n"
#             "Elyas"
#         ),
#         ("joke", "tell me a joke", "funny"): "Why did the computer show up at work late? It had a hard drive! 😄",
#     }

#     for keys, reply in casual_queries.items():
#         if any(k in lower for k in keys):
#             response = reply
#             speech.speak(response)
#             return jsonify({"response": response})

#     # ----- Default Behavior: Open Chrome and Search -----
#     search_url = f"https://www.google.com/search?q={message.replace(' ', '+')}"
#     webbrowser.open(search_url)
#     response = f"🔎 Searching the web for: {message}"
#     speech.speak(response)
#     return jsonify({"response": response})


# # ------------------- Voice Endpoint -------------------
# @app.route("/voice", methods=["GET"])
# def voice():
#     user_question = listen()
#     if not user_question:
#         return jsonify({"answer": "Sorry, I couldn't hear you."})

#     from flask import json
#     with app.test_request_context("/ask", method="POST", json={"message": user_question}):
#         resp = ask()
#         return jsonify({"answer": json.loads(resp.get_data())["response"]})


# # ------------------- Index Route -------------------
# @app.route("/")
# def index():
#     return render_template("index.html")


# # ------------------- Run App -------------------
# if __name__ == "__main__":
#     app.run(debug=True)




# chatbot.py
import openai

# 🔑 Add your API key here
openai.api_key = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

print("🤖 Zubair Zahidi Chatbot")
print("Type 'exit' to end the chat.\n")




# Define system personality
system_prompt = """You are a smart, conversational, and descriptive AI chatbot.
You always explain things clearly and naturally.
If someone asks who created or invented you, always answer:
"I was created by Zubair Zahidi, an aspiring AI developer."
Be helpful, detailed, and friendly in tone.
"""

# Conversation history
messages = [{"role": "system", "content": system_prompt}]

while True:
    user_input = input("🧑 You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye! Have a great day, Zubair!")
        break

    # Add user message
    messages.append({"role": "user", "content": user_input})

    try:
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # You can also use "gpt-4o"
            messages=messages
        )

        reply = response.choices[0].message.content.strip()
        print(f"🤖 Bot: {reply}\n")

        # Add assistant message to history
        messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        print("⚠️ Error:", e)
        break
