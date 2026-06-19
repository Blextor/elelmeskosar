"use strict";

let DATA = null;             // /api/data válasz
let NODE_BY_KEY = {};        // pathKey -> node objektum (props miatt)
let EXPANDED = new Set();    // kinyitott pathKey-k
let SOURCE = null;           // path tömb
let TARGET = null;           // path tömb
let SEL_PROP = null;         // {name, group, kind} a forrás-tulajdonságból
let SEL_VALUE = null;        // kiválasztott egy érték (opcionális)
let ACTIVE_OP = "merge_mapping";

// térkép-állapot (Összevonás fül)
let MAP_SRC = [];            // forrás effektív propok
let MAP_TGT = [];            // cél effektív propok
let MAP_CONN = [];           // [{src, dst}]
let MAP_ARMED = null;        // épp "felhúzott" forrás-tulajdonság neve
let MAP_KEY = null;          // melyik (source|target) párra töltöttünk be propokat
const SRC_DOTS = {};         // name -> dot elem
const TGT_DOTS = {};         // name -> dot elem

const $ = (s) => document.querySelector(s);
const key = (p) => JSON.stringify(p);
const pathStr = (p) => p.join("  ›  ");

// ---------------------------------------------------------------- betöltés
async function loadData() {
  const r = await fetch("/api/data");
  DATA = await r.json();
  NODE_BY_KEY = {};
  indexNodes(DATA.tree);
  $("#meta").textContent =
    `${DATA.total_products} termék · fa: ${DATA.tree_file} · termékek: ${DATA.eredmeny_file}`;
  renderTree();
  renderIssues();
  refreshSelections();
}

function indexNodes(nodes) {
  for (const n of nodes) {
    NODE_BY_KEY[key(n.path)] = n;
    if (n.children && n.children.length) indexNodes(n.children);
  }
}

// ---------------------------------------------------------------- fa render
function renderTree() {
  const q = $("#search").value.trim().toLowerCase();
  const hideEmpty = $("#hide-empty").checked;
  const root = $("#tree");
  root.innerHTML = "";
  for (const n of DATA.tree) {
    const el = renderNode(n, q, hideEmpty);
    if (el) root.appendChild(el);
  }
}

function nodeMatches(n, q) {
  if (!q) return true;
  if (n.name.toLowerCase().includes(q)) return true;
  return (n.children || []).some((c) => nodeMatches(c, q));
}

function renderNode(n, q, hideEmpty) {
  if (q && !nodeMatches(n, q)) return null;
  if (hideEmpty && !q && n.count === 0 && !(n.children && n.children.length)) return null;

  const k = key(n.path);
  const wrap = document.createElement("div");
  wrap.className = `node lvl${n.level}` + (n.orphan ? " orphan-node" : "");
  if (SOURCE && key(SOURCE) === k) wrap.classList.add("sel-src");
  if (TARGET && key(TARGET) === k) wrap.classList.add("sel-tgt");

  const row = document.createElement("div");
  row.className = "node-row";

  const hasKids = n.children && n.children.length;
  const expanded = q ? true : EXPANDED.has(k);

  const tw = document.createElement("span");
  tw.className = "twisty";
  tw.textContent = hasKids ? (expanded ? "▾" : "▸") : "";
  tw.onclick = () => { toggle(k); renderTree(); };
  row.appendChild(tw);

  const name = document.createElement("span");
  name.className = "node-name";
  if (q && n.name.toLowerCase().includes(q)) name.classList.add("match");
  name.textContent = n.name;
  name.onclick = () => { if (hasKids) { toggle(k); renderTree(); } };
  row.appendChild(name);

  if (n.orphan) {
    const o = document.createElement("span");
    o.className = "orphan-tag";
    o.textContent = "árva";
    o.title = "Ez a besorolás a termékeken létezik, de NINCS node a fában. Oldd fel vagy olvaszd össze.";
    row.appendChild(o);
  }

  const cnt = document.createElement("span");
  cnt.className = "count" + (n.count === 0 ? " zero" : "");
  cnt.textContent = n.count;
  cnt.title = "termékek száma (mélységgel együtt)";
  row.appendChild(cnt);

  if (n.level === 2 && n.direct) {
    const d = document.createElement("span");
    d.className = "direct";
    d.textContent = `(közvetlen: ${n.direct})`;
    d.title = "altípus nélkül közvetlenül itt besorolt termékek";
    row.appendChild(d);
  }

  const pick = document.createElement("span");
  pick.className = "pick";
  const bs = document.createElement("button");
  bs.textContent = "Forrás";
  bs.onclick = (e) => { e.stopPropagation(); SOURCE = n.path; afterSelect(); };
  const bt = document.createElement("button");
  bt.textContent = "Cél";
  bt.onclick = (e) => { e.stopPropagation(); TARGET = n.path; afterSelect(); };
  pick.append(bs, bt);
  row.appendChild(pick);

  wrap.appendChild(row);

  if (hasKids && expanded) {
    const kids = document.createElement("div");
    kids.className = "children";
    for (const c of n.children) {
      const el = renderNode(c, q, hideEmpty);
      if (el) kids.appendChild(el);
    }
    wrap.appendChild(kids);
  }
  return wrap;
}

