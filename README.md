<div align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/velvet-ribbon-theme/main/logo/logo128.png" alt="Velvet Ribbon Theme icon" width="88">
  <h1>Velvet Ribbon Theme</h1>
  <p>A soft Chrome theme in coral pink, lavender and gentle blue.</p>
  <p>
    <img src="https://img.shields.io/badge/version-1.0-FF95A5" alt="Version 1.0">
    <img src="https://img.shields.io/badge/license-Non--Commercial-lightgrey" alt="Non-Commercial License">
    <img src="https://img.shields.io/badge/Chrome%20Web%20Store-theme-D4BAD4?logo=googlechrome" alt="Chrome Web Store">
  </p>
</div>

---

## About

Velvet Ribbon Theme gives the browser a calm, ribbon-soft surface. A coral pink frame carries the window and tab strip, a blush-white toolbar and bookmark bar sit just below it, and a porcelain new-tab page keeps the reading area open and quiet. Lavender runs through the tab strip and the store artwork.

Every layer is painted as a single flat solid colour, so the window stays light and uncluttered, and the text colours are tuned so tabs, toolbar, bookmarks and the address bar stay readable on each surface.

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Coral Pink | `#FF95A5` | Window frame, tab strip, window buttons |
| Blush Mist | `#F6F1F6` | Toolbar, bookmark bar, active tab |
| Soft Lavender | `#ECCCED` | Tab strip accent, incognito frame |
| Porcelain | `#FAF7FA` | New-tab page background |
| Deep Plum | `#391D3A` | Tab, new-tab and address-bar text |
| Gentle Blue | `#425B9A` | Toolbar icons, bookmarks, links |

## Chrome UI Notes

Some parts of the browser are painted by Chrome itself rather than by the theme manifest. The store screenshots follow what Chrome actually renders after installing this theme:

- **Google mark on the new-tab page:** Chrome draws it as one flat colour computed from the new-tab background. With this palette it renders as soft lilac `#C19BC1`.
- **Shortcut tiles:** Chrome tints the round shortcut buttons from the new-tab background, rendering them as muted lavender `#D4BAD4`.
- **Window buttons:** Chrome keeps the minimize / maximize / close glyphs dark against the coral frame.
- **Address bar:** the omnibox keeps its own white background and Chrome's focus outline, so it stays legible against the blush toolbar.

## Features

| Feature | Detail |
|---------|--------|
| 🎀 Coral and lavender palette | Soft pink frame with a porcelain reading surface |
| 🟣 Flat color layers | Each surface is one solid colour |
| 👓 Tuned contrast | Tab, toolbar, bookmark and address-bar text stays readable |
| 🌙 Incognito styling | A deeper coral frame keeps private windows distinct |
| 🪶 Pure theme package | A manifest and an icon |

## Install

### From source (unpacked)

1. Download or clone this repository.
2. Open Chrome and navigate to `chrome://extensions`.
3. Enable **Developer mode** in the top-right corner.
4. Click **Load unpacked** and select this folder.

### From Chrome Web Store

Search for **Velvet Ribbon Theme** in the Chrome Web Store and install it.

## Preview

![Velvet Ribbon Theme browser preview](https://raw.githubusercontent.com/vaxicy/velvet-ribbon-theme/main/store-assets/screenshots/en/screenshot-1-browser.png)

![Velvet Ribbon Theme color palette](https://raw.githubusercontent.com/vaxicy/velvet-ribbon-theme/main/store-assets/screenshots/en/screenshot-2-introduction.png)

## Files

| File | Description |
|------|-------------|
| `manifest.json` | Chrome theme manifest (MV3) with inline `theme` config |
| `logo/logo128.png` | Theme icon (128x128, transparent background) |
| `store-assets/screenshots/en/` | Store listing screenshots (1280x800) |
| `store-assets/promo/` | Promo tiles (440x280 and 1400x560) |
| `store-assets/ASSET-NOTES.md` | How the store artwork is composed and calibrated |
| `scripts/generate-store-assets.py` | Renders every store asset from one HTML/CSS source |
| `scripts/trim_logo.py` | Builds `logo/logo128.png` from the source artwork |
| `scripts/package.py` | Builds the release ZIP into the default output folder |

## Packaging

```bash
python3 scripts/package.py
```

The archive is written as `velvet-ribbon-theme-<version>.zip` into the default output folder (two levels above the project, derived from the script location).

Packaged: `manifest.json`, `README.md`, `logo/`. Left out, because Chrome Web Store takes them as separate uploads: `store-assets/` (screenshots, promo tiles, listing text), `scripts/`, `.gitignore`, `Cached Theme.pak`. The script re-reads `manifest.json` from inside the finished archive and fails if the archive root or the referenced files are wrong.

## License

Non-Commercial License — personal use permitted.

- ✅ Personal use, modification for personal use, sharing with attribution.
- ❌ Commercial use without permission.

Commercial licensing: contact the author.
