"use strict";

const $ = id => document.getElementById(id);
const childKeys = ["", "alkategóriák", "altípusok"];
const levelNames = ["Teljes fa", "Főkategória", "Alkategória", "Altípus"];
const groups = ["egyedi", "csoportos"];
const noteKey = "tulajdonságmegjegyzések";
const cacheKey = "reszfa-tervezo-v1";
let source, tree, version, selection = [], dirty = false, persisted = false, editing;

function element(tag, label, css) {
  const item = document.createElement(tag);
  if (label !== undefined) item.textContent = label;
  if (css) item.className = css;
  return item;
}

function button(label, action, css) {
  const item = element("button", label, css);
  item.type = "button";
  item.onclick = action;
  return item;
}

// Category and property names are user data, including names of built-in object members.
function put(container, name, value) {
  Object.defineProperty(container, name, {value, writable: true, configurable: true, enumerable: true});
}

function ensure(container, name) {
  if (!Object.hasOwn(container, name)) put(container, name, {});
  return container[name];
}

function nodeAt(path) {
  let children = tree, node;
  for (const [index, name] of path.entries()) {
    if (!children || !Object.hasOwn(children, name)) throw new Error("Az útvonal nem található.");
    node = children[name];
    children = node[childKeys[index + 1]];
  }
  return node;
}

function childrenAt(path) {
  if (!path.length) return tree;
  return nodeAt(path)[childKeys[path.length]] || {};
}

function selectPath(path) {
  selection = path;
  $("search").value = "";
  render();
  document.querySelector("article").scrollTop = 0;
}

function renderTree() {
  const nav = $("tree");
  nav.replaceChildren();
  const query = $("search").value.trim().toLocaleLowerCase("hu");
  const home = button("Teljes fa", () => selectPath([]), selection.length ? "" : "selected");
  nav.append(home);
  let matches = 0;
  function visit(nodes, parent, target) {
    for (const [name, node] of Object.entries(nodes)) {
      const path = [...parent, name];
      const onPath = path.every((part, index) => selection[index] === part);
      if (!query || name.toLocaleLowerCase("hu").includes(query)) {
        const link = button(query ? path.join(" › ") : name, () => selectPath(path),
                            onPath && path.length === selection.length ? "selected" : "");
        if (link.className) link.setAttribute("aria-current", "true");
        target.append(link);
        matches++;
      }
      const children = node[childKeys[path.length]];
      if (children && (query || onPath)) {
        const nested = query ? target : element("div", undefined, "nested");
        if (!query) target.append(nested);
        visit(children, path, nested);
      }
    }
  }
  visit(tree, [], nav);
  if (query && !matches) nav.append(element("small", "Nincs találat."));
}

function payload() {
  return selection.length ? {[selection.at(-1)]: nodeAt(selection)} : tree;
}

function persist() {
  dirty = true;
  try {
    sessionStorage.setItem(cacheKey, JSON.stringify({tree, version, selection}));
    persisted = true;
  } catch {
    persisted = false;
    // Never restore an older snapshot as though the last edit had been saved.
    try { sessionStorage.removeItem(cacheKey); } catch {}
  }
  render();
}

function panel(title, action) {
  const section = element("section", undefined, "panel");
  const head = element("div", undefined, "section-head");
  head.append(element("h3", title));
  if (action) head.append(action);
  section.append(head);
  return section;
}

function renderProperties(section, path, inherited) {
  const node = nodeAt(path);
  let count = 0;
  for (const group of groups) {
    for (const [name, value] of Object.entries(node.tulajdonságok?.[group] || {})) {
      count++;
      const item = element("div", undefined, "entry");
      const row = element("div", undefined, "row");
      const key = element("div");
      key.append(element("strong", name), element("small", typeLabel(group, value)));
      row.append(key);
      if (!inherited) {
        const tools = element("div", undefined, "tools");
        tools.append(button("Szerkesztés", () => openEditor({type: "property", group, name})),
                     button("Törlés", () => removeProperty(group, name), "danger"));
        row.append(tools);
      }
      item.append(row);
      if (Array.isArray(value)) {
        const chips = element("div", undefined, "chips");
        for (const option of value) chips.append(element("span", String(option), "chip"));
        if (!value.length) chips.append(element("small", "Nincs megadott érték."));
        if (value.length > 8) {
          const details = element("details");
          details.append(element("summary", value.length + " lehetséges érték"), chips);
          item.append(details);
        } else item.append(chips);
      }
      const notes = node[noteKey];
      if (group === "csoportos" && notes && Object.hasOwn(notes, name)) {
        item.append(element("p", notes[name], "note"));
      }
      section.append(item);
    }
  }
  if (!count) section.append(element("p", "Itt nincs saját tulajdonság.", "muted"));
}

function typeLabel(group, value) {
  if (group === "csoportos") return "Lista · több választás";
  return Array.isArray(value) ? "Egyedi · fix lehetőségek" : "Egyedi · igen/nem";
}

