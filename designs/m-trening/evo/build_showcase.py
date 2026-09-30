#!/usr/bin/env python3
import shutil
import os

ROOT = "/home/user/Logomtrening"
EVO = os.path.join(ROOT, "designs/m-trening/evo")
KIT = os.path.join(ROOT, "designs/m-trening/kit")

# Copy main board and individual variants to workspace root for easy access:
shutil.copyfile(os.path.join(ROOT, "designs/m-trening/evo-board.png"), os.path.join(ROOT, "logo-board.png"))
shutil.copyfile(os.path.join(ROOT, "designs/m-trening/evo-board.svg"), os.path.join(ROOT, "logo-board.svg"))

shutil.copyfile(os.path.join(EVO, "evo-a-v5-dark.png"), os.path.join(ROOT, "variant-a-classic.png"))
shutil.copyfile(os.path.join(EVO, "evo-b-v5-dark.png"), os.path.join(ROOT, "variant-b-sail-m.png"))
shutil.copyfile(os.path.join(EVO, "evo-c-v5-dark.png"), os.path.join(ROOT, "variant-c-aero.png"))

shutil.copyfile(os.path.join(KIT, "logo-classic-remaster-white.svg"), os.path.join(ROOT, "variant-a-classic.svg"))
shutil.copyfile(os.path.join(KIT, "logo-mono-white.svg"), os.path.join(ROOT, "variant-b-sail-m.svg"))
shutil.copyfile(os.path.join(KIT, "logo-aero-flow-white.svg"), os.path.join(ROOT, "variant-c-aero.svg"))

with open(os.path.join(EVO, "evo-a-white.svg"), encoding="utf-8") as f:
    svg_a_w = f.read()
with open(os.path.join(EVO, "evo-a-dark-coral.svg"), encoding="utf-8") as f:
    svg_a_dc = f.read()
with open(os.path.join(EVO, "evo-a-light-coral.svg"), encoding="utf-8") as f:
    svg_a_lc = f.read()

with open(os.path.join(EVO, "evo-b-white.svg"), encoding="utf-8") as f:
    svg_b_w = f.read()
with open(os.path.join(EVO, "evo-b-dark-coral.svg"), encoding="utf-8") as f:
    svg_b_dc = f.read()
with open(os.path.join(EVO, "evo-b-light-coral.svg"), encoding="utf-8") as f:
    svg_b_lc = f.read()

with open(os.path.join(EVO, "evo-c-white.svg"), encoding="utf-8") as f:
    svg_c_w = f.read()
with open(os.path.join(KIT, "logo-aero-flow-color.svg"), encoding="utf-8") as f:
    svg_c_cy = f.read()
with open(os.path.join(EVO, "evo-c-light-coral.svg"), encoding="utf-8") as f:
    svg_c_lc = f.read()

with open(os.path.join(ROOT, "designs/m-trening/evo-board.svg"), encoding="utf-8") as f:
    board_svg = f.read()

