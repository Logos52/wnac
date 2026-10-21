"""Dashboard component CSS and category hues. Values are unchanged."""
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
