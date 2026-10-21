"""Markdown subset used by the journal view. Output matches the previous renderer."""
import html
import re

def inline(s):
    s = html.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    s = re.sub(r'\[\[(.+?)\]\]', r'\1', s)
    return s

def flush_p(state):
    para = state["para"]
    if para:
        state["out"].append("<p>" + inline(" ".join(para)) + "</p>")
        para.clear()

def flush_l(state):
    if state["inlist"][0]:
        state["out"].append("</ul>")
        state["inlist"][0] = False

def heading(state, s):
    flush_p(state)
    flush_l(state)
    state["out"].append("<h4>" + inline(s[4:]) + "</h4>")

def quote(state, s):
    flush_p(state)
    flush_l(state)
    state["out"].append("<blockquote>" + inline(s[2:]) + "</blockquote>")

def rule(state, _s):
    flush_p(state)
    flush_l(state)
    state["out"].append("<hr>")

def open_list(state):
    if state["inlist"][0]:
        return
    state["out"].append("<ul>")
    state["inlist"][0] = True

def item(state, s):
    flush_p(state)
    open_list(state)
    state["out"].append("<li>" + inline(s.lstrip()[2:]) + "</li>")

def text(state, s):
    flush_l(state)
    state["para"].append(s.strip())

def kind_of(s):
    if s.startswith("### "):
        return "h"
    if s.startswith("> "):
        return "q"
    if s.strip() == "---":
        return "r"
    if s.lstrip()[:2] in ("- ", "* "):
        return "i"
    return "t"

HANDLERS = {"h": heading, "q": quote, "r": rule, "i": item, "t": text}

def apply_line(state, s):
    HANDLERS[kind_of(s)](state, s)

def blank(state):
    flush_p(state)
    flush_l(state)

def dispatch(state, s):
    if s.strip():
        apply_line(state, s)
    else:
        blank(state)

def on_line(state, ln):
    dispatch(state, ln.rstrip())

def finish(state):
    flush_p(state)
    flush_l(state)
    return "".join(state["out"])

def md2html(md):
    state = {"out": [], "para": [], "inlist": [False]}
    for ln in md.split("\n"):
        on_line(state, ln)
    return finish(state)
