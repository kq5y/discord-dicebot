# discord-dicebot

## Usage

1. Create an Application on [Developer Portal](https://discord.com/developers/applications).
1. Set `MESSAGE CONTENT INTENT` to True from the **Bot** and issue a token.
1. Select `scopes=bot` in the **OAuth2** URL Generator and select the following permissions.
    - Read Messages/View Channels
    - Send Messages
    - Send Messages in Threads
    - Read Message History
1. Invite the bot to the server using the generated URL.
1. Write `DISCORD_TOKEN` in the `.env` file.
1. Execute the command below.

```bash
poetry install
poetry run python app/main.py
```

or

```bash
docker build .
```

## LICENSE

[MIT License](https://github.com/tksnnx/discord-dicebot/blob/main/LICENSE)