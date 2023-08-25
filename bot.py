import os
import asyncio
import google.generativeai as palm
from pyrogram import Client, filters
from quart import Quart, render_template_string, send_from_directory
import time
from datetime import datetime
import random

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

# Quart App Initialization
app = Quart(__name__)

# ------------------ Palm Generator ------------------
def palmgen(text):
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
    
    if not message.text.startswith("."):
        return

    prompt_text = message.text[1:]
    generated_text = palmgen(prompt_text)
    
    # Edit the original message with the generated text
    await message.edit_text(f"{generated_text}")

    if message.text == ".ping":
        await message.edit_text(f"Pong! `{time.time() - start_time:.3f}` ms")
        return    

@userbot.on_message(filters.command("time", prefixes="!") & filters.me)
async def time(client, message):
    now = datetime.datetime.now().strftime("Date: %d/%m/%Y\nTime: %H:%M:%S")
    await message.edit(now)

    
# ------------------ Quart Routes ------------------
@app.route('/')
async def index():
    chosen_file = random.choice(['index.html', 'index2.html'])
    return await render_template_string(chosen_file)

# ------------------ Main Execution ------------------

async def main():
    await asyncio.gather(
        app.run_task(host="0.0.0.0", port=8080),
        userbot.start()
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
