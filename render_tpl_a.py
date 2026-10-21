"""Dashboard markup, first half. Concatenate with render_tpl_b.PART."""
PART = """<!doctype html><html lang="en"><head><meta charset="utf-8">
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
    if(t.category && t.applied){r.appendChild(catChip(t.category));}"""
