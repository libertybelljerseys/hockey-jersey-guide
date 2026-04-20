# Editing Guide

How to work with `index.html` programmatically (Python or otherwise).

## Reading Passages

```python
import re

with open('index.html', 'r') as f:
    content = f.read()

passages = re.findall(
    r'<tw-passagedata[^>]*name="([^"]*)"[^>]*>(.*?)</tw-passagedata>',
    content, re.DOTALL
)
pd = {name.strip(): body for name, body in passages}

# Access a passage
print(pd['manufacturer'])
```

## Replacing a Passage

Passage names in the XML may have leading/trailing spaces (e.g. `' neck '`). This helper handles both:

```python
def replace_passage(content, exact_name, new_body):
    for candidate in [exact_name, ' '+exact_name+' ', exact_name+' ', ' '+exact_name]:
        pattern = r'(<tw-passagedata[^>]*name="' + re.escape(candidate) + r'"[^>]*>)(.*?)(</tw-passagedata>)'
        m = re.search(pattern, content, re.DOTALL)
        if m:
            return content[:m.start()] + m.group(1) + new_body + m.group(3) + content[m.end():]
    raise ValueError(f"Passage not found: {exact_name!r}")
```

## Adding a New Passage

```python
new_passage = (
    '<tw-passagedata pid="86" name="my-new-passage" tags="" '
    'position="800,800" size="100,100">'
    'Passage content here\n\n'
    '[[Continue ->next-passage]]'
    '</tw-passagedata>\n'
)
content = content.replace('</tw-storydata>', new_passage + '</tw-storydata>')
```

**Always increment the pid.** Current max is 85.

## Passage Content Encoding

Passage bodies are HTML-escaped inside the XML. The mapping:

| Raw | In passage body |
|-----|----------------|
| `"` | `&quot;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `'` | `&#39;` |
| `&` | `&amp;` |

So a Harlowe link like `(go-to: "my-passage")` appears in the file as:
```
(go-to: &quot;my-passage&quot;)
```

And an image like `<img src="images/foo.png">` appears as:
```
&lt;img src=&quot;images/foo.png&quot;&gt;
```

## Injecting CSS

Our custom CSS lives inside the `<style title="Twine CSS">` block. To add more:

```python
insertion_point = 'a{color:#93c5fd;text-decoration:underline}a:hover{color:#7dd3fc}'
new_css = insertion_point + '\n\n/* My new CSS */\n.my-class { ... }'
content = content.replace(insertion_point, new_css, 1)
```

## Common Patterns

### Red flag link (text choice)
```
(link: &quot;❌ Bad thing&quot;)[(set: $flags to $flags + 1)(set: $flagnames to $flagnames + (a: &quot;Label for result page&quot;))(go-to: &quot;next-passage&quot;)]
```

### Red flag link (clickable image)
```
|hookName>[ &lt;img src=&quot;images/fake.png&quot;&gt; ](click: ?hookName)[(set: $flags to $flags + 1)(set: $flagnames to $flagnames + (a: &quot;Label&quot;))(go-to: &quot;next-passage&quot;)]
```

### I'm not sure link
```
(link: &quot;🤔 I'm not sure&quot;)[(set: $unsure to $unsure + 1)(set: $unsurenames to $unsurenames + (a: &quot;Check name&quot;))(go-to: &quot;next-passage&quot;)]
```

### Manufacturer-conditional routing
```
(if: $manu is &quot;fanatics&quot;)[(go-to: &quot;fanatics-passage&quot;)](else:)[(go-to: &quot;other-passage&quot;)]
```

### Named hook + click (for clickable non-link elements like brand logos)
```
|hookName>[ content ](click: ?hookName)[(go-to: &quot;destination&quot;)]
```

## Passages With Spaced Names

These must be referenced with their exact spaces in `(go-to:)` macros:

```python
SPACED_PASSAGES = {
    'neck':           ' neck ',
    'band':           ' band ',
    'hangar':         ' hangar ',
    'shield':         ' shield ',
    'box':            ' box ',
    'dimples':        ' dimples ',
    'laces':          ' laces ',
    'cut':            ' cut ',
    'button-check':   ' button-check ',
    'button-older':   ' button-older ',
    'shield-present': ' shield-present ',
    'adidas-size':    '  adidas-size',    # two leading spaces
    'manu-switch':    ' manu-switch',     # one leading space
    'vintage-number': 'vintage-number ',  # one trailing space
}
```

The `[[ text -> passage ]]` syntax is forgiving and trims spaces automatically.
The `(go-to: "passage name")` macro requires exact match.

## Verifying Changes

After editing, run these checks:

```python
# No duplicate discord links
assert content.count('discord.com/invite/hockeyjerseys&quot;&gt;Hockey Jerseys Discord&lt;/a&gt; or the &lt;a href=&quot;https://discord.com/invite') == 0

# No old emoji chars
assert '✔' not in content
assert '✘' not in content

# All manufacturer links reset variables
for manu in ['adidas', 'fanatics', 'reebok', 'CCM', 'Starter']:
    assert f'$manu to &quot;{manu}&quot;' not in content or \
           f'set: $flags to 0' in content  # rough check

# result passage exists
assert 'name="result"' in content

# No broken routing to non-existent passages  
passage_names = set(name.strip() for name in re.findall(r'<tw-passagedata[^>]*name="([^"]*)"', content))
go_tos = re.findall(r'go-to: &quot;([^&]+)&quot;', content)
for dest in go_tos:
    if dest.strip() not in passage_names:
        print(f"WARNING: go-to destination not found: {dest!r}")
```
