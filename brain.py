# kit fail proof
"""WNAC brain (P1 = offline stub).

Contract (swap point for claude/hermes later):
    categorize_and_narrate(data) -> {"categories": {tx_id: {category, confidence, reasoning[, alternates]}}}

The stub is deterministic, needs no network/API key, and reasons by merchant keyword.
Confidence-gating is applied downstream in analyze.py (auto-apply only >= threshold).
"""
import re

RULES = [
    (r"starting balance",                          "Starting Balance", 0.99),
    (r"interest|late fee|finance charge",          "Fees",             0.90),
    (r"insurance",                                 "Insurance",        0.88),
    (r"payment|transfer|ach deposit|direct dep",   "Transfer",         0.88),
    (r"coffee|cafe|espresso",                      "Coffee",           0.85),
    (r"netflix|spotify|hulu|disney\+|streaming",   "Entertainment",    0.85),
    (r"airline|airways|flight|hotel|expedia|booking", "Travel",        0.85),
    (r"grocer|supermarket|\bmart\b|market",        "Groceries",        0.82),
    (r"pharmac|clinic|hospital|dental|medical|health", "Medical",      0.82),
    (r"restaurant|pizza|burger|sushi|ramen|diner|dining|eatery", "Dining", 0.75),
    (r"apparel|clothing|outfitter|shoes",          "Clothing",         0.72),
    (r"vpn|subscription|software|saas",            "Subscriptions",    0.72),
    (r"electronic|store|\bshop",                   "Shopping",         0.70),
]

def categorize_one(payee):
    p = (payee or "").lower()
    for rx, cat, conf in RULES:
        if re.search(rx, p):
            return {"category": cat, "confidence": conf, "reasoning": f"payee matches /{rx.split('|')[0]}/"}
    return {"category": None, "confidence": 0.0,
            "reasoning": "no rule matched — needs review", "alternates": ["Shopping", "Dining"]}

def categorize_and_narrate(data):
    return {"categories": {t["id"]: categorize_one(t["payee"]) for t in data["transactions"]}}
