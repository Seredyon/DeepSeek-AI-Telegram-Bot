# Telegram Bot with DeepSeek Integration

This is a Telegram bot that integrates with the DeepSeek API to provide chat and coding assistance.

## Features

- Interactive chat mode with the DeepSeek AI.
- Coding assistance mode for programming tasks.
- Ability to switch between modes.
- Clear command to reset the dialog context.
- Send requests and responses from users (indicating the username in the hyperlink) directly to you in Discord using a webhook.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Seredyon/DeepSeek-AI-Telegram-Bot.git
cd DeepSeek-AI-Telegram-Bot
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Replace the placeholders in the `bot.py` file with your actual bot token, DeepSeek API key, and Discord webhook URL.

4. Run the bot:

```bash
python bot.py
```

## Usage

- Use the `/start` command to begin interacting with the bot.
- Use the `/mode` command to switch between chat and coding modes.
- Use the `/clear` command to reset the dialog context.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial License 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
