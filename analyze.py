#!/usr/bin/env python3
"""WNAC analyze (P1): data.json + budget.config.json + brain -> insights.json.

The only nondeterministic stage. P1 uses the offline stub brain (no API key).
Computes: net worth, the flex number, the pay-down goal, spending-by-category,
the follow-the-line series (cumulative spend vs ideal pace), recent txns, narrative.
"""
import json, os, calendar
from collections import defaultdict
import brain

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(f"{HERE}/data.json"))
cfg = json.load(open(f"{HERE}/budget.config.json"))
THRESH = cfg.get("high_confidence_threshold", 0.8)

cats = brain.categorize_and_narrate(data)["categories"]
for c in cats.values():
    c["applied"] = bool(c["category"]) and c["confidence"] >= THRESH

# AI-blend: apply Claude's reasoned merchant overrides (overrides.json, gitignored/private).
# Substring rules win over the stub and auto-apply at full confidence.
ovp = f"{HERE}/overrides.json"
if os.path.exists(ovp):
    rules = json.load(open(ovp)).get("rules", [])
    for t in data["transactions"]:
        p = (t["payee"] or "").lower()
        for r in rules:
            if r["match"] in p:
                cats[t["id"]] = {"category": r["category"], "confidence": 1.0,
                                 "applied": True, "reasoning": "AI override: " + r["match"]}
                break

NON_SPEND = set(cfg.get("non_spend_categories", ["Transfer", "Starting Balance", "Income", "Benefits"]))
cat_of = lambda t: cats[t["id"]]["category"]
is_spend = lambda t: t["amount_cents"] < 0 and cat_of(t) not in NON_SPEND

# pick the display month = latest month with real spending (fall back if sparse)
month_spend, month_cnt = defaultdict(int), defaultdict(int)
for t in data["transactions"]:
    if is_spend(t):
        m = t["date"][:7]; month_spend[m] += -t["amount_cents"]; month_cnt[m] += 1
months = sorted(month_spend)
disp = months[-1] if months else None
if disp and month_cnt[disp] < 5 and len(months) > 1:
    disp = months[-2]

# net worth
assets = sum(a["balance_cents"] for a in data["accounts"] if a["balance_cents"] > 0)
debts  = sum(-a["balance_cents"] for a in data["accounts"] if a["balance_cents"] < 0)

# budget / flex number
income = round(cfg["income_monthly"] * 100)
fixed_total = round(sum(cfg["fixed_costs"].values()) * 100)
goal_total = round(sum(g.get("monthly", 0) for g in cfg.get("goals", [])) * 100)
flex = income - fixed_total - goal_total
spent = month_spend.get(disp, 0)

# pay-down goal
paydown = None
for g in cfg.get("goals", []):
    if g.get("type") == "paydown":
        acct = next((a for a in data["accounts"] if a["name"] == g["account"]), None)
        cur = -acct["balance_cents"] if acct else 0           # owed, positive cents
        start = round(g["start_balance"] * 100)
        paydown = {"name": g["name"], "start_cents": start, "current_cents": cur,
                   "progress": max(0, min(1, (start - cur) / start)) if start else 0,
                   "monthly_cents": round(g.get("monthly", 0) * 100)}

# spending by category (display month)
bycat = defaultdict(int)
for t in data["transactions"]:
    if is_spend(t) and t["date"][:7] == disp:
        bycat[cat_of(t) or "Uncategorized"] += -t["amount_cents"]
spending_by_category = sorted(({"category": k, "cents": v} for k, v in bycat.items()),
                              key=lambda x: -x["cents"])

# follow-the-line: cumulative spend vs ideal(flex) across the display month
points, final_delta = [], 0
if disp:
    yr, mo = int(disp[:4]), int(disp[5:7]); dim = calendar.monthrange(yr, mo)[1]
    daily = defaultdict(int)
    for t in data["transactions"]:
        if is_spend(t) and t["date"][:7] == disp:
            daily[int(t["date"][8:10])] += -t["amount_cents"]
    cum = 0
    for day in range(1, dim + 1):
        cum += daily.get(day, 0)
        points.append({"day": day, "cum": cum, "ideal": round(flex * day / dim)})
    final_delta = points[-1]["ideal"] - points[-1]["cum"]     # >0 under, <0 over

# recent (exclude starting balances)
recent = [{"date": t["date"], "payee": t["payee"], "account": t["account"],
           "amount_cents": t["amount_cents"], "category": cat_of(t),
           "applied": cats[t["id"]]["applied"]}
          for t in data["transactions"] if not t["starting_balance"]][:8]
reviewable = [t for t in data["transactions"] if not t["starting_balance"]]
needs_review = sum(1 for t in reviewable if not cats[t["id"]]["applied"])

# narrative (stub, data-driven — the manual insight loop, automated)
status = "under" if final_delta >= 0 else "over"
mname = (calendar.month_name[int(disp[5:7])] + " " + disp[:4]) if disp else "this month"
top = spending_by_category[0]["category"] if spending_by_category else "—"
pd_name = paydown["name"] if paydown else "debt account"
narrative = (f"Net worth is ${(assets-debts)/100:,.0f} — ${assets/100:,.0f} cash vs "
             f"${debts/100:,.0f} card debt. In {mname} you spent ${spent/100:,.0f} against a "
             f"${flex/100:,.0f} flex target, finishing ${abs(final_delta)/100:,.0f} {status}. "
             f"Biggest category: {top}. The {pd_name} "
             f"(${(paydown['current_cents'] if paydown else 0)/100:,.0f}) is the pay-down goal — "
             f"every flex dollar you skip goes at it.")

out = {"schema_version": 1, "display_month": disp,
       "net_worth": {"assets_cents": assets, "debts_cents": debts, "net_cents": assets - debts},
       "budget": {"income_cents": income, "fixed_cents": fixed_total, "goal_cents": goal_total,
                  "flex_cents": flex, "spent_cents": spent,
                  "final_delta_cents": final_delta, "status": status},
       "paydown": paydown, "spending_by_category": spending_by_category,
       "monthly_line": {"points": points}, "recent": recent,
       "needs_review": needs_review, "narrative": narrative, "categories": cats}
json.dump(out, open(f"{HERE}/insights.json", "w"), indent=1)

tops = ", ".join(f"{c['category']}:${c['cents']/100:,.0f}" for c in spending_by_category[:6])
print(f"display_month={disp}  net=${(assets-debts)/100:,.2f}  flex=${flex/100:,.2f}  "
      f"spent=${spent/100:,.2f}  ({status} ${abs(final_delta)/100:,.2f})")
print("top categories:", tops)
print(f"needs_review={needs_review}/{len(reviewable)}   paydown={paydown}")
