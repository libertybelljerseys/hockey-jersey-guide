# Backlog & Known Issues

## Pending Tasks

### High Priority
- [ ] Add brand disclaimer to `about` passage:
  > "Brand logos are used solely to identify manufacturers and are the property of their respective owners. This guide is not affiliated with, endorsed by, or sponsored by Adidas, Fanatics, Reebok, CCM, Koho, or Starter."

### Content / Knowledge
- [ ] All `<!-- EDIT: ADD EXPLANATORY TEXT HERE -->` placeholders have been filled in by the author, but worth reviewing for completeness
- [ ] The `adidas-size` passage is missing size 58 — **wait, this was added**. Confirm 58 is present.
- [ ] Verify `fanatics-size` size range is correct for current Fanatics Premium/Pro Authentic sizing

### UX / Navigation
- [ ] `shield-present` has two duplicate "I'm not sure" links (both route to the same place — harmless but untidy)
- [ ] `reebok-laces-yes` and `reebok-laces-no` both have "I'm not sure → ask" — consider if these should track `$unsure` instead of just going to `ask`

### Subreddit / External
- [ ] Update subreddit sidebar link from old URL (`legitcheck.thedejocker.net`) to new URL
- [ ] Update subreddit wiki pages with new URL  
- [ ] Check AutoModerator config for hardcoded old URL
- [ ] Contact hockeyjerseyaddicts.com — their Resources page still credits "The Dejocker" and links to the old URL

## Known Orphaned Passages
These passages exist in the file but are no longer reachable:
- `Button` — replaced by `adidas-button` and the Fanatics conditional logic
- `neck` — replaced by `adidas-neck` and `fanatics-neck`
- `Adidas` — `manu-switch` now routes directly to `adidas-size`
- `Fanatics-auth` — leftover from an earlier intermediate architecture

These are harmless (Harlowe won't render them unless navigated to) but could be cleaned up.

## Architecture Notes / Decisions Made

### Why Fanatics has its own source check passages
The Fanatics source check flow (`fanatics-source`, `fanatics-ebay`, etc.) is a duplicate of the Adidas/Reebok/CCM flow (`ebay-ask`, `ebay`, etc.) rather than sharing the same passages. This was done intentionally so the flows can diverge independently in the future without cross-contamination.

### Why `dimples` silently skips for Fanatics
Fanatics Authentic jerseys never have shoulder dimples. Rather than asking the question and slamming fake, the `dimples` passage uses `(if: $manu is "fanatics")[(go-to: " laces ")](else:)[...]` to silently skip. This is better UX than a misleading question.

### Why `cut` images are not used for Fanatics
The cut check (`cut` passage) uses Adidas-specific cut images. Fanatics jerseys reach this passage too (shared flow), but the images still reference Adidas cuts. This is a known imperfection — ideally there would be Fanatics-specific cut reference images.

### The `legit-disclaimer` passage
This is a one-line pass-through: `(go-to: "result")`. It exists as a legacy endpoint name since many passages route to it. All paths that "pass" all checks converge here before going to the result page.

## Harlowe Version Constraint
The file uses **Harlowe 2.1.0**. Do not upgrade — it would require testing every passage. Key things that differ from Harlowe 3.x:
- Array syntax: `(a: item1, item2)` not `(array: ...)`
- `(for:)` loop syntax may differ slightly
- Some macro names changed between versions
