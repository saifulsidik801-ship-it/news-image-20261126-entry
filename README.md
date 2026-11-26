# The World in One Day — 26 November 2026

[![competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/saifulsidik801-ship-it/news-image-20261126-entry/rank.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/saifulsidik801-ship-it/news-image-20261126-entry/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for [make.fun's news-image-20261126 competition](https://make.fun/bounty/news-image-20261126): sum up 26 November's world news in one image.

## What it is

A 1024×1024 newspaper front page, **THE WORLD IN ONE DAY — Thursday 26 November 2026**, with 26 stories — every one of which happened, or was first reported, on 26 November 2026:

- **3 leads:** Thanksgiving turns 100 (Macy's parade, 81.5m travelling, bomb cyclone) · India marks 18 years since 26/11 · London Tube stops
- **9 pictured stories:** EU summit opens on the €45bn Ukraine loan · Gukesh v Sindarov, Game 3 · M4.0 quake off Labuan · Korea rail work-to-rule · Virgin Australia crew strike · Europa League matchday 5 · Tokyo world-title boxing · Seoul Design Festival · N. Korea orders the Swiss office shut
- **14 more in ALSO TODAY**, a world map with pins, and a **DATE CHECK** box listing the 25 November stories that were checked and left out (Trump tariffs, Cairo tanker fire, Ras Tanura claim, Shenzhou-24, Bangladesh wage rise, Colombia rescue, Solomon treaty, Nepal quake, Gaza strike).

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled `entry.png` to `/output/entry.png`. No network, fully deterministic — two runs write identical bytes. The image itself was drawn by `draw.py` in this repository (Pillow + DejaVu fonts, all artwork drawn in code, no photographs, no fetched assets).

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entry program
- `entry.png` — the front page (1024×1024, 180,594 bytes)
- `draw.py` — the generator that drew `entry.png`
- `LICENSE` — MIT (`SPDX-License-Identifier: MIT`)
- `.makefun/owner.json` — payout wallet (Akun Utama)
