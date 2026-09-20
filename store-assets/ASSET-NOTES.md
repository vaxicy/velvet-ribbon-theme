# Assets

Four English deliverables, all rendered from one headless-Chromium source
(`scripts/generate-store-assets.py`):

| File | Size | Content |
|------|------|---------|
| `screenshots/en/screenshot-1-browser.png` | 1280x800 | Full-window mockup of the themed browser |
| `screenshots/en/screenshot-2-introduction.png` | 1280x800 | Theme intro with the 2x2 colour cards |
| `promo/440x280.png` | 440x280 | Brand tile |
| `promo/1400x560.png` | 1400x560 | Marquee with a scaled window preview |

## Colors

Theme-controlled colours are read from `manifest.json` (single source of truth).
Chrome-controlled UI colours are hardcoded because Chrome paints them itself:

- Google mark on the new-tab page (`ntp_logo_alternate`): `#C19BC1` (sampled from a real install)
- Shortcut tiles (Chrome tint of `ntp_background`): `#D4BAD4` (sampled from a real install)
- Omnibox focus outline: `#7585A1`; placeholder / shortcut labels: `#5F6368`
- Customize Chrome pill: `#202124` with a `#A8C7FA` label

Sampled values were measured from a real installed-Chrome screenshot (1080x646)
of this theme; the tab strip `#FF95A5`, active tab / bookmark bar `#F6F1F6` and
new-tab background `#FAF7FA` match `manifest.json`.

The 440x280 brand tile puts the logo on a white rounded plate so the pink mark
does not merge into the coral tile background.

## Logo

`logo/logo128.png` only (128x128, transparent background). The source artwork the
icon was trimmed from is kept at `store-assets/icon-candidates/logo-source.png`;
`scripts/trim_logo.py` removes the outer white page (corner flood fill, so white
details inside the artwork survive) and crops the circle tight.
