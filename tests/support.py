"""Fake public fixtures for the dashboard. No real balances."""
import datetime
import html
import json
import os
import shutil
import subprocess
import tempfile

from render import page

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOW = datetime.datetime(2026, 1, 15, 12, 0, 0)
PROBE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe.js")
JOURNAL = "\n## 2026-01-04 — Sample note\n\n**Kept** the plan\n"


def sample_data():
    return {
        "accounts": [
            {"name": "Sample Checking", "balance_cents": 150000, "type": "cash"},
            {"name": "Sample Card", "balance_cents": -40000, "type": "credit"},
        ],
        "transactions": [
            {"id": "sb", "date": "2026-01-01", "payee": "Opening", "account": "Sample Checking",
             "amount_cents": 0, "starting_balance": True},
            {"id": "t1", "date": "2026-01-03", "payee": "Cafe 99", "account": "Sample Checking",
             "amount_cents": -450, "starting_balance": False},
            {"id": "t2", "date": "2026-02-03", "payee": "Cafe 99", "account": "Sample Checking",
             "amount_cents": -500, "starting_balance": False},
            {"id": "t3", "date": "2026-03-03", "payee": "Cafe 99", "account": "Sample Card",
             "amount_cents": -550, "starting_balance": False},
            {"id": "t4", "date": "2026-01-15", "payee": "<b>Odd</b>", "account": "Sample Checking",
             "amount_cents": -2000, "starting_balance": False},
            {"id": "t5", "date": "2026-01-20", "payee": "Grocery Mart", "account": "Sample Checking",
             "amount_cents": -8000, "starting_balance": False},
        ],
    }


def sample_ins():
    return {
        "display_month": "January 2026",
        "net_worth": {"assets_cents": 150000, "debts_cents": 40000, "net_cents": 110000},
        "budget": {"flex_cents": 10000, "spent_cents": 6000, "final_delta_cents": 4000, "status": "under"},
        "paydown": {"name": "Sample Card payoff", "current_cents": 40000, "progress": 0.25, "monthly_cents": 10000},
        "spending_by_category": [
            {"category": "Groceries", "cents": 8000},
            {"category": "Coffee", "cents": 1400},
            {"category": "Dining", "cents": 1200},
            {"category": "Shopping", "cents": 900},
            {"category": "Transport", "cents": 700},
            {"category": "Entertainment", "cents": 500},
            {"category": "Health", "cents": 400},
            {"category": "Fees", "cents": 300},
            {"category": "Uncategorized", "cents": 500},
        ],
        "monthly_line": {"points": [
            {"day": 1, "cum": 1000, "ideal": 3000},
            {"day": 2, "cum": 2000, "ideal": 4000},
            {"day": 3, "cum": 7000, "ideal": 4500},
            {"day": 4, "cum": 9000, "ideal": 2000},
            {"day": 5, "cum": 12000, "ideal": 3000},
            {"day": 6, "cum": 16000, "ideal": 4000},
        ]},
        "recent": [
            {"payee": "North Cafe", "amount_cents": -450, "category": "Coffee", "applied": True},
            {"payee": "Odd Payee", "amount_cents": -2000, "category": None, "applied": False},
            {"payee": "Sample Refund", "amount_cents": 2500, "category": "Shopping", "applied": True},
        ],
        "needs_review": 2,
        "narrative": "Sample narrative for the public test.",
        "categories": {
            "t1": {"category": "Coffee", "applied": True},
            "t2": {"category": "Coffee", "applied": True},
            "t3": {"category": "Coffee", "applied": True},
            "t4": {"category": None, "applied": False},
            "t5": {"category": "Groceries", "applied": True},
        },
    }


def write_case(dest, spec):
    os.makedirs(dest, exist_ok=True)
    _write(dest, "data.json", spec["data"])
    _write(dest, "insights.json", spec["ins"])
    shutil.copy(os.path.join(ROOT, "tokens.css"), os.path.join(dest, "tokens.css"))
    journal = spec.get("journal")
    if journal is not None:
        path = os.path.join(dest, "journal.md")
        with open(path, "w") as handle:
            handle.write(journal)
        cfg = dict(spec.get("config") or {})
        cfg["journal_path"] = path
        _write(dest, "budget.config.json", cfg)
    elif spec.get("config") is not None:
        _write(dest, "budget.config.json", spec["config"])
    _times(dest, bool(spec.get("stale")))
    return dest


def _write(dest, name, obj):
    with open(os.path.join(dest, name), "w") as handle:
        json.dump(obj, handle)


def _times(dest, stale):
    data_t = 2000 if stale else 1000
    ins_t = 1000 if stale else 2000
    os.utime(os.path.join(dest, "data.json"), (data_t, data_t))
    os.utime(os.path.join(dest, "insights.json"), (ins_t, ins_t))


def render_at(dest, spec):
    write_case(dest, spec)
    return page(dest, NOW)


def run_probe(page_html):
    dest = tempfile.mkdtemp(prefix="wnac-probe-")
    with open(PROBE) as handle:
        probe = handle.read()
    baked = page_html.replace("</body>", "<script>\n" + probe + "\n</script></body>", 1)
    path = os.path.join(dest, "page.html")
    with open(path, "w") as handle:
        handle.write(baked)
    cmd = ["/usr/bin/google-chrome-stable", "--headless=new", "--disable-gpu", "--no-sandbox",
           "--disable-dev-shm-usage", "--lang=en-US",
           "--user-data-dir=" + os.path.join(dest, "profile"),
           "--dump-dom", "file://" + path]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20, check=False)
        text, err = proc.stdout.decode(), proc.stderr.decode()
    except subprocess.TimeoutExpired as exc:
        text = (exc.stdout or b"").decode()
        err = (exc.stderr or b"").decode()
    start = text.find('<pre id="probe">')
    end = text.find("</pre>", start)
    if start < 0 or end < 0:
        raise RuntimeError(err[-1500:] + "\n" + text[-1500:])
    return json.loads(html.unescape(text[start + len('<pre id="probe">'):end]))
