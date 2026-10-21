"""Dashboard markup, second half. Concatenate with render_tpl_a.PART."""
PART = """    else {const ch=el('span','chip','review');ch.style.color=cssv('--text-muted');ch.style.background=cssv('--surface-card-alt');r.appendChild(ch);}
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
