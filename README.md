# news-image-20261123 — "The World Today"

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Bradestudio/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Bradestudio/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up world news for
**Monday 23 November 2026**, rendered as a 1024×1024 PNG.

## Stories (all from 23 November 2026)

1. **Lead — COP31 COLLAPSES** (Antalya, Turkey): nearly 200 nations leave
   the UN climate talks with no deal; the final draft never mentions
   "fossil fuels"; the EU walked out; UN chief Guterres "deeply
   disappointed"; the longest COP in history.
2. **MIDDLE EAST — War spreads at Hormuz**: 25 tankers attacked near the
   Strait of Hormuz in 7 days; Gulf oil flows plunge; Houthis hit Riyadh
   a third day; Trump signals an Iran strike in 2027.
3. **EUROPE — War spills into the Baltic**: a Russian cargo ship burns
   off Finland after a Baltic drone strike; 14 missing after drones hit
   a building near Kyiv, Zelensky says.
4. **UNITED NATIONS — AI weapons talks drag on**: states in Geneva agree
   to keep negotiating lethal autonomous weapons, with no binding rules;
   work continues until 2028.
5. **ASIA — Exam scandal topples minister**: education minister
   Choi Kyo-jin resigns over an AI-assisted college entrance exam
   cheating scandal.
6. **ASIA — Factory fire in Indonesia**: a candy factory fire kills 3;
   dozens of workers missing — reports say 36 to 50 unaccounted for.

Plus a "BY THE NUMBERS" strip: 25 tankers, 200 nations, 14 missing,
36–50 workers missing.

## How it works

- `render.py` draws the page with PIL (DejaVu fonts, fixed layout, no
  network, no timestamps) and writes `entry.png`.
- `main.ts` (Node, stdlib only) validates the bundled `entry.png`
  (PNG signature, 1024×1024, under 1 MiB) and copies it byte-for-byte
  to `$MAKEFUN_OUTPUT_DIR/entry.png`, then verifies the copy by sha256.
- Run: `MAKEFUN_OUTPUT_DIR=out node main.ts`
- Deterministic: two runs produce byte-identical output
  (sha256 `a5778e2ed9817279820f6a310019298f3d1673fd2bd5b77890e0d8ca932c131b`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=qjs4e9sj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