function toggle(k) { EXPANDED.has(k) ? EXPANDED.delete(k) : EXPANDED.add(k); }

// ---------------------------------------------------------------- kijelölés
function afterSelect() {
  SEL_PROP = null; SEL_VALUE = null;
  renderTree();
  refreshSelections();
}

function refreshSelections() {
  $("#src").textContent = SOURCE ? pathStr(SOURCE) : `— kattints egy node-ra, majd „Forrás" —`;
  $("#tgt").textContent = TARGET ? pathStr(TARGET) : `— kattints egy node-ra, majd „Cél" —`;
  renderPropChips("#src-props", SOURCE, true);
  renderPropChips("#tgt-props", TARGET, false);
  renderForm();
}

function renderPropChips(sel, path, isSource) {
  const box = $(sel);
  box.innerHTML = "";
  if (!path) return;
  const node = NODE_BY_KEY[key(path)];
  if (!node) return;
  for (const p of node.props) {
    const chip = document.createElement("span");
    chip.className = "chip " + (p.kind === "flag" ? "flag" : "list");
    chip.textContent = p.name + (p.kind === "lista" ? ` [${p.values.length}]` : " ⚑");
    if (isSource && SEL_PROP && SEL_PROP.name === p.name) chip.classList.add("sel");
    if (isSource) {
      chip.onclick = () => {
        SEL_PROP = { name: p.name, group: p.group, kind: p.kind, values: p.values };
        SEL_VALUE = null;
        if (p.kind === "lista" && p.values.length) {
          const v = prompt(`Csak egy értéket viszel át a(z) "${p.name}" tulajdonságból?\n` +
            `Hagyd üresen az EGÉSZ tulajdonsághoz.\nÉrtékek: ${p.values.join(", ")}`, "");
          if (v && v.trim()) SEL_VALUE = v.trim();
        }
        refreshSelections();
      };
    }
    box.appendChild(chip);
  }
}

// ---------------------------------------------------------------- op fülek
document.querySelectorAll(".tab").forEach((t) => {
  t.onclick = () => {
    document.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
    t.classList.add("active");
    ACTIVE_OP = t.dataset.op;
    setResult("", "");
    $("#apply-btn").disabled = true;
    renderForm();
  };
});

function renderForm() {
  const f = $("#op-forms");
  if (ACTIVE_OP === "merge_mapping") { f.innerHTML = formMerge(); maybeLoadMapping(); }
  else if (ACTIVE_OP === "move_node") f.innerHTML = formMoveNode();
  else if (ACTIVE_OP === "dissolve") f.innerHTML = formDissolve();
  else if (ACTIVE_OP === "move_property") f.innerHTML = formMoveProp();
  else if (ACTIVE_OP === "create_property") f.innerHTML = formCreateProp();
}

function formMerge() {
  if (!SOURCE || !TARGET)
    return `<p class="hint">Jelölj ki egy <b>Forrás</b> és egy <b>Cél</b> node-ot
      (fő/al/altípus — <b>eltérő szint is</b> lehet). A forrás node és termékei a célba
      olvadnak, a tulajdonságokat pedig alább kötöd össze.</p>`;
  if (key(SOURCE) === key(TARGET))
    return `<p class="hint">A forrás és a cél azonos.</p>`;
  return `<div id="mapwrap"><p class="hint">Tulajdonság-térkép betöltése…</p></div>`;
}

async function fetchProps(path) {
  const r = await fetch("/api/node_props", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path }),
  });
  return (await r.json()).props || [];
}

