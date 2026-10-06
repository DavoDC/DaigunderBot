"""Upscale every emote whose long side is under 128px to a 128px long side (Real-ESRGAN anime x4, then Lanczos down).

Usage: python -I upscale_small.py <out_dir> <in_dir> [<in_dir> ...]
PNG: upscaled directly. GIF: frames split, upscaled in one batch, rebuilt with the original timing.
"""
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageSequence

HERE = Path(__file__).resolve().parent
EXE = HERE / "esrgan" / "realesrgan-ncnn-vulkan.exe"
WORK = HERE / "work"
TARGET = 128


def run_esrgan(src_dir, dst_dir):
    dst_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [str(EXE), "-i", str(src_dir), "-o", str(dst_dir), "-n", "realesrgan-x4plus-anime", "-f", "png"],
        check=True, cwd=EXE.parent, capture_output=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def fit(img):
    w, h = img.size
    s = TARGET / max(w, h)
    return img.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)


def do_png(path, out_dir):
    src, dst = WORK / "p_in", WORK / "p_out"
    shutil.rmtree(WORK, ignore_errors=True)
    src.mkdir(parents=True)
    shutil.copy(path, src / "a.png")
    run_esrgan(src, dst)
    fit(Image.open(dst / "a.png").convert("RGBA")).save(out_dir / path.name)


def do_gif(path, out_dir):
    src, dst = WORK / "g_in", WORK / "g_out"
    shutil.rmtree(WORK, ignore_errors=True)
    src.mkdir(parents=True)
    im = Image.open(path)
    durations = []
    for i, fr in enumerate(ImageSequence.Iterator(im)):
        fr.convert("RGBA").save(src / f"{i:04d}.png")
        durations.append(fr.info.get("duration", 50))
    run_esrgan(src, dst)
    frames = [fit(Image.open(p).convert("RGBA")) for p in sorted(dst.glob("*.png"))]
    frames[0].save(
        out_dir / path.name, save_all=True, append_images=frames[1:],
        duration=durations, loop=0, disposal=2, optimize=False,
    )


def main():
    t0 = time.time()
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    done, failed = [], []
    for d in sys.argv[2:]:
        for p in sorted(Path(d).iterdir()):
            if p.suffix.lower() not in (".png", ".gif"):
                continue
            with Image.open(p) as im:
                if max(im.size) >= TARGET:
                    continue
            try:
                (do_gif if p.suffix.lower() == ".gif" else do_png)(p, out_dir)
                done.append(p.name)
                print(f"ok {p.name}", flush=True)
            except Exception as ex:  # noqa: BLE001
                failed.append((p.name, repr(ex)))
                print(f"FAIL {p.name} {ex!r}", flush=True)
    shutil.rmtree(WORK, ignore_errors=True)
    print(f"upscaled {len(done)}, failed {len(failed)}, {time.time() - t0:.0f}s")
    for n, m in failed:
        print(f"  {n}: {m}")


if __name__ == "__main__":
    main()
