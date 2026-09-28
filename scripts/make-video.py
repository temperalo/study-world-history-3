# -*- coding: utf-8 -*-
"""Сборка ролика (mp4) из глав: слайд-карточки + озвучка.

Использование:
    python make-video.py <episode.txt> <out.mp4>

episode.txt — по строке на главу:  <путь к mp3>|<Заголовок>|<Подзаголовок>
Каждая глава показывается карточкой ровно на время звучания её mp3.
Требует: ffmpeg, ffprobe, Pillow. LLM-токенов не расходует.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
BG = (15, 23, 42)
FG = (241, 245, 249)
MUT = (148, 163, 184)
DIM = (100, 116, 139)
ACCENTS = [(167, 139, 250), (245, 158, 11), (239, 68, 68), (34, 197, 94), (59, 130, 246)]


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)


def wrap(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, maxw: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def card(idx: int, total: int, title: str, sub: str, accent: tuple) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=accent)
    d.text((80, 90), f"ГЛАВА {idx} / {total}", font=font(26), fill=MUT)
    y = 180
    ft = font(52)
    for line in wrap(d, title, ft, W - 160):
        d.text((80, y), line, font=ft, fill=FG)
        y += 66
    if sub:
        fs = font(30, bold=False)
        y += 24
        for line in wrap(d, sub, fs, W - 160):
            d.text((80, y), line, font=fs, fill=MUT)
            y += 46
    d.text((80, H - 96), "История человечества · тур «на троешника»", font=font(24, bold=False), fill=DIM)
    return img


def dur_of(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    ep_file, out = Path(sys.argv[1]), Path(sys.argv[2])
    chapters = []
    for line in ep_file.read_text(encoding="utf-8").strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("|")
        chapters.append((Path(parts[0].strip()), parts[1].strip(),
                         parts[2].strip() if len(parts) > 2 else ""))
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        vlines = ["ffconcat version 1.0"]
        for i, (mp3, title, sub) in enumerate(chapters, 1):
            p = tdp / f"card{i}.png"
            card(i, len(chapters), title, sub, ACCENTS[(i - 1) % len(ACCENTS)]).save(p)
            vlines.append(f"file '{p.as_posix()}'")
            vlines.append(f"duration {dur_of(mp3):.3f}")
        vlines.append(f"file '{(tdp / f'card{len(chapters)}.png').as_posix()}'")
        vlist = tdp / "video.ffconcat"
        vlist.write_text("\n".join(vlines), encoding="utf-8")
        alist = tdp / "audio.txt"
        alist.write_text("\n".join(f"file '{m.resolve().as_posix()}'" for m, _, _ in chapters), encoding="utf-8")
        audio = tdp / "all.m4a"
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(alist),
                        "-c:a", "aac", "-b:a", "96k", str(audio)], check=True, capture_output=True)
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(vlist),
                        "-i", str(audio), "-c:v", "libx264", "-tune", "stillimage",
                        "-pix_fmt", "yuv420p", "-shortest", str(out)],
                       check=True, capture_output=True)
    size = out.stat().st_size
    total = sum(dur_of(m) for m, _, _ in chapters)
    print(f"OK: {out} ({size/1024/1024:.1f} MB, {total/60:.1f} мин, {len(chapters)} главы)")


if __name__ == "__main__":
    main()
