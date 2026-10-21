#!/usr/bin/env python3
"""WNAC import (P1) — export the wnab/Actual engine -> data.json.

P1 reads the existing wnab budget DB directly (wnab = the headless data engine behind WNAC).
Declarative CSV/QFX adapters are the next import mode (see PRD §7.1). Deterministic: no AI here.
"""
import sqlite3, json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
_cfg_path = os.path.join(HERE, "budget.config.json")
_cfg = json.load(open(_cfg_path)) if os.path.exists(_cfg_path) else {}
DB = os.path.expanduser(os.environ.get("WNAC_DB") or _cfg.get("db_path", ""))
if not DB or not os.path.exists(DB):
    sys.exit('WNAC import: set your data-engine DB path via $WNAC_DB or '
             'budget.config.json:"db_path" (see budget.config.example.json). '
             'No path is committed — your finances stay local.')
OUT = os.path.join(HERE, "data.json")

def d2iso(d):
    d = int(d); return f"{d//10000:04d}-{(d//100)%100:02d}-{d%100:02d}"

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True); cur = con.cursor()

accounts, name_of = [], {}
for aid, name, off, typ, bal in cur.execute("""
        SELECT id, name, offbudget, type,
               (SELECT COALESCE(SUM(amount),0) FROM transactions
                WHERE acct = accounts.id AND tombstone = 0)
        FROM accounts WHERE tombstone = 0 ORDER BY sort_order"""):
    accounts.append({"id": aid, "name": name, "type": typ or "other",
                     "offbudget": bool(off), "balance_cents": bal})
    name_of[aid] = name

txns = []
for tid, acct, date, amt, sbf, payee in cur.execute("""
        SELECT t.id, t.acct, t.date, t.amount, t.starting_balance_flag,
               (SELECT name FROM payees WHERE id = pm.targetId)
        FROM transactions t LEFT JOIN payee_mapping pm ON pm.id = t.description
        WHERE t.tombstone=0 AND t.date IS NOT NULL
        ORDER BY t.date DESC, t.sort_order DESC"""):
    txns.append({"id": tid, "account_id": acct, "account": name_of.get(acct),
                 "date": d2iso(date), "payee": payee or "—",
                 "amount_cents": amt, "starting_balance": bool(sbf)})

data = {"schema_version": 1,
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "currency": "USD", "accounts": accounts, "transactions": txns}
json.dump(data, open(OUT, "w"), indent=1)
con.close()

sys.stdout.write(f"wrote {OUT}: {len(accounts)} accounts, {len(txns)} transactions\n")
for a in accounts:
    sys.stdout.write(f"  {a['name']:18} ${a['balance_cents']/100:>10,.2f}\n")