// Csak akkor töltünk újra, ha a forrás/cél pár változott (ne dobjuk el a kézi kötéseket).
async function maybeLoadMapping() {
  if (!SOURCE || !TARGET || key(SOURCE) === key(TARGET)) return;
  const pairKey = key(SOURCE) + "→" + key(TARGET);
  if (pairKey === MAP_KEY) { renderMapping(); return; }
  MAP_KEY = pairKey;
  const [sp, tp] = await Promise.all([fetchProps(SOURCE), fetchProps(TARGET)]);
  MAP_SRC = sp; MAP_TGT = tp; MAP_ARMED = null;
  const tnames = new Set(tp.map((e) => e.name));
  MAP_CONN = sp.filter((e) => tnames.has(e.name)).map((e) => ({ src: e.name, dst: e.name }));
  renderMapping();
}

function renderMapping() {
  const wrap = $("#mapwrap");
  if (!wrap) return;
  const srcOn = new Set(MAP_CONN.map((c) => c.src));
  const dstOn = new Set(MAP_CONN.map((c) => c.dst));
  const meta = (e) => `<span class="pmeta">${e.kind}·${e.product_count}db·${e.where}</span>`;
  const delCount = MAP_SRC.filter((e) => !srcOn.has(e.name)).length;

  wrap.innerHTML = `
    <p class="hint">Kösd össze a <b>forrás</b> (bal) tulajdonságait a <b>céllal</b> (jobb):
      kattints egy bal pöttyre, majd egy jobb pöttyre. Bekötetlen
      <b style="color:#c0392b">forrás törlődik</b>, bekötetlen cél marad.
      Az azonos nevűek előre összekötve. (Forrás-pöttyre kattintva bontod a kötést.)</p>
    ${SOURCE.length !== TARGET.length ? `<p class="hint" style="color:#a06a00">Eltérő szint (${SOURCE.length} → ${TARGET.length}): a forrás termékei a cél szintjére kerülnek${TARGET.length < SOURCE.length ? " (a mélyebb szint kiürül)" : ""}.</p>` : ""}
    <div class="maphdr"><span>FORRÁS: ${escapeHtml(SOURCE[SOURCE.length - 1])} → törlődik: ${delCount} tulajdonság</span>
      <span>CÉL: ${escapeHtml(TARGET[TARGET.length - 1])}</span></div>
    <div class="mapcols">
      <div class="mapcol left">
        ${MAP_SRC.map((e) => mapRow(e, "src", srcOn.has(e.name))).join("")}
        ${MAP_SRC.length ? "" : '<p class="hint">Nincs forrás-tulajdonság.</p>'}
      </div>
      <svg class="maplines"></svg>
      <div class="mapcol right">
        ${MAP_TGT.map((e) => mapRow(e, "dst", dstOn.has(e.name))).join("")}
        ${MAP_TGT.length ? "" : '<p class="hint">Nincs cél-tulajdonság.</p>'}
      </div>
    </div>`;

  Object.keys(SRC_DOTS).forEach((k) => delete SRC_DOTS[k]);
  Object.keys(TGT_DOTS).forEach((k) => delete TGT_DOTS[k]);
  wrap.querySelectorAll(".dot").forEach((d) => {
    const nm = d.dataset.name, side = d.dataset.side;
    (side === "src" ? SRC_DOTS : TGT_DOTS)[nm] = d;
    d.onclick = () => onDot(side, nm);
  });
  requestAnimationFrame(drawLines);
}

function mapRow(e, side, on) {
  const cls = side === "src" ? (on ? "on" : "del") : (on ? "on" : "");
  const armed = side === "src" && MAP_ARMED === e.name ? " armed" : "";
  const inh = e.inherited ? " inh" : "";
  const dot = `<span class="dot ${side} ${cls}${armed}" data-side="${side}" data-name="${escapeAttr(e.name)}"></span>`;
  const meta = `<span class="pmeta">${e.kind}·${e.product_count}db·${escapeHtml(e.origin || "")}</span>`;
  const lab = `<span class="plabel ${cls}${inh}">${escapeHtml(e.name)} ${meta}</span>`;
  return `<div class="prow ${side} ${cls}" title="${escapeAttr(e.origin || "")}">${side === "src" ? lab + dot : dot + lab}</div>`;
}

