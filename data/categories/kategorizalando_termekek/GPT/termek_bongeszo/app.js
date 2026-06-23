"use strict";

const $ = (s) => document.querySelector(s);

let TREE = {};           // fokat -> {alkat -> {altipus: count}}
let COUNTS = {};         // fokat -> count
let TOTAL = 0;

const state = {
  fokat: "",
  alkat: "",
  altipus: "",
  name: "",
  props: {},             // propname -> [values]
  sort: "name",
  page: 1,
};

const facetSearch = {};  // propname -> kereső szöveg (csak kliens-oldali szűkítés)
const facetOpen = {};    // propname -> kinyitva?
let CUR_FACETS = [];     // a legutóbb (teljesen) kirajzolt fazetta-adat

// ---------------------------------------------------------------- init
async function init() {
  const r = await fetch("/api/tree");
  const d = await r.json();
  TREE = d.tree; COUNTS = d.counts; TOTAL = d.total;
  buildFokat();
  bindEvents();
  search();
}

function buildFokat() {
  const sel = $("#fokat");
  const fks = Object.keys(TREE).sort((a, b) => a.localeCompare(b, "hu"));
  sel.innerHTML = `<option value="">Összes főkategória (${TOTAL})</option>` +
    fks.map(fk => `<option value="${esc(fk)}">${esc(fk)} (${COUNTS[fk]})</option>`).join("");
  buildAlkat();
}

function buildAlkat() {
  const sel = $("#alkat");
  if (!state.fokat || !TREE[state.fokat]) {
    sel.innerHTML = `<option value="">— előbb főkategória —</option>`;
    sel.disabled = true;
    buildAltipus();
    return;
  }
  sel.disabled = false;
  const aks = Object.keys(TREE[state.fokat]).sort((a, b) => a.localeCompare(b, "hu"));
  const cnt = (ak) => Object.values(TREE[state.fokat][ak]).reduce((s, n) => s + n, 0);
  sel.innerHTML = `<option value="">Összes alkategória</option>` +
    aks.map(ak => `<option value="${esc(ak)}"${ak === state.alkat ? " selected" : ""}>${esc(ak || "—")} (${cnt(ak)})</option>`).join("");
  buildAltipus();
}

function buildAltipus() {
  const sel = $("#altipus");
  if (!state.fokat || !state.alkat || !TREE[state.fokat] || !TREE[state.fokat][state.alkat]) {
    sel.innerHTML = `<option value="">— előbb alkategória —</option>`;
    sel.disabled = true;
    return;
  }
  sel.disabled = false;
  const node = TREE[state.fokat][state.alkat];
  const ts = Object.keys(node).sort((a, b) => a.localeCompare(b, "hu"));
  sel.innerHTML = `<option value="">Összes altípus</option>` +
    ts.map(t => `<option value="${esc(t)}"${t === state.altipus ? " selected" : ""}>${esc(t || "—")} (${node[t]})</option>`).join("");
}

// ---------------------------------------------------------------- events
function bindEvents() {
  $("#fokat").addEventListener("change", (e) => {
    state.fokat = e.target.value; state.alkat = ""; state.altipus = "";
    state.props = {}; state.page = 1;
    buildAlkat(); search();
  });
  $("#alkat").addEventListener("change", (e) => {
    state.alkat = e.target.value; state.altipus = "";
    state.props = {}; state.page = 1;
    buildAltipus(); search();
  });
  $("#altipus").addEventListener("change", (e) => {
    state.altipus = e.target.value; state.props = {}; state.page = 1;
    search();
  });
  $("#clear-cat").addEventListener("click", () => {
    state.fokat = ""; state.alkat = ""; state.altipus = ""; state.props = {}; state.page = 1;
    $("#fokat").value = ""; buildAlkat(); search();
  });
  $("#clear-props").addEventListener("click", () => {
    state.props = {}; state.page = 1; search();
  });
  // rendezés nem érinti a fazettákat → ne rajzoljuk újra a panelt
  $("#sort").addEventListener("change", (e) => { state.sort = e.target.value; state.page = 1; search({ facetMode: "skip" }); });

  bindFacetDelegation();

  // részletes nézet bezárása: × gomb, háttérre kattintás, Esc
  $("#modal-close").addEventListener("click", () => showModal(false));
  $("#modal").querySelector(".modal-backdrop").addEventListener("click", () => showModal(false));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !$("#modal").classList.contains("hidden")) showModal(false);
  });

  let t = null;
  $("#name").addEventListener("input", (e) => {
    clearTimeout(t);
    t = setTimeout(() => { state.name = e.target.value.trim(); state.page = 1; search(); }, 250);
  });
}

