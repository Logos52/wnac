"""WNAC render (P1): data.json + insights.json + tokens.css -> self-contained dashboard.html.

Inlines everything (tokens, data, insights) into ONE file so it opens by double-click on file://
with no server and no network (no CDN). Pure presentation — reads, never writes budget data.
"""
import datetime
import json
import os
import re
import sys

from render_css import CAT_HUE, COMPONENT_CSS
from render_md import md2html
from render_tpl_a import PART as TEMPLATE_A
from render_tpl_b import PART as TEMPLATE_B

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = TEMPLATE_A + "\n" + TEMPLATE_B
STALE_NOTE = " — ANALYSIS OUT OF DATE: data.json is newer than insights.json, run analyze.py"
WARN = ("WARNING: data.json is newer than insights.json — run analyze.py before render.py, "
        "or the dashboard shows stale analysis\n")


def journal_entries(here):
    journal = []
    cfg_path = f"{here}/budget.config.json"
    cfg = {}
    if os.path.exists(cfg_path):
        with open(cfg_path) as handle:
            cfg = json.load(handle)
    path = os.path.expanduser(os.environ.get("WNAC_JOURNAL") or cfg.get("journal_path", "") or "")
    if path and os.path.exists(path):
        with open(path) as handle:
            parts = re.split(r'\n## (\d{4}-\d{2}-\d{2}) [—-] (.+)', handle.read())
        for k in range(1, len(parts) - 2, 3):
            journal.append({"date": parts[k], "title": parts[k + 1].strip(),
                            "html": md2html(parts[k + 2].strip())})
    return journal


def fill(bundle):
    stamp = bundle["stamp"] + (STALE_NOTE if bundle["stale"] else "")
    return (TEMPLATE
            .replace("/*TOKENS*/", bundle["tokens"])
            .replace("/*COMPONENT*/", COMPONENT_CSS)
            .replace("/*DATA*/", json.dumps(bundle["data"]))
            .replace("/*INS*/", json.dumps(bundle["ins"]))
            .replace("/*CATHUE*/", json.dumps(CAT_HUE))
            .replace("/*JOURNAL*/", json.dumps(bundle["journal"]))
            .replace("/*STAMP*/", stamp))


def page(here, now):
    data_path = f"{here}/data.json"
    ins_path = f"{here}/insights.json"
    with open(data_path) as handle:
        data = json.load(handle)
    with open(ins_path) as handle:
        ins = json.load(handle)
    with open(f"{here}/tokens.css") as handle:
        tokens = handle.read()
    bundle = {
        "data": data,
        "ins": ins,
        "tokens": tokens,
        "journal": journal_entries(here),
        "stamp": now.strftime("%b %d, %Y %H:%M"),
        "stale": os.path.getmtime(data_path) > os.path.getmtime(ins_path),
    }
    return fill(bundle), bundle["stale"]


def main(here=None, now=None):
    here = here or HERE
    now = now or datetime.datetime.now()
    html_out, stale = page(here, now)
    if stale:
        sys.stderr.write(WARN)
    with open(f"{here}/dashboard.html", "w") as handle:
        handle.write(html_out)
    sys.stdout.write(f"wrote dashboard.html ({len(html_out):,} bytes) — open it in a browser\n")


if __name__ == "__main__":
    main()