function render() {
  renderTree();
  const message = dirty ? (persisted ? "Vázlat mentve ezen a böngészőlapon." :
    "A vázlat csak a memóriában van. Bezárás előtt töltsd le a JSON-t.") : "Forrásfa betöltve.";
  $("status").textContent = source.fajl + " · " + message +
    (version !== source.verzio ? " A forrásfájl a vázlat indítása óta változott." : "");
  $("reset").disabled = !dirty;
  $("export").disabled = false;
  $("export").textContent = selection.length ? "Részfa letöltése" : "Teljes fa letöltése";
  const workspace = $("workspace");
  workspace.replaceChildren();
  if (selection.length) {
    const crumbs = element("div", undefined, "crumbs");
    crumbs.append(button("Teljes fa", () => selectPath([])));
    selection.slice(0, -1).forEach((part, i) => {
      crumbs.append(element("span", "›"), button(part, () => selectPath(selection.slice(0, i + 1))));
    });
    crumbs.append(element("span", "› " + levelNames[selection.length]));
    workspace.append(crumbs);
  }
  workspace.append(element("h2", selection.at(-1) || "Teljes kategóriafa", "title"));
  if (selection.length) {
    const actions = element("div", undefined, "tools");
    actions.append(button("Átnevezés", () => openEditor({type: "rename", name: selection.at(-1)})));
    if (selection.length > 1) actions.append(button("Áthelyezés", () => openEditor({type: "move", name: selection.at(-1)})));
    actions.append(button("Ág törlése", removeBranch, "danger"));
    workspace.append(actions);
  }
  if (selection.length < 3) {
    const names = Object.keys(childrenAt(selection));
    const section = panel(["Főkategóriák", "Alkategóriák", "Altípusok"][selection.length] + " · " + names.length,
      button("+ " + levelNames[selection.length + 1], () => openEditor({type: "add"})));
    const list = element("div", undefined, "chips");
    for (const name of names) list.append(button(name, () => selectPath([...selection, name])));
    if (!names.length) list.append(element("small", "Ez az ág üres."));
    section.append(list);
    workspace.append(section);
  }
  if (selection.length) {
    const section = panel("Saját tulajdonságok", button("+ Tulajdonság", () => openEditor({type: "property"})));
    renderProperties(section, selection, false);
    workspace.append(section);
    for (let depth = selection.length - 1; depth > 0; depth--) {
      const ancestor = selection.slice(0, depth);
      const details = element("details", undefined, "panel");
      details.append(element("summary", "Örökölt tulajdonságok · " + ancestor.at(-1)),
                     button("Szerkesztés a felmenőn", () => selectPath(ancestor)));
      details.addEventListener("toggle", () => {
        if (details.open && !details.dataset.loaded) {
          renderProperties(details, ancestor, true);
          details.dataset.loaded = "1";
        }
      });
      workspace.append(details);
    }
  }
  const preview = element("details", undefined, "panel");
  preview.append(element("summary", "Exportálandó JSON"));
  preview.ontoggle = () => {
    if (preview.open && !preview.querySelector("pre")) preview.append(element("pre", JSON.stringify(payload(), null, 2)));
  };
  workspace.append(preview);
}

function kindFields() {
  $("value-fields").hidden = $("kind").value === "flag";
  $("note-fields").hidden = $("kind").value !== "multi";
}

function openEditor(options) {
  editing = options;
  $("form").reset();
  $("error").textContent = "";
  const property = options.type === "property";
  $("dialog-title").textContent = property ? (options.name ? "Tulajdonság szerkesztése" : "Új tulajdonság") :
    ({rename: "Ág átnevezése", move: "Ág áthelyezése"}[options.type] ||
      "Új " + levelNames[selection.length + 1]);
  $("prop-fields").hidden = !property;
  $("parent-field").hidden = options.type !== "move";
  if (options.type === "move") {
    const select = $("parent");
    select.replaceChildren();
    for (const main of Object.keys(tree)) {
      const paths = selection.length === 2 ? [[main]] :
        Object.keys(childrenAt([main])).map(sub => [main, sub]);
      for (const path of paths) select.add(new Option(path.join(" › "), JSON.stringify(path)));
    }
    select.value = JSON.stringify(selection.slice(0, -1));
  }
  $("name").value = options.name ?? "";
  if (property && options.group) {
    const node = nodeAt(selection);
    const value = node.tulajdonságok[options.group][options.name];
    $("kind").value = options.group === "csoportos" ? "multi" : Array.isArray(value) ? "single" : "flag";
    if (Array.isArray(value)) $("values").value = value.join("\n");
    if (options.group === "csoportos" && Object.hasOwn(node[noteKey] || {}, options.name)) {
      $("note").value = node[noteKey][options.name];
    }
  }
  kindFields();
  $("editor").showModal();
  $("name").focus();
  $("name").select();
}

function removeNote(node, name) {
  if (node[noteKey]) {
    delete node[noteKey][name];
    if (!Object.keys(node[noteKey]).length) delete node[noteKey];
  }
}

