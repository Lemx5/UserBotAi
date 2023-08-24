# PALM Telegram Bot 🤖
#### A Telegram user bot powered by Google's PALM generativeai to instantly transform prompts into expansive text.

### 🌟 Features
Instant Response: Automatically listens to messages beginning with a . (dot).
In-place Editing: Modifies the original message to display the newly generated content.
Safe & Secure: All operations and data remain within your chosen hosting environment.

### 🛠 Setup & Deployment
#### Requirements
- Python 3.6 or higher
- Telegram API Key
- Google Cloud API Key
- Pyrogram

#### Installation
1. Clone the repository: `git clone https://github.com/irymee/PaLM-UserBot.git`
2. Enter the directory: `cd PaLM-UserBot`
3. Install the required dependencies: `pip3 install -r requirements.txt`
4. Fill in the required values in `bot.py`
5. Run the bot: `python3 bot.py`

#### Deployment in Render
Push the repository containing the Dockerfile and render.yml to GitHub or GitLab.
Securely set your secrets (API_ID, API_HASH, SESSION_STRING, PALM_API_KEY) in the Render dashboard.
Link your repository to Render. It will recognize the render.yml and initiate the deployment.

### 💡 Usage
1. Send a message beginning with a . (dot) to the bot.

```javascript
.Hello
```
2. Wait for the bot to respond with the generated text.