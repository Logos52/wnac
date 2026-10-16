import os
import sys
"""WNAC render (P1): data.json + insights.json + tokens.css -> self-contained dashboard.html.

Inlines everything (tokens, data, insights) into ONE file so it opens by double-click on file://
with no server and no network (no CDN). Pure presentation — reads, never writes budget data.
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(f"{HERE}/data.json"))
ins  = json.load(open(f"{HERE}/insights.json"))
STALE = os.path.getmtime(f"{HERE}/data.json") > os.path.getmtime(f"{HERE}/insights.json")
if STALE:
    print("WARNING: data.json is newer than insights.json — run analyze.py before render.py, or the dashboard shows stale analysis", file=sys.stderr)
tokens = open(f"{HERE}/tokens.css").read()
stamp = datetime.datetime.now().strftime("%b %d, %Y %H:%M")

import re as _re, html as _html
def md2html(md):
    out, para, inlist = [], [], [False]
    def inline(s):
        s = _html.escape(s)
        s = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = _re.sub(r'`(.+?)`', r'<code>\1</code>', s)
        s = _re.sub(r'\[\[(.+?)\]\]', r'\1', s)
        return s
    def flush_p():
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para.clear()
    def flush_l():
        if inlist[0]: out.append("</ul>"); inlist[0] = False
    for ln in md.split("\n"):
        s = ln.rstrip()
        if not s.strip(): flush_p(); flush_l(); continue
        if s.startswith("### "): flush_p(); flush_l(); out.append("<h4>" + inline(s[4:]) + "</h4>")
        elif s.startswith("> "): flush_p(); flush_l(); out.append("<blockquote>" + inline(s[2:]) + "</blockquote>")
        elif s.strip() == "---": flush_p(); flush_l(); out.append("<hr>")
        elif s.lstrip()[:2] in ("- ", "* "):
            flush_p()
            if not inlist[0]: out.append("<ul>"); inlist[0] = True
            out.append("<li>" + inline(s.lstrip()[2:]) + "</li>")
        else: flush_l(); para.append(s.strip())
    flush_p(); flush_l()
    return "".join(out)

journal = []
_cfgp = f"{HERE}/budget.config.json"
_jcfg = json.load(open(_cfgp)) if os.path.exists(_cfgp) else {}
_jpath = os.path.expanduser(os.environ.get("WNAC_JOURNAL") or _jcfg.get("journal_path", "") or "")
if _jpath and os.path.exists(_jpath):
    _parts = _re.split(r'\n## (\d{4}-\d{2}-\d{2}) [—-] (.+)', open(_jpath).read())
    for _k in range(1, len(_parts) - 2, 3):
        journal.append({"date": _parts[_k], "title": _parts[_k + 1].strip(),
                        "html": md2html(_parts[_k + 2].strip())})

COMPONENT_CSS = """
*{box-sizing:border-box} html,body{margin:0}
body{background:var(--surface-base);color:var(--text-primary);font-family:var(--font);
  font-feature-settings:'tnum' 1;font-size:14px}
#app{display:flex;min-height:100vh}
.sidebar{width:240px;flex:0 0 240px;background:var(--surface-sidebar);padding:18px 14px;
  display:flex;flex-direction:column;gap:6px;border-right:1px solid var(--border-subtle)}
.logo{color:var(--accent-bright);font-weight:700;padding:6px 10px 14px;display:flex;gap:8px;align-items:center}
.search{background:var(--surface-card-alt);border:1px solid var(--border-subtle);border-radius:10px;
  color:var(--text-muted);padding:9px 12px;margin-bottom:8px;font-size:13px}
