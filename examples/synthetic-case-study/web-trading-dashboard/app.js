"use strict";
// Demo market simulator (FT-4): seeded random walk with volatility clustering, tick-size rounding,
// market-hours clock, and holdings, orders and P&L that stay consistent after every simulated fill.
(function () {
  const SEED = 26112026;
  function mulberry32(a) { return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const rnd = mulberry32(SEED);
  const gauss = () => { let u = 0, v = 0; while (!u) u = rnd(); while (!v) v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  const TICK = 0.05;
  const roundTick = p => Math.max(TICK, Math.round(p / TICK) * TICK);
  const inr = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const num = new Intl.NumberFormat("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const pct = v => (v >= 0 ? "+" : "−") + Math.abs(v).toFixed(2) + "%";
  const signed = v => (v >= 0 ? "+" : "−") + inr.format(Math.abs(v));
  const arrow = v => (v >= 0 ? "▲" : "▼");

  // Fictional instruments (demo symbols, not real listings).
  const UNIVERSE = [["ARVO", "Arvo Textiles", 412], ["NILP", "Nilgiri Power", 186.4], ["KSHT", "Kshitij Finance", 1288], ["MAYU", "Mayur Foods", 742.15],
    ["SETU", "Setu Infra", 93.6], ["TARA", "Tara Pharma", 2150.5], ["VAYU", "Vayu Logistics", 318.25], ["DHRU", "Dhruv Steel", 128.9],
    ["KIRN", "Kiran Retail", 564.3], ["PRAN", "Pran Agro", 77.45], ["SURY", "Surya Solar", 1034.8], ["NADI", "Nadi Water", 241.7]];
  const inst = UNIVERSE.map(([sym, name, p]) => ({ sym, name, prevClose: p, last: p, vol: 0.006, history: [] }));
  // Warm-up so the first screen already has a history (90 ticks per instrument).
  for (const i of inst) { for (let k = 0; k < 90; k++) step(i); i.prevClose = i.history[0]; }

  function step(i) {
    // Volatility clustering: next vol pulls toward a long-run level plus a random shock (bounded).
    i.vol = Math.min(0.03, Math.max(0.002, 0.94 * i.vol + 0.06 * 0.006 + 0.0015 * Math.abs(gauss())));
    i.last = roundTick(i.last * Math.exp(i.vol * gauss() * 0.35));
    i.history.push(i.last); if (i.history.length > 90) i.history.shift();
  }

  // Demo clock: a trading day in IST, advancing 20 demo seconds per real tick.
  const clock = new Date("2026-11-16T10:42:00+05:30");
  const marketOpen = d => { const ist = new Date(d.getTime() + 5.5 * 3600e3); const day = ist.getUTCDay(); const m = ist.getUTCHours() * 60 + ist.getUTCMinutes();
    return day >= 1 && day <= 5 && m >= 555 && m < 930; };
  const timeFmt = new Intl.DateTimeFormat("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit", timeZone: "Asia/Kolkata" });

  const account = { cash: 250000, holdings: new Map([["KSHT", { qty: 40, avg: 1201.35 }], ["NILP", { qty: 300, avg: 171.2 }], ["SURY", { qty: 25, avg: 1110 }]]), orders: [] };
  const usedKeys = new Set();
  let selected = inst[0], paused = false, lastUpdate = new Date(clock);

  const $ = id => document.getElementById(id);
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };

  function renderStatus() {
    const s = $("market-status"); s.textContent = "";
    const open = marketOpen(clock);
    const state = el("span", paused ? "paused" : "live", paused ? "Feed paused" : (open ? "Market open (demo)" : "Market closed (demo)"));
    s.append(state, document.createTextNode(" · last update " + timeFmt.format(lastUpdate) + " IST" + (paused ? ", prices are stale" : "")));
  }

  function renderWatchlist() {
    const body = $("wl-body"); body.textContent = "";
    for (const i of inst) {
      const ch = i.last - i.prevClose, chp = ch / i.prevClose * 100;
      const tr = el("tr", i === selected ? "selected" : "");
      const td = el("td"); const b = el("button", "rowbtn"); b.type = "button";
      b.setAttribute("aria-pressed", String(i === selected));
      b.append(el("span", "sym", i.sym), el("span", "name", i.name));
      b.addEventListener("click", () => { selected = i; renderAll(); $("qty").focus({ preventScroll: true }); });
      td.append(b);
      const last = el("td", "num", num.format(i.last));
      const chg = el("td", "num " + (ch >= 0 ? "up" : "down"), arrow(ch) + " " + pct(chp));
      chg.setAttribute("aria-label", (ch >= 0 ? "up " : "down ") + Math.abs(chp).toFixed(2) + " percent");
      tr.append(td, last, chg); body.append(tr);
    }
  }

  function renderChart() {
    const h = selected.history, svg = $("chart");
    const min = Math.min(...h), max = Math.max(...h), span = max - min || 1;
    const pts = h.map((p, k) => (k * 600 / (h.length - 1)).toFixed(1) + "," + (190 - (p - min) / span * 180).toFixed(1)).join(" ");
    const first = h[0], lastP = h[h.length - 1], chp = (lastP - first) / first * 100;
    svg.querySelectorAll("polyline,line").forEach(n => n.remove());
    const ns = "http://www.w3.org/2000/svg";
    const base = document.createElementNS(ns, "line"); const y = (190 - (selected.prevClose - min) / span * 180).toFixed(1);
    Object.entries({ x1: 0, x2: 600, y1: y, y2: y, class: "base" }).forEach(([k, v]) => base.setAttribute(k, v));
    const line = document.createElementNS(ns, "polyline"); line.setAttribute("points", pts); line.setAttribute("class", "line");
    svg.append(base, line);
    $("ch-desc").textContent = selected.sym + " price over the last " + h.length + " demo ticks: from " + num.format(first) + " to " + num.format(lastP) + ", " + (chp >= 0 ? "up " : "down ") + Math.abs(chp).toFixed(2) + " percent. Dashed line is the previous close.";
    $("ch-symbol").textContent = selected.sym + " · " + selected.name;
    const st = $("stats"); st.textContent = "";
    for (const [k, v] of [["Last", num.format(lastP)], ["Prev close", num.format(selected.prevClose)], ["Day high", num.format(Math.max(...h))], ["Day low", num.format(Math.min(...h))]]) {
      const d = el("div"); d.append(el("dt", "", k), el("dd", "", v)); st.append(d); }
  }

  function portfolio() {
    let value = 0, invested = 0;
    for (const [sym, h] of account.holdings) { const i = inst.find(x => x.sym === sym); value += h.qty * i.last; invested += h.qty * h.avg; }
    let day = 0; for (const [sym, h] of account.holdings) { const i = inst.find(x => x.sym === sym); day += h.qty * (i.last - i.prevClose); }
    return { value, invested, pnl: value - invested, day };
  }

  function renderPortfolio() {
    const p = portfolio();
    $("pf-value").textContent = inr.format(p.value);
    const dayPct = p.value ? p.day / (p.value - p.day) * 100 : 0;
    const c = $("pf-change"); c.className = "change " + (p.day >= 0 ? "up" : "down");
    c.textContent = arrow(p.day) + " " + signed(p.day) + " (" + pct(dayPct) + ") today";
    $("pf-invested").textContent = inr.format(p.invested);
    const pnl = $("pf-pnl"); pnl.textContent = signed(p.pnl); pnl.className = p.pnl >= 0 ? "up" : "down";
    $("pf-margin").textContent = inr.format(account.cash);
    const body = $("hd-body"); body.textContent = "";
    if (!account.holdings.size) { const tr = el("tr"); const td = el("td", "", "No holdings yet. Buy an instrument to see it here."); td.colSpan = 4; tr.append(td); body.append(tr); }
    for (const [sym, h] of account.holdings) {
      const i = inst.find(x => x.sym === sym), v = h.qty * i.last, pl = v - h.qty * h.avg;
      const tr = el("tr"); tr.append(el("td", "sym", sym), el("td", "num", String(h.qty)), el("td", "num", inr.format(v)), el("td", "num " + (pl >= 0 ? "up" : "down"), arrow(pl) + " " + signed(pl)));
      body.append(tr);
    }
  }

  function readOrder() {
    const side = document.querySelector("input[name=side]:checked").value;
    const type = document.querySelector("input[name=otype]:checked").value;
    const qty = Number($("qty").value);
    const price = type === "LIMIT" ? Number($("price").value) : selected.last;
    const value = qty * price, charges = Math.round(value * 0.0012 * 100) / 100;
    return { side, type, qty, price, value, charges, need: side === "BUY" ? value + charges : charges };
  }

  function validate(o) {
    let ok = true;
    const qe = $("qty-err"), pe = $("price-err");
    qe.hidden = pe.hidden = true; $("qty").removeAttribute("aria-invalid"); $("price").removeAttribute("aria-invalid");
    const held = (account.holdings.get(selected.sym) || { qty: 0 }).qty;
    let qmsg = "";
    if (!Number.isInteger(o.qty) || o.qty < 1) qmsg = "Enter a whole number of shares, 1 or more.";
    else if (o.side === "SELL" && o.qty > held) qmsg = "You hold " + held + " " + selected.sym + ". Enter " + held + " or fewer to sell.";
    if (qmsg) { qe.textContent = qmsg; qe.hidden = false; $("qty").setAttribute("aria-invalid", "true"); ok = false; }
    if (o.type === "LIMIT") {
      let pmsg = "";
      if (!(o.price > 0)) pmsg = "Enter a limit price above zero.";
      else if (Math.abs(o.price / TICK - Math.round(o.price / TICK)) > 1e-6) pmsg = "Prices move in steps of 0.05. Try " + num.format(roundTick(o.price)) + ".";
      if (pmsg) { pe.textContent = pmsg; pe.hidden = false; $("price").setAttribute("aria-invalid", "true"); ok = false; }
    }
    return ok;
  }

  function renderTicket() {
    $("tk-instrument").textContent = selected.sym + " · " + selected.name + " · last " + num.format(selected.last);
    const limit = document.querySelector("input[name=otype]:checked").value === "LIMIT";
    $("price-row").hidden = !limit; $("mkt-note").hidden = limit;
    if (limit && !$("price").value) $("price").value = selected.last.toFixed(2);
    const o = readOrder();
    const valid = o.qty > 0 && o.price > 0;
    $("est-value").textContent = valid ? inr.format(o.value) : "—";
    $("est-charges").textContent = valid ? inr.format(o.charges) : "—";
    $("est-margin").textContent = valid ? inr.format(o.need) + " / " + inr.format(account.cash) : "—";
    $("review").textContent = "Review order";
  }

  function renderOrders() {
    const ul = $("orders"); ul.textContent = "";
    $("orders-empty").hidden = account.orders.length > 0;
    for (const o of account.orders) {
      const li = el("li");
      li.append(el("span", "", o.side + " " + o.qty + " " + o.sym + " @ " + num.format(o.fill) + " (" + o.type.toLowerCase() + ")"),
        el("span", "tag", o.status + " · " + timeFmt.format(o.time)));
      ul.append(li);
    }
  }

  function renderAll() { renderStatus(); renderWatchlist(); renderChart(); renderPortfolio(); renderTicket(); renderOrders(); }

  // Mock order server: accepts once per idempotency key, checks margin, fills at the next demo price.
  function mockServer(order) {
    return new Promise(resolve => setTimeout(() => {
      if (usedKeys.has(order.key)) return resolve({ ok: true, duplicate: true });
      if (order.side === "BUY" && order.need > account.cash) {
        const maxQty = Math.floor(account.cash / (order.price * 1.0012));
        return resolve({ ok: false, reason: "Insufficient margin: this order needs " + inr.format(order.need) + " and " + inr.format(account.cash) + " is available. Reduce the quantity to " + maxQty + " or less." });
      }
      if (order.type === "LIMIT" && ((order.side === "BUY" && order.price < selected.last) || (order.side === "SELL" && order.price > selected.last)))
        return resolve({ ok: true, pending: true });
      usedKeys.add(order.key);
      const fill = order.type === "MARKET" ? roundTick(selected.last * (1 + (order.side === "BUY" ? 1 : -1) * 0.0005)) : order.price;
      const h = account.holdings.get(order.sym) || { qty: 0, avg: 0 };
      if (order.side === "BUY") { const q = h.qty + order.qty; h.avg = (h.qty * h.avg + order.qty * fill) / q; h.qty = q; account.cash -= order.qty * fill + order.charges; }
      else { h.qty -= order.qty; account.cash += order.qty * fill - order.charges; }
      if (h.qty > 0) account.holdings.set(order.sym, h); else account.holdings.delete(order.sym);
      resolve({ ok: true, fill });
    }, 600));
  }

  let pendingOrder = null;
  const newKey = () => (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random());

  $("order-form").addEventListener("submit", e => {
    e.preventDefault();
    const o = readOrder();
    if (!validate(o)) { (document.querySelector("[aria-invalid=true]") || $("qty")).focus(); return; }
    pendingOrder = Object.assign(o, { sym: selected.sym, key: newKey() });
    $("cf-sentence").textContent = (o.side === "BUY" ? "Buy " : "Sell ") + o.qty + " " + selected.sym + " (" + selected.name + ") at " +
      (o.type === "MARKET" ? "market price, now about " + num.format(selected.last) : "a limit of " + num.format(o.price)) + ".";
    const f = $("cf-figures"); f.textContent = "";
    for (const [k, v] of [["Estimated value", inr.format(o.value)], ["Charges (estimate)", inr.format(o.charges)], ["Margin needed / available", inr.format(o.need) + " / " + inr.format(account.cash)]]) {
      const d = el("div"); d.append(el("dt", "", k), el("dd", "", v)); f.append(d); }
    $("cf-error").hidden = true; $("cf-place").disabled = false; $("cf-place").textContent = "Place order";
    $("confirm").showModal(); $("cf-edit").focus();
  });

  $("cf-edit").addEventListener("click", () => { $("confirm").close(); $("qty").focus(); });
  $("cf-place").addEventListener("click", async () => {
    if (!pendingOrder) return;
    const btn = $("cf-place"); btn.disabled = true; btn.textContent = "Placing order";
    const res = await mockServer(pendingOrder);
    if (!res.ok) { $("cf-error").textContent = res.reason + " No order was placed."; $("cf-error").hidden = false; btn.disabled = false; btn.textContent = "Place order"; return; }
    if (!res.duplicate) account.orders.unshift({ side: pendingOrder.side, qty: pendingOrder.qty, sym: pendingOrder.sym, type: pendingOrder.type,
      fill: res.fill || pendingOrder.price, status: res.pending ? "Open, waiting for the limit price" : "Filled", time: new Date(clock) });
    pendingOrder = null; $("confirm").close(); renderAll(); $("review").focus();
    $("market-status").textContent = "Order " + (res.pending ? "placed and open" : "filled") + " (demo). " + $("market-status").textContent;
  });

  document.querySelectorAll("input[name=side], input[name=otype]").forEach(r => r.addEventListener("change", () => { validate(readOrder()); renderTicket(); }));
  $("qty").addEventListener("input", renderTicket); $("price").addEventListener("input", renderTicket);
  $("qty").addEventListener("blur", () => validate(readOrder()));
  $("pause").addEventListener("click", () => { paused = !paused; $("pause").textContent = paused ? "Resume demo feed" : "Pause demo feed"; renderStatus(); });

  function tick() {
    if (!paused && marketOpen(clock)) {
      const before = new Map(inst.map(i => [i.sym, i.last]));
      inst.forEach(step); clock.setTime(clock.getTime() + 20e3); lastUpdate = new Date(clock);
      renderAll();
      const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!reduce) document.querySelectorAll("#wl-body tr").forEach((tr, k) => { const d = inst[k].last - before.get(inst[k].sym);
        if (d) { tr.classList.remove("flash-up", "flash-down"); void tr.offsetWidth; tr.classList.add(d > 0 ? "flash-up" : "flash-down"); } });
    } else if (!paused) { clock.setTime(clock.getTime() + 20e3); renderStatus(); }
  }
  setTimeout(() => { renderAll(); setInterval(tick, 2000); }, 350);
})();
