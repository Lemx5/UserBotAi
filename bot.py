import os
import asyncio
import google.generativeai as palm
from pyrogram import Client, filters
from quart import Quart, render_template_string
import random

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
    
# ------------------ Quart Routes ------------------
# Function to load the content of a template file into a string
def load_template(filename):
    with open(os.path.join('templates', filename), 'r') as f:
        return f.read()

INDEX = load_template('index.html')
INDEX2 = load_template('index2.html')

@app.route('/')
async def index():
    chosen_template_content = random.choice([INDEX, INDEX2])
    return await render_template_string(INDEX2)
# ------------------ Main Execution ------------------

async def main():
    print("Starting the main function.")
    await asyncio.gather(
        app.run_task(host="0.0.0.0", port=8080),
        userbot.start()
    )
    print("Main function completed.")

if __name__ == "__main__":
    print("Script starting.")
    asyncio.run(main())
