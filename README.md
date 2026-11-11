# Cutest Cat — make.fun bounty cutest-cat-01

A ginger kitten drawn entirely in code: big round head with a slight tilt,
oversized bright amber eyes, tiny pink nose, blush cheeks, whiskers, a
curled tail, front paws on a red yarn ball.

## Files

- `main.ts` — the entry (Node 22, stdlib only): copies `entry.png` to
  `/output/entry.png`.
- `entry.png` — the cat, 1024×1024 PNG (226 KB), rendered by `draw_cat.py`.
- `draw_cat.py` — the procedural drawing script (Pillow, build time only).
  No photo, no copied artwork, no network, no API key.
- `LICENSE` — MIT.

## Run locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
