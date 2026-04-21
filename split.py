#!/usr/bin/env python3
"""
split.py — one-time extraction of source files from index.html.

Outputs:
  src/style.css             our custom CSS
  src/story-style.css       Twine user stylesheet (tw-story colors etc.)
  src/story-script.js       Twine user JS (currently empty)
  src/story-meta.json       story metadata
  src/passages/<pid>-<name>.twee  one file per passage
  harlowe/harlowe-2.1.0-engine.css  archived Harlowe 2.x engine CSS
  harlowe/harlowe-2.1.0-engine.js   archived Harlowe 2.x engine JS
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / 'src'
PASSAGES_DIR = SRC / 'passages'
HARLOWE_DIR = ROOT / 'harlowe'

# Alt text for every image referenced in passages.
ALT_TEXT = {
    'images/adidas-cut-fake-01.png':      'Fake Adidas jersey cut — example 1',
    'images/adidas-cut-fake-02.png':      'Fake Adidas jersey cut — example 2',
    'images/adidas-cut-legit.png':        'Legit Adidas jersey cut',
    'images/adidas-laces-fake-01.png':    'Fake Adidas lace hole — example 1',
    'images/adidas-laces-fake-02.png':    'Fake Adidas lace hole — example 2',
    'images/adidas-laces-legit.png':      'Legit Adidas lace hole',
    'images/adidas-shield-fake.png':      'Fake NHL shield on Adidas jersey',
    'images/adidas-shield-legit.png':     'Legit NHL shield on Adidas jersey',
    'images/band-fake-short.png':         'Fake information band (truncated)',
    'images/band-fake.png':               'Fake information band',
    'images/band-legit.png':              'Legit information band',
    'images/blues_concept.jpg':           'Example fantasy/concept jersey (Blues)',
    'images/button-fake-stitched.png':    'Fake button stitched over',
    'images/button-fake.png':             'Fake Adidas button',
    'images/button-legit.png':            'Legit Adidas button',
    'images/ccmvintage-fake.png':         'Fake CCM vintage jersey neck tag',
    'images/ccmvintage-legit.png':        'Legit CCM vintage jersey neck tag',
    'images/crap-design-01.png':          'Fantasy/fake jersey design example 1',
    'images/crap-design-02.png':          'Fantasy/fake jersey design example 2',
    'images/crap-design-03.png':          'Fantasy/fake jersey design example 3',
    'images/crap-design-04.png':          'Fantasy/fake jersey design example 4',
    'images/crest-fake.png':              'Fake jersey crest stitching',
    'images/crest-legit.png':             'Legit jersey crest stitching',
    'images/dimples-fake.png':            'Fake jersey eyelets/dimples',
    'images/dimples-legit.png':           'Legit jersey eyelets/dimples',
    'images/fightstrap-fake.png':         'Fake fight strap',
    'images/fightstrap-indo.png':         'Indo-style fight strap',
    'images/fightstrap-retail.png':       'Legit retail fight strap',
    'images/fightstrap-ti.png':           'Legit TI fight strap',
    'images/flyers_concept.jpeg':         'Example fantasy/concept jersey (Flyers)',
    'images/hangar-fake.png':             'Fake hangar/jock tag text',
    'images/hangar-legit.png':            'Legit hangar/jock tag text',
    'images/inside-fake.png':             'Fake jersey interior (neck area)',
    'images/inside-legit.png':            'Legit jersey interior (neck area)',
    'images/jock-tag-adidas.png':         'Adidas jersey jock tag',
    'images/jock-tag-fanatics.png':       'Fanatics jersey jock tag',
    'images/jock-tag-reebok.png':         'Reebok jersey jock tag',
    'images/kings_concept.jpg':           'Example fantasy/concept jersey (Kings)',
    'images/lettering-fake-patch.png':    'Fake jersey lettering — patch style',
    'images/lettering-fake.png':          'Fake jersey lettering',
    'images/logo.png':                    'Liberty Bell Jerseys logo',
    'images/logos/adidas.png':            'Adidas logo',
    'images/logos/ccm.png':               'CCM logo',
    'images/logos/fanatics.png':          'Fanatics logo',
    'images/logos/koho.png':              'Koho logo',
    'images/logos/reebok.png':            'Reebok logo',
    'images/logos/starter.png':           'Starter logo',
    'images/neck-fake.png':               'Fake back-of-neck logo placement',
    'images/neck-legit.png':              'Legit back-of-neck logo placement',
    'images/pens_concept.jpg':            'Example fantasy/concept jersey (Penguins)',
    'images/reebok-laces-fake.png':       'Fake Reebok lace hole',
    'images/reebok-laces-legit.png':      'Legit Reebok lace hole',
    'images/reebok-shield-fake-01.png':   'Fake NHL shield on Reebok jersey — example 1',
    'images/reebok-shield-fake-02.png':   'Fake NHL shield on Reebok jersey — example 2',
    'images/reebok-shield-legit-01.png':  'Legit NHL shield on Reebok jersey — example 1',
    'images/reebok-shield-legit-02.png':  'Legit NHL shield on Reebok jersey — example 2',
    'images/reebok-vector-fake.png':      'Fake Reebok vector mark inside collar',
    'images/reebok-vector-legit.png':     'Legit Reebok vector mark inside collar',
    'images/reebok-vneck-fake.png':       'Fake Reebok v-neck interior',
    'images/reebok-vneck-legit.png':      'Legit Reebok v-neck interior',
    'images/reebok-wordmark-fake.png':    'Fake Reebok wordmark inside collar',
    'images/reebok-wordmark-legit.png':         'Legit Reebok wordmark inside collar',
    'images/ccmvintage-legitlettered.png':      'Legit CCM vintage lettered jersey neck tag',
    'images/insta.png':                         'Example of a suspicious Instagram jersey ad',
    'images/ccm_fake_tag.jpg':                  'Fake CCM size tag',
    'images/ccm_tag_korea.jpg':                 'CCM size tag with Korea origin',
    'images/ccm_fake_stitching_crest.jpg':      'Fake CCM jersey — crest stitching detail',
    'images/ccm_fake_stitching_patch.jpg':      'Fake CCM jersey — patch stitching detail',
    'images/ccm_fake_lettering.jpg':            'Fake CCM jersey lettering',
    'images/ccm_fake_lettering_tb.jpg':         'Fake CCM jersey lettering (Tampa Bay)',
    'images/ccm_fake_lettering_edm.jpg':        'Fake CCM jersey lettering (Edmonton)',
}


def add_alt_text(decoded_content: str) -> str:
    """Add alt attributes to <img> tags that are missing them."""
    def replace_img(m):
        tag = m.group(0)
        if 'alt=' in tag:
            return tag
        # Handle both single- and double-quoted src
        src_m = re.search(r"""src=['"]([^'"]+)['"]""", tag)
        if not src_m:
            return tag
        src = src_m.group(1)
        alt = ALT_TEXT.get(src, '')
        # Insert alt before the closing > or />
        if tag.endswith('/>'):
            return tag[:-2] + f' alt="{alt}"' + '/>'
        else:
            return tag[:-1] + f' alt="{alt}"' + '>'
    # (?<!-) lookbehind prevents matching the > in -> (Twee link arrow inside [[ ]] syntax)
    return re.sub(r'<img\s[^>]*(?<!-)>', replace_img, decoded_content)


def main():
    PASSAGES_DIR.mkdir(parents=True, exist_ok=True)
    HARLOWE_DIR.mkdir(exist_ok=True)
    SRC.mkdir(exist_ok=True)

    content = (ROOT / 'index.html').read_text(encoding='utf-8')

    # ── CSS extraction ────────────────────────────────────────────────────────
    style_m = re.search(r'<style title="Twine CSS">(.*?)</style>', content, re.DOTALL)
    if not style_m:
        sys.exit('ERROR: Could not find <style title="Twine CSS">')
    full_css = style_m.group(1)

    # Lines longer than 500 chars are minified Harlowe engine CSS.
    our_lines = []
    engine_lines = []
    for line in full_css.split('\n'):
        if len(line) > 500:
            engine_lines.append(line)
        else:
            our_lines.append(line)

    our_css = '\n'.join(our_lines).strip()
    engine_css = '\n'.join(engine_lines).strip()

    (SRC / 'style.css').write_text(our_css + '\n', encoding='utf-8')
    print(f'  src/style.css ({len(our_css)} chars)')

    (HARLOWE_DIR / 'harlowe-2.1.0-engine.css').write_text(engine_css + '\n', encoding='utf-8')
    print(f'  harlowe/harlowe-2.1.0-engine.css ({len(engine_css)} chars)')

    # ── User stylesheet ───────────────────────────────────────────────────────
    ss_m = re.search(
        r'<style role="stylesheet" id="twine-user-stylesheet"[^>]*>(.*?)</style>',
        content, re.DOTALL
    )
    story_style = ss_m.group(1).strip() if ss_m else ''
    (SRC / 'story-style.css').write_text(story_style + '\n', encoding='utf-8')
    print(f'  src/story-style.css')

    # ── User script ───────────────────────────────────────────────────────────
    us_m = re.search(
        r'<script role="script" id="twine-user-script"[^>]*>(.*?)</script>',
        content, re.DOTALL
    )
    story_script = us_m.group(1).strip() if us_m else ''
    (SRC / 'story-script.js').write_text(story_script + '\n', encoding='utf-8')
    print(f'  src/story-script.js')

    # ── Harlowe 2.x engine JS ────────────────────────────────────────────────
    ej_m = re.search(
        r'<script title="Twine engine code"[^>]*>(.*?)</script>',
        content, re.DOTALL
    )
    engine_js = ej_m.group(1).strip() if ej_m else ''
    (HARLOWE_DIR / 'harlowe-2.1.0-engine.js').write_text(engine_js + '\n', encoding='utf-8')
    print(f'  harlowe/harlowe-2.1.0-engine.js ({len(engine_js)} chars)')

    # ── Story metadata ────────────────────────────────────────────────────────
    sd_m = re.search(
        r'<tw-storydata'
        r'\s+name="([^"]+)"'
        r'\s+startnode="(\d+)"'
        r'\s+creator="([^"]*)"'
        r'\s+creator-version="([^"]*)"'
        r'\s+format="([^"]*)"'
        r'\s+format-version="([^"]*)"'
        r'\s+ifid="([^"]*)"',
        content
    )
    if not sd_m:
        sys.exit('ERROR: Could not parse tw-storydata attributes')

    start_pid = sd_m.group(2)
    # Find the passage name for the startnode pid
    start_name_m = re.search(
        rf'<tw-passagedata pid="{start_pid}" name="([^"]+)"', content
    )
    start_name = start_name_m.group(1) if start_name_m else start_pid

    meta = {
        'name': sd_m.group(1),
        'startpassage': start_name,
        'creator': sd_m.group(3),
        'creator-version': sd_m.group(4),
        'format': sd_m.group(5),
        'format-version': '3.3.9',
        'ifid': sd_m.group(7),
    }
    (SRC / 'story-meta.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')
    print(f'  src/story-meta.json (startpassage: {start_name})')

    # ── Passages ──────────────────────────────────────────────────────────────
    passage_re = re.compile(
        r'<tw-passagedata'
        r'\s+pid="(\d+)"'
        r'\s+name="([^"]*)"'
        r'\s+tags="([^"]*)"'
        r'\s+position="([^"]*)"'
        r'\s+size="([^"]*)"'
        r'>(.*?)</tw-passagedata>',
        re.DOTALL
    )

    count = 0
    seen_pids = set()
    for m in passage_re.finditer(content):
        pid, name, tags, position, size, raw = m.groups()
        pid_int = int(pid)

        if pid_int in seen_pids:
            print(f'  WARNING: duplicate pid {pid} (passage "{name}") — skipping')
            continue
        seen_pids.add(pid_int)

        # Decode XML entities → real characters
        decoded = html.unescape(raw)

        # Add alt text to images
        decoded = add_alt_text(decoded)

        # Build Twee 3 header
        tag_part = f' [{tags}]' if tags else ''
        pos_meta = json.dumps({'position': position, 'size': size})
        header = f':: {name}{tag_part} {pos_meta}'

        twee = header + '\n' + decoded.rstrip('\n') + '\n'

        safe = re.sub(r'[^\w\-]', '-', name)
        filename = f'{pid_int:03d}-{safe}.twee'
        (PASSAGES_DIR / filename).write_text(twee, encoding='utf-8')
        count += 1

    print(f'  src/passages/ ({count} passages)')
    print('\nDone. Run build.py to regenerate index.html.')


if __name__ == '__main__':
    main()
