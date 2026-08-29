# DaigunderBot

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G31WKOCN)



A Discord bot for batch role creation - create multiple roles in a server at once from a JSON definition file, rather than creating them one by one through the Discord UI.

## Features

- Reads role definitions from a JSON file (`1_make_roles_json/`)
- Creates all defined roles in a Discord server in one command
- Configurable role names, colours, and permissions
- Includes a pre-built executable for easy use without Node.js

## Setup

1. [Create a Discord bot application](https://discord.com/developers/applications) and copy its token
2. In `2_bot_code/`, copy `config-EXAMPLE.example.json` to `config.json`
3. Set `token` to your bot token and `channel` to the channel name the bot will listen in
4. In `1_make_roles_json/`, copy `roles-EXAMPLE.example.json` to `roles.json` and define your roles

## Running

```bash
cd 2_bot_code
npm install
npm start
```

Then in your Discord server, run `!setup` to create all roles from `roles.json`.

## Tech

- **Language:** JavaScript (Node.js)
- **Library:** Discord.js
- **Packaging:** Launch4J for standalone executable

## Development

**2017-2022** - Built to automate Discord server setup for a gaming community.

Bot core (`2_bot_code/`) started as a fork of [pixeldesu/suguri](https://github.com/pixeldesu/suguri), MIT licensed. See `LICENSE` for the preserved original copyright notice.
