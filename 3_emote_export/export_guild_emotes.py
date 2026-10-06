"""Download every custom emote of a guild at size 128 (PNG static, GIF animated).

Usage: python -I export_guild_emotes.py <out_dir>   (reads config.json next to this script)
Never prints the token.
"""
import json
import struct
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = "DiscordBot (https://example.invalid, 1.0)"


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def dims(data, animated):
    if animated and data[:3] == b"GIF":
        return struct.unpack("<HH", data[6:10])
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    return (0, 0)


def main():
    t0 = time.time()
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    raw = get(
        f"https://discord.com/api/v10/guilds/{cfg['guild_id']}/emojis",
        {"Authorization": f"Bot {cfg['token']}"},
    )
    emojis = json.loads(raw)
    print(f"{len(emojis)} emotes listed")
    small, failed = [], []
    for e in emojis:
        animated = bool(e.get("animated"))
        ext = "gif" if animated else "png"
        name = e["name"]
        dest = out / f"{name}.{ext}"
        if dest.exists():
            dest = out / f"{name}_{e['id']}.{ext}"
        url = f"https://cdn.discordapp.com/emojis/{e['id']}.{ext}?size=128&quality=lossless"
        try:
            data = get(url)
        except Exception as ex:  # noqa: BLE001
            failed.append((name, str(ex)))
            continue
        dest.write_bytes(data)
        w, h = dims(data, animated)
        if 0 < w < 128:
            small.append((dest.name, w, h))
        time.sleep(0.15)
    print(f"saved to {out}")
    print(f"under 128px: {len(small)}")
    for n, w, h in small:
        print(f"  {n} {w}x{h}")
    print(f"failed: {len(failed)}")
    for n, m in failed:
        print(f"  {n}: {m}")
    print(f"done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
