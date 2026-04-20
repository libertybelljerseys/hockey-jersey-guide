# Passage Routing Map

Complete routing for all 85 passages in `index.html`. Arrows show all possible destinations from each passage.

## Terminal Passages
These passages end the flow (no outbound navigation except Start Over / Back):
- **`Fake`** — definitive fake indicator
- **`Fake-site`** — fake seller detected
- **`Fake-premier`** — Reebok Premier with fight strap
- **`result`** — final verdict page
- **`ask`** — fringe case, send to community
- **`premier`** — legit Reebok Premier confirmed
- **`fanatics`** — Fanatics Breakaway (generally not faked)
- **`6100`** — Reebok 6100 (generally not faked)
- **`vintage-lettered`** — CCM Vintage lettered size (generally not faked)
- **`about`** — About this guide page

## Full Routing Table

| Passage | Destinations |
|---------|-------------|
| `manufacturer` | `ebay-ask`, `fanatics-ask`, `Starter`, `ask`, `about` |
| `about` | `manufacturer` (back link only) |
| **SOURCE CHECKS — Adidas/Reebok/CCM** | |
| `ebay-ask` | `ebay`, `insta`, `strap` (skip) |
| `ebay` | `strap`, `Fake-site` |
| `insta` | `majorcorp`, `site-check` |
| `majorcorp` | `strap`, `sketch` |
| `site-check` | `Fake-site`, `ddos` |
| `sketch` | `Fake-site`, `ddos` |
| `ddos` | `Fake-site`, `whois` |
| `whois` | `tgtbt`, `Fake-site` |
| `tgtbt` | `Fake-site`, `strap` |
| **SOURCE CHECKS — Fanatics** | |
| `fanatics-ask` | `fanatics`, `fanatics-source`, `manufacturer` |
| `fanatics-source` | `fanatics-ebay`, `fanatics-insta`, `strap` (skip) |
| `fanatics-ebay` | `strap`, `Fake-site` |
| `fanatics-insta` | `fanatics-majorcorp`, `fanatics-site-check` |
| `fanatics-majorcorp` | `strap`, `fanatics-sketch` |
| `fanatics-site-check` | `Fake-site`, `fanatics-ddos` |
| `fanatics-sketch` | `Fake-site`, `fanatics-ddos` |
| `fanatics-ddos` | `Fake-site`, `fanatics-whois` |
| `fanatics-whois` | `fanatics-tgtbt`, `Fake-site` |
| `fanatics-tgtbt` | `Fake-site`, `strap` |
| **SHARED CHECKS (all manufacturers)** | |
| `strap` | `fight-strap`, `no-strap` |
| `fight-strap` | `no-strap`, `Lettering`, `Fake` |
| `no-strap` | `reebok-replica`(reebok), `CCM`(ccm), `Lettering`(fanatics), `adidaswcoh`(adidas), `legit-disclaimer`(starter) |
| `Lettering` | `crest` |
| `crest` | `crap-design` |
| `crap-design` | `Fake`, `pause` |
| `pause` | `manu-switch` |
| `manu-switch` | `edgeorno`(reebok), `adidas-size`(adidas), `fanatics-size`(fanatics), `CCM`(ccm), `legit-disclaimer`(starter) |
| **ADIDAS BRAND-SPECIFIC** | |
| `adidas-size` | `adidas-button`, `Fake`(size 48) |
| `adidas-button` | `button-check`(yes), `adidas-neck`(no) |
| `button-check` | `button-older`(yes), `adidas-neck`(no/flag) |
| `button-older` | `adidas-neck` |
| `adidas-neck` | `band` |
| `adidas-box` | `dimples` |
| **FANATICS BRAND-SPECIFIC** | |
| `fanatics-size` | `fanatics-button` |
| `fanatics-button` | `Fake`(has button), `fanatics-neck`(no button) |
| `fanatics-neck` | `band` |
| `fanatics-box` | `laces` |
| **SHARED PHYSICAL CHECKS** | |
| `neck` | `band` *(orphaned — was old shared neck, now replaced by adidas-neck/fanatics-neck)* |
| `band` | `hangar` |
| `hangar` | `shield` |
| `shield` | `shield-present`(yes), `Fake`(no shield) |
| `shield-present` | `fanatics-box`(fanatics), `box`(others) |
| `box` | `dimples` |
| `dimples` | `laces` *(silently skips for fanatics via `(if: $manu is "fanatics")`)* |
| `laces` | `cut` |
| `cut` | `legit-disclaimer`, `ask`(not sure) |
| `legit-disclaimer` | `result` |
| `result` | `manufacturer` (start over) |
| **REEBOK BRAND-SPECIFIC** | |
| `edgeorno` | `Reebok`(edge), `Fake-premier`(premier), `6100`, `edge`(not sure) |
| `Reebok` | `edge`, `Fake`(size 48), `reebok-replica` |
| `edge` | `reebok-neck` |
| `reebok-neck` | `reebok-neck-vector`, `reebok-neck-wordmark` |
| `reebok-neck-vector` | `reebok-laces-ask` |
| `reebok-neck-wordmark` | `reebok-laces-ask` |
| `reebok-laces-ask` | `reebok-laces-yes`, `reebok-laces-no` |
| `reebok-laces-yes` | `legit-disclaimer`, `ask` |
| `reebok-laces-no` | `legit-disclaimer`, `ask` |
| `reebok-replica` | `premier`, `replica-wc` |
| `replica-wc` | `premier`, `premier-size` |
| `premier-size` | `premier`, `ask` |
| **CCM BRAND-SPECIFIC** | |
| `CCM` | `ccm-vintage`(yes), `ccm-novintage`(no) |
| `ccm-vintage` | `vintage-number`(numbered), `vintage-lettered`(lettered) |
| `vintage-number` | `Fake`(gray bands), `legit-disclaimer`(blue bands) |
| `ccm-novintage` | `ccm-novintage-sizes`(lettered), `legit-disclaimer`(numbered) |
| `ccm-novintage-sizes` | `ccm-novintage-stitching`(consistent), `Fake`(inconsistent) |
| `ccm-novintage-stitching` | `Fake`(drop stitches), `ccm-nonvintage-lettering`(clean) |
| `ccm-nonvintage-lettering` | `legit-disclaimer` |
| **ADIDAS WORLD CUP OF HOCKEY** | |
| `adidaswcoh` | `wcoh`(yes), `ask`(no) |
| `wcoh` | `legit-disclaimer`(has jock tag), `ask`(no) |
| **UNUSED / LEGACY** | |
| `Button` | `Fake`(fanatics+yes), `button-check`(adidas+yes), `neck`(no) — *orphaned, replaced by adidas-button* |
| `neck` | `band` — *orphaned, replaced by adidas-neck and fanatics-neck* |
| `Adidas` | `adidas-size` — *orphaned, manu-switch now goes directly to adidas-size* |
| `Fanatics-auth` | `legit-disclaimer` — *orphaned leftover* |
