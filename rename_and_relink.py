#!/usr/bin/env python3
"""
1. Atnevezi az index.html?page_id=X.html fajlokat baratsagos nevekre
2. Minden HTML fajlban kicsereli az osszes belso linket az uj nevekre
3. A duplikat index.html?p=X.html fajlokat torli (mar feleslegesek)
Futtatni: python3 rename_and_relink.py
"""

import os
import glob
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))

# page_id -> uj fajlnev mapping
RENAME = {
    '6':    'kapcsolat.html',
    '12':   'sieles.html',
    '16':   'rafting.html',
    '18':   'viaferrata.html',
    '24':   'galeria.html',
    '26':   'cim.html',
    '28':   'apartmanok.html',
    '777':  'reichenstein.html',
    '779':  'polster.html',
    '781':  'grublsee.html',
    '783':  'leopoldsteinersee.html',
    '785':  'murmeltierwanderung.html',
    '787':  'krumpensee.html',
    '789':  'wasserlochklamm.html',
    '791':  'kraushohle.html',
    '793':  'frauenmauerhohle.html',
    '1152': 'mountainbike.html',
    '1154': 'buvarkogas.html',
    '1156': 'sikloernyo.html',
    '1158': 'mautern.html',
    '1160': 'wasserspielpark.html',
    '1162': 'erzberg.html',
    '1164': 'asiaspa.html',
    '1166': 'vitalbad.html',
    '1168': 'traktormuzeum.html',
    '1170': 'radwerk.html',
    '1172': 'eisenerz.html',
    '1613': 'sioktatas.html',
    '1645': 'covid.html',
}

# Osszes lehetseges regi link forma -> uj fajlnev
# Pl. https://praebichl.net/?page_id=12  ->  sieles.html
# Pl. https://praebichl.net/?p=12        ->  sieles.html
LINK_REPLACEMENTS = {}
for pid, newname in RENAME.items():
    LINK_REPLACEMENTS[f'https://praebichl.net/?page_id={pid}'] = newname
    LINK_REPLACEMENTS[f'https://praebichl.net/?p={pid}']       = newname
    LINK_REPLACEMENTS[f'http://praebichl.net/?page_id={pid}']  = newname
    LINK_REPLACEMENTS[f'http://praebichl.net/?p={pid}']        = newname
    # Helyi statikus verzio (ha valahol igy lenne)
    LINK_REPLACEMENTS[f'index.html?page_id={pid}.html']        = newname
    LINK_REPLACEMENTS[f'index.html?p={pid}.html']              = newname

print("=== 1. Fajlok atnevezese ===")
for pid, newname in RENAME.items():
    old_path = os.path.join(BASE, f'index.html?page_id={pid}.html')
    new_path = os.path.join(BASE, newname)
    if os.path.exists(old_path):
        shutil.copy2(old_path, new_path)
        print(f"  {os.path.basename(old_path)} -> {newname}")
    else:
        print(f"  [HIANYZIK] index.html?page_id={pid}.html")

print("\n=== 2. Linkek cserelese az osszes HTML fajlban ===")

# Az osszes HTML fajl (index.html + az uj nevesek)
all_html = [os.path.join(BASE, 'index.html')]
for newname in RENAME.values():
    p = os.path.join(BASE, newname)
    if os.path.exists(p):
        all_html.append(p)

changed_files = 0
for fpath in sorted(all_html):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for old_link, new_link in LINK_REPLACEMENTS.items():
        content = content.replace(old_link, new_link)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] {os.path.basename(fpath)}")
        changed_files += 1
    else:
        print(f"  [valtozatlan] {os.path.basename(fpath)}")

print(f"\n  Osszesen frissitett fajl: {changed_files}")

print("\n=== 3. Regi ?p= es ?page_id= fajlok torlese ===")
deleted = 0
for pattern in ['index.html?page_id=*.html', 'index.html?p=*.html']:
    for f in glob.glob(os.path.join(BASE, pattern)):
        os.remove(f)
        print(f"  Torolve: {os.path.basename(f)}")
        deleted += 1
print(f"  Osszesen torolve: {deleted} fajl")

print("\n=== KESZ ===")
print("Az uj fajlok:")
for newname in sorted(RENAME.values()):
    p = os.path.join(BASE, newname)
    if os.path.exists(p):
        print(f"  {newname}")