// ---------------------------------------------------------------- search
let reqSeq = 0;
// facetMode:
//   "render" — teljes újrarajzolás (kategória-/névváltáskor)
//   "update" — csak a darabszámok frissítése helyben, sorrend/görgetés változatlan
//   "skip"   — a fazettákhoz nem nyúlunk (pl. rendezés)
async function search(opts = {}) {
  const facetMode = opts.facetMode || "render";
  const seq = ++reqSeq;
  const q = new URLSearchParams();
  if (state.fokat) q.set("fokategoria", state.fokat);
  if (state.alkat) q.set("alkategoria", state.alkat);
  if (state.altipus) q.set("altipus", state.altipus);
  if (state.name) q.set("name", state.name);
  q.set("props", JSON.stringify(state.props));
  q.set("sort", state.sort);
  q.set("page", state.page);

  $("#grid").classList.add("loading");
  const r = await fetch("/api/search?" + q.toString());
  const d = await r.json();
  if (seq !== reqSeq) return;   // elavult válasz eldobása
  $("#grid").classList.remove("loading");

  renderInfo(d);
  if (facetMode === "render") renderFacets(d.facets);
  else if (facetMode === "update") updateFacetCounts(d.facets);
  renderActiveFilters();
  renderGrid(d.items);
  renderPager(d);
}

function renderInfo(d) {
  $("#result-info").innerHTML = `<b>${d.total.toLocaleString("hu")}</b> találat`;
  $("#meta").textContent = `${TOTAL.toLocaleString("hu")} termék összesen`;
}

// ---------------------------------------------------------------- facets
//
// Fontos: a fazetta-panel NEM rajzolódik újra, amikor a felhasználó tulajdonságot
// jelöl be. A teljes újrarajzolás csak kategória-/névváltáskor történik (search()).
// Egy érték bejelölése csak a terméklistát frissíti, a panel a helyén marad, így
// több értéket is be lehet jelölni egymás után görgetés-ugrás nélkül.

function renderFacets(facets) {
  CUR_FACETS = facets;
  const host = $("#facets");
  if (!facets.length) {
    host.innerHTML = `<div class="facet-more">Nincs szűrhető tulajdonság.</div>`;
    return;
  }
  host.innerHTML = facets.map(facetHTML).join("");
}

function isOpen(name) {
  return !!(facetOpen[name] || (state.props[name] && state.props[name].length));
}

function facetHTML(f) {
  const sel = new Set(state.props[f.name] || []);   // a valódi állapot, nem a szerver válasza
  const open = isOpen(f.name);
  const fsearch = facetSearch[f.name] || "";
  const fnorm = stripAccents(fsearch.toLowerCase());

  const rows = open ? f.values.map(v => {
    const checked = sel.has(v.value);
    const zero = v.count === 0 && !checked;
    const hide = fnorm && !stripAccents(v.value.toLowerCase()).includes(fnorm);
    return `<label class="facet-val${checked ? " checked" : ""}${zero ? " zero" : ""}"${hide ? ' style="display:none"' : ""}>
      <input type="checkbox" data-prop="${escAttr(f.name)}" data-val="${escAttr(v.value)}"${checked ? " checked" : ""}>
      <span class="v" title="${escAttr(v.value)}">${esc(v.value)}</span>
      <span class="c">${v.count}</span>
    </label>`;
  }).join("") : "";

  const moreNote = (open && f.truncated)
    ? `<div class="facet-more">… csak az első ${f.values.length} érték (szűkíts a keresővel)</div>` : "";
  const showSearch = open && f.values.length > 12;
  const badge = sel.size ? `<span class="sel-badge"> · ${sel.size}</span>` : `<span class="sel-badge"></span>`;

  return `<div class="facet" data-prop="${escAttr(f.name)}">
    <div class="facet-title" data-toggle="${escAttr(f.name)}">
      <span>${esc(f.name)}${badge}</span>
      <span class="count">${open ? "▾" : "▸"} ${f.total}</span>
    </div>
    ${showSearch ? `<input class="facet-search" data-search="${escAttr(f.name)}" placeholder="szűrés…" value="${escAttr(fsearch)}">` : ""}
    ${open ? `<div class="facet-values">${rows}</div>` : ""}
    ${moreNote}
  </div>`;
}

