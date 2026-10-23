(function () {
  const pre = document.createElement("pre");
  pre.id = "probe";
  let payload;
  try {
    payload = collect();
  } catch (e) {
    payload = {error: String(e && e.stack || e)};
  }
  pre.textContent = JSON.stringify(payload);
  document.body.appendChild(pre);

  function findCard(title) {
    const cards = document.querySelectorAll(".card");
    for (let i = 0; i < cards.length; i++) {
      const h = cards[i].querySelector("h2");
      if (h && h.textContent === title) return cards[i];
    }
    return null;
  }

  function rowsOf(root) {
    const rows = [];
    if (!root) return rows;
    root.querySelectorAll(".row").forEach(r => rows.push(r.innerText));
    return rows;
  }

  function collect() {
    const pace = (typeof paceColor === "function") ? {
      z: paceColor(0), n: paceColor(-1), m: paceColor(0.5), h: paceColor(1)
    } : null;
    const moneyOut = (typeof money === "function") ? {
      pos: money(150000), neg: money(-40000), zero: money(0)
    } : null;
    const bodyText = document.body.innerText || "";
    if (bodyText.indexOf("WNAC mount error") !== -1) {
      return {mountError: true, pace: pace, money: moneyOut};
    }
    const views = {};
    document.querySelectorAll(".view").forEach(v => { views[v.id] = v.style.display; });
    let navActive = "";
    document.querySelectorAll(".nav a").forEach(a => {
      if (a.classList.contains("active")) navActive = a.getAttribute("data-view");
    });
    const accounts = [];
    document.querySelectorAll(".sidebar .acct").forEach(r => {
      const dot = r.querySelector(".dot");
      accounts.push({
        name: r.children[1].textContent,
        bal: r.querySelector(".bal").textContent,
        dot: dot.style.backgroundColor || dot.style.background
      });
    });
    const hero = [];
    document.querySelectorAll("#view-dashboard .hero .card").forEach(c => hero.push(c.innerText));
    const spend = findCard("Monthly spending");
    const strokes = [];
    spend.querySelectorAll("line").forEach(l => strokes.push(l.getAttribute("stroke")));
    const recent = [];
    findCard("Transactions to review").querySelectorAll(".row").forEach(r => {
      const amt = r.querySelector(".amt");
      recent.push({
        text: r.innerText,
        raw: r.textContent,
        color: amt ? (amt.style.color || "") : ""
      });
    });
    const txLink = document.querySelector('.nav a[data-view="transactions"]');
    txLink.click();
    const afterClick = {
      tx: document.getElementById("view-transactions").style.display,
      dash: document.getElementById("view-dashboard").style.display,
      active: txLink.classList.contains("active"),
      dashActive: document.querySelector('.nav a[data-view="dashboard"]').classList.contains("active")
    };
    return {
      mountError: false,
      error: null,
      pace: pace,
      money: moneyOut,
      views: views,
      navActive: navActive,
      accounts: accounts,
      hero: hero,
      strokes: strokes,
      catRows: rowsOf(findCard("Top categories")),
      catView: rowsOf(document.getElementById("view-categories")),
      recent: recent,
      txRows: rowsOf(document.getElementById("view-transactions")),
      acctView: document.querySelector("#view-accounts .stamp").textContent,
      recurRows: rowsOf(document.getElementById("view-recurrings")),
      journal: document.getElementById("view-journal").innerText,
      journalHtml: document.getElementById("view-journal").innerHTML,
      insight: findCard("Your money, today").innerText,
      stamp: document.querySelector("#view-dashboard .stamp").textContent,
      afterClick: afterClick
    };
  }
})();