html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>М-ТРЕНИНГ — Презентация логотипа</title>
  <style>
    :root {{
      --bg: #070B14;
      --card: #0F172A;
      --border: #1E293B;
      --accent: #FF5733;
      --cyan: #38BDF8;
      --text: #F8FAFC;
      --muted: #94A3B8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'DejaVu Sans', sans-serif;
      line-height: 1.5;
      padding: 28px 24px 64px;
    }}
    .container {{ max-width: 1360px; margin: 0 auto; }}
    .eyebrow {{
      color: var(--accent);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    h1 {{ font-size: 32px; font-weight: 800; margin-bottom: 8px; }}
    .sub {{ color: var(--muted); font-size: 17px; margin-bottom: 28px; }}
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 24px;
      margin-bottom: 40px;
    }}
    .card {{
      background: linear-gradient(180deg, #0F172A 0%, #090D16 100%);
      border: 1.5px solid var(--border);
      border-radius: 20px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .card.featured {{
      border: 2.5px solid var(--accent);
      box-shadow: 0 12px 40px rgba(255, 87, 51, 0.15);
    }}
    .badge {{
      display: inline-block;
      align-self: flex-start;
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      background: #1E293B;
      color: #fff;
    }}
    .badge.hot {{ background: var(--accent); }}
    .badge.cyan {{ background: #0284C7; }}
    .stage-row {{
      display: grid;
      grid-template-columns: 1.45fr 1fr;
      gap: 12px;
      align-items: stretch;
    }}
    .stage-main {{
      background: #04060B;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .stage-main svg {{ width: 100%; height: auto; max-width: 240px; }}
    .stage-side {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .mini-box {{
      flex: 1;
      border-radius: 14px;
      padding: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .mini-box.light {{ background: #FFFFFF; }}
    .mini-box.dark {{ background: #0B1325; border: 1px solid var(--border); }}
    .mini-box svg {{ width: 100%; height: auto; max-width: 125px; }}
    .card h2 {{ font-size: 21px; font-weight: 700; }}
    .card ul {{ padding-left: 18px; color: #CBD5E1; font-size: 14.5px; display: flex; flex-direction: column; gap: 6px; }}
    .dl-row {{ display: flex; gap: 10px; margin-top: auto; padding-top: 8px; flex-wrap: wrap; }}
    .btn {{
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 10px;
      background: #1E293B;
      color: #fff;
      border: 1px solid #334155;
      transition: 0.15s;
    }}
    .btn:hover {{ background: var(--accent); border-color: var(--accent); }}
    .board-wrap {{
      background: #090D16;
      border: 1.5px solid var(--border);
      border-radius: 22px;
      padding: 20px;
      margin-top: 16px;
    }}
    .board-wrap svg, .board-wrap img {{
      width: 100%;
      height: auto;
      border-radius: 14px;
      display: block;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="eyebrow">Редизайн и стилизация исходного логотипа · Без щитов и рамок</div>
    <h1>М-ТРЕНИНГ — Футбольная школа силового тренинга</h1>
    <p class="sub">Три варианта эволюции вашего родного знака (восходящий мяч, орбита, парусник и горизонт «М-ТРЕНИНГ») + примерка на форму и инвентарь</p>

    <div class="grid-3">
      <!-- VARIANT A -->
      <div class="card">
        <span class="badge">ВАРИАНТ A · КЛАССИКА</span>
        <div class="stage-row">
          <div class="stage-main">{svg_a_w}</div>
          <div class="stage-side">
            <div class="mini-box light">{svg_a_lc}</div>
            <div class="mini-box dark">{svg_a_dc}</div>
          </div>
        </div>
        <h2>A. «Чистая Классика» (Ремастеринг)</h2>
        <ul>
          <li>Бережная ювелирная огранка вашего исходного логотипа 1-в-1</li>
          <li>Идеальная сфера мяча, ровные швы и 3 полных прямых паруса</li>
          <li>Убрана мелкая паутина вант — чисто печатается в любом размере</li>
          <li>Выверенный гео-гротеск «М-ТРЕНИНГ» со скруглёнными штрихами</li>
        </ul>
        <div class="dl-row">
          <a class="btn" href="variant-a-classic.png" download>Скачать PNG</a>
          <a class="btn" href="variant-a-classic.svg" download>Скачать SVG</a>
        </div>
      </div>

      <!-- VARIANT B -->
      <div class="card featured">
        <span class="badge hot">ВАРИАНТ B · ФИРМЕННЫЙ ПАРУС-М ★</span>
        <div class="stage-row">
          <div class="stage-main">{svg_b_w}</div>
          <div class="stage-side">
            <div class="mini-box light">{svg_b_lc}</div>
            <div class="mini-box dark">{svg_b_dc}</div>
          </div>
        </div>
        <h2>B. «Фирменный Парус-М» (С изюминкой)</h2>
        <ul>
          <li>Паруса кораблика надуты ветром в форме стильной буквы <strong>«М»</strong></li>
          <li>Уникальная деталь, которую сразу замечают и запоминают дети и родители</li>
          <li>Орбита решена стремительным спортивным росчерком (Swoosh)</li>
          <li>Сохраняет 100% родной композиции, делая её эксклюзивной</li>
        </ul>
        <div class="dl-row">
          <a class="btn" href="variant-b-sail-m.png" download>Скачать PNG</a>
          <a class="btn" href="variant-b-sail-m.svg" download>Скачать SVG</a>
        </div>
      </div>

      <!-- VARIANT C -->
      <div class="card">
        <span class="badge cyan">ВАРИАНТ C · АЭРО-ПОТОК</span>
        <div class="stage-row">
          <div class="stage-main">{svg_c_w}</div>
          <div class="stage-side">
            <div class="mini-box light">{svg_c_lc}</div>
            <div class="mini-box dark">{svg_c_cy}</div>
          </div>
        </div>
        <h2>C. «Скоростной Импульс» (Aero Flow)</h2>
        <ul>
          <li>Лаконичный обтекаемый корпус яхты в едином потоке с орбитой</li>
          <li>Упругие паруса-крылья и заострённые динамические дуги</li>
          <li>Максимальная читаемость при термотрансфере и мелкой вышивке</li>
          <li>Отлично работает с двухцветным голубым или коралловым акцентом</li>
        </ul>
        <div class="dl-row">
          <a class="btn" href="variant-c-aero.png" download>Скачать PNG</a>
          <a class="btn" href="variant-c-aero.svg" download>Скачать SVG</a>
        </div>
      </div>
    </div>

    <div class="eyebrow">Полный планшет с примеркой на форму и силовой инвентарь</div>
    <div class="board-wrap">
      {board_svg}
    </div>
  </div>
</body>
</html>
'''

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
with open(os.path.join(ROOT, "designs/m-trening/presentation.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("Created root showcase files and index.html")