// Egyetlen fazetta (nyit/zár miatti) újrarajzolása — a panel többi része érintetlen.
function rerenderOneFacet(name) {
  const f = CUR_FACETS.find(x => x.name === name);
  if (!f) return;
  for (const el of $("#facets").children) {
    if (el.getAttribute && el.getAttribute("data-prop") === name) {
      const tmp = document.createElement("div");
      tmp.innerHTML = facetHTML(f);
      el.replaceWith(tmp.firstElementChild);
      return;
    }
  }
}

function facetEl(name) {
  for (const el of $("#facets").children) {
    if (el.getAttribute && el.getAttribute("data-prop") === name) return el;
  }
  return null;
}

// A fazetta-darabszámok helyben frissítése a szerver (skip-self) válaszából,
// a panel ÚJRARAJZOLÁSA NÉLKÜL — így a sorrend és a görgetés nem változik.
// A számok az aktuális szűrést tükrözik: egy másik tulajdonságra szűrve a többi
// tulajdonság értékei mellett az látszik, hányukra igaz a szűrés (akár 0 is).
function updateFacetCounts(facets) {
  CUR_FACETS = facets;                       // a friss adat a nyitás/zárás újrarajzoláshoz
  const host = $("#facets");
  const byName = new Map(facets.map(f => [f.name, f]));

  for (const el of host.children) {
    const name = el.getAttribute && el.getAttribute("data-prop");
    if (!name) continue;
    const f = byName.get(name);
    const total = f ? f.total : 0;

    const cntEl = el.querySelector(".facet-title .count");
    if (cntEl) cntEl.textContent = `${isOpen(name) ? "▾" : "▸"} ${total}`;

    const vmap = new Map();
    if (f) for (const v of f.values) vmap.set(v.value, v.count);

    el.querySelectorAll(".facet-val").forEach(row => {
      const cb = row.querySelector("input[data-val]");
      const val = cb ? cb.getAttribute("data-val") : null;
      const c = (val != null && vmap.has(val)) ? vmap.get(val) : 0;
      const cEl = row.querySelector(".c");
      if (cEl) cEl.textContent = c;
      // a 0 találatú (és be nem jelölt) értékeket halványítjuk, de nem rejtjük el
      row.classList.toggle("zero", c === 0 && !(cb && cb.checked));
    });
  }
}

// A bal oldali fazetta vizuális állapotának szinkronizálása a state.props-szal,
// teljes újrarajzolás nélkül (badge + checkbox + checked-osztály).
function syncFacetUI(name) {
  const el = facetEl(name);
  if (!el) return;
  const sel = new Set(state.props[name] || []);
  el.querySelectorAll("input[type=checkbox][data-prop]").forEach(cb => {
    const on = sel.has(cb.getAttribute("data-val"));
    cb.checked = on;
    cb.closest(".facet-val").classList.toggle("checked", on);
  });
  const badge = el.querySelector(".sel-badge");
  if (badge) badge.textContent = sel.size ? ` · ${sel.size}` : "";
}

// Esemény-delegáció a #facets konténeren — túléli a részleges újrarajzolásokat.
function bindFacetDelegation() {
  const host = $("#facets");

  // érték be-/kijelölése → csak a terméklista frissül, a panel marad
  host.addEventListener("change", (e) => {
    const cb = e.target.closest("input[type=checkbox][data-prop]");
    if (!cb) return;
    const p = cb.getAttribute("data-prop");
    const v = cb.getAttribute("data-val");
    const cur = new Set(state.props[p] || []);
    if (cb.checked) cur.add(v); else cur.delete(v);
    if (cur.size) state.props[p] = [...cur]; else delete state.props[p];
    cb.closest(".facet-val").classList.toggle("checked", cb.checked);
    const badge = facetEl(p)?.querySelector(".sel-badge");
    if (badge) badge.textContent = cur.size ? ` · ${cur.size}` : "";
    state.page = 1;
    renderActiveFilters();
    search({ facetMode: "update" });   // darabszámok helyben frissülnek, panel marad
  });

  // tulajdonság nyitása/zárása → csak az adott fazetta rajzolódik újra
  host.addEventListener("click", (e) => {
    const t = e.target.closest("[data-toggle]");
    if (!t) return;
    if (e.target.closest("input")) return;   // a kereső mezőre kattintás ne nyisson/zárjon
    const p = t.getAttribute("data-toggle");
    facetOpen[p] = !isOpen(p);
    rerenderOneFacet(p);
  });

  // helyi értékkereső → csak a sorok megjelenítését szűri, nincs újrarajzolás (fókusz marad)
  host.addEventListener("input", (e) => {
    const inp = e.target.closest("input[data-search]");
    if (!inp) return;
    const p = inp.getAttribute("data-search");
    facetSearch[p] = inp.value;
    const q = stripAccents(inp.value.toLowerCase());
    const facet = inp.closest(".facet");
    facet.querySelectorAll(".facet-val").forEach(row => {
      const vEl = row.querySelector(".v");
      const val = vEl.getAttribute("title") || vEl.textContent;
      row.style.display = (!q || stripAccents(val.toLowerCase()).includes(q)) ? "" : "none";
    });
  });
}

