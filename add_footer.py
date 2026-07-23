#!/usr/bin/env python3
"""
Lablec hozzaadasa az osszes HTML fajlhoz.
Futtatni: python3 add_footer.py
"""

import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

FOOTER_HTML = '''
<footer id="site-footer">
    <p>&copy; 2025 Salamandra &amp; Enc&iacute;an Apartmanok, Pr&auml;bichl &mdash; Minden jog fenntartva</p>
    <p>
        Tel: <a href="tel:+36203239536">+36 20 323 9536</a> &nbsp;|&nbsp;
        <a href="tel:+436991726110">+43 699 172 6111 0</a><br />
        E-mail: <a href="mailto:somogyierwin@gmail.com">somogyierwin@gmail.com</a>
    </p>
    <p>
        <a href="wp-content/uploads/2018/06/GDPR_2018_HU.pdf" target="_blank">Adatv&eacute;delem (HU)</a>
        &nbsp;|&nbsp;
        <a href="wp-content/uploads/2018/06/GDPR_2018_DE.pdf" target="_blank">Datenschutz (DE)</a>
    </p>
</footer>
'''

# A Content div utan illesztjuk be, a container lezarasa ele
MARKER = ' </div><!-- End Content -->'

html_files = [os.path.join(BASE, 'index.html')]
html_files += glob.glob(os.path.join(BASE, 'index.html?page_id=*.html'))
html_files += glob.glob(os.path.join(BASE, 'index.html?p=*.html'))

print(f"Talalt fajlok szama: {len(html_files)}")

changed = 0
skipped = 0

for fpath in sorted(html_files):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'id="site-footer"' in content:
        print(f"  [mar kesz] {os.path.basename(fpath)}")
        skipped += 1
        continue

    if MARKER not in content:
        # Probaljuk meg a szokozos valtozattal
        alt = '</div><!-- End Content -->'
        if alt in content:
            content = content.replace(alt, alt + FOOTER_HTML, 1)
        else:
            print(f"  [HIBA: marker nem talalhato] {os.path.basename(fpath)}")
            continue
    else:
        content = content.replace(MARKER, MARKER + FOOTER_HTML, 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] {os.path.basename(fpath)}")
    changed += 1

print(f"\nKesz! Modositva: {changed}, Kihagyva: {skipped}")
