"""Download emotes listed in emote_ids.txt (name=id,...) from the public CDN at size 128.

Animated ones saved as GIF, static as PNG. Usage: python -I download_from_ids.py <out_dir>
"""
import struct
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def dims(data):
    if data[:3] == b"GIF":
        return struct.unpack("<HH", data[6:10])
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    return (0, 0)


def main():
    t0 = time.time()
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    pairs = [p.split("=") for p in (HERE / "emote_ids.txt").read_text().strip().split(",")]
    small, failed, anim = [], [], 0
    for name, eid in pairs:
        base = f"https://cdn.discordapp.com/emojis/{eid}"
        try:
            probe = get(f"{base}.webp?size=128&animated=true")
            animated = b"ANIM" in probe[:64]
            if animated:
                data, ext = get(f"{base}.gif?size=128"), "gif"
                anim += 1
            else:
                data, ext = get(f"{base}.png?size=128&quality=lossless"), "png"
        except Exception as ex:  # noqa: BLE001
            failed.append((name, str(ex)))
            continue
        dest = out / f"{name}.{ext}"
        if dest.exists():
            dest = out / f"{name}_{eid}.{ext}"
        dest.write_bytes(data)
        w, h = dims(data)
        if 0 < max(w, h) < 128:
            small.append((dest.name, w, h))
        time.sleep(0.15)
    print(f"{len(pairs)} listed, {anim} animated, saved to {out}")
    print(f"under 128px: {len(small)}")
    for n, w, h in small:
        print(f"  {n} {w}x{h}")
    print(f"failed: {len(failed)}")
    for n, m in failed:
        print(f"  {n}: {m}")
    print(f"done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