function renderActiveFilters() {
  const host = $("#active-filters");
  const chips = [];
  for (const [p, vals] of Object.entries(state.props)) {
    for (const v of vals) {
      chips.push(`<span class="chip">${esc(p)}: ${esc(v)}
        <button data-rmprop="${escAttr(p)}" data-rmval="${escAttr(v)}">×</button></span>`);
    }
  }
  host.innerHTML = chips.join("");
  host.querySelectorAll("button[data-rmprop]").forEach(b => {
    b.addEventListener("click", () => {
      const p = b.getAttribute("data-rmprop"), v = b.getAttribute("data-rmval");
      const cur = new Set(state.props[p] || []); cur.delete(v);
      if (cur.size) state.props[p] = [...cur]; else delete state.props[p];
      state.page = 1;
      syncFacetUI(p);                    // bal oldali pipa frissítése újrarajzolás nélkül
      search({ facetMode: "update" });   // darabszámok helyben frissülnek
    });
  });
}

// ---------------------------------------------------------------- grid
function renderGrid(items) {
  const grid = $("#grid");
  if (!items.length) {
    grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1">Nincs a szűrőknek megfelelő termék.</div>`;
    return;
  }
  grid.innerHTML = items.map(p => {
    const thumb = p.img
      ? `<div class="thumb"><img loading="lazy" src="/img/${encodeURI(p.img)}" alt=""
            onerror="this.parentElement.classList.add('empty');this.remove();this.parentElement.textContent='nincs kép'"></div>`
      : `<div class="thumb empty">nincs kép</div>`;
    const price = p.price ? `<span class="price">${fmtPrice(p.price)} Ft${p.unit ? "/" + esc(p.unit) : ""}</span>` : "";
    const qty = (p.qty && p.qunit) ? `<span>${esc(p.qty)} ${esc(p.qunit)}</span>` : "";
    const cat = [p.fokat, p.alkat, p.altipus].filter(Boolean).map(esc).join(" › ");
    const tags = Object.entries(p.props).slice(0, 6).map(([k, v]) =>
      `<span class="tag" title="${escAttr(k)}">${esc(Array.isArray(v) ? v.join(", ") : v)}</span>`).join("");
    return `<div class="product" data-id="${p.id}" title="Részletek megtekintése">
      ${thumb}
      <div class="body">
        <div class="pname" title="${escAttr(p.name)}">${esc(p.name)}</div>
        <div class="pmeta">${price} ${qty} ${p.store ? `<span>${esc(p.store)}</span>` : ""}</div>
        <div class="cat">${cat}</div>
        <div class="pprops">${tags}</div>
      </div>
    </div>`;
  }).join("");

  grid.querySelectorAll(".product[data-id]").forEach(el => {
    el.addEventListener("click", () => openDetail(el.getAttribute("data-id")));
  });
}

// ---------------------------------------------------------------- részletes nézet
async function openDetail(id) {
  const body = $("#modal-body");
  body.innerHTML = `<div class="detail-missing">Betöltés…</div>`;
  showModal(true);
  let d;
  try {
    d = await (await fetch("/api/product?id=" + encodeURIComponent(id))).json();
  } catch (e) {
    body.innerHTML = `<div class="detail-missing">Hiba a betöltéskor.</div>`;
    return;
  }
  if (d.error) { body.innerHTML = `<div class="detail-missing">${esc(d.error)}</div>`; return; }

  const er = d.eredmeny || {};
  const t = er.termek || {};
  const name = t.product_name || "(névtelen)";
  const cat = [er.fokategoria, er.alkategoria, er.altipus].filter(Boolean).map(esc).join(" › ");

  const thumb = d.img
    ? `<div class="thumb"><img src="/img/${encodeURI(d.img)}" alt=""
          onerror="this.parentElement.classList.add('empty');this.remove();this.parentElement.textContent='nincs kép'"></div>`
    : `<div class="thumb empty">nincs kép</div>`;

  // az eredmeny.json rekord a 'termek' nélkül (a termék-mezőket külön szekcióban mutatjuk)
  const erRest = {};
  for (const [k, v] of Object.entries(er)) if (k !== "termek") erRest[k] = v;

  const csvSection = d.csv
    ? `<div class="detail-section"><h3>Eredeti CSV sor (kategorizalatlan_termekek.csv)</h3>${kvTable(d.csv)}</div>`
    : `<div class="detail-section"><h3>Eredeti CSV sor</h3><div class="detail-missing">Nincs párosítható CSV sor ehhez a termékhez (store_product_id alapján).</div></div>`;

  body.innerHTML = `
    <div class="detail-head">
      ${thumb}
      <div>
        <h2>${esc(name)}</h2>
        <div class="sub">
          ${d.store ? `<span class="store-badge">${esc(d.store)}</span>` : ""}
          ${t.store_product_id ? `<span>azonosító: ${esc(t.store_product_id)}</span>` : ""}
        </div>
        ${cat ? `<div class="sub" style="margin-top:6px">${cat}</div>` : ""}
      </div>
    </div>

    <div class="detail-section">
      <h3>Termék adatai (eredmeny.json → termek)</h3>
      ${kvTable(t)}
    </div>

    <div class="detail-section">
      <h3>Besorolás és tulajdonságok (eredmeny.json)</h3>
      ${kvTable(erRest)}
    </div>

    ${csvSection}
  `;
}

