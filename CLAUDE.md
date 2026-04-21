# NHL Jersey Legit Check Guide — Claude Code Project

## Project Overview

This is an interactive NHL jersey authentication guide built with **Twine/Harlowe 2.1.0**, hosted as a single self-contained HTML file at:

**https://legitcheck.libertybelljerseys.com/**

- GitHub repo: https://github.com/libertybelljerseys/hockey-jersey-guide
- Buy Me a Coffee: https://buymeacoffee.com/libertybelljerseys
- Discord: https://discord.com/invite/hockeyjerseys
- Subreddit: https://reddit.com/r/hockeyjerseys

The guide was originally "the r/hockeyjerseys guide" but has been fully rebranded to **Liberty Bell Jerseys**. The author is DexterMorgan67 on Reddit, and is a moderator of r/hockeyjerseys.

---

## Tech Stack

| Component | Detail |
|-----------|--------|
| Engine | Twine + Harlowe 2.1.0 |
| Format | Single HTML file (`index.html`) |
| Hosting | GitHub Pages with custom domain via Cloudflare DNS |
| Images | Hosted in `images/` folder in the GitHub repo (formerly S3) |
| Brand logos | `images/logos/$brand.png` — pre-processed 32px transparent PNGs |

The entire guide — engine, CSS, all passage content, and Harlowe runtime — lives in one `index.html` file. There is no build step.

---

## File Structure (repo)

```
index.html          # The entire guide
images/
  logos/
    adidas.png      # 48x32px transparent PNG
    ccm.png         # 80x19px transparent PNG
    fanatics.png    # 37x32px transparent PNG
    koho.png        # 80x20px transparent PNG
    reebok.png      # 57x32px transparent PNG
    starter.png     # 66x32px transparent PNG
  [all other guide images referenced in passages]
```

---

## How Twine/Harlowe Works in This File

Passages are stored as `<tw-passagedata>` XML elements inside a `<tw-storydata>` block in the HTML. The Harlowe runtime (minified JS) is also embedded and reads/executes these passages at runtime.

### Key Harlowe syntax used in this project

```
(link: "text")[action]          # Clickable link with arbitrary action
(go-to: "passage name")         # Navigate to a passage
(set: $var to value)            # Set a variable
(if: condition)[...](else:)[...]# Conditional display
|hookName>[ content ]           # Named hook
(click: ?hookName)[action]      # Click enchantment on a named hook
(undo:)                         # Navigate back (used in FOOTER)
(for: each _item, ...$array)[_item]  # Loop over array
```

### Special tagged passages
- `FOOTER` (tags: `footer`) — appended to every passage automatically by Harlowe
- `HEADER` (tags: none) — was `header` tag but removed; logo now only on manufacturer page

### Variables
| Variable | Type | Purpose |
|----------|------|---------|
| `$manu` | string | Manufacturer: `'adidas'`, `'fanatics'`, `'reebok'`, `'CCM'`, `'Starter'`, `'Other'` |
| `$flags` | number | Count of red flags accumulated |
| `$flagnames` | array | Labels of each red flag for display on result page |
| `$unsure` | number | Count of "I'm not sure" answers |
| `$unsurenames` | array | Labels of each uncertain check |
| `$strap` | string | `'true'` or `'false'` — whether jersey has a fight strap |

All variables are reset to zero/empty on every manufacturer selection and on "Start Over".

---

## Passage Architecture

See `docs/passage-routing.md` for the complete routing map.

### The three terminal passages
- **`fake`** — Slam-dunk fake (single definitive indicator). Shows `$unsure` note if any.
- **`fake-site`** — Fake seller/website detected in source checks.
- **`result`** — All accumulated red flags evaluated. Shows verdict + flag list + unsure list.

### The result verdicts (in `result` passage)
| Flags | Verdict |
|-------|---------|
| 0 | ✅ Probably Legit |
| 1 | ⚠️ One Red Flag — Worth a Closer Look |
| 2–3 | ⚠️ Multiple Red Flags — Check Closer |
| 4+ | ❌ Very Likely Fake |

### Slam-dunk fakes (go directly to `fake`, no flag accumulation)
- Size 48 (Adidas `adidas-size` or Reebok `reebok-intro` passage)
- No NHL shield present (`shield` passage)
- Fake fight strap image (`fight-strap` passage)
- Fanatics jersey has a button (`fanatics-button` passage)
- Fantasy/crap design (`fake-design` passage)
- CCM: inconsistent size tag (`ccm-non-vintage-sizes`)
- CCM: drop stitches on crest/patches (`ccm-non-vintage-stitching`)
- CCM vintage: gray-banded neck tag (`ccm-vintage-number`)

### Red flag checks (accumulate `$flags`, continue the guide)
These passages add to `$flags` and `$flagnames` then continue to the next check:
`button-check`, `button-older`, `adidas-neck`, `fanatics-neck`, `band`, `hangar`, `shield-present`, `adidas-box`, `fanatics-box`, `box`, `dimples`, `laces`, `cut`, `lettering`, `crest`, `reebok-edge`, `reebok-neck-vector`, `reebok-neck-wordmark`, `reebok-laces-yes`, `reebok-laces-no`, `ccm-non-vintage-lettering`

---

## Complete Flow by Manufacturer

### Adidas
```
manufacturer → source-ask → [source checks] → strap → fight-strap/no-strap
→ lettering → crest → fake-design → checkpoint → manu-switch → adidas-size
→ adidas-button → [button checks if yes] → adidas-neck → band → hangar
→ shield → shield-present → adidas-box → dimples → laces → cut
→ legit-disclaimer → result
```

