import os
import threading
import google.generativeai as palm
from pyrogram import Client, filters
from flask import Flask
import time

start_time = time.time() 

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
    try:
        response = palm.generate_text(
            model='models/text-bison-001',
            prompt=text,
            temperature=0.7,
            candidate_count=1,
            top_k=40,
            top_p=0.95,
            max_output_tokens=1024,
        )
        return response.result
    except Exception as e:
        return f"Error generating text: {str(e)}"

# ------------------ Bot Commands ------------------

@userbot.on_message(filters.text & ~filters.bot & filters.me)
async def generate_text(client, message):
    # Check if the message starts with "."
    if not message.text.startswith("."):
        return

    # Generate text based on the prompt
    prompt_text = message.text[1:]
    generated_text = await palmgen(prompt_text)

    # Reply to the original message with the generated text
    await message.reply_text(generated_text)

@userbot.on_message(filters.command("ping") & filters.me)
async def ping(client, message):
    await message.reply("Pong!")

@userbot.on_message(filters.command("start") & filters.me)
async def start(client, message):
    await message.reply("Welcome to PalmUserBot! Use /help for a list of commands.")

@userbot.on_message(filters.command("stats") & filters.me)
async def stats(client, message):
    uptime = time.time() - start_time
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    await message.reply(f"**Uptime:** {int(hours)}h {int(minutes)}m {int(seconds)}s")

@userbot.on_message(filters.command("help") & filters.me)
async def help_command(client, message):
    help_text = """
    **Commands:**
    /start - Start the userbot.
    /stats - Display bot uptime.
    /help - This help message.
    /echo - Echo back a message.
    /id - Get the chat or a user's ID.
    """
    await message.reply(help_text)

@userbot.on_message(filters.command("echo") & filters.me)
async def echo(client, message):
    if message.reply_to_message:
        await message.reply(message.reply_to_message.text)
    else:
        await message.reply("Reply to a message to echo it.")

@userbot.on_message(filters.command("id") & filters.me)
async def get_id(client, message):
    if message.reply_to_message:
        uid = message.reply_to_message.from_user.id
        await message.reply(f"User ID: {uid}")
    else:
        cid = message.chat.id
        await message.reply(f"Chat ID: {cid}")    

# ------------------ Flask Routes ------------------

@app.route("/")
def health_check():
    return "Health Check: OK!", 200

# ------------------ Main Execution ------------------

def run_flask_app():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask_app)
    t.start()
    userbot.run()