function removeProperty(group, name) {
  if (!confirm("Törlöd a vázlatból ezt a tulajdonságot az értékeivel együtt?\n" + name)) return;
  const node = nodeAt(selection);
  delete node.tulajdonságok[group][name];
  if (group === "csoportos") removeNote(node, name);
  persist();
}

function removeBranch() {
  if (!confirm("Törlöd a vázlatból a teljes ágat a gyerekeivel együtt?\n" + selection.join(" › "))) return;
  const name = selection.at(-1);
  selection = selection.slice(0, -1);
  delete childrenAt(selection)[name];
  persist();
}

function editedValues(previous) {
  const original = Array.isArray(previous) ? previous : [];
  const raw = $("values").value;
  if (raw === original.join("\n")) return original;
  const lines = raw.split("\n").map(line => line.trim()).filter(Boolean);
  if (new Set(lines).size !== lines.length) throw new Error("Minden lehetséges értéket csak egyszer adj meg.");
  return lines.map(line => {
    const known = original.find(value => String(value) === line);
    if (known !== undefined) return known;
    if (original.length && original.every(value => typeof value === "number") && /^-?\d+$/.test(line)) {
      const number = Number(line);
      if (Number.isSafeInteger(number)) return number;
    }
    return line;
  });
}

function saveProperty(name) {
  const node = nodeAt(selection);
  const props = node.tulajdonságok || {};
  const kind = $("kind").value;
  const group = kind === "multi" ? "csoportos" : "egyedi";
  const sameKey = editing.group === group && editing.name === name;
  if (!sameKey && groups.some(g => Object.hasOwn(props[g] || {}, name) &&
      !(editing.group === g && editing.name === name))) throw new Error("Ilyen nevű tulajdonság már van ezen a szinten.");
  const previous = editing.group ? props[editing.group][editing.name] : undefined;
  const value = kind === "flag" ? {} : editedValues(previous);
  if (editing.group && !sameKey) delete props[editing.group][editing.name];
  if (editing.group === "csoportos") removeNote(node, editing.name);
  put(ensure(ensure(node, "tulajdonságok"), group), name, value);
  if (group === "csoportos" && $("note").value.trim()) {
    put(ensure(node, noteKey), name, $("note").value.trim());
  }
}

function saveBranch(name) {
  const existing = editing.type !== "add";
  const oldParent = selection.slice(0, -1);
  const parent = editing.type === "move" ? JSON.parse($("parent").value) : existing ? oldParent : selection;
  const siblings = parent.length ? ensure(nodeAt(parent), childKeys[parent.length]) : tree;
  const original = existing ? childrenAt(oldParent) : null;
  if (original === siblings && name === editing.name) return;
  if (Object.hasOwn(siblings, name)) throw new Error("Ezen a szinten már van ilyen nevű kategória.");
  const node = existing ? original[editing.name] : {tulajdonságok: {egyedi: {}, csoportos: {}}};
  if (existing) delete original[editing.name];
  else if (parent.length < 2) node[childKeys[parent.length + 1]] = {};
  put(siblings, name, node);
  selection = [...parent, name];
  $("search").value = "";
}

$("form").onsubmit = event => {
  event.preventDefault();
  try {
    const name = $("name").value.trim();
    if (!name) throw new Error("Adj meg egy nevet.");
    if (editing.type === "property") saveProperty(name);
    else saveBranch(name);
    $("editor").close();
    persist();
  } catch (error) { $("error").textContent = error.message; }
};
$("cancel").onclick = () => $("editor").close();
$("kind").onchange = kindFields;
$("search").oninput = renderTree;
$("export").onclick = () => {
  const json = JSON.stringify(payload(), null, 2) + "\n";
  const url = URL.createObjectURL(new Blob([json], {type: "application/json;charset=utf-8"}));
  const a = element("a");
  a.href = url;
  a.download = "reszfa_" + (selection.join("_") || "teljes").replace(/[<>:"/\\|?*]/g, "_").slice(0, 160) + ".json";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
};
$("reset").onclick = () => {
  if (!confirm("Elveted a teljes vázlatot, és visszatérsz a betöltött forrásfához?")) return;
  try { sessionStorage.removeItem(cacheKey); } catch {}
  tree = structuredClone(source.fa);
  version = source.verzio;
  dirty = false;
  selectPath([]);
};

async function init() {
  try {
    const response = await fetch("/api/kategoriafa", {cache: "no-store"});
    if (!response.ok) throw new Error("HTTP " + response.status);
    source = await response.json();
    tree = structuredClone(source.fa);
    version = source.verzio;
    let cached;
    try { cached = JSON.parse(sessionStorage.getItem(cacheKey)); } catch {}
    if (cached?.tree && cached.version) {
      tree = cached.tree;
      version = cached.version;
      selection = cached.selection || [];
      dirty = persisted = true;
    }
    $("search").disabled = false;
    render();
  } catch (error) {
    $("status").className = "failure";
    $("status").textContent = "A kategóriafa betöltése sikertelen. " + error.message;
  }
}
init();