// Általános kulcs–érték tábla tetszőleges JSON-értékre (egymásba ágyazva is).
function kvTable(obj) {
  if (obj == null || typeof obj !== "object" || Array.isArray(obj)) {
    return `<div>${valHTML(obj)}</div>`;
  }
  const keys = Object.keys(obj);
  if (!keys.length) return `<div class="detail-missing">(üres)</div>`;
  const rows = keys.map(k =>
    `<tr><th>${esc(k)}</th><td${(obj[k] && typeof obj[k] === "object" && !Array.isArray(obj[k])) ? ' class="nested"' : ""}>${valHTML(obj[k])}</td></tr>`
  ).join("");
  return `<table class="kv"><tbody>${rows}</tbody></table>`;
}

function valHTML(v) {
  if (v === null || v === undefined || v === "") return `<span class="empty-val">—</span>`;
  if (typeof v === "boolean") return v ? `<span class="bool-true">igen</span>` : `<span class="bool-false">nem</span>`;
  if (Array.isArray(v)) {
    if (!v.length) return `<span class="empty-val">—</span>`;
    return `<div class="arr">${v.map(x =>
      (x && typeof x === "object") ? kvTable(x) : `<span class="tag">${esc(x)}</span>`).join("")}</div>`;
  }
  if (typeof v === "object") return kvTable(v);
  return esc(v);
}

function showModal(on) {
  $("#modal").classList.toggle("hidden", !on);
}

// ---------------------------------------------------------------- pager
function renderPager(d) {
  const host = $("#pager");
  if (d.pages <= 1) { host.innerHTML = ""; return; }
  const cur = d.page, pages = d.pages;
  const btn = (label, page, opts = {}) =>
    `<button ${opts.disabled ? "disabled" : ""} ${opts.active ? 'class="active"' : ""} data-page="${page}">${label}</button>`;

  const nums = [];
  const add = (n) => nums.push(btn(n, n, { active: n === cur }));
  const win = 2;
  let lo = Math.max(1, cur - win), hi = Math.min(pages, cur + win);
  if (lo > 1) { add(1); if (lo > 2) nums.push(`<span>…</span>`); }
  for (let n = lo; n <= hi; n++) add(n);
  if (hi < pages) { if (hi < pages - 1) nums.push(`<span>…</span>`); add(pages); }

  host.innerHTML =
    btn("‹ Előző", cur - 1, { disabled: cur <= 1 }) +
    nums.join("") +
    btn("Következő ›", cur + 1, { disabled: cur >= pages });

  host.querySelectorAll("button[data-page]").forEach(b => {
    b.addEventListener("click", () => {
      state.page = parseInt(b.getAttribute("data-page"), 10);
      $("#content").scrollTo({ top: 0, behavior: "smooth" });
      search({ facetMode: "skip" });
    });
  });
}

// ---------------------------------------------------------------- utils
function esc(s) { return String(s == null ? "" : s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])); }
function escAttr(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
function cssEsc(s) { return String(s).replace(/"/g, '\\"'); }
function stripAccents(s) { return s.normalize("NFKD").replace(/[̀-ͯ]/g, ""); }
function fmtPrice(s) { const n = parseFloat(String(s).replace(",", ".")); return isNaN(n) ? esc(s) : Math.round(n).toLocaleString("hu"); }

init();
