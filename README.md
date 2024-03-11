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

- [Get DeepSeek API key](https://platform.deepseek.com/usage)
- Use the `/start` command to begin interacting with the bot.
- Use the `/mode` command to switch between chat and coding modes.
- Use the `/clear` command to reset the dialog context.

## Code Explanation

### Data Payload

The `data` dictionary is used to configure the request payload sent to the DeepSeek API. Here's a brief explanation of each parameter:

- `'model'`: The model to use for the chat completion. Replace with the actual model name if different.
- `'messages'`: The conversation history for the current chat. It includes the messages from the dialog context for the current chat ID.
- `'frequency_penalty'`: A value between 0.0 and 1.0 that adjusts the likelihood of the model to repeat the same line of text. Adjust as needed.
- `'max_tokens'`: The maximum number of tokens (words or subwords) in the generated text. Adjust as needed. (The default in the code is 1000).
- `'presence_penalty'`: A value between 0.0 and 1.0 that adjusts the likelihood of the model to include new topics in the conversation. Adjust as needed.
- `'stop'`: A list of strings that the model will stop generating text after it encounters any of these strings. Adjust as needed.
- `'temperature'`: A value between 0.0 and 1.0 that controls the randomness of the model's output. Higher values will result in more random completions. Adjust as needed.
- `'top_p'`: The cumulative probability threshold for top-p sampling. Adjust as needed.

This payload is then sent to the DeepSeek API via a POST request.
## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial License 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