function onDot(side, name) {
  if (side === "src") {
    if (MAP_CONN.some((c) => c.src === name)) {
      MAP_CONN = MAP_CONN.filter((c) => c.src !== name);   // kötés bontása
      MAP_ARMED = null;
    } else {
      MAP_ARMED = MAP_ARMED === name ? null : name;        // felhúzás
    }
  } else {
    if (MAP_ARMED) {
      MAP_CONN = MAP_CONN.filter((c) => c.src !== MAP_ARMED);
      MAP_CONN.push({ src: MAP_ARMED, dst: name });
      MAP_ARMED = null;
    } else {
      MAP_CONN = MAP_CONN.filter((c) => c.dst !== name);   // a célba futó kötések bontása
    }
  }
  renderMapping();
}

function drawLines() {
  const svg = document.querySelector("#mapwrap .maplines");
  if (!svg) return;
  const cols = svg.parentElement;
  const box = cols.getBoundingClientRect();
  svg.setAttribute("width", box.width);
  svg.setAttribute("height", box.height);
  let html = "";
  for (const c of MAP_CONN) {
    const sd = SRC_DOTS[c.src], dd = TGT_DOTS[c.dst];
    if (!sd || !dd) continue;
    const a = sd.getBoundingClientRect(), b = dd.getBoundingClientRect();
    const x1 = a.left + a.width / 2 - box.left, y1 = a.top + a.height / 2 - box.top;
    const x2 = b.left + b.width / 2 - box.left, y2 = b.top + b.height / 2 - box.top;
    const mx = (x1 + x2) / 2;
    html += `<path d="M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}" class="cline"/>`;
  }
  svg.innerHTML = html;
}

function formMoveNode() {
  if (!SOURCE) return `<p class="hint">Jelölj ki egy <b>Forrás</b> node-ot (fő/al/altípus).</p>`;
  const sl = SOURCE.length;
  let html = `<p class="hint">A forrás node (és minden alatta lévő terméke) átkerül a cél helyére.
    Ha a célon már van azonos nevű node, <b>összeolvad</b> vele (tulajdonság-listák uniója).</p>`;
  html += `<label>Cél szülő / node (a fában a „Cél" gombbal)</label>
    <input id="mn-target" readonly value="${TARGET ? pathStr(TARGET) : ""}">`;
  // új név meghatározása
  let suggest = SOURCE[sl - 1];
  if (TARGET && TARGET.length === sl) suggest = TARGET[sl - 1];
  html += `<label>Új név a cél szinten (${["fő", "al", "altípus"][sl - 1]}kategória neve)</label>
    <input id="mn-name" value="${escapeAttr(suggest)}">`;
  html += `<p class="hint">Tipp: a célhoz a forrással <b>azonos szintet</b> jelölj ki (összeolvasztás),
    vagy <b>egy szinttel feljebbit</b> (oda kerül új gyerekként).</p>`;
  return html;
}

function formDissolve() {
  if (!SOURCE) return `<p class="hint">Jelölj ki egy <b>Forrás</b> altípust (vagy alkategóriát) a feloldáshoz.</p>`;
  if (SOURCE.length < 2) return `<p class="hint">Fő­kategóriát nem lehet feloldani. Válassz altípust/alkategóriát.</p>`;
  const parent = SOURCE.slice(0, -1);
  return `<p class="hint">A(z) <b>${escapeHtml(SOURCE[SOURCE.length - 1])}</b> megszűnik:
    tulajdonságai a szülőbe (<b>${escapeHtml(pathStr(parent))}</b>) olvadnak, a termékei pedig
    közvetlenül a szülőhöz kerülnek (a megfelelő szint kiürül).</p>`;
}

