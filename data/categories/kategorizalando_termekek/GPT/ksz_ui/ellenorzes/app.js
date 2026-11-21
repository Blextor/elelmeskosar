"use strict";

const $ = id => document.getElementById(id);
const PAGE = 25;
const number = n => n.toLocaleString("hu-HU");
const markLabels = {todo: "Ellenőrizetlen", ok: "Rendben", fix: "Javítandó"};
let rows = [], visible = [], selected = null, page = 0, marks = {}, storageKey = "";
let changesOnly = true, activeSource = "", draft, requestId = 0, storageWarning = "";

function el(tag, text, cls) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (cls) node.className = cls;
  return node;
}
function btn(text, fn, cls) {
  const node = el("button", text, cls);
  node.type = "button"; node.onclick = fn;
  return node;
}
function norm(value) {
  return String(value ?? "").normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
}
function equal(a, b) {
  if (a === b) return true;
  if (!a || !b || typeof a !== "object" || typeof b !== "object" || Array.isArray(a) !== Array.isArray(b)) return false;
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every(k => Object.hasOwn(b, k) && equal(a[k], b[k]));
}
function fields(r) {
  return [...new Set([...Object.keys(r.before || {}), ...Object.keys(r.after)])].map(name => {
    const old = Object.hasOwn(r.before || {},name) ? r.before[name] : undefined;
    const next = Object.hasOwn(r.after,name) ? r.after[name] : undefined;
    let status = "Azonos";
    if (r.before === null && r.old !== null) status = "Korábbi érték ismeretlen";
    else if (!Object.hasOwn(r.before || {}, name)) status = "Új";
    else if (!Object.hasOwn(r.after, name)) status = "Törölt";
    else if (!equal(old, next)) status = "Módosult";
    return {name, old, next, status};
  }).sort((a, b) => (a.status === "Azonos") - (b.status === "Azonos") || a.name.localeCompare(b.name, "hu"));
}

