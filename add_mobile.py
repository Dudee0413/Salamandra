#!/usr/bin/env python3
"""
Mobilos reszponziv tamogatas hozzaadasa az osszes HTML fajlhoz.
Futtatni: python3 add_mobile.py
"""

import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

MOBILE_NAV_HTML = '''<div id="mobile-nav">
    <button id="hamburger-btn">&#9776; Menü</button>
    <nav id="mobile-menu">
        <ul>
            <li><a href="index.html">Főoldal</a></li>
            <li><a href="https://praebichl.net/?page_id=6">Kapcsolat</a></li>
            <li><a href="https://www.bergfex.at/praebichl/wetter/" target="_blank">Időjárás</a></li>
            <li><a href="https://www.bergfex.at/praebichl/webcams/" target="_blank">Webcam</a></li>
            <li><a href="https://praebichl.net/?page_id=12">Síelés</a></li>
            <li><a href="https://praebichl.net/?page_id=16">Rafting</a></li>
            <li><a href="https://praebichl.net/?page_id=18">Via Ferrata</a></li>
            <li>
                <span class="sub-toggle" data-sub="tura-sub">Túrák</span>
                <ul id="tura-sub" class="submenu">
                    <li><a href="https://praebichl.net/?page_id=777">Reichenstein (2165 m)</a></li>
                    <li><a href="https://praebichl.net/?page_id=779">Polster (1911 m)</a></li>
                    <li><a href="https://praebichl.net/?page_id=781">Grüblsee</a></li>
                    <li><a href="https://praebichl.net/?page_id=783">Leopoldsteinersee</a></li>
                    <li><a href="https://praebichl.net/?page_id=785">Murmeltierwanderung</a></li>
                    <li><a href="https://praebichl.net/?page_id=787">Krumpensee</a></li>
                    <li><a href="https://praebichl.net/?page_id=789">Wasserlochklamm</a></li>
                    <li><a href="https://praebichl.net/?page_id=791">Kraushöhle</a></li>
                    <li><a href="https://praebichl.net/?page_id=793">Frauenmauerhöhle</a></li>
                </ul>
            </li>
            <li>
                <span class="sub-toggle" data-sub="egyeb-sub">Egyéb</span>
                <ul id="egyeb-sub" class="submenu">
                    <li><a href="https://praebichl.net/?page_id=1152">Mountain bike</a></li>
                    <li><a href="https://praebichl.net/?page_id=1154">Alpesi búvárkodás</a></li>
                    <li><a href="https://praebichl.net/?page_id=1156">Siklóernyőzés</a></li>
                    <li><a href="https://praebichl.net/?page_id=1158">Mautern</a></li>
                    <li><a href="https://praebichl.net/?page_id=1160">Wasserspielpark</a></li>
                    <li><a href="https://praebichl.net/?page_id=1162">Erzberg-i látványbánya</a></li>
                    <li><a href="https://praebichl.net/?page_id=1164">Asia spa</a></li>
                    <li><a href="https://praebichl.net/?page_id=1166">Vitalbad Eisenerz</a></li>
                    <li><a href="https://praebichl.net/?page_id=1168">Traktormúzeum</a></li>
                    <li><a href="https://praebichl.net/?page_id=1170">Radwerk kohómúzeum</a></li>
                    <li><a href="https://praebichl.net/?page_id=1172">Eisenerz</a></li>
                </ul>
            </li>
            <li><a href="https://praebichl.net/?page_id=24">Galéria</a></li>
            <li><a href="https://praebichl.net/?page_id=28">Apartmanok</a></li>
            <li><a href="https://praebichl.net/?page_id=26">Cím</a></li>
            <li><a href="https://praebichl.net/?page_id=28">Üzenet</a></li>
            <li class="fb-links">
                <a href="https://www.facebook.com/pages/Salamandra-Apartments/247516531946946" target="_blank">FB Salamandra</a>
                <a href="https://www.facebook.com/pages/Encian-Apartments/322854897731722" target="_blank">FB Encián</a>
            </li>
        </ul>
    </nav>
</div>
'''

CSS_LINK = "<link rel='stylesheet' href='wp-content/themes/praebichl/stylesheets/responsive.css' type='text/css' media='all' />\n"
JS_LINK  = "<script type='text/javascript' src='wp-content/themes/praebichl/js/responsive.js'></script>\n"

CONTAINER_MARKER = '<div class="container">'
HEAD_CLOSE = '</head>'
BODY_CLOSE = '</body>'

# Az osszes index.html* fajl a konyvtarban
html_files = [os.path.join(BASE, 'index.html')]
html_files += glob.glob(os.path.join(BASE, 'index.html?page_id=*.html'))
html_files += glob.glob(os.path.join(BASE, 'index.html?p=*.html'))

print(f"Talalt fajlok szama: {len(html_files)}")

changed = 0
skipped = 0

for fpath in sorted(html_files):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ha mar modositva volt, kihagyjuk
    if 'id="mobile-nav"' in content:
        print(f"  [mar kesz] {os.path.basename(fpath)}")
        skipped += 1
        continue

    original = content

    # 1. CSS link hozzaadasa a </head> ele
    if HEAD_CLOSE in content:
        content = content.replace(HEAD_CLOSE, CSS_LINK + HEAD_CLOSE, 1)

    # 2. Mobilmenü HTML hozzaadasa a <div class="container"> utan
    if CONTAINER_MARKER in content:
        content = content.replace(CONTAINER_MARKER, CONTAINER_MARKER + '\n' + MOBILE_NAV_HTML, 1)

    # 3. JS link hozzaadasa a </body> ele
    if BODY_CLOSE in content:
        content = content.replace(BODY_CLOSE, JS_LINK + BODY_CLOSE, 1)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] {os.path.basename(fpath)}")
        changed += 1
    else:
        print(f"  [valtozas nelkul] {os.path.basename(fpath)}")

print(f"\nKesz! Modositva: {changed}, Kihagyva (mar kesz): {skipped}")
