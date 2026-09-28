# -*- coding: utf-8 -*-
"""Генерация прогулочного аудио (mp3) из текстового скрипта через edge-tts.

Использование:
    python make-audio.py <script.txt> <out.mp3> [voice]

Скрипт — простой UTF-8 текст, абзацы через пустую строку. Голос по умолчанию
ru-RU-DmitryNeural (альтернатива: ru-RU-SvetlanaNeural). Нужен интернет
на момент генерации; результат — самодостаточный mp3 для телефона.
"""
import asyncio
import sys
from pathlib import Path

import edge_tts

DEFAULT_VOICE = "ru-RU-DmitryNeural"


async def make(text: str, out: Path, voice: str) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out))


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    voice = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_VOICE
    text = src.read_text(encoding="utf-8").strip()
    # edge-tts лучше переваривает текст с одинарными переносами строк внутри абзаца
    out.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(make(text, out, voice))
    size = out.stat().st_size
    print(f"OK: {out} ({size/1024:.0f} KB, voice={voice})")


if __name__ == "__main__":
    main()
