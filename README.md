# NHL Jersey Legit Check Guide

An interactive guide for authenticating NHL hockey jerseys — built with [Twine/Harlowe 3.3.9](https://twinery.org/), hosted as a single self-contained HTML file.

**[legitcheck.libertybelljerseys.com](https://legitcheck.libertybelljerseys.com/)**

---

## What It Does

Step-by-step authentication for NHL jerseys from Adidas, Fanatics, Reebok, CCM/Koho, and Starter. The guide walks through source checks, physical inspection points, and accumulates red flags to give a final verdict:

- ✅ Probably Legit
- ⚠️ One or more red flags — worth a closer look
- ❌ Very likely fake

## About

Built and maintained by [Liberty Bell Jerseys](https://libertybelljerseys.com/). Originally created as the r/hockeyjerseys community guide. The author is a moderator of [r/hockeyjerseys](https://reddit.com/r/hockeyjerseys).

- **Discord:** [discord.com/invite/hockeyjerseys](https://discord.com/invite/hockeyjerseys)
- **Subreddit:** [r/hockeyjerseys](https://reddit.com/r/hockeyjerseys)
- **Support the guide:** [buymeacoffee.com/libertybelljerseys](https://buymeacoffee.com/libertybelljerseys)

## Tech Stack

`index.html` is the build output — it includes the Harlowe 3.3.9 runtime, all passage content, and CSS, and is what gets deployed. The source lives in `src/`:

| Path | Purpose |
|------|---------|
| `src/passages/*.twee` | One file per passage (Twee 3 format) |
| `src/style.css` | Custom CSS |
| `src/story-style.css` | Twine user stylesheet |
| `src/story-meta.json` | Story name, IFID, start passage |
| `harlowe/harlowe-3.3.9-engine.*` | Harlowe runtime (do not edit) |
| `build.py` | Assembles everything into `index.html` |

**To rebuild after editing source files:**

```
python3 build.py
```

Then push `index.html` to deploy.

Hosted on GitHub Pages with a custom domain via Cloudflare DNS.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to report issues, suggest content, or edit passages directly.

## License

Brand logos are used solely to identify manufacturers and are the property of their respective owners. This guide is not affiliated with, endorsed by, or sponsored by Adidas, Fanatics, Reebok, CCM, Koho, or Starter.

The source code is made publicly available for viewing and personal study only. You may not copy, deploy, host, repackage, or use this project (or any derivative) in any form — commercial or otherwise — without explicit written permission from Liberty Bell Jerseys.

For licensing inquiries, contact Liberty Bell Jerseys.

See the [LICENSE](./LICENSE) file for full legal text.