### Fanatics Premium/Pro Authentic
```
manufacturer → fanatics-intro → source-ask → [source checks] → strap
→ fight-strap/no-strap → lettering → crest → fake-design → checkpoint
→ manu-switch → fanatics-size → fanatics-button → fanatics-neck → band
→ hangar → shield → shield-present → fanatics-box → laces → cut
→ legit-disclaimer → result
```

### Fanatics Breakaway
```
manufacturer → fanatics-intro → fanatics-breakaway → [dead end, start over]
```
Breakaway jerseys are generally not faked — the `fanatics-breakaway` passage says so and provides a jock tag reference image.

### Reebok Edge
```
manufacturer → source-ask → [source checks] → strap → fight-strap/no-strap
→ lettering → crest → fake-design → checkpoint → manu-switch → reebok-edge-or-premier
→ reebok-intro → [size check, 48=fake] → reebok-edge → reebok-neck → reebok-neck-vector
or reebok-neck-wordmark → reebok-laces-ask → reebok-laces-yes/no
→ legit-disclaimer → result
```

### Reebok Premier/Replica
```
... → reebok-edge-or-premier → fake-premier (has strap) or reebok-replica → reebok-premier-legit
```

### CCM/Koho
```
manufacturer → source-ask → [source checks] → strap → fight-strap/no-strap
→ lettering → crest → fake-design → checkpoint → manu-switch → ccm-intro
→ ccm-vintage or ccm-non-vintage → [vintage/non-vintage checks]
→ legit-disclaimer → result
```

### Starter/Pro Player
```
manufacturer → starter-intro → strap → [shared checks] → manu-switch
→ legit-disclaimer → result
```

---

## Emoji Convention

| Emoji | Meaning | Usage |
|-------|---------|-------|
| ✅ | Good / Legit / Yes (this is fine) | Legit-path answers |
| ❌ | Bad / Fake / Yes (this is a problem) | Flag-triggering answers |
| 🤔 | Uncertain | "I'm not sure" on all checks |

**Important:** `✅ Yes` does NOT always mean "yes is good". It means "yes, this is the correct/expected state". For example, `✅ Yes` on "does it have an NHL shield?" is good. But `❌ Yes` on "does the band look shiny?" means yes = bad. Always check semantic meaning, not just emoji.

---

## CSS Architecture

All CSS is injected into the `<style title="Twine CSS">` block in the HTML `<head>`. Our additions follow the Harlowe default CSS. Key sections we've added:

```css
/* 1. Brand logo sizing */
.brand-logo-inline { height: 1em; ... }
.brand-logo-header { height: 3em; ... }

/* 2. Manufacturer choice hooks */
tw-hook[name=mAdidas], tw-hook[name=mFanatics], ... { display: flex; ... }

/* 3. Choice button styling */
tw-passage tw-link, tw-passage .enchantment-link { display: inline-block; ... }

/* 4. Footer nav */
.footer-nav { ... }

/* 5. Mobile responsive */
@media (max-width: 700px) { ... }

/* 6. Watermark logo */
#site-logo { position: fixed; bottom: 10px; right: 10px; width: 32px; ... }

/* 7. Fluid images */
img:not(#site-logo) { max-width: 100%; height: auto; }
.BTG-header img { width: 120px !important; ... }
```

---

## Known Passage Name Quirks

All passage names now use consistent lowercase kebab-case with no leading/trailing spaces. There are no longer any whitespace-padded names to work around. Passage names match exactly what you write in `(go-to: "name")` macros.

---

## Editing Patterns

### To add a new red-flag check to a passage
```
(link: "&lt;flag text&gt;")[(set: $flags to $flags + 1)(set: $flagnames to $flagnames + (a: "&lt;label for result page&gt;"))(go-to: "&lt;next passage&gt;")]
```

### To make an image clickable (flag-triggering)
```
|hookName>[ &lt;img src="images/example.png"&gt; ](click: ?hookName)[(set: $flags to $flags + 1)(set: $flagnames to $flagnames + (a: "&lt;label&gt;"))(go-to: "&lt;next passage&gt;")]
```

### To add an "I'm not sure" link
```
(link: "🤔 I'm not sure")[(set: $unsure to $unsure + 1)(set: $unsurenames to $unsurenames + (a: "&lt;check name&gt;"))(go-to: "&lt;next passage&gt;")]
```

### To add a new passage
Add a `<tw-passagedata>` element before `</tw-storydata>`. Use the next available pid (currently max is 85).
```html
<tw-passagedata pid="86" name="my-passage" tags="" position="x,y" size="100,100">
passage content here
</tw-passagedata>
```

---

## Important Notes

- **No build step** — edit `index.html` directly. Changes are live after pushing to GitHub.
- **Max pid is 85** — increment for any new passages.
- **Harlowe does not support HTML inside `(link: "...")` text** — using `&quot;` inside link text breaks parsing. Use named hook + `(click:)` pattern for clickable images/complex elements.
- **`[[ ]]` link syntax** can sometimes fail with emoji in display text. Prefer `(link:)` macro for choices that include emoji.
- **Session state** is saved in the URL hash by Harlowe. Users resuming from a bookmarked URL will pick up where they left off. "Start Over" resets all variables and navigates to `manufacturer`.
- **The `FOOTER` passage** (tagged `footer`) renders on every page. It contains the Back `(undo:)` button, Start Over link, and the watermark logo.