.nav{display:flex;flex-direction:column;gap:2px}
.nav a{color:var(--text-secondary);padding:9px 12px;border-radius:10px;text-decoration:none;font-weight:500}
.nav a.active{background:var(--accent);color:#fff;font-weight:600}
.grp{color:var(--text-secondary);font-size:12px;font-weight:600;margin:16px 6px 6px;text-transform:none}
.acct{display:flex;align-items:center;gap:8px;padding:7px 10px;color:var(--text-primary);font-size:13px}
.acct .dot{width:8px;height:8px;border-radius:50%}
.acct .bal{margin-left:auto;color:var(--text-secondary)}
.foot{margin-top:auto;display:flex;flex-direction:column;gap:2px}
.main{flex:1;padding:22px 26px;display:grid;grid-template-columns:1fr 1fr;gap:var(--gap-grid);align-content:start}
.topbar{grid-column:1/-1;display:flex;align-items:center;gap:14px;color:var(--text-secondary);margin-bottom:2px}
.topbar h1{font-size:18px;color:var(--text-primary);margin:0;font-weight:600}
.topbar .stamp{margin-left:auto;font-size:12px}
.card{background:var(--surface-card);border:1px solid var(--border-subtle);border-radius:var(--radius-card);
  padding:22px;box-shadow:var(--shadow-card);min-width:0}
.card.span{grid-column:1/-1}
.hero{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--gap-grid)}
.chead{display:flex;align-items:center;margin-bottom:14px}
.chead h2{font-size:15px;font-weight:600;margin:0}
.chead .link{margin-left:auto;color:var(--accent);font-size:13px;text-decoration:none}
.big{font-size:34px;font-weight:700;letter-spacing:-.5px}
.sub{color:var(--text-secondary);font-size:13px;margin-top:2px}
.badge{display:inline-flex;align-items:center;gap:4px;border-radius:999px;padding:3px 9px;font-size:12px;font-weight:600}
.row{display:flex;align-items:center;gap:10px;padding:9px 0;border-top:1px solid var(--border-subtle)}
.row:first-of-type{border-top:0}
.chip{display:inline-flex;align-items:center;gap:5px;border-radius:8px;padding:3px 8px;font-size:11px;
  font-weight:600;letter-spacing:.4px;text-transform:uppercase}
.amt{margin-left:auto;font-variant-numeric:tabular-nums}
.bar{height:8px;border-radius:999px;background:var(--bar-track);overflow:hidden;flex:1}
.bar>span{display:block;height:100%;border-radius:999px}
.muted{color:var(--text-muted)}.sec{color:var(--text-secondary)}
.dialwrap{display:flex;flex-direction:column;align-items:center;gap:6px}
.narr{font-size:14px;line-height:1.55;color:var(--text-primary)}
.pill{display:inline-block;background:var(--callout-green);color:#04210f;font-weight:700;
  border-radius:10px;padding:4px 10px;font-size:13px}