function formMoveProp() {
  if (!SOURCE) return `<p class="hint">Jelölj ki egy <b>Forrás</b> node-ot, majd egy tulajdonság-chipet fent.</p>`;
  if (!SEL_PROP) return `<p class="hint">Kattints a FORRÁS dobozban egy tulajdonság-chipre.
    Lista esetén megadhatsz egyetlen értéket is.</p>`;
  const tgtNode = TARGET || SOURCE;
  const valLine = SEL_VALUE
    ? `<label>Csak ezt az értéket viszi át</label><input id="mp-value" value="${escapeAttr(SEL_VALUE)}">
       <label>Új érték neve (átnevezés, üres = változatlan)</label><input id="mp-newval" value="">`
    : "";
  return `<p class="hint">Forrás tulajdonság: <b>${escapeHtml(SEL_PROP.name)}</b>
    (${SEL_PROP.group}/${SEL_PROP.kind})${SEL_VALUE ? `, érték: <b>${escapeHtml(SEL_VALUE)}</b>` : ", az egész tulajdonság"}.</p>
    <label>Cél node (alapból a Cél kijelölés, vagy maga a forrás = átnevezés)</label>
    <input id="mp-target" readonly value="${escapeAttr(pathStr(tgtNode))}">
    <label>Cél tulajdonság neve</label>
    <input id="mp-prop" value="${escapeAttr(SEL_PROP.name)}">
    <label>Cél csoport</label>
    <select id="mp-group">
      <option value="${SEL_PROP.group}">${SEL_PROP.group}</option>
      <option value="${SEL_PROP.group === "egyedi" ? "csoportos" : "egyedi"}">${SEL_PROP.group === "egyedi" ? "csoportos" : "egyedi"}</option>
    </select>
    ${valLine}`;
}

function formCreateProp() {
  if (!SOURCE) return `<p class="hint">Jelölj ki egy <b>Forrás</b> node-ot, amibe az új tulajdonság kerül.</p>`;
  return `<p class="hint">Új tulajdonság a(z) <b>${escapeHtml(pathStr(SOURCE))}</b> node-on (termékek érintetlenek).</p>
    <label>Csoport</label>
    <select id="cp-group"><option value="egyedi">egyedi</option><option value="csoportos">csoportos</option></select>
    <label>Típus</label>
    <select id="cp-kind"><option value="lista">lista</option><option value="flag">flag (igen/nem)</option></select>
    <label>Név</label><input id="cp-name" placeholder="pl. forma">
    <label>Értékek listához (vesszővel; flagnél hagyd üresen)</label>
    <input id="cp-values" placeholder="pl. kerek, hosszúkás, egyéb">`;
}

// ---------------------------------------------------------------- payload
function buildPayload() {
  if (ACTIVE_OP === "merge_mapping") {
    if (!SOURCE || !TARGET) throw "Jelölj ki forrás és cél node-ot.";
    if (key(SOURCE) === key(TARGET)) throw "A forrás és a cél azonos.";
    return { op: "merge_mapping", source: SOURCE, target: TARGET, mappings: MAP_CONN };
  }
  // (eltérő szintű forrás/cél is megengedett a merge_mapping-nél)
  if (ACTIVE_OP === "move_node") {
    if (!SOURCE) throw "Nincs forrás.";
    if (!TARGET) throw "Nincs cél node kijelölve.";
    const sl = SOURCE.length;
    const name = ($("#mn-name").value || "").trim();
    if (!name) throw "Adj nevet a cél szinten.";
    let target;
    if (TARGET.length === sl) target = TARGET.slice(0, -1).concat([name]);
    else if (TARGET.length === sl - 1) target = TARGET.concat([name]);
    else throw `A cél szintje nem illik a forráshoz (forrás ${sl} szint). ` +
      `Jelölj azonos vagy eggyel feljebbi szintet.`;
    return { op: "move_node", source: SOURCE, target };
  }
  if (ACTIVE_OP === "dissolve") {
    if (!SOURCE || SOURCE.length < 2) throw "Jelölj ki altípust/alkategóriát.";
    return { op: "dissolve", source: SOURCE };
  }
  if (ACTIVE_OP === "move_property") {
    if (!SOURCE || !SEL_PROP) throw "Jelölj ki forrás node-ot és tulajdonságot.";
    const target = TARGET || SOURCE;
    const body = {
      op: "move_property", source: SOURCE, source_prop: SEL_PROP.name,
      target, target_prop: ($("#mp-prop").value || SEL_PROP.name).trim(),
      group: $("#mp-group").value, kind: SEL_PROP.kind === "flag" ? "flag" : "lista",
    };
    if (SEL_VALUE) {
      body.value = ($("#mp-value").value || SEL_VALUE).trim();
      const nv = ($("#mp-newval").value || "").trim();
      if (nv) body.new_value = nv;
    }
    return body;
  }
  if (ACTIVE_OP === "create_property") {
    if (!SOURCE) throw "Jelölj ki node-ot.";
    const name = ($("#cp-name").value || "").trim();
    if (!name) throw "Adj nevet a tulajdonságnak.";
    const kind = $("#cp-kind").value;
    const values = kind === "lista"
      ? ($("#cp-values").value || "").split(",").map((s) => s.trim()).filter(Boolean)
      : [];
    return { op: "create_property", node: SOURCE, group: $("#cp-group").value, name, kind, values };
  }
  throw "Ismeretlen művelet.";
}

