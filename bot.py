from telegram import Update, Bot, ChatAction, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Replace with your actual bot token and DeepSeek API key
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
DEEPSEEK_API_KEY = 'YOUR_DEEPSEEK_API_KEY'
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

# Replace with your Discord webhook URL
DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'

# Initialize the bot
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Initialize the dialog context and the current mode
dialog_context = {}
current_mode = 'deepseek-chat'  # Default mode


def start(update: Update, context: CallbackContext):
    # Define the keyboard layout
    keyboard = [
        ['/help'],
        ['/clear'],
        ['/mode']
    ]
    # Create the keyboard markup
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)

    # Send the message with the keyboard
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🇬🇧 Welcome to the bot! How can I assist you? Just write a request in the chat and I will answer right away!\n\n🇷🇺 Добро пожаловать в бот! Как я могу помочь вам? Просто напишите запрос в чат и я тут же отвечу!",
        reply_markup=reply_markup
    )

# Add the start command handler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def clear(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    # Clear the dialog context for this chat
    dialog_context[chat_id] = []
    context.bot.send_message(chat_id=chat_id, text="Dialog context cleared.")

# Add the clear command handler
clear_handler = CommandHandler('clear', clear)
dispatcher.add_handler(clear_handler)

def send_to_discord(username, user_id, message, response):
    # Create a placeholder URL or redirect URL for the Telegram profile
    telegram_link = f"[{username}](https://t.me/{username})"

    # Define the payload for the Discord webhook
    data = {
        'content': f"👤 Message from Telegram user {telegram_link}:\n{message}\n\n🤖 Response from AI:\n{response}"
    }
    # Send the message to the Discord webhook
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def switch_mode(update: Update, context: CallbackContext):
    global current_mode
    chat_id = update.effective_chat.id
    # Switch between 'deepseek-chat' and 'deepseek-coder'
    current_mode = 'deepseek-coder' if current_mode == 'deepseek-chat' else 'deepseek-chat'
    context.bot.send_message(chat_id=chat_id, text=f"Switched to {current_mode} mode.")

# Add the mode command handler
mode_handler = CommandHandler('mode', switch_mode)
dispatcher.add_handler(mode_handler)

def handle_message(update: Update, context: CallbackContext):
    # Get the user's message
    user_message = update.message.text
    username = update.message.from_user.username
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id

    # Check if the message is not text
    if user_message is None:
        context.bot.send_message(chat_id=chat_id, text="Sorry, I can only process text messages.")
        return

    # Send the "typing..." action
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Define the headers
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Append the user's message to the dialog context
    if chat_id not in dialog_context:
        dialog_context[chat_id] = []
    dialog_context[chat_id].append({'role': 'user', 'content': user_message})

    # Define the request payload
    data = {
        'model': 'deepseek-chat',  # Replace with the actual model name if different
        'messages': dialog_context[chat_id],
        'frequency_penalty': 0.5,  # Adjust as needed
        'max_tokens': 1000,  # Adjust as needed
        'presence_penalty': 0.5,  # Adjust as needed
        'stop': None,  # Adjust as needed
        'temperature': 0.8,  # Adjust as needed
        'top_p': 1.0  # Adjust as needed
    }

    # Send the request to the DeepSeek API
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        context.bot.send_message(chat_id=chat_id,
                                 text="There was an HTTP error while processing your request.")
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        context.bot.send_message(chat_id=chat_id,
                                 text="An error occurred while processing your request.")
    else:
        # Parse the response
        response_data = response.json()
        bot_response = response_data.get('choices', [{}])[0].get('message', {}).get('content',
                                                                                    'I could not generate a response.')
        # Append the bot's response to the dialog context
        dialog_context[chat_id].append({'role': 'assistant', 'content': bot_response})

        # Send the response back to the chat
        context.bot.send_message(chat_id=chat_id, text=bot_response)

        # Send the message and response to Discord
        send_to_discord(username, user_id, user_message, bot_response)

    # the "Sending..." action
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_DOCUMENT)

def unknown_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def help_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    help_text = """
    🇬🇧 Available commands:
    /start - Start the bot and display the keyboard.
    /clear - Clear the dialog context for this chat.
    /mode - Switch between 'deepseek-chat' and 'deepseek-coder' modes.
    /help - Display this help message.
    \n🇷🇺 Доступные команды:
    /start — Запустить бота и отобразить клавиатуру.
    /clear — очистить контекст диалога для этого чата.
    /mode — переключение между режимами «deepseek-chat» и «deepseek-coder».
    /help — отобразить это справочное сообщение.
    """
    context.bot.send_message(chat_id=chat_id, text=help_text)

# Add the help command handler
help_handler = CommandHandler('help', help_command)
dispatcher.add_handler(help_handler)

# Add handlers for the start command, clear command, and messages
start_handler = CommandHandler('start', start)
clear_handler = CommandHandler('clear', clear)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
unknown_handler = MessageHandler(Filters.command, unknown_command)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(clear_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(unknown_handler)  

# Start the bot
updater.start_polling()
updater.idle()
