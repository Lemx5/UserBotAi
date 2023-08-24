import os
import threading
import google.generativeai as palm
from pyrogram import Client, filters
from flask import Flask

# ------------------ Configuration ------------------

# Environmental Variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
PALM_API_KEY = os.environ.get("PALM_API_KEY")

# Palm Client Configuration
palm.configure(api_key=PALM_API_KEY)

# Pyrogram Client Configuration
userbot = Client(
    name="PalmUserBot",
    session_string=SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH
)

# Flask App Initialization
app = Flask(__name__)

# ------------------ Palm Generator ------------------
async def palmgen(text):
    defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.7,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
        'max_output_tokens': 1024,
        'stop_sequences': [],
        'safety_settings': [
            {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 4},
            {"category": "HARM_CATEGORY_TOXICITY", "threshold": 4},
            {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 4},
            {"category": "HARM_CATEGORY_SEXUAL", "threshold": 4},
            {"category": "HARM_CATEGORY_MEDICAL", "threshold": 4},
            {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 4}
        ]
    }

    response = palm.generate_text(**defaults, prompt=text)
    return response.result

# ------------------ Bot Commands ------------------

@userbot.on_message(filters.text & ~filters.bot)
async def generate_text(client, message):
    # Check if the message starts with "."
    if not message.text.startswith("."):
        return

    # Strip the leading "." and generate text based on the remaining message
    prompt_text = message.text[1:]
    generated_text = await palmgen(prompt_text)

    # Edit the original message with the generated text
    await message.edit_text(generated_text)


@userbot.on_message(filters.command("ping", prefixes="."))
async def start(client, message):
    await message.edit_text("Pong!")

# ------------------ Flask Routes ------------------

@app.route("/")
def home():
    return "Hello World!"

# ------------------ Main Execution ------------------

def run_flask_app():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    # Use threading to run both Flask and Pyrogram concurrently
    t = threading.Thread(target=run_flask_app)
    t.start()
    userbot.run()