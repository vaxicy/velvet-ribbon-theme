"""Compose every Velvet Ribbon store asset from one HTML/CSS source.

Layering and geometry mirror a real installed-Chrome screenshot (1080x646 capture
of a maximized window). The window is authored in that capture's pixel space and
scaled once per output:
  screenshot-1  1280x800  scale 1.18519 (1080 -> 1280, 675 -> 800)
  promo wide    scaled preview, window height trimmed so the whole frame fits

Theme-controlled colors are read from manifest.json (single source of truth).
Chrome-controlled UI colors are hardcoded from the real screenshot and marked.
"""
from pathlib import Path
import base64
import json
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'store-assets' / 'references'
OUT.mkdir(parents=True, exist_ok=True)
C = json.loads((ROOT / 'manifest.json').read_text('utf-8-sig'))['theme']['colors']
C['leaf'] = [226, 106, 128]  # brand accent used by the intro colour card only
C['deep'] = [57, 29, 58]     # deep plum for AA text


def color(k):
    return '#%02X%02X%02X' % tuple(C[k])


# ---------------------------------------------------------------------------
# UI colors NOT controlled by the theme: sampled from the installed-Chrome
# screenshot, so the mockup matches what a user actually sees.
# ---------------------------------------------------------------------------
LOGO = '#C19BC1'          # Chrome computes the NTP Google mark (sampled from a real install)
CIRCLE = '#D4BAD4'        # Chrome tints the shortcut tiles (sampled from a real install)
OMNI_BORDER = '#7585A1'   # focused omnibox outline
UI_TEXT = '#5F6368'       # placeholder / shortcut label grey
UI_ICON = '#444746'       # mic, lens, chip glyphs
CHIP_BG = '#F3F5F6'       # "AI Mode" chip inside the search fields
PILL_BG = '#202124'       # Customize Chrome pill
PILL_FG = '#A8C7FA'       # its blue label + pencil
WIN_BTN = '#2B2B2B'       # minimize / maximize / close glyphs
G_RED, G_BLUE, G_YELLOW, G_GREEN = '#EA4335', '#4285F4', '#FBBC05', '#34A853'

VARS = f""":root{{
  --sand:{color('frame')};
  --oat:{color('toolbar')};
  --milk:{color('ntp_background')};
  --ink:{color('ntp_text')};
  --rose:{color('leaf')};
  --deep:{color('deep')};
  --logoc:{LOGO};
  --circle:{CIRCLE};
}}"""