async function fetchJSON(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw Error(data.error || "A kiszolgáló nem tudta betölteni az adatokat.");
  return data;
}
function fillSelect(id, label, values) {
  $(id).replaceChildren(new Option(label, ""));
  for (const val of [...new Set(values.filter(Boolean))].sort((a,b) => a.localeCompare(b,"hu"))) {
    $(id).add(new Option(val, val));
  }
}
function readMarks() {
  try { return JSON.parse(localStorage.getItem(storageKey)) || {}; } catch { return {}; }
}
function show(data, source) {
  activeSource = source;
  $("reports").value = source;
  for (const r of data.rows) {
    r.key = JSON.stringify([r.store, r.id]);
    r.search = norm([r.name, r.store, r.id, r.brand, ...(r.old || []), ...r.new].join(" "));
    r.moved = !equal(r.old, r.new);
    r.changed = r.before !== null && !equal(r.before, r.after);
    r.exception = Boolean(r.reason);
  }
  rows = data.rows;
  storageKey = "besorolas-ellenorzes:" + data.version;
  marks = readMarks(); storageWarning = "";
  $("search").value = ""; $("kind").value = ""; $("state").value = "";
  fillSelect("store", "Minden bolt", rows.map(r => r.store));
  fillSelect("old-cat", "Minden alkategória", rows.map(r => r.old?.[1]));
  fillSelect("new-cat", "Minden alkategória", rows.map(r => r.new[1]));
  $("error").hidden = true;
  selected = null;
  filter();
}
function filter() {
  const q = norm($("search").value.trim()), kind = $("kind").value, state = $("state").value;
  visible = rows.filter(r => r.search.includes(q) &&
    (!state || (marks[r.key] || "todo") === state) &&
    (!$("store").value || r.store === $("store").value) &&
    (!$("old-cat").value || r.old?.[1] === $("old-cat").value) &&
    (!$("new-cat").value || r.new[1] === $("new-cat").value) &&
    (!kind || {path: r.moved, props: r.changed, exception: r.exception,
      same: r.before !== null && !r.moved && !r.changed}[kind]));
  const index = visible.indexOf(selected);
  if (index < 0) selected = visible[0] || null;
  page = Math.max(0, Math.floor(index / PAGE));
  draw();
}
function choose(index) {
  if (index < 0 || index >= visible.length) return;
  selected = visible[index]; page = Math.floor(index / PAGE);
  draw();
  $("list").querySelector('[aria-current="true"]')?.scrollIntoView({block:"nearest",container:"nearest"});
}
function photo(r, big) {
  const box = el(big && r.image ? "button" : "span", undefined, big ? "photo" : "thumb");
  if (!r.image) { box.textContent = big ? "Nincs termékfotó" : "—"; return box; }
  const url = "/api/ellenorzes/kep?utvonal=" + encodeURIComponent(r.image);
  const img = el("img"); img.alt = big ? r.name : ""; img.loading = big ? "eager" : "lazy";
  img.onerror = () => {
    box.textContent = big ? "A kép nem érhető el" : "—";
    if (big) box.disabled = true;
  };
  img.src = url; box.append(img);
  if (big) {
    box.title = "Termékfotó nagyítása"; box.setAttribute("aria-label", box.title);
    box.append(el("span","Nagyítás","photo-hint"));
    box.onclick = () => { $("large").src = url; $("large").alt = r.name; $("zoom").showModal(); };
  }
  return box;
}
function draw() {
  const reviewed = rows.reduce((sum,r) => sum + Number(Boolean(marks[r.key])), 0);
  const prefix = activeSource === "@draft" ? number(draft.data.compared) + " összevetett termék · " : "";
  $("summary").textContent = prefix + number(rows.length) + (activeSource === "@draft" ? " eltérés" : " termék") +
    " · " + number(reviewed) + " ellenőrizve" + storageWarning;
  $("count").textContent = number(visible.length);
  const start = page * PAGE;
  const list = $("list"); list.replaceChildren();
  for (const [i,r] of visible.slice(start, start + PAGE).entries()) {
    const item = btn("", () => choose(start+i), "product");
    item.setAttribute("aria-current", String(selected === r));
    const info = el("span"); info.append(el("strong",r.name), el("small",[r.store,marks[r.key] ? markLabels[marks[r.key]] : r.new[1]].filter(Boolean).join(" · ")));
    item.append(photo(r,false),info); list.append(item);
  }
  if (!visible.length) list.append(el("p","Nincs találat.","empty"));
  $("page-info").textContent = visible.length ? (start+1) + "–" + Math.min(start+PAGE,visible.length) + " / " + number(visible.length) : "0 termék";
  $("prev-page").disabled = page === 0; $("next-page").disabled = start + PAGE >= visible.length;
  drawDetail();
}
function mark(value) {
  if (!selected) return;
  const original = selected;
  const pos = visible.indexOf(original);
  if (!storageWarning) marks = readMarks();
  if (marks[original.key] === value) delete marks[original.key];
  else marks[original.key] = value;
  try { localStorage.setItem(storageKey,JSON.stringify(marks)); }
  catch { storageWarning = " · A jelölések csak ezen a megnyitott lapon érhetők el."; }
  filter();
  if (!visible.includes(original) && visible.length) choose(Math.min(pos,visible.length-1));
}
function route(title, path, css) {
  const node = el("div",undefined,"route "+css);
  const parts = (path || []).filter(Boolean);
  node.append(el("small",title));
  if (parts.length > 1) node.append(el("div",parts.slice(0,-1).join(" › "),"parents"));
  node.append(el("strong",parts.at(-1) || (path ? "Besorolatlan" : "Új termék")));
  return node;
}
function valueCell(value, other, side, unknown) {
  const cell = el("td");
  if (unknown || value === undefined) {
    cell.append(el("span",unknown ? "Nincs korábbi adat" : "Nincs megadva","missing")); return cell;
  }
  const values = Array.isArray(value) ? value : [value];
  const others = Array.isArray(other) ? other : [other];
  const wrap = el("div",undefined,"values");
  for (const v of values) {
    const text = v === null ? "null" : v === "" ? "Üres szöveg" : typeof v === "boolean" ? (v ? "Igen" : "Nem") :
      typeof v === "object" ? JSON.stringify(v) : String(v);
    wrap.append(el("span", text, "chip " + (!unknown && others.every(x => !equal(x,v)) ? side : "")));
  }
  if (!values.length) wrap.append(el("span","Üres lista","missing"));
  cell.append(wrap);
  if (other !== undefined && (Array.isArray(value) !== Array.isArray(other) || typeof value !== typeof other)) {
    const type = Array.isArray(value) ? "Lista" : ({boolean:"Igen/nem",number:"Szám",string:"Szöveg"}[typeof value] || "Érték");
    cell.append(el("small",type,"shape"));
  }
  return cell;
}
function attributes(r) {
  const section = el("div",undefined,"card block");
  const head = el("div",undefined,"spread prop-head");
  const all = fields(r), changed = all.filter(f => f.status !== "Azonos");
  const unknown = r.before === null && r.old !== null;
  head.append(el("h2", "Tulajdonságok" + (unknown ? "" : " · " + changed.length + " eltérés")));
  const label = el("label"), check = el("input"); check.type="checkbox"; check.checked=changesOnly;
  label.append(check,document.createTextNode("Csak eltérések")); head.append(label); section.append(head);
  const content=el("div",undefined,"table-scroll"); section.append(content);
  function renderTable() {
    content.replaceChildren();
    const shown = changesOnly ? changed : all;
    if (!shown.length) {
      content.append(el("p",all.length ? "Minden tulajdonság megegyezik. A kapcsolóval megjelenítheted az azonos értékeket is." : "Nincsenek rögzített tulajdonságok.","empty"));
      return;
    }
    const table=el("table"), header=table.createTHead().insertRow(), body=table.createTBody();
    for (const title of ["Tulajdonság","Korábbi érték","Új érték"]) header.append(el("th",title));
    for (const f of shown) {
      const row=body.insertRow(), name=el("td"); name.append(el("span",f.name,"field-name"),el("small",f.status,"field-status"));
      row.append(name,valueCell(f.old,f.next,"lost",unknown),valueCell(f.next,f.old,unknown ? "" : "gained",false));
    }
    content.append(table);
  }
  check.onchange=()=>{changesOnly=check.checked;renderTable();};
  renderTable();
  return section;
}
function drawDetail() {
  const detail=$("detail"); detail.replaceChildren();
  const r=selected;
  if (!r) {
    detail.append(el("p",rows.length ? "A szűrők módosításával választhatsz másik terméket." :
      activeSource === "@draft" ? "A tervezetben szereplő besorolások és tulajdonságok megegyeznek a jelenlegi adatokkal." : "Nincs megjeleníthető termék.","card empty"));
    return;
  }
  const card=el("div",undefined,"card"),hero=el("div",undefined,"hero"),info=el("div");
  const badges=el("div",undefined,"badges");
  badges.append(el("span",r.store || "Ismeretlen bolt","badge"));
  if (r.exception) badges.append(el("span","Kivétel","badge warn"));
  info.append(badges,el("h2",r.name));
  info.append(el("div",[r.brand,r.size,"Bolti azonosító: "+r.id].filter(Boolean).join(" · "),"meta"));
  if (r.aisle) info.append(el("p","Bolti kategória: "+r.aisle,"source-path"));
  if (r.imageSource && r.imageSource !== "Helyi kép") info.append(el("small","Képforrás: "+r.imageSource));
  hero.append(photo(r,true),info);card.append(hero);
  if (r.reason) card.append(el("p",r.reason,"reason"));
  const actions=el("div",undefined,"review-actions"), buttons=el("div",undefined,"badges");
  for (const [key,title,cls] of [["ok","Rendben","active-ok"],["fix","Javítandó","active-fix"]]) {
    const b=btn(title,()=>mark(key),marks[r.key]===key ? cls : "");
    b.setAttribute("aria-pressed",String(marks[r.key]===key));buttons.append(b);
  }
  const nav=el("div",undefined,"badges"), pos=visible.indexOf(r);
  const prev=btn("‹",()=>choose(pos-1),"navbtn"),next=btn("›",()=>choose(pos+1),"navbtn");
  prev.setAttribute("aria-label","Előző termék");next.setAttribute("aria-label","Következő termék");
  prev.disabled=pos<=0;next.disabled=pos>=visible.length-1;
  nav.append(prev,el("small",(pos+1)+" / "+number(visible.length)),next); actions.append(buttons,nav);card.append(actions);
  const paths=el("div",undefined,"card block"), head=el("div",undefined,"spread");
  head.append(el("h2","Besorolás"),el("small",r.moved ? "Megváltozott" : "Azonos útvonal"));
  const columns=el("div",undefined,"routes"); columns.append(route("Korábbi besorolás",r.old,"old"),route("Új besorolás",r.new,"new"));
  paths.append(head,columns); detail.append(card,paths,attributes(r));
}
function showError(error) { $("error").hidden=false; $("error").textContent=error.message; }
async function loadReport(key) {
  const req=++requestId;
  if (key==="@draft" && draft) return show(draft.data,key);
  $("summary").textContent="Változásjegyzék betöltése…";
  try {
    const data=await fetchJSON("/api/ellenorzes/jegyzek?nev="+encodeURIComponent(key));
    if (req===requestId) show(data,key);
  } catch(error) {
    if (req!==requestId) return;
    $("reports").value=activeSource; draw(); showError(error);
  }
}
for(const id of ["kind","state","store","old-cat","new-cat"]) $(id).onchange=filter;
$("search").oninput=filter;
$("prev-page").onclick=()=>choose((page-1)*PAGE);$("next-page").onclick=()=>choose((page+1)*PAGE);
$("reports").onchange=()=>loadReport($("reports").value);
$("open-draft").onclick=()=>{$("upload-error").textContent="";$("draft").showModal();};
for(const close of document.querySelectorAll("[data-close]")) close.onclick=()=>close.closest("dialog").close();
$("upload").onsubmit=async event=>{
  event.preventDefault();
  const file=$("file").files[0]; if(!file) return;
  const req=++requestId;
  $("compare").disabled=true; $("compare").textContent="Összevetés folyamatban…";$("upload-error").textContent="";
  try {
    const data=await fetchJSON("/api/ellenorzes/tervezet",{method:"POST",headers:{"Content-Type":"application/json"},body:file});
    if (req!==requestId || !$("draft").open) return;
    draft={data};
    $("reports").querySelector('option[value="@draft"]')?.remove();
    $("reports").add(new Option(file.name,"@draft"));show(data,"@draft");$("draft").close();
  } catch(error){$("upload-error").textContent=error.message;}
  finally{$("compare").disabled=false;$("compare").textContent="Összevetés";}
};
window.addEventListener("storage",event=>{if(event.key===storageKey){marks=readMarks();filter();}});
async function init() {
  try {
    const keys=await fetchJSON("/api/ellenorzes/jegyzekek");
    for(const key of keys) {
      const label=key === "fagyasztott_aruk_luna_20261121" ? "Fagyasztott áruk · Luna · 2026. 11. 21." : key.replaceAll("_"," ");
      $("reports").add(new Option(label,key));
    }
    if(keys.length) await loadReport(keys[0]);
    else {draw();$("summary").textContent="Az első összevetéshez nyiss meg egy tervezetet.";}
  } catch(error){showError(error);$("summary").textContent="A jegyzékek betöltése sikertelen.";}
}
init();
