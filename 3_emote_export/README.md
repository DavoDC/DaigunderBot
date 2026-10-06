# 3_emote_export

Download custom Discord emotes at the best quality Discord has (up to 128x128): PNG for static, GIF for animated.

## Facts

- The emote CDN is `https://cdn.discordapp.com/emojis/<id>.<ext>?size=N`. Discord never upscales, so `size=1024` or `4096` returns the original upload (128x128 at most, often smaller). Always ask for `size=128` and check the real size.
- Static: `.png?quality=lossless`. Animated: `.gif`. A plain `.webp` is lossy and only the first frame if animated.
- A bot can list only the emotes of servers it is in (`GET /guilds/<id>/emojis`). Emotes from other servers need their IDs another way (see below).
- The export and download scripts need no libraries, only Python 3. `upscale_small.py` also needs Pillow (`pip install pillow`).

## Export one server's emotes (needs this bot in the server)

1. In the [Developer Portal](https://discord.com/developers/applications) open the app, OAuth2, URL Generator, scope `bot`, no permissions needed, open the link and add it to the server (needs Manage Server).
2. Bot page, Reset Token, copy it. Copy `config-EXAMPLE.example.json` to `config.json` (gitignored) and fill in `token` and `guild_id` (right-click the server, Copy Server ID).
3. `python -I export_guild_emotes.py <out_dir>`. It lists every emote under 128px so you know which ones are small.
4. Kick the bot and reset the token when done.

## Download emotes by ID (no bot needed)

`emote_ids.txt` holds `name=id` pairs separated by commas (the shipped file is a sample list). `python -I download_from_ids.py <out_dir>` fetches each from the public CDN, detects animated ones and saves GIF or PNG.

To get IDs for emotes from other servers, open the emote in Discord with developer tools: the `img.emoji` element's `src` contains the ID. A bot like NQN lists names in its alias list; the buttons carry the IDs in the page, so one DOM query per page collects them all.

## Small originals

Many emotes are 56px or 112px at the source and cannot be improved by Discord. Options: find the original art (7TV, BTTV, FFZ serve larger versions) or upscale with an AI upscaler.

## Upscale the small ones

`upscale_small.py <out_dir> <in_dir> [<in_dir> ...]` upscales every PNG or GIF whose long side is under 128px to a 128px long side, using [Real-ESRGAN ncnn Vulkan](https://github.com/xinntao/Real-ESRGAN/releases) (the `realesrgan-ncnn-vulkan-...-windows.zip` from release v0.2.5.0, needs a Vulkan GPU). Unzip it into an `esrgan/` folder next to the script. It uses the `realesrgan-x4plus-anime` model (cleanest on cartoon art) then shrinks to 128px with Lanczos. GIFs are split into frames, upscaled in one batch and rebuilt with the original timing. Works well on flat cartoon emotes; very tiny sources (around 30px) come out softer.