CSS = VARS + """
*{box-sizing:border-box}
body{margin:0;overflow:hidden;font-family:Arial,'Helvetica Neue',sans-serif;background:var(--milk);color:var(--ink)}
.window{width:1080px;height:675px;background:var(--milk);position:relative;overflow:hidden;display:flex;flex-direction:column}
.row{display:flex;align-items:center;flex:0 0 auto}
svg{display:block}

/* ---- tab strip (frame colour) ---- */
.tabstrip{height:32px;background:var(--sand);display:flex;align-items:flex-end;padding-left:33px}
.chev{position:absolute;left:14px;top:13px}
.tab{width:168px;height:27px;border-radius:9px 9px 0 0;margin-right:7px;padding:0 10px 0 30px;display:flex;align-items:center;
     font-size:11.5px;color:var(--ink);position:relative;outline:1px solid rgba(255,255,255,.30);outline-offset:-1px}
.tab.on{background:var(--oat);outline:0;color:var(--ink)}
.tab i{position:absolute;left:11px;top:7px;width:12px;height:12px;border-radius:3px;background:rgba(80,61,75,.22)}
.tab.on i{background:var(--logoc)}
.tab .x{margin-left:auto;opacity:.75}
.tab .x svg{margin:0}
.newtab{width:20px;height:20px;margin:0 0 4px 8px;display:flex;align-items:center;justify-content:center}
.wbtns{margin-left:auto;margin-bottom:9px;margin-right:12px;display:flex;gap:24px}

/* ---- toolbar ---- */
.toolbar{height:32px;background:var(--oat);display:flex;align-items:center;gap:16px;padding:0 14px}
.nav{display:flex;gap:15px;align-items:center}
.omni{flex:1;height:27px;border:2px solid var(--omni-border);border-radius:14px;background:#FFFFFF;display:flex;align-items:center;
      padding:0 4px 0 11px;gap:9px;font-size:12.5px;color:var(--ui-text)}
.omni .ph{flex:1;white-space:nowrap;overflow:hidden}
.chip{height:20px;border-radius:10px;background:#F3F5F6;display:flex;align-items:center;gap:4px;padding:0 8px;font-size:11px;color:#444746}
.tools{display:flex;gap:17px;align-items:center}

/* ---- bookmark bar ---- */
.bookmarks{height:32px;background:var(--oat);display:flex;align-items:center;gap:19px;padding:0 14px;font-size:11.5px;color:var(--ink)}
.bookmarks .sep{width:1px;height:14px;background:rgba(80,61,75,.25)}
.bm{display:flex;align-items:center;gap:6px}

/* ---- new tab page ---- */
.ntp{flex:1;position:relative;background:var(--milk)}
.gtop{position:absolute;top:13px;right:12px;display:flex;align-items:center;gap:16px;font-size:12.5px;color:var(--ui-text)}
.gtop .av{border-radius:50%;overflow:hidden}
.glogo{position:absolute;top:86.5px;left:0;right:0;text-align:center;font-family:'Google Sans','Product Sans',Arial,sans-serif;
        font-size:66px;font-weight:500;letter-spacing:-2.8px;color:var(--logoc);line-height:1}
.nsearch{position:absolute;top:187px;left:50%;margin-left:-264px;width:529px;height:44px;border-radius:22px;background:#FFFFFF;
         box-shadow:0 1px 6px rgba(0,0,0,.14);display:flex;align-items:center;gap:13px;padding:0 8px 0 20px}
.nsearch .ph{flex:1;font-size:15px;color:var(--ui-text);white-space:nowrap;overflow:hidden}
.nsearch .chip{height:28px;border-radius:14px;font-size:12px;padding:0 11px;gap:6px}
.shortcuts{position:absolute;top:251px;left:0;right:0;display:flex;justify-content:center;gap:8px}
.shortcut{width:72px;text-align:center;font-size:12px;color:var(--ui-text)}
.shortcut .circle{width:33px;height:33px;border-radius:50%;background:var(--circle);margin:0 auto 14px;display:flex;align-items:center;justify-content:center}
.shortcut .lbl{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.customize{position:absolute;right:10px;bottom:10px;height:26px;border-radius:13px;background:#202124;color:#A8C7FA;
           display:flex;align-items:center;gap:6px;padding:0 12px;font-size:11.5px}

/* ---- promo: 440x280 brand tile ---- */
.tile{width:440px;height:280px;background:var(--sand);position:relative;overflow:hidden;text-align:center;color:var(--deep)}
.tile .plate{width:96px;height:96px;border-radius:24px;background:#FFFFFF;margin:22px auto 0;display:flex;
             align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(57,29,58,.14)}
.tile .plate img{width:72px;height:72px;display:block;margin:0}
.tile h1{font-family:Georgia,serif;font-weight:normal;font-size:37px;margin:14px 0 0}
.tile .kicker{font-size:13px;letter-spacing:5px;margin-top:9px}
.tile p{font-size:14px;margin:19px 0 0}
.tile:after{content:'';position:absolute;left:0;right:0;bottom:0;height:14px;background:var(--oat)}

/* ---- promo: 1400x560 marquee ---- */
.marquee{width:1400px;height:560px;background:var(--milk);position:relative;overflow:hidden;text-align:center;
         border-top:8px solid var(--sand)}
.marquee h1{font-family:Georgia,serif;font-weight:normal;font-size:47px;margin:26px 0 0;color:var(--ink)}
.marquee p{font-size:17px;margin:9px 0 0;color:var(--ui-text)}
.marquee .frame{position:absolute;top:139px;left:300px;width:800px;height:370px;overflow:hidden;border:2px solid var(--sand);
                border-radius:16px;box-shadow:0 10px 30px rgba(80,61,75,.13)}
.marquee .frame .window{transform:scale(.740741);transform-origin:top left}

/* ---- screenshot 2: palette card ---- */
.intro{width:1280px;height:800px;background:var(--milk);padding:66px 74px}
.intro .kicker{font-size:12px;letter-spacing:4px;color:var(--ui-text)}
.intro h1{font-family:Georgia,serif;font-weight:normal;font-size:54px;margin:16px 0 0}
.intro .lead{font-size:21px;margin:14px 0 0}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:38px}
.card{height:196px;border-radius:18px;padding:30px;display:flex;flex-direction:column;justify-content:flex-end}
.card strong{font-size:28px}
.card span{font-size:16.5px;margin-top:10px}
.intro .chips{font-size:16px;margin-top:32px;color:var(--ui-text)}
"""


def g_mark(size):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 48 48">'
            f'<path fill="{G_RED}" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>'
            f'<path fill="{G_BLUE}" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>'
            f'<path fill="{G_YELLOW}" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>'
            f'<path fill="{G_GREEN}" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>')


def sparkle(size, fill):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}">'
            f'<path d="M12 2.6l1.75 4.85L18.6 9.2l-4.85 1.75L12 15.8l-1.75-4.85L5.4 9.2l4.85-1.75z"/>'
            f'<path d="M19 14l.9 2.4 2.4.9-2.4.9-.9 2.4-.9-2.4-2.4-.9 2.4-.9z"/></svg>')


def apps(size, fill):
    dots = ''.join(f'<circle cx="{3 + 9 * (i % 3)}" cy="{3 + 9 * (i // 3)}" r="2.6"/>' for i in range(9))
    return f'<svg width="{size}" height="{size}" viewBox="0 0 30 30" fill="{fill}">{dots}</svg>'


def mic(size, fill):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24">'
            f'<rect x="9" y="2" width="6" height="11" rx="3" fill="{fill}"/>'
            f'<path d="M5 11v1a7 7 0 0 0 14 0v-1" fill="none" stroke="{fill}" stroke-width="2"/>'
            f'<path d="M12 19v3" stroke="{fill}" stroke-width="2"/></svg>')


def lens(size, fill):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24">'
            f'<rect x="3" y="6" width="18" height="13" rx="4" fill="none" stroke="{fill}" stroke-width="2"/>'
            f'<circle cx="12" cy="12.5" r="3.2" fill="none" stroke="{fill}" stroke-width="2"/></svg>')


def avatar(size):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24">'
            f'<circle cx="12" cy="12" r="12" fill="{color("leaf")}"/>'
            f'<circle cx="12" cy="9.4" r="4.1" fill="#FFF7F3"/>'
            f'<path d="M3.8 21.2c1.6-4.3 4.7-6.4 8.2-6.4s6.6 2.1 8.2 6.4z" fill="#FFF7F3"/></svg>')


def win_buttons():
    g = f'stroke="{WIN_BTN}" stroke-width="1.5" stroke-linecap="round" fill="none"'
    return ('<div class="wbtns">'
            f'<svg width="10" height="10" viewBox="0 0 12 12"><path d="M1.2 6h9.6" {g}/></svg>'
            f'<svg width="10" height="10" viewBox="0 0 12 12"><rect x="1.8" y="1.8" width="8.4" height="8.4" rx="2" {g}/></svg>'
            f'<svg width="10" height="10" viewBox="0 0 12 12"><path d="M2.2 2.2l7.6 7.6M9.8 2.2L2.2 9.8" {g}/></svg>'
            '</div>')


def nav_icons():
    g = f'stroke="{color("ntp_text")}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    return ('<div class="nav">'
            f'<svg width="16" height="16" viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7" {g}/></svg>'
            f'<svg width="16" height="16" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7" {g}/></svg>'
            f'<svg width="16" height="16" viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-2.6-5.9" {g}/><path d="M20 3.6V7h-3.4" {g}/></svg>'
            f'<svg width="16" height="16" viewBox="0 0 24 24"><path d="M4 11l8-7 8 7v8.5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z" {g}/></svg>'
            '</div>')


def tab(title, active=False):
    cls = 'tab on' if active else 'tab'
    return (f'<div class="{cls}"><i></i>{title}'
            f'<span class="x"><svg width="9" height="9" viewBox="0 0 12 12">'
            f'<path d="M2 2l8 8M10 2l-8 8" stroke="{color("ntp_text")}" stroke-width="1.6" stroke-linecap="round"/></svg></span></div>')


def bookmarks():
    g = f'stroke="{color("ntp_text")}" stroke-width="1.5" stroke-linejoin="round" fill="none"'
    kids = ''.join(
        f'<div class="bm"><svg width="12" height="12" viewBox="0 0 24 24">'
        f'<path d="M3 7.5h6l2 2.5h10v8.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z" {g}/></svg>{name}</div>'
        for name in ('Bookmarks', 'Reading', 'Design', 'Inspiration'))
    return ('<div class="bookmarks">' + apps(13, color('ntp_text')) + '<div class="sep"></div>' + kids + '</div>')


def window(height=675, tabs=('New Tab', 'Reading list', 'Design inspiration', 'Velvet Ribbon')):
    strip = ('<div class="tabstrip">'
             f'<div class="chev"><svg width="11" height="11" viewBox="0 0 24 24">'
             f'<path d="M6 10l6 6 6-6" stroke="{color("ntp_text")}" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg></div>'
             + ''.join(tab(t, i == 0) for i, t in enumerate(tabs))
             + f'<div class="newtab"><svg width="13" height="13" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14" stroke="{color("ntp_text")}" stroke-width="2.1" stroke-linecap="round"/></svg></div>'
             + win_buttons() + '</div>')
    omni = ('<div class="omni">' + g_mark(14) + '<span class="ph">Search Google or type a URL</span>'
            + f'<div class="chip">{sparkle(12, UI_ICON)}AI Mode</div>'
            + f'<svg width="13" height="13" viewBox="0 0 24 24"><circle cx="10" cy="10" r="6.4" fill="none" stroke="{UI_ICON}" stroke-width="2.2"/><path d="M15 15l5.6 5.6" stroke="{UI_ICON}" stroke-width="2.2" stroke-linecap="round"/></svg>'
            + '</div>')
    dots = ''.join(f'<circle cx="12" cy="{5 + 7 * i}" r="1.7" fill="{color("ntp_text")}"/>' for i in range(3))
    kebab = ('<div class="tools">'
             f'<svg width="15" height="15" viewBox="0 0 24 24"><path d="M12 3.6l2.5 5.6 6.1.5-4.6 4 1.4 6-5.4-3.2-5.4 3.2 1.4-6-4.6-4 6.1-.5z" fill="none" stroke="{color("ntp_text")}" stroke-width="1.6" stroke-linejoin="round"/></svg>'
             f'<svg width="15" height="15" viewBox="0 0 24 24">{dots}</svg>'
             '</div>')
    toolbar = '<div class="toolbar">' + nav_icons() + omni + kebab + '</div>'
    gtop = ('<div class="gtop"><span>Gmail</span><span>Images</span>' + apps(13, UI_TEXT)
            + f'<div class="av">{avatar(24)}</div></div>')
    glogo = '<div class="glogo">Google</div>'
    nsearch = ('<div class="nsearch">'
               f'<svg width="20" height="20" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14" stroke="#3C4043" stroke-width="2.3" stroke-linecap="round"/></svg>'
               '<span class="ph">Search Google or type a URL</span>'
               + mic(17, UI_ICON) + lens(18, UI_ICON)
               + f'<div class="chip">{sparkle(13, UI_ICON)}AI Mode</div>'
               + '</div>')
    short = ('<div class="shortcuts">'
             f'<div class="shortcut"><div class="circle"><svg width="17" height="17" viewBox="0 0 24 24">'
             f'<rect x="1" y="5" width="22" height="14" rx="4.4" fill="#FF0000"/>'
             f'<path d="M10 8.8l6 3.2-6 3.2z" fill="#FFFFFF"/></svg></div><div class="lbl">YouTube</div></div>'
             f'<div class="shortcut"><div class="circle"><svg width="17" height="17" viewBox="0 0 24 24">'
             f'<circle cx="12" cy="12" r="11" fill="#FFFFFF"/>'
             f'<path d="M12 1a11 11 0 0 1 9.53 5.5L12 12z" fill="{G_RED}"/>'
             f'<path d="M21.53 6.5A11 11 0 0 1 12 23L12 12z" fill="{G_GREEN}"/>'
             f'<path d="M12 23A11 11 0 0 1 2.47 17.5L12 12z" fill="{G_YELLOW}"/>'
             f'<circle cx="12" cy="12" r="5" fill="{G_BLUE}"/><circle cx="12" cy="12" r="2.1" fill="#FFFFFF"/></svg></div>'
             f'<div class="lbl">Chrome Web Store</div></div>'
             f'<div class="shortcut"><div class="circle"><svg width="15" height="15" viewBox="0 0 24 24">'
             f'<path d="M12 5v14M5 12h14" stroke="#3C4043" stroke-width="2.2" stroke-linecap="round"/></svg></div>'
             f'<div class="lbl">Add shortcut</div></div></div>')
    customize = ('<div class="customize">'
                 f'<svg width="12" height="12" viewBox="0 0 24 24"><path d="M4 20l4.2-1.1L20 7.1 16.9 4 5.1 15.8z" fill="none" stroke="{PILL_FG}" stroke-width="2" stroke-linejoin="round"/></svg>'
                 'Customize Chrome</div>')
    ntp = f'<div class="ntp">{gtop}{glogo}{nsearch}{short}{customize}</div>'
    return f'<div class="window" style="height:{height}px">' + strip + toolbar + bookmarks() + ntp + '</div>'


# the promo tile draws its own white plate, so it uses the bare artwork to
# avoid stacking two plates
_PLAIN = ROOT / 'store-assets' / 'icon-candidates' / 'logo-plain-128.png'
LOGO_URI = 'data:image/png;base64,' + base64.b64encode(
    (_PLAIN if _PLAIN.exists() else ROOT / 'logo' / 'logo128.png').read_bytes()).decode()

tile = ('<div class="tile">' + f'<div class="plate"><img src="{LOGO_URI}" alt="Velvet Ribbon logo"></div>'
        + '<h1>Velvet Ribbon</h1><div class="kicker">CHROME THEME</div>'
        + '<p>Soft coral, lavender and blue.</p></div>')
marquee = ('<div class="marquee"><h1>Velvet Ribbon Theme</h1><p>Coral pink, soft lavender and gentle blue.</p>'
           + '<div class="frame">' + window(height=500) + '</div></div>')

PALETTE = [
    ('Coral Pink', 'frame', 'Window frame', 'deep'),
    ('Soft Lavender', 'background_tab', 'Tab strip accent', 'deep'),
    ('Blush Mist', 'toolbar', 'Toolbar & active tab', 'ntp_text'),
    ('Porcelain', 'ntp_background', 'New tab background', 'ntp_text'),
]
cards = ''.join(
    f'<div class="card" style="background:{color(k)};color:{color(fg)};border:1px solid rgba(80,61,75,.16)">'
    f'<strong>{name}</strong><span>{color(k)} · {role}</span></div>' for name, k, role, fg in PALETTE)
intro = ('<div class="intro"><div class="kicker">SOFT AND ELEGANT</div><h1>Velvet Ribbon Theme</h1>'
         '<p class="lead">Four colors. One calm, elegant space.</p><div class="cards">' + cards + '</div>'
         '<p class="chips">Solid colors · Flat design · Coral, lavender and blue</p></div>')


def page(body):
    return '<!doctype html><html lang="en"><meta charset="utf-8"><style>' + CSS + '</style><body>' + body + '</body></html>'


# name, output size, design size. The browser window is authored at 1080x675
# (the real capture's pixel space) and rasterised at a matching device scale
# factor so the 1280x800 store shot stays crisp instead of being upscaled.
JOBS = [
    ('screenshot-1-browser', 1280, 800, 1080, 675, window(675)),
    ('screenshot-2-introduction', 1280, 800, 1280, 800, intro),
    ('promo-440x280', 440, 280, 440, 280, tile),
    ('promo-1400x560', 1400, 560, 1400, 560, marquee),
]

with sync_playwright() as p:
    engine = p.chromium.launch(headless=True)
    for name, w, h, dw, dh, body in JOBS:
        dsf = w / dw
        html = page(body)
        (OUT / f'{name}.html').write_text(html, 'utf-8')
        sheet = engine.new_page(device_scale_factor=dsf, viewport={'width': dw, 'height': dh})
        sheet.set_content(html)
        sheet.screenshot(path=str(OUT / f'{name}.png'))
        sheet.close()
        destination = ROOT / 'store-assets' / ('promo' if name.startswith('promo-') else 'screenshots/en') / (
            name.removeprefix('promo-') + '.png')
        destination.parent.mkdir(parents=True, exist_ok=True)
        temp = destination.with_suffix('.new.png')
        with Image.open(OUT / f'{name}.png') as img:
            out = img.convert('RGB')
            if out.size != (w, h):
                print(f'  resampling {name} {out.size} -> {(w, h)}')
                out = out.resize((w, h), Image.LANCZOS)
            assert out.size == (w, h), f'{name}: got {out.size}, expected {(w, h)}'
            out.save(temp)
        temp.replace(destination)
        print(f'Rendered {name} {w}x{h}')
    engine.close()
