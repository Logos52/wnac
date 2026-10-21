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
data = json.load(open(f"{HERE}/data.json"))
ins = json.load(open(f"{HERE}/insights.json"))
STALE = os.path.getmtime(f"{HERE}/data.json") > os.path.getmtime(f"{HERE}/insights.json")
if STALE:
    sys.stderr.write("WARNING: data.json is newer than insights.json — run analyze.py before render.py, or the dashboard shows stale analysis\n")
tokens = open(f"{HERE}/tokens.css").read()
stamp = datetime.datetime.now().strftime("%b %d, %Y %H:%M")
TEMPLATE = TEMPLATE_A + "\n" + TEMPLATE_B

journal = []
_cfgp = f"{HERE}/budget.config.json"
_jcfg = json.load(open(_cfgp)) if os.path.exists(_cfgp) else {}
_jpath = os.path.expanduser(os.environ.get("WNAC_JOURNAL") or _jcfg.get("journal_path", "") or "")
if _jpath and os.path.exists(_jpath):
    _parts = re.split(r'\n## (\d{4}-\d{2}-\d{2}) [—-] (.+)', open(_jpath).read())
    for _k in range(1, len(_parts) - 2, 3):
        journal.append({"date": _parts[_k], "title": _parts[_k + 1].strip(),
                        "html": md2html(_parts[_k + 2].strip())})

html_out = (TEMPLATE
        .replace("/*TOKENS*/", tokens)
        .replace("/*COMPONENT*/", COMPONENT_CSS)
        .replace("/*DATA*/", json.dumps(data))
        .replace("/*INS*/", json.dumps(ins))
        .replace("/*CATHUE*/", json.dumps(CAT_HUE))
        .replace("/*JOURNAL*/", json.dumps(journal))
        .replace("/*STAMP*/", stamp + (" — ANALYSIS OUT OF DATE: data.json is newer than insights.json, run analyze.py" if STALE else "")))
open(f"{HERE}/dashboard.html", "w").write(html_out)
sys.stdout.write(f"wrote dashboard.html ({len(html_out):,} bytes) — open it in a browser\n")
