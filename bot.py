import os
import asyncio
import google.generativeai as palm
from pyrogram import Client, filters
from quart import Quart, render_template
import aiohttp
import openai
from openai.api_resources import ChatCompletion
# ------------------ Configuration ------------------

# Environmental Variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
PALM_API_KEY = os.environ.get("PALM_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
APP_URL = os.environ.get("APP_URL")


# Palm Client Configuration
palm.configure(api_key=PALM_API_KEY)
# openai api key
openai.api_key = OPENAI_API_KEY

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

# ------------------ OpenAI Generator ------------------
def openaigen(text):
    messages = [{"role": "assistant", "content": text}]
    try:
        MODEL = "gpt-3.5-turbo"    # gpt-3.5-turbo model
        resp = ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
        )
        rep = resp['choices'][0]["message"]["content"]
        return rep
    except Exception as e:
        return f"Error generating text: {str(e)}"
    

# Bot command to switch between generation functions
@userbot.on_message(filters.text & ~filters.bot & filters.me)
async def generate_text(client, message):
    if message.text.startswith("."):  # If the message starts with a dot, use palmgen
        generation_function = palmgen
    elif message.text.startswith(","):  # If the message starts with an exclamation mark, use openaigen
        generation_function = openaigen
    else:
        return  # If the message doesn't start with "." or "!", do nothing
    
    # Extract the prompt text (remove the first character)
    prompt_text = message.text[1:]
    
    # Call the selected generation function
    generated_text = generation_function(prompt_text)
    
    # Edit the original message with the generated text
    await message.edit_text(f"{generated_text}")
       
# ------------------ Quart Routes ------------------

@app.route('/')
async def index():
    return await render_template('profile.html')

@app.route('/status')
async def health_check():
    return {"status": "alive", "message": "Server is running"}

# ------------------ Ping Route so it don't sleep ------------------ 

async def ping_self():
    """Periodically ping itself to prevent sleeping."""
    await asyncio.sleep(10)  # initial sleep for 10 seconds
    while True:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(APP_URL) as response:
                    data = await response.json()  # Fetch the JSON response
                    if response.status == 200 and data.get('status') == 'alive':
                        print("Ping successful!")
                    else:
                        print(f"Ping failed with status: {response.status}")
            except Exception as e:
                print(f"Ping error: {e}")
            await asyncio.sleep(300)  # ping every 5 minutes


# ------------------ Main Execution ------------------

async def main():
    # Start the ping task in the background
    asyncio.create_task(ping_self())
    
    await asyncio.gather(
        app.run_task(host="0.0.0.0", port=8080),
        userbot.start()
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
