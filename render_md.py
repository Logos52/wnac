"""Markdown subset used by the journal view. Output matches the previous renderer."""
import html
import re

def inline(s):
    s = html.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    s = re.sub(r'\[\[(.+?)\]\]', r'\1', s)
    return s

def flush_p(out, para):
    if para:
        out.append("<p>" + inline(" ".join(para)) + "</p>")
        para.clear()

def flush_l(out, inlist):
    if inlist[0]:
        out.append("</ul>")
        inlist[0] = False

def heading(out, para, inlist, s):
    flush_p(out, para)
    flush_l(out, inlist)
    out.append("<h4>" + inline(s[4:]) + "</h4>")

def quote(out, para, inlist, s):
    flush_p(out, para)
    flush_l(out, inlist)
    out.append("<blockquote>" + inline(s[2:]) + "</blockquote>")

def rule(out, para, inlist, _s):
    flush_p(out, para)
    flush_l(out, inlist)
    out.append("<hr>")

def open_list(out, inlist):
    if inlist[0]:
        return
    out.append("<ul>")
    inlist[0] = True

def item(out, para, inlist, s):
    flush_p(out, para)
    open_list(out, inlist)
    out.append("<li>" + inline(s.lstrip()[2:]) + "</li>")

def text(out, para, inlist, s):
    flush_l(out, inlist)
    para.append(s.strip())

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

def apply_line(out, para, inlist, s):
    HANDLERS[kind_of(s)](out, para, inlist, s)

def blank(out, para, inlist):
    flush_p(out, para)
    flush_l(out, inlist)

def dispatch(out, para, inlist, s):
    if s.strip():
        apply_line(out, para, inlist, s)
    else:
        blank(out, para, inlist)

def on_line(out, para, inlist, ln):
    dispatch(out, para, inlist, ln.rstrip())

def finish(out, para, inlist):
    flush_p(out, para)
    flush_l(out, inlist)
    return "".join(out)

def md2html(md):
    out, para, inlist = [], [], [False]
    for ln in md.split("\n"):
        on_line(out, para, inlist, ln)
    return finish(out, para, inlist)
