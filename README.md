# WNAC: *Wedge Needs A Copilot*

A lightweight, private, AI-centric personal-finance dashboard. Static HTML, JSON data, a swappable AI
brain. No server, no Electron, no cloud. Copilot-styled "sight" + a flex-number/pay-down budget model.

## Setup
Copy the templates and fill in your own values (the copies are gitignored):
```sh
cp budget.config.example.json budget.config.json   # income, goals, and your data-engine db_path
cp overrides.example.json     overrides.json        # your private merchant-to-category map
```
Point `db_path` (and optional `journal_path`) at your local files, or set `$WNAC_DB` / `$WNAC_JOURNAL`. No real paths or finances are committed.

## Run (P1)
```sh
python3 import.py      # wnab/Actual engine  -> data.json   (accounts + transactions; deterministic)
python3 analyze.py     # data.json + budget.config.json + brain -> insights.json
python3 render.py      # -> dashboard.html  (self-contained; open in a browser)
# or:  python3 import.py && python3 analyze.py && python3 render.py && open dashboard.html
```

## Pieces
- `import.py` reads the wnab budget DB (the data engine). CSV/QFX adapters are the next import mode.
- `analyze.py` is the *only* AI stage. P1 uses `brain.py`'s offline `stub` (no network, no API key).
- `brain.py` is the swappable brain. Contract: `categorize_and_narrate(data)`. Add `claude`/`hermes` later.
- `render.py` inlines `tokens.css` + data into a self-contained `dashboard.html` (no server/CDN; `file://`-safe).
- `tokens.css` has the Copilot-derived design tokens (pixel-sampled). `DESIGN.md` has the component anatomy and line logic.
- `budget.config.json` is your income, fixed costs, and goals. GITIGNORED.
- `data.json`, `insights.json`, and `dashboard.html` get generated. GITIGNORED.

## Privacy
*The method is public, the money is private.* `budget.config.json`, `data.json`, `insights.json`,
`dashboard.html` are gitignored. Code may be public; financial data never is.

## Roadmap
- P2 adds a `claude` brain. It categorizes cryptic merchants, which kills the "to review" pile. It also adds a projected debt-free date (APR amortization), in-UI category correction, and recurring/subscription detection.
- P3 adds a `hermes` brain, direct CSV/QFX import, a light theme, and the "Next two weeks" recurring card.

## License

Code in this repository is Apache-2.0. The licence text is `LICENSE`.

Own content, such as copy, data, and docs prose, is all rights reserved. No content licence is chosen.

Third-party files keep their own licences.
