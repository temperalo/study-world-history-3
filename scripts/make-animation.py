# -*- coding: utf-8 -*-
"""Программная мультипликация: сцены эпохи 1 (неолит) + озвучка = mp4.

Использование:
    python make-animation.py

Рисует кадры PIL-ом (река разливается, растут города, пирамиды, клинопись),
синхронно с главами epoch-01-neolit.mp3, собирает ffmpeg-ом в
epoch-01-neolit-anim.mp4. Требует Pillow + ffmpeg. LLM-токенов не расходует.
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

W, H, FPS = 1280, 720, 10
AUDIO = Path("epoch-01-neolit.mp3")
OUT = Path("epoch-01-neolit-anim.mp4")
CUTS = [87, 134, 178, 201, 243, 286]  # границы глав в секундах

SKY = (15, 23, 42)
LAND = (52, 78, 65)
LAND2 = (38, 58, 48)
WATER = (59, 130, 246)
WATER2 = (96, 165, 250)
SAND = (217, 180, 120)
WHEAT = (234, 200, 90)
FG = (241, 245, 249)
MUT = (148, 163, 184)
PYR = (180, 150, 105)
FIG = (226, 232, 240)


def font(sz, bold=True):
    from PIL import ImageFont
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(f"C:/Windows/Fonts/{name}", sz)


def river(d, y, t, amp=6, band=80):
    """Полоса реки с бегущей волной (не заливает всё ниже)."""
    import math
    top = [(x, y + amp * math.sin(x / 40 + t * 3)) for x in range(0, W + 20, 20)]
    bot = [(x, y + band + amp * math.sin(x / 40 + t * 3 + 0.5)) for x in range(W, -20, -20)]
    d.polygon(top + bot, fill=WATER)
    for x in range(0, W, 90):
        xx = (x + int(t * 60)) % (W + 90) - 45
        d.line([(xx, y + 14), (xx + 26, y + 14)], fill=WATER2, width=3)


def house(d, x, y, s=1, done=True):
    w, h = int(46 * s), int(30 * s)
    if not done:
        d.rectangle([x - w // 2, y - h, x + w // 2, y], outline=MUT, width=2)
        return
    d.rectangle([x - w // 2, y - h, x + w // 2, y], fill=SAND)
    d.polygon([(x - w // 2 - 8, y - h), (x + w // 2 + 8, y - h), (x, y - h - int(20 * s))], fill=(146, 116, 82))


def person(d, x, y, s=1, color=FIG):
    d.ellipse([x - 6 * s, y - int(30 * s), x + 6 * s, y - int(18 * s)], fill=color)
    d.line([(x, y - int(18 * s)), (x, y - int(6 * s))], fill=color, width=max(2, int(4 * s)))
    d.line([(x - int(8 * s), y), (x, y - int(6 * s)), (x + int(8 * s), y)], fill=color, width=max(2, int(4 * s)))


def caption(d, text, sub=""):
    d.rectangle([0, H - 92, W, H], fill=(2, 6, 23))
    d.text((50, H - 74), text, font=font(30), fill=FG)
    if sub:
        d.text((50, H - 34), sub, font=font(20, False), fill=MUT)


def pulse(t, period=4.0):
    return (t % period) / period


def ease(p):
    return min(1.0, max(0.0, p))


# ---------- сцены ----------

def scene_paradox(d, t):
    """Гл 1: охотники против земледельцев: пашня растёт, 'детей' больше."""
    ground = 470
    d.rectangle([0, ground, W, H], fill=LAND)
    river(d, 120, t)
    # слева: охотники бродят
    d.text((90, ground - 260), "охотники", font=font(24, False), fill=MUT)
    for i in range(3):
        x = 100 + i * 70 + int(24 * __import__("math").sin(t * 2 + i))
        person(d, x, ground - 10, 1.3)
    # справа: поле растёт + хижины + много фигурок
    d.text((760, ground - 260), "земледельцы", font=font(24, False), fill=MUT)
    rows = int(ease(t * 1.4) * 5)
    for r in range(rows):
        for c in range(9):
            d.arc([700 + c * 55, ground - 120 + r * 22, 736 + c * 55, ground - 96 + r * 22],
                  180, 300, fill=WHEAT, width=3)
    n = int(ease(t * 1.2) * 7)
    for i in range(n):
        house(d, 760 + (i % 4) * 70, ground - 130 - (i // 4) * 40, 0.8)
    for i in range(2 + int(ease(t) * 8)):
        person(d, 730 + i * 42, ground - 20, 0.9)
    # весы смысла: «рост: x2»
    d.text((W - 340, 70), f"детей: x{2 + int(t * 3)}", font=font(34), fill=WHEAT)
    caption(d, "Парадокс неолита: земледелие сделало жизнь хуже — и победило",
            "проиграло в качестве жизни, выиграло в рождаемости")


def scene_chain(d, t):
    """Гл 2: амбар наполняется, табличка с клинописью, караван."""
    ground = 470
    d.rectangle([0, ground, W, H], fill=LAND2)
    # амбар с зерном
    d.rectangle([120, ground - 150, 300, ground], fill=(87, 68, 48))
    d.polygon([(110, ground - 150), (310, ground - 150), (210, ground - 200)], fill=(146, 116, 82))
    fill_h = int(ease(t * 1.3) * 130)
    for r in range(fill_h // 16):
        for c in range(7):
            d.ellipse([140 + c * 22, ground - 20 - r * 16, 152 + c * 22, ground - 8 - r * 16], fill=WHEAT)
    d.text((140, ground + 14), "излишки → запасы", font=font(22, False), fill=MUT)
    # табличка с "клинописью"
    d.rounded_rectangle([520, ground - 160, 780, ground - 30], 12, fill=(201, 178, 140))
    for r in range(4):
        for c in range(6):
            if (r * 6 + c) < int(ease(t * 1.5) * 24):
                x, y = 545 + c * 38, ground - 140 + r * 30
                d.polygon([(x, y), (x + 16, y + 6), (x, y + 12)], fill=(90, 70, 50))
    d.text((540, ground + 14), "письменность = бухгалтерия", font=font(22, False), fill=MUT)
    # караван
    y = 200
    d.arc([-100, y - 40, W + 100, y + 260], 200, 340, fill=(70, 90, 110), width=4)
    for i in range(6):
        x = 120 + i * 120 + int(ease(t) * 480)
        if x < W - 60:
            d.ellipse([x, y + 40, x + 40, y + 64], fill=(120, 100, 80))
            d.rectangle([x + 12, y + 16, x + 28, y + 44], fill=(150, 120, 90))
    d.text((90, y - 20), "торговые пути", font=font(22, False), fill=MUT)
    caption(d, "Цепочка: запасы → специалисты → торговля → письменность",
            "первая клинопись — таблички учёта зерна и овец (Урук)")


def scene_river_state(d, t):
    """Гл 3: разлив по расписанию, каналы, растёт город, налог течёт в храм."""
    ground = 430
    d.rectangle([0, ground, W, H], fill=LAND)
    # разлив: уровень воды дышит
    lvl = 150 + int(26 * __import__("math").sin(t * 2.2))
    river(d, lvl, t, amp=4)
    # каналы растут
    for i in range(int(ease(t * 1.2) * 4)):
        d.line([(180 + i * 200, lvl + 30), (180 + i * 200, ground)], fill=WATER, width=8)
    # город растёт
    n = int(ease(t * 1.1) * 12)
    for i in range(n):
        house(d, 140 + (i % 6) * 130, ground - 14 - (i // 6) * 46, 1.0)
    # храм-зиккурат справа
    for k in range(3):
        w = 150 - k * 34
        d.rectangle([W - 210 - w // 2, ground - 40 - k * 36, W - 210 + w // 2, ground - k * 36 - 6], fill=SAND)
    # монеты к храму
    p = pulse(t * 0.7)
    x = int(200 + p * (W - 480))
    d.ellipse([x, ground - 60, x + 16, ground - 44], fill=(250, 204, 21))
    caption(d, "Река даёт расписание → каналы требуют организации → власть и налог",
            "кто организует тысячи людей, тот говорит от имени богов")


def scene_india_china(d, t):
    """Гл 4: две панели — Инд (сетка+водопровод) и Китай (вертикаль)."""
    d.rectangle([0, 0, W, H], fill=SKY)
    d.line([(W // 2, 60), (W // 2, H - 110)], fill=(51, 65, 85), width=4)
    ground = 540
    # Инд
    d.rectangle([0, ground, W // 2, H], fill=LAND)
    river(d, 130, t)
    for i in range(int(ease(t * 1.3) * 6) + 1):
        d.line([(120, 200 + i * 52), (560, 200 + i * 52)], fill=(148, 163, 184), width=4)
        d.line([(120 + i * 88, 200), (120 + i * 88, 456)], fill=(148, 163, 184), width=3)
    d.text((90, ground + 24), "Инд: сетка, водопровод — и ни одного дворца", font=font(20, False), fill=MUT)
    # Китай
    d.rectangle([W // 2, ground, W, H], fill=LAND)
    river(d, 130, t)
    base = W - 220
    for k in range(int(ease(t * 1.3) * 5) + 1):
        w = 260 - k * 40
        d.rectangle([base - w // 2, ground - 30 - k * 54, base + w // 2, ground - k * 54], fill=SAND)
    d.text((W // 2 + 70, ground + 24), "Хуанхэ: наводнение → вертикаль власти", font=font(20, False), fill=MUT)
    caption(d, "Мазки: долина Инда и Хуанхэ", "две реки — два разных ответа на вопрос «кто главный»")


def scene_life(d, t):
    """Гл 5: год крестьянина: поле, дом, сборщик налога, микробы."""
    ground = 470
    d.rectangle([0, ground, W, H], fill=LAND)
    river(d, 130, t)
    house(d, 240, ground - 10, 1.4)
    person(d, 320, ground - 6, 1.4)
    for c in range(8):
        d.arc([380 + c * 70, ground - 70, 430 + c * 70, ground - 20], 180, 300, fill=WHEAT, width=4)
    # сборщик приходит по фазе пульса
    phase = pulse(t, 6.0)
    if 0.25 < phase < 0.75:
        person(d, int(480 + (phase - 0.25) * 700), ground - 6, 1.3, color=(250, 204, 21))
        d.text((int(480 + (phase - 0.25) * 700) - 40, ground - 90), "налог!", font=font(22), fill=(250, 204, 21))
    # микробы вокруг деревни
    import math
    for i in range(9):
        a = t * 1.5 + i * 0.7
        x, y = 240 + int(120 * math.cos(a)), ground - 160 + int(50 * math.sin(a))
        r = 6 + int(3 * math.sin(t * 4 + i))
        d.ellipse([x - r, y - r, x + r, y + r], outline=(239, 68, 68), width=3)
    d.text((150, ground - 250), "город и микроб выросли вместе", font=font(22, False), fill=(239, 68, 68))
    caption(d, "Как жили: год задан разливом, налог раз в сезон", "власть на расстоянии = религия, налог = дань богу")


def scene_summary(d, t):
    """Гл 6: три вещи появляются по очереди."""
    d.rectangle([0, 0, W, H], fill=SKY)
    items = ["1 · детей важнее качества жизни", "2 · письменность изобрели для налогов",
             "3 · государство родилось из разлива"]
    for i, s in enumerate(items):
        if t * 3 > i:
            d.rounded_rectangle([140, 170 + i * 120, W - 140, 240 + i * 120], 16,
                                outline=(167, 139, 250), width=3)
            d.text((180, 186 + i * 120), s, font=font(34), fill=FG)
    caption(d, "Эпоха 1 закрыта", "разминка на следующей сессии начнётся с этих трёх вещей")


SCENES = [scene_paradox, scene_chain, scene_river_state, scene_india_china, scene_life, scene_summary]


def main():
    total = CUTS[-1]
    bounds = [0] + CUTS
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        for i in range(int(total * FPS)):
            sec = i / FPS
            ch = max(j for j, b in enumerate(bounds) if sec >= b)
            t_local = (sec - bounds[ch]) / max(1, (bounds[ch + 1] - bounds[ch]))
            img = Image.new("RGB", (W, H), SKY)
            d = ImageDraw.Draw(img)
            SCENES[ch](d, t_local)
            img.save(tdp / f"f{i:05d}.jpg", quality=82)
            if i % 300 == 0:
                print(f"кадр {i}/{int(total * FPS)}")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                        "-i", str(tdp / "f%05d.jpg"), "-i", str(AUDIO),
                        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
                        "-shortest", str(OUT)], check=True)
    print(f"OK: {OUT} ({OUT.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
