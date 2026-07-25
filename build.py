#!/usr/bin/env python3
"""
build.py — assembles index.html from source files.

Source layout:
  src/style.css             our custom CSS
  src/story-style.css       Twine user stylesheet
  src/story-script.js       Twine user JS
  src/story-meta.json       story metadata
  src/passages/*.twee       passage files (Twee 3 format)
  harlowe/harlowe-3.3.9-engine.css   Harlowe engine CSS
  harlowe/harlowe-3.3.9-engine.js    Harlowe engine JS

Usage:
  python3 build.py              # writes index.html
  python3 build.py --check      # diff only, no write
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


def xml_escape(s: str) -> str:
    return (s
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def parse_twee(path: Path) -> dict:
    """Parse a Twee 3 passage file. Returns passage dict."""
    text = path.read_text(encoding='utf-8')
    lines = text.split('\n')

    # Header: :: Name [tags] {"position":"x,y","size":"w,h"}
    header = lines[0]
    if not header.startswith(':: '):
        raise ValueError(f'{path}: passage header must start with ":: "')

    rest = header[3:]  # strip ':: '

    # Tags: optional [tag1 tag2]
    tags = ''
    tags_m = re.match(r'^(.*?)\s+\[([^\]]*)\]\s+(\{.*\})\s*$', rest)
    no_tags_m = re.match(r'^(.*?)\s+(\{.*\})\s*$', rest)

    if tags_m:
        name = tags_m.group(1)
        tags = tags_m.group(2)
        meta_json = json.loads(tags_m.group(3))
    elif no_tags_m:
        name = no_tags_m.group(1)
        meta_json = json.loads(no_tags_m.group(2))
    else:
        raise ValueError(f'{path}: cannot parse header: {header!r}')

    content = '\n'.join(lines[1:]).rstrip('\n')

    return {
        'name': name,
        'tags': tags,
        'position': meta_json.get('position', '100,100'),
        'size': meta_json.get('size', '100,100'),
        'content': content,
    }


def load_passages() -> list:
    twee_files = sorted(PASSAGES_DIR.glob('*.twee'))
    if not twee_files:
        sys.exit(f'ERROR: No .twee files found in {PASSAGES_DIR}')
    passages = []
    for f in twee_files:
        # pid is the numeric prefix of the filename
        pid_str = f.stem.split('-')[0]
        p = parse_twee(f)
        p['pid'] = int(pid_str)
        passages.append(p)
    passages.sort(key=lambda p: p['pid'])
    return passages


def build_passage_xml(passages: list, start_name: str) -> tuple[str, int]:
    """Return (xml_string, startnode_pid)."""
    parts = []
    startnode = None
    for p in passages:
        if p['name'] == start_name:
            startnode = p['pid']
        escaped = xml_escape(p['content'])
        attrs = (
            f'pid="{p["pid"]}"'
            f' name="{html.escape(p["name"])}"'
            f' tags="{p["tags"]}"'
            f' position="{p["position"]}"'
            f' size="{p["size"]}"'
        )
        parts.append(f'<tw-passagedata {attrs}>{escaped}</tw-passagedata>')
    if startnode is None:
        # Fall back to first passage
        startnode = passages[0]['pid']
        print(f'WARNING: startpassage "{start_name}" not found; using pid={startnode}')
    return '\n'.join(parts), startnode


HEAD_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="apple-touch-icon" href="images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<meta property="og:title" content="NHL Jersey Legit Check Guide — Liberty Bell Jerseys">
<meta property="og:description" content="An interactive guide to help you determine if your NHL jersey is legitimate or a fake. Covers Adidas, Fanatics, Reebok, CCM, and more.">
<meta property="og:image" content="https://legitcheck.libertybelljerseys.com/images/logo.png">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="NHL Jersey Legit Check Guide — Liberty Bell Jerseys">
<meta name="twitter:description" content="An interactive guide to help you determine if your NHL jersey is legitimate or a fake. Covers Adidas, Fanatics, Reebok, CCM, and more.">
<meta name="twitter:image" content="https://legitcheck.libertybelljerseys.com/images/logo.png">

<title>NHL Jersey Legit Check Guide — Liberty Bell Jerseys</title>
<style title="Twine CSS">
{engine_css}
{custom_css}
</style>
</head>

<body>

<tw-story></tw-story>

<tw-storydata name="{story_name}" startnode="{startnode}" creator="{creator}" creator-version="{creator_version}" format="{fmt}" format-version="{fmt_version}" ifid="{ifid}" options="" tags="" zoom="1" hidden>\
<style role="stylesheet" id="twine-user-stylesheet" type="text/twine-css">
{story_style}
</style>\
<script role="script" id="twine-user-script" type="text/twine-javascript">
{story_script}
</script>\
{passages}
</tw-storydata>

<script title="Twine engine code" data-main="harlowe">{engine_js}</script>

</body>
</html>"""


def main():
    check_only = '--check' in sys.argv

    meta = json.loads((SRC / 'story-meta.json').read_text(encoding='utf-8'))
    custom_css = (SRC / 'style.css').read_text(encoding='utf-8').strip()
    story_style = (SRC / 'story-style.css').read_text(encoding='utf-8').strip()
    story_script = (SRC / 'story-script.js').read_text(encoding='utf-8').strip()

    engine_css_path = HARLOWE_DIR / 'harlowe-3.3.9-engine.css'
    engine_js_path = HARLOWE_DIR / 'harlowe-3.3.9-engine.js'
    for p in (engine_css_path, engine_js_path):
        if not p.exists():
            sys.exit(f'ERROR: Missing {p}. Run: python3 extract_harlowe.py')

    engine_css = engine_css_path.read_text(encoding='utf-8').strip()
    engine_js = engine_js_path.read_text(encoding='utf-8').strip()

    passages = load_passages()
    passage_xml, startnode = build_passage_xml(passages, meta['startpassage'])

    output = HEAD_TEMPLATE.format(
        engine_css=engine_css,
        custom_css=custom_css,
        story_name=html.escape(meta['name']),
        startnode=startnode,
        creator=html.escape(meta['creator']),
        creator_version=html.escape(meta['creator-version']),
        fmt=html.escape(meta['format']),
        fmt_version=html.escape(meta['format-version']),
        ifid=html.escape(meta['ifid']),
        story_style=story_style,
        story_script=story_script,
        passages=passage_xml,
        engine_js=engine_js,
    )

    out_path = ROOT / 'index.html'

    if check_only:
        current = out_path.read_text(encoding='utf-8') if out_path.exists() else ''
        if current == output:
            print('index.html is up to date.')
        else:
            print('index.html would change.')
        return

    out_path.write_text(output, encoding='utf-8')
    print(f'Built index.html ({len(output):,} bytes, {len(passages)} passages, Harlowe 3.3.9)')


if __name__ == '__main__':
    main()