.view{display:contents}
.jbody{color:var(--text-secondary);line-height:1.65;font-size:14px}
.jbody h4{color:var(--text-primary);margin:14px 0 6px;font-size:14px}
.jbody strong{color:var(--text-primary)}
.jbody ul{margin:6px 0;padding-left:18px}.jbody li{margin:3px 0}
.jbody blockquote{border-left:2px solid var(--border-strong);margin:8px 0;padding:2px 0 2px 12px;color:var(--text-muted)}
.jbody hr{border:0;border-top:1px solid var(--border-subtle);margin:14px 0}
.jbody code{background:var(--surface-card-alt);padding:1px 5px;border-radius:5px;font-size:12px}
.jbody p{margin:8px 0}
"""

CAT_HUE = {
 "Dining":"--chip-orange-fg","Coffee":"--hue-orange","Groceries":"--pace-under",
 "Clothing":"--chip-magenta-fg","Shopping":"--accent-bright","Insurance":"--accent",
 "Entertainment":"--chip-purple-fg","Travel":"--debt-coral","Medical":"--chip-blue-fg",
 "Fees":"--pace-budget","Subscriptions":"--chip-blue-fg","Benefits":"--pace-under",
 "Health":"--chip-blue-fg","Cash":"--text-secondary","Transfer":"--text-muted","Transport":"--hue-orange",
}

TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WNAC</title><style>/*TOKENS*//*COMPONENT*/</style></head>
<body><div id="app"></div>
<script>
window.addEventListener('error',function(e){try{document.body.innerHTML='<pre style="color:#ff6b6b;background:#111;padding:24px;font:13px/1.6 ui-monospace,monospace;white-space:pre-wrap">WNAC error:\\n'+(e.message||'')+'\\n'+((e.error&&e.error.stack)||'')+'</pre>';}catch(_){}});
const DATA = /*DATA*/;
const INS = /*INS*/;
const CAT_HUE = /*CATHUE*/;
const JOURNAL = /*JOURNAL*/;
const CHIP={orange:['--chip-orange-bg','--chip-orange-fg'],green:['--chip-green-bg','--chip-green-fg'],magenta:['--chip-magenta-bg','--chip-magenta-fg'],blue:['--chip-blue-bg','--chip-blue-fg'],purple:['--chip-purple-bg','--chip-purple-fg'],red:['--chip-red-bg','--chip-red-fg'],muted:['--surface-card-alt','--text-muted']};
const CAT_STYLE={Dining:['orange','\\uD83C\\uDF54'],Coffee:['orange','\\u2615'],Groceries:['green','\\uD83E\\uDD51'],Clothing:['magenta','\\uD83D\\uDC55'],Shopping:['blue','\\uD83D\\uDECD'],Entertainment:['purple','\\uD83C\\uDFAE'],Subscriptions:['blue','\\uD83D\\uDCB3'],Travel:['orange','\\u2708'],Insurance:['blue','\\uD83D\\uDEE1'],Health:['blue','\\uD83D\\uDC8A'],Medical:['blue','\\uD83D\\uDC8A'],Transport:['orange','\\uD83D\\uDE95'],Fees:['red','\\uD83D\\uDCB8'],Transfer:['muted','\\uD83D\\uDD01'],Cash:['muted','\\uD83D\\uDCB5'],'Benefits':['green','\\uD83C\\uDF96']};
function catChip(cat){const st=CAT_STYLE[cat]||['muted','\\u2022'];const cc=CHIP[st[0]];
  const ch=el('span','chip',st[1]+' '+esc(cat));ch.style.background=cssv(cc[0]);ch.style.color=cssv(cc[1]);return ch;}
function catIcon(cat){return (CAT_STYLE[cat]||['','\\u2022'])[1];}
function catCol(cat){const st=CAT_STYLE[cat]||['muted'];return cssv(CHIP[st[0]][1]);}
const cssv = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const money = c => (c<0?'-':'')+'$'+Math.abs(Math.round(c/100)).toLocaleString();
const el = (t,c,h)=>{const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;};
const esc = s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
window.showView = function(n){
  document.querySelectorAll('.view').forEach(v=>{v.style.display='none';});
  var t=document.getElementById('view-'+n); if(t)t.style.display='';
  document.querySelectorAll('.nav a').forEach(a=>a.classList.toggle('active', a.getAttribute('data-view')===n));
};
const GREEN='#00BB36',AMBER='#ED8001',RED='#F3241A';
const h2r=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));
const r2h=a=>'#'+a.map(x=>Math.max(0,Math.min(255,Math.round(x))).toString(16).padStart(2,'0')).join('');
const mix=(a,b,t)=>{const x=h2r(a),y=h2r(b);return r2h(x.map((v,i)=>v+(y[i]-v)*t));};
function paceColor(over){ // over = (cum-ideal)/scale ; >0 over budget
  if(over<=0) return GREEN;
  if(over<=0.5) return mix(GREEN,AMBER,over/0.5);
  return mix(AMBER,RED,Math.min(1,(over-0.5)/0.5));
}
function card(title,link){const c=el('div','card');const hd=el('div','chead');
  hd.appendChild(el('h2',null,title)); if(link){const a=el('a','link',link+' \\u203a');a.href='#';hd.appendChild(a);} c.appendChild(hd); return c;}

/* ---------- sidebar ---------- */
function sidebar(){const s=el('div','sidebar');
  s.appendChild(el('div','logo','\\u27a4 WNAC'));
  s.appendChild(el('div','search','\\u26b2  Search'));
  const nav=el('div','nav');
  [['Dashboard','dashboard'],['Journal','journal'],['Transactions','transactions'],['Accounts','accounts'],['Categories','categories'],['Recurrings','recurrings']].forEach(([n,view])=>{
    const a=el('a',view==='dashboard'?'active':'',n);a.href='#';
    if(view){a.setAttribute('data-view',view);a.onclick=ev=>{ev.preventDefault();showView(view);};}
    nav.appendChild(a);});
  s.appendChild(nav);
  s.appendChild(el('div','grp','Accounts'));
  DATA.accounts.forEach(a=>{const r=el('div','acct');
    const dot=el('span','dot');dot.style.background = a.balance_cents<0?cssv('--debt-coral'):cssv('--accent-bright');
    r.appendChild(dot);r.appendChild(el('span',null,a.name));
    const b=el('span','bal',money(a.balance_cents));r.appendChild(b);s.appendChild(r);});
  const f=el('div','foot');['Explore','Get help','Settings'].forEach(n=>{const a=el('a','',n);a.href='#';a.style.color=cssv('--text-secondary');a.style.padding='8px 10px';a.style.textDecoration='none';f.appendChild(a);});
  s.appendChild(f); return s;}

/* ---------- ring/dial ---------- */
function ring(pct,color,label,sub){const sz=140,r=58,c=2*Math.PI*r;const off=c*(1-pct);
  const w=el('div','dialwrap');
  w.innerHTML=`<svg width="${sz}" height="${sz}" viewBox="0 0 ${sz} ${sz}">
    <circle cx="70" cy="70" r="${r}" fill="none" stroke="${cssv('--bar-track')}" stroke-width="12"/>
    <circle cx="70" cy="70" r="${r}" fill="none" stroke="${color}" stroke-width="12" stroke-linecap="round"
       stroke-dasharray="${c}" stroke-dashoffset="${off}" transform="rotate(-90 70 70)"/>
    <text x="70" y="66" text-anchor="middle" fill="${cssv('--text-primary')}" font-size="22" font-weight="700">${label}</text>
    <text x="70" y="88" text-anchor="middle" fill="${cssv('--text-secondary')}" font-size="12">${sub}</text></svg>`;
  return w;}

/* ---------- follow-the-line ---------- */
function followLine(){const c=card('Monthly spending','Transactions');
  const pts=INS.monthly_line.points; const W=560,H=200,pad=14;
  const maxV=Math.max(...pts.map(p=>Math.max(p.cum,p.ideal)),1);
  const X=i=>pad+(W-2*pad)*i/(pts.length-1); const Y=v=>H-pad-(H-2*pad)*v/maxV;
  // Copilot's exact rule (help.copilot.money/.../dashboard-line-colors):
  //   ideal = budget * day/daysInMonth (the dashed line) ; below it = under pace.
  //   green: spent<ideal ; red: spent>=budget ; else diff=(spent-ideal)/budget: <20pts light-orange, >=20pts dark-orange
  const budget=INS.budget.flex_cents||1;
  const LO=cssv('--pace-slight'), DO=cssv('--pace-over');
  const lineColor=(cum,ideal)=>{
    if(cum < ideal) return GREEN;                              // below the dashed line = under pace
    if(cum >= budget) return (cum/budget < 1.25) ? DO : RED;   // over budget: amber-orange until 25% over, then red (our softening of Copilot's hard red)
    return ((cum-ideal)/budget) < 0.20 ? LO : DO;              // over pace, under budget -> light/dark orange
  };
  let segs='';
  for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i];
    segs+=`<line x1="${X(i-1)}" y1="${Y(a.cum)}" x2="${X(i)}" y2="${Y(b.cum)}" stroke="${lineColor((a.cum+b.cum)/2,(a.ideal+b.ideal)/2)}" stroke-width="3.5" stroke-linecap="round"/>`;}
  const idl=`M ${X(0)} ${Y(pts[0].ideal)} L ${X(pts.length-1)} ${Y(pts[pts.length-1].ideal)}`;
  const last=pts[pts.length-1]; const endColor=lineColor(last.cum,last.ideal);
  const big=el('div');big.innerHTML=`<div class="big">${money(INS.budget.spent_cents)} spent</div>
    <div class="sub">vs ${money(INS.budget.flex_cents)} flex target \\u00b7 ${INS.display_month}</div>`;
  c.appendChild(big);
  const delta=INS.budget.final_delta_cents;
  const callout=`<div style="position:absolute;right:18px;top:6px"><span class="pill" style="background:${endColor};color:${delta>=0?'#04210f':'#2a0606'}">${money(Math.abs(delta))} ${INS.budget.status}</span></div>`;
  let fillD=`M ${X(0)} ${Y(pts[0].cum)}`;
  for(let i=1;i<pts.length;i++) fillD+=` L ${X(i)} ${Y(pts[i].cum)}`;
  fillD+=` L ${X(pts.length-1)} ${H-pad} L ${X(0)} ${H-pad} Z`;
  const svgwrap=el('div');svgwrap.style.position='relative';svgwrap.style.marginTop='8px';
  svgwrap.innerHTML=callout+`<svg viewBox="0 0 ${W} ${H}" width="100%" preserveAspectRatio="none" style="display:block">
    <defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${endColor}" stop-opacity=".16"/><stop offset="1" stop-color="${endColor}" stop-opacity="0"/></linearGradient></defs>
    <path d="${fillD}" fill="url(#lg)"/>
    <path d="${idl}" stroke="${cssv('--border-strong')}" stroke-width="1.5" stroke-dasharray="5 6" fill="none" opacity=".8"/>
    ${segs}
    <circle cx="${X(pts.length-1)}" cy="${Y(last.cum)}" r="6" fill="${cssv('--surface-card')}" stroke="${endColor}" stroke-width="3"/></svg>`;
  c.appendChild(svgwrap); return c;}

/* ---------- top categories ---------- */
function categories(){const c=card('Top categories','Categories');
  const list=INS.spending_by_category.filter(x=>x.category!=='Uncategorized');
  const max=Math.max(...list.map(x=>x.cents),1);
  list.slice(0,7).forEach(x=>{const r=el('div','row');
    const hue=catCol(x.category);
    const ic=el('span',null,catIcon(x.category));ic.style.cssText='width:22px;text-align:center;font-size:15px';
    r.appendChild(ic);r.appendChild(el('span',null,x.category));
    const amt=el('span','amt sec',money(x.cents));amt.style.minWidth='64px';amt.style.textAlign='right';
    const bar=el('div','bar');const sp=el('span');sp.style.width=(100*x.cents/max)+'%';sp.style.background=hue;bar.appendChild(sp);
    r.appendChild(bar);r.appendChild(amt);c.appendChild(r);});
  const unc=INS.spending_by_category.find(x=>x.category==='Uncategorized');
  if(unc){const r=el('div','row');r.style.marginTop='4px';
    r.innerHTML=`<span class="muted">\\u26a0 ${money(unc.cents)} uncategorized</span><span class="amt"><span class="badge" style="background:var(--chip-blue-bg);color:var(--chip-blue-fg)">${INS.needs_review} to review</span></span>`;
    c.appendChild(r);} return c;}

/* ---------- recent ---------- */
function recent(){const c=card('Transactions to review','View all');
  INS.recent.forEach(t=>{const r=el('div','row');
    const av=el('span',null,(t.payee||'?').slice(0,1).toUpperCase());
    av.style.cssText=`width:30px;height:30px;border-radius:50%;background:var(--surface-card-alt);display:flex;align-items:center;justify-content:center;font-weight:600;color:var(--text-secondary);font-size:13px`;
    r.appendChild(av);
    const nm=el('span',null,t.payee);nm.style.overflow='hidden';nm.style.textOverflow='ellipsis';nm.style.whiteSpace='nowrap';nm.style.maxWidth='140px';r.appendChild(nm);
    if(t.category && t.applied){r.appendChild(catChip(t.category));}
    else {const ch=el('span','chip','review');ch.style.color=cssv('--text-muted');ch.style.background=cssv('--surface-card-alt');r.appendChild(ch);}
    const a=el('span','amt',money(t.amount_cents));if(t.amount_cents>0)a.style.color=cssv('--pace-under');r.appendChild(a);
    c.appendChild(r);}); return c;}

/* ---------- hero ---------- */
function hero(){const h=el('div','hero');
  // net worth
  const nw=card('Net worth','Accounts');const n=INS.net_worth;
  nw.appendChild(el('div','big',money(n.net_cents)));
  const sb=el('div','sub');sb.innerHTML=`<span style="color:${cssv('--accent-bright')}">\\u25cf Assets ${money(n.assets_cents)}</span> &nbsp; <span style="color:${cssv('--debt-coral')}">\\u25cf Debts ${money(n.debts_cents)}</span>`;
  nw.appendChild(sb);
  const lines=el('div');lines.style.marginTop='18px';
  lines.innerHTML=`<svg viewBox="0 0 300 60" width="100%"><line x1="6" y1="20" x2="280" y2="20" stroke="${cssv('--accent-bright')}" stroke-width="3"/><circle cx="288" cy="20" r="6" fill="none" stroke="${cssv('--accent-bright')}" stroke-width="3"/><line x1="6" y1="44" x2="200" y2="44" stroke="${cssv('--debt-coral')}" stroke-width="3"/><circle cx="208" cy="44" r="6" fill="none" stroke="${cssv('--debt-coral')}" stroke-width="3"/></svg>`;
  nw.appendChild(lines);h.appendChild(nw);
  // flex
  const fx=card('Flex this month',null);const b=INS.budget;
  const over=b.spent_cents>b.flex_cents; const fcolor=over?cssv('--pace-budget'):cssv('--pace-under');
  fx.appendChild(el('div','big',money(b.flex_cents)));
  fx.appendChild(el('div','sub','flex budget \\u00b7 one number'));
  const meter=el('div');meter.style.marginTop='16px';
  const pct=Math.min(100,100*b.spent_cents/b.flex_cents);
  meter.innerHTML=`<div class="bar" style="height:10px"><span style="width:${pct}%;background:${fcolor}"></span></div>
    <div class="sub" style="margin-top:8px">${money(b.spent_cents)} spent \\u00b7 <span style="color:${fcolor}">${money(Math.abs(b.final_delta_cents))} ${b.status}</span></div>`;
  fx.appendChild(meter);h.appendChild(fx);
  // paydown dial
  const pd=card('Debt pay-down',null);const p=INS.paydown;
  const months=p.monthly_cents?Math.ceil(p.current_cents/p.monthly_cents):null;
  pd.appendChild(ring(p.progress, cssv('--debt-coral'), Math.round(p.progress*100)+'%', money(p.current_cents)+' left'));
  pd.appendChild(el('div','sub',(p.name)+(months?` \\u00b7 ~${months} mo at ${money(p.monthly_cents)}/mo`:'')));
  pd.lastChild.style.textAlign='center';pd.lastChild.style.marginTop='8px';
  h.appendChild(pd); return h;}

/* ---------- insight ---------- */
function insight(){const c=el('div','card');
  const hd=el('div','chead');hd.appendChild(el('h2',null,'Your money, today'));
  const lk=el('a','link','Open journal &rsaquo;');lk.href='#';lk.onclick=ev=>{ev.preventDefault();showView('journal');};hd.appendChild(lk);
  c.appendChild(hd);
  c.appendChild(el('div','narr',INS.narrative));
  const chips=el('div');chips.style.marginTop='14px';chips.style.display='flex';chips.style.gap='8px';chips.style.flexWrap='wrap';
  [['AI blend','--accent-bright'],[`${INS.needs_review} to review`,'--chip-blue-fg'],[INS.budget.status==='under'?'on track':'over flex',INS.budget.status==='under'?'--pace-under':'--pace-budget']].forEach(([t,col])=>{
    const ch=el('span','chip',t);ch.style.color=cssv(col);ch.style.background=cssv('--surface-card-alt');chips.appendChild(ch);});
  c.appendChild(chips);return c;}

/* ---------- mount ---------- */
function topbarEl(t,sub){const e=el('div','topbar');e.innerHTML='<h1>'+esc(t)+'</h1>'+(sub?'<span class="stamp">'+esc(sub)+'</span>':'');return e;}
function avatarEl(p){const av=el('span',null,(p||'?').slice(0,1).toUpperCase());av.style.cssText='width:30px;height:30px;border-radius:50%;background:var(--surface-card-alt);display:flex;align-items:center;justify-content:center;font-weight:600;color:var(--text-secondary);font-size:13px;flex:0 0 30px';return av;}
function txView(){const v=el('div','view');v.id='view-transactions';v.style.display='none';
  const rows=DATA.transactions.filter(t=>!t.starting_balance);
  v.appendChild(topbarEl('Transactions',rows.length+' transactions'));
  const c=el('div','card span');
  rows.forEach(t=>{const cat=INS.categories[t.id];const r=el('div','row');
    r.appendChild(avatarEl(t.payee));
    const nm=el('span',null,esc(t.payee));nm.style.cssText='flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap';r.appendChild(nm);
    const ac=el('span','sec',esc(t.account||''));ac.style.cssText='font-size:12px;width:120px;flex:0 0 120px';r.appendChild(ac);
    if(cat&&cat.applied){r.appendChild(catChip(cat.category));}
    const dt=el('span','sec',t.date);dt.style.cssText='font-size:12px;width:92px;flex:0 0 92px;text-align:right';r.appendChild(dt);
    const a=el('span','amt',money(t.amount_cents));a.style.cssText='width:96px;flex:0 0 96px;text-align:right';if(t.amount_cents>0)a.style.color=cssv('--pace-under');r.appendChild(a);
    c.appendChild(r);});
  v.appendChild(c);return v;}
function acctView(){const v=el('div','view');v.id='view-accounts';v.style.display='none';
  v.appendChild(topbarEl('Accounts','net worth '+money(INS.net_worth.net_cents)));
  const c=el('div','card span');
  DATA.accounts.forEach(a=>{const r=el('div','row');
    const dot=el('span',null,'');dot.style.cssText='width:10px;height:10px;border-radius:50%;flex:0 0 10px;background:'+(a.balance_cents<0?cssv('--debt-coral'):cssv('--accent-bright'));r.appendChild(dot);
    const nm=el('span',null,esc(a.name));nm.style.flex='1';r.appendChild(nm);
    const ty=el('span','sec',esc(a.type));ty.style.cssText='width:90px;flex:0 0 90px;font-size:12px';r.appendChild(ty);
    const b=el('span','amt',money(a.balance_cents));if(a.balance_cents<0)b.style.color=cssv('--debt-coral');r.appendChild(b);
    c.appendChild(r);});
  v.appendChild(c);return v;}
function catView(){const v=el('div','view');v.id='view-categories';v.style.display='none';
  v.appendChild(topbarEl('Categories',INS.display_month+' spending'));
  const c=el('div','card span');const list=INS.spending_by_category.filter(x=>x.category!=='Uncategorized');
  const max=Math.max(...list.map(x=>x.cents),1);
  list.forEach(x=>{const r=el('div','row');const hue=catCol(x.category);
    const ic=el('span',null,catIcon(x.category));ic.style.cssText='width:22px;text-align:center;font-size:15px';r.appendChild(ic);
    const nm=el('span',null,esc(x.category));nm.style.cssText='flex:0 0 140px';r.appendChild(nm);
    const bar=el('div','bar');const sp=el('span');sp.style.width=(100*x.cents/max)+'%';sp.style.background=hue;bar.appendChild(sp);r.appendChild(bar);
    const a=el('span','amt sec',money(x.cents));a.style.cssText='width:82px;flex:0 0 82px;text-align:right';r.appendChild(a);
    c.appendChild(r);});
  v.appendChild(c);return v;}
function recurView(){const v=el('div','view');v.id='view-recurrings';v.style.display='none';
  v.appendChild(topbarEl('Recurrings','payees that repeat 3+ months'));
  const g={};
  DATA.transactions.forEach(t=>{if(t.starting_balance)return;const k=(t.payee||'').toLowerCase().replace(/[0-9]+/g,'').trim();
    if(!g[k])g[k]={payee:t.payee,months:new Set(),sum:0,n:0,id:t.id};g[k].months.add(t.date.slice(0,7));g[k].sum+=t.amount_cents;g[k].n++;});
  const rec=Object.values(g).filter(x=>x.months.size>=3).sort((a,b)=>Math.abs(b.sum/b.n)-Math.abs(a.sum/a.n));
  const c=el('div','card span');
  rec.forEach(x=>{const cat=INS.categories[x.id];const r=el('div','row');r.appendChild(avatarEl(x.payee));
    const nm=el('span',null,esc(x.payee));nm.style.cssText='flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap';r.appendChild(nm);
    if(cat&&cat.applied){r.appendChild(catChip(cat.category));}
    const m=el('span','sec',x.months.size+' mo');m.style.cssText='width:62px;flex:0 0 62px;text-align:right;font-size:12px';r.appendChild(m);
    const a=el('span','amt',money(Math.round(x.sum/x.n)));a.style.cssText='width:96px;flex:0 0 96px;text-align:right';r.appendChild(a);
    c.appendChild(r);});
  if(!rec.length){c.innerHTML='<div class="narr sec">No recurring payees detected.</div>';}
  v.appendChild(c);return v;}
function journalView(){
  const v=el('div','view');v.id='view-journal';v.style.display='none';
  const top=el('div','topbar');top.innerHTML='<h1>Journal</h1><span class="stamp">your money decisions over time</span>';v.appendChild(top);
  const nc=el('div','card span');nc.innerHTML='<div class="chead"><h2>Your money, today</h2></div><div class="narr">'+esc(INS.narrative)+'</div>';v.appendChild(nc);
  if(JOURNAL.length){JOURNAL.forEach(e=>{const c=el('div','card span');
    c.innerHTML='<div class="chead"><h2>'+esc(e.title)+'</h2><span class="link" style="cursor:default;pointer-events:none">'+esc(e.date)+'</span></div><div class="jbody">'+e.html+'</div>';
    v.appendChild(c);});}
  else{const c=el('div','card span');c.innerHTML='<div class="narr sec">No journal entries yet \\u2014 add dated notes to budget-journal.md.</div>';v.appendChild(c);}
  return v;}
const app=document.getElementById('app');
try{
  app.appendChild(sidebar());
  const main=el('div','main');
  const dash=el('div','view');dash.id='view-dashboard';
  const top=el('div','topbar');top.innerHTML=`<h1>Dashboard</h1><span class="stamp">updated /*STAMP*/</span>`;
  dash.appendChild(top);
  dash.appendChild(hero());
  dash.appendChild(followLine());
  dash.appendChild(insight());
  dash.appendChild(categories());
  dash.appendChild(recent());
  main.appendChild(dash);
  main.appendChild(journalView());
  main.appendChild(txView());
  main.appendChild(acctView());
  main.appendChild(catView());
  main.appendChild(recurView());
  app.appendChild(main);
}catch(e){
  document.body.innerHTML='<pre style="color:#ff6b6b;background:#111;padding:24px;font:13px/1.6 ui-monospace,monospace;white-space:pre-wrap">WNAC mount error:\\n'+(e&&e.stack||e)+'</pre>';
}
</script></body></html>"""

html = (TEMPLATE
        .replace("/*TOKENS*/", tokens)
        .replace("/*COMPONENT*/", COMPONENT_CSS)
        .replace("/*DATA*/", json.dumps(data))
        .replace("/*INS*/", json.dumps(ins))
        .replace("/*CATHUE*/", json.dumps(CAT_HUE))
        .replace("/*JOURNAL*/", json.dumps(journal))
        .replace("/*STAMP*/", stamp + (" — ANALYSIS OUT OF DATE: data.json is newer than insights.json, run analyze.py" if STALE else "")))
open(f"{HERE}/dashboard.html", "w").write(html)
print(f"wrote dashboard.html ({len(html):,} bytes) — open it in a browser")