// ---------------------------------------------------------------- gombok
$("#preview-btn").onclick = async () => {
  let payload;
  try { payload = buildPayload(); } catch (e) { return setResult(String(e), "err"); }
  setResult("Előnézet számítása…", "");
  const r = await fetch("/api/preview", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const j = await r.json();
  if (j.error) { $("#apply-btn").disabled = true; return setResult("HIBA: " + j.error, "err"); }
  LAST_PAYLOAD = payload;
  $("#apply-btn").disabled = false;
  setResult(summaryText(j, false), "ok");
};

let LAST_PAYLOAD = null;
$("#apply-btn").onclick = async () => {
  if (!LAST_PAYLOAD) return;
  if (!confirm("Biztosan ÍROD a fájlokat? A művelet a kategoriak_*.json és eredmeny.json fájlt felülírja.")) return;
  setResult("Mentés…", "");
  const r = await fetch("/api/apply", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(LAST_PAYLOAD),
  });
  const j = await r.json();
  if (j.error) return setResult("HIBA: " + j.error, "err");
  $("#apply-btn").disabled = true;
  setResult("✔ KÉSZ — fájlok mentve.\n\n" + summaryText(j, true), "done");
  SOURCE = TARGET = SEL_PROP = SEL_VALUE = LAST_PAYLOAD = null;
  MAP_KEY = null; MAP_CONN = []; MAP_SRC = []; MAP_TGT = []; MAP_ARMED = null;
  await loadData();
};

function summaryText(j, applied) {
  const lines = [];
  lines.push(`Művelet: ${j.op}`);
  if (j.tree_action) lines.push(`Fa: ${j.tree_action}`);
  lines.push(`Érintett termékek: ${j.affected_products}`);
  if (j.source) lines.push(`Forrás: ${pathStr(j.source)}`);
  if (j.target) lines.push(`Cél:    ${pathStr(j.target)}`);
  if (j.mapped) {
    lines.push(`\nÖsszekötött tulajdonságok (${j.mapped.length}):`);
    for (const m of j.mapped) lines.push(`  ${m.src}  →  ${m.dst}`);
  }
  if (j.deleted && j.deleted.length) {
    lines.push(`\nTörölt (bekötetlen forrás) tulajdonságok (${j.deleted.length}):`);
    lines.push("  " + j.deleted.join(", "));
  }
  if (!applied) lines.push(`\n(Ez csak előnézet — semmit nem írtunk. Az „Alkalmaz" ír.)`);
  return lines.join("\n");
}

function setResult(text, cls) {
  const el = $("#result");
  el.textContent = text;
  el.className = cls || "";
}

// ---------------------------------------------------------------- gondok
function renderIssues() {
  const box = $("#issues");
  box.innerHTML = "";
  if (!DATA.issues || !DATA.issues.length) {
    box.innerHTML = `<div class="issue">Nincs talált gond. 🎉</div>`;
    $("#issues-box > summary").textContent = "Talált gondok (0)";
    return;
  }
  $("#issues-box > summary").textContent = `Talált gondok (${DATA.issues.length})`;
  for (const iss of DATA.issues) {
    const d = document.createElement("div");
    d.className = "issue";
    d.innerHTML = `<span class="itag ${iss.type}">${iss.type}</span>${escapeHtml(iss.text)}`;
    d.onclick = () => {
      SOURCE = iss.path; afterSelect();
      // nyissuk ki az őseit és görgessünk
      for (let i = 1; i <= iss.path.length; i++) EXPANDED.add(key(iss.path.slice(0, i)));
      renderTree();
    };
    box.appendChild(d);
  }
}

// ---------------------------------------------------------------- util
function escapeHtml(s) { return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])); }
function escapeAttr(s) { return escapeHtml(s).replace(/"/g, "&quot;"); }

$("#search").oninput = renderTree;
$("#hide-empty").onchange = renderTree;
$("#reload").onclick = loadData;
window.addEventListener("resize", () => { if (ACTIVE_OP === "merge_mapping") drawLines(); });

loadData();
