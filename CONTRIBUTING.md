# Contributing to the NHL Jersey Legit Check Guide

Thanks for helping improve the guide. Contributions can range from correcting outdated info to adding new manufacturer checks.

## Ways to Contribute

- **Report an error or outdated info** — open a GitHub issue
- **Suggest a new check or manufacturer** — open an issue with details
- **Fix a passage directly** — open a pull request (see below)
- **Share with the community** — post in [r/hockeyjerseys](https://reddit.com/r/hockeyjerseys) or the [Discord](https://discord.com/invite/hockeyjerseys)

---

## How the Guide Works

Everything lives in `index.html` — the Twine/Harlowe 2.1.0 runtime, all CSS, and all content. Passages are stored as `<tw-passagedata>` XML elements inside a `<tw-storydata>` block. There is no build step.

See [`docs/passage-routing.md`](docs/passage-routing.md) for the full routing map, and [`docs/editing-guide.md`](docs/editing-guide.md) for programmatic editing patterns.

---

## Making Edits

### Editing a passage

Find the passage by name in `index.html`:

```html
<tw-passagedata pid="12" name="my-passage" tags="" position="x,y" size="100,100">
passage content here
</tw-passagedata>
```

Passage bodies are HTML-escaped. The key mappings:

| Raw | In file |
|-----|---------|
| `"` | `&quot;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |

So a Harlowe link like `(go-to: "next-passage")` appears in the file as:
```
(go-to: &quot;next-passage&quot;)
```

### Adding a new passage

Add a `<tw-passagedata>` element before `</tw-storydata>`. The current max pid is **85** — always increment.

```html
<tw-passagedata pid="86" name="my-new-passage" tags="" position="800,800" size="100,100">
passage content here
</tw-passagedata>
```

### Passage name quirks

Several passage names have leading or trailing spaces from the original Twine file. When using `(go-to:)` you must match exactly. The `[[ ]]` link syntax trims spaces automatically.

Spaced names to watch out for:
- `' neck '`, `' band '`, `' hangar '`, `' shield '`
- `' box '`, `' dimples '`, `' laces '`, `' cut '`
- `' button-check '`, `' button-older '`, `' shield-present '`
- `'  adidas-size'` (two leading spaces), `' manu-switch'` (one leading space)
- `'vintage-number '` (one trailing space)

---

## Common Harlowe Patterns

### Red flag choice (text)
```
(link: &quot;❌ Bad thing&quot;)[(set: $flags to $flags + 1)(set: $flagnames to $flagnames + (a: &quot;Label for result page&quot;))(go-to: &quot;next-passage&quot;)]
```

### Red flag choice (clickable image)
```
|hookName>[ &lt;img src=&quot;images/fake.png&quot;&gt; ](click: ?hookName)[(set: $flags to $flags + 1)(set: $flagnames to $flagnames + (a: &quot;Label&quot;))(go-to: &quot;next-passage&quot;)]
```

### "I'm not sure" link
```
(link: &quot;🤔 I'm not sure&quot;)[(set: $unsure to $unsure + 1)(set: $unsurenames to $unsurenames + (a: &quot;Check name&quot;))(go-to: &quot;next-passage&quot;)]
```

### Slam-dunk fake (no flag accumulation, go directly to Fake)
```
(link: &quot;❌ Yes&quot;)[(go-to: &quot;Fake&quot;)]
```

---

## Emoji Convention

| Emoji | Meaning |
|-------|---------|
| ✅ | Legit-path answer (this is the correct/expected state) |
| ❌ | Flag-triggering answer (this is a problem) |
| 🤔 | Uncertain — "I'm not sure" |

**Note:** `✅ Yes` does not always mean "yes is good." It means "yes, this matches expectations." Always check the semantic meaning in context.

---

## Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `$manu` | string | Active manufacturer (`'adidas'`, `'fanatics'`, `'reebok'`, `'CCM'`, `'Starter'`, `'Other'`) |
| `$flags` | number | Count of red flags accumulated |
| `$flagnames` | array | Labels shown on the result page |
| `$unsure` | number | Count of "I'm not sure" answers |
| `$unsurenames` | array | Labels for uncertain checks |
| `$strap` | string | `'true'` or `'false'` — whether jersey has a fight strap |

All variables reset to zero/empty on manufacturer selection and on "Start Over."

---

## Images

Guide images live in `images/`. Brand logos are in `images/logos/$brand.png` — pre-processed 32px transparent PNGs.

When adding a new image, reference it in a passage like:
```
&lt;img src=&quot;images/my-image.png&quot;&gt;
```

---

## Pull Request Guidelines

- Keep PRs focused — one logical change per PR
- Test your change by opening `index.html` in a browser and walking through the affected flow
- Don't modify the minified Harlowe runtime (the large `<script>` block)
- If adding a new passage, update `docs/passage-routing.md`

---

## Questions?

Open an issue or ask in the [Discord](https://discord.com/invite/hockeyjerseys).
