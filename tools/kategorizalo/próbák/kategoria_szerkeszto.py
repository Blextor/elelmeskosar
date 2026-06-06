# app.py — Élelmes kosár: séma‑szerkesztő UI (Streamlit)
# Futtatás:
#   pip install streamlit
#   streamlit run app.py
# A szerkesztő képes a csatolt JSON‑séma (kategória → alkategória → altípus → tulajdonságok\n# {"egyedi": {...}, "csoportos": {...}}) módosítására, bővítésére és rendezésére.
# Megjegyzés: a séma *definíciót* kezeli (nem termékeket). A bool jelzők üres objektumként\n# ({}), az opciós tulajdonságok listaként (list[str]) tárolódnak.

from __future__ import annotations
import json
import os
import copy
from typing import Dict, Any, Optional

import streamlit as st

st.set_page_config(page_title="Séma-szerkesztő – Élelmes kosár", layout="wide")
st.title("📚 Séma-szerkesztő – kategóriák, alkategóriák, altípusok és tulajdonságok")


# ---------- Segédfüggvények ----------

def ensure_node_scaffold(node: Dict[str, Any], level: str) -> Dict[str, Any]:
    """Biztosítja, hogy a node tartalmazza a szükséges kulcsokat.
    level ∈ {"kategoria", "alkategoria", "altipus"}
    """
    node.setdefault("tulajdonságok", {})
    node["tulajdonságok"].setdefault("egyedi", {})
    node["tulajdonságok"].setdefault("csoportos", {})
    if level == "kategoria":
        node.setdefault("alkategóriák", {})
    elif level == "alkategoria":
        node.setdefault("altípusok", {})
    return node


def sort_properties(props: Dict[str, Any]) -> Dict[str, Any]:
    """Alfabetikusan rendezi a tulajdonságokat és az opciólistákat, duplikátumok nélkül."""
    sorted_props: Dict[str, Any] = {}
    for key in sorted(props.keys(), key=lambda s: s.lower()):
        val = props[key]
        if isinstance(val, list):
            # Egyedi opciók rendezése és duplikátumok szűrése
            seen = set()
            clean = []
            for v in val:
                v = str(v).strip()
                if v and v not in seen:
                    seen.add(v)
                    clean.append(v)
            sorted_props[key] = sorted(clean, key=lambda s: s.lower())
        else:
            # Bool jelző (üres dict) vagy ismeretlen – mindkettőt támogatjuk
            sorted_props[key] = {} if isinstance(val, dict) else {}
    return sorted_props


def sort_schema_rec(node: Dict[str, Any]) -> Dict[str, Any]:
    """Rekurzívan rendez minden szintet és listát."""
    node = copy.deepcopy(node)
    # Tulajdonságok
    if "tulajdonságok" in node:
        egyedi = node["tulajdonságok"].get("egyedi", {})
        csoportos = node["tulajdonságok"].get("csoportos", {})
        node["tulajdonságok"]["egyedi"] = sort_properties(egyedi)
        node["tulajdonságok"]["csoportos"] = sort_properties(csoportos)
    # Gyerekek
    if "alkategóriák" in node:
        node["alkategóriák"] = {k: sort_schema_rec(v) for k, v in
                                sorted(node["alkategóriák"].items(), key=lambda kv: kv[0].lower())}
    if "altípusok" in node:
        node["altípusok"] = {k: sort_schema_rec(v) for k, v in
                             sorted(node["altípusok"].items(), key=lambda kv: kv[0].lower())}
    return node


def rename_key(d: Dict[str, Any], old: str, new: str) -> None:
    if new == old:
        return
    if new in d:
        raise ValueError(f'"{new}" már létezik ezen a szinten.')
    d[new] = d.pop(old)


def get_node(schema: Dict[str, Any], cat: Optional[str], sub: Optional[str], subsub: Optional[str]) -> Dict[str, Any]:
    if not cat:
        return {}
    cat_node = ensure_node_scaffold(schema[cat], "kategoria")
    if not sub:
        return cat_node
    sub_node = ensure_node_scaffold(cat_node["alkategóriák"][sub], "alkategoria")
    if not subsub:
        return sub_node
    subsub_node = ensure_node_scaffold(sub_node["altípusok"][subsub], "altipus")
    return subsub_node


def delete_node(schema: Dict[str, Any], cat: str, sub: Optional[str], subsub: Optional[str]) -> None:
    if subsub:
        del schema[cat]["alkategóriák"][sub]["altípusok"][subsub]
    elif sub:
        del schema[cat]["alkategóriák"][sub]
    else:
        del schema[cat]


# ---------- Állapot ----------

if "schema" not in st.session_state:
    st.session_state.schema: Dict[str, Any] = {}
if "loaded_from" not in st.session_state:
    st.session_state.loaded_from: Optional[str] = None

# ---------- Betöltés / új séma ----------

with st.sidebar:
    st.subheader("📁 Séma betöltése")
    upl = st.file_uploader("JSON séma feltöltése (opcionális)", type=["json"], accept_multiple_files=False)
    path_input = st.text_input("Vagy add meg a helyi fájlt…",
                               value=st.session_state.loaded_from or "kategori_tulajdonsagok_uj_sorted.json")
    cols_load = st.columns(2)
    with cols_load[0]:
        if st.button("Betöltés fájlból"):
            try:
                with open(path_input, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Rendezzük és scaffoldoljuk
                data = {k: sort_schema_rec(ensure_node_scaffold(v, "kategoria")) for k, v in data.items()}
                st.session_state.schema = data
                st.session_state.loaded_from = path_input
                st.success(f"Betöltve: {path_input}")
            except Exception as e:
                st.error(f"Nem sikerült betölteni: {e}")
    with cols_load[1]:
        if upl is not None and st.button("Betöltés a feltöltöttből"):
            try:
                data = json.loads(upl.getvalue().decode("utf-8"))
                data = {k: sort_schema_rec(ensure_node_scaffold(v, "kategoria")) for k, v in data.items()}
                st.session_state.schema = data
                st.session_state.loaded_from = None
                st.success("Feltöltött séma betöltve.")
            except Exception as e:
                st.error(f"Hiba a feltöltött fájl olvasásakor: {e}")

    st.markdown("---")
    if st.button("➕ Új üres séma indítása"):
        st.session_state.schema = {}
        st.session_state.loaded_from = None

schema = st.session_state.schema

if not schema:
    st.info("Tölts be egy sémát, vagy indíts újat a bal oldali sávban.")
    st.stop()

# ---------- Navigáció (hierarchia) ----------

left, right = st.columns([1, 2])
with left:
    st.subheader("🧭 Navigáció")
    cats = ["(válassz)"] + sorted(list(schema.keys()), key=lambda s: s.lower()) + ["+ Új kategória…"]
    cat_choice = st.selectbox("Kategória", cats, key="nav_cat")

    new_cat_name = None
    if cat_choice == "+ Új kategória…":
        with st.form("form_new_cat", clear_on_submit=True):
            name = st.text_input("Új kategória neve")
            submitted = st.form_submit_button("Hozzáadás")
            if submitted and name:
                if name in schema:
                    st.warning("Ilyen nevű kategória már létezik.")
                else:
                    schema[name] = ensure_node_scaffold({}, "kategoria")
                    schema = sort_schema_rec(schema)
                    st.session_state.schema = schema
                    st.success(f"Kategória hozzáadva: {name}")
                    new_cat_name = name

    # Aktív kategória (ha most hoztuk létre, azt válasszuk ki)
    if new_cat_name:
        cat_choice = new_cat_name

    sub_choice = None
    subsub_choice = None

    if cat_choice and cat_choice not in ("(válassz)", "+ Új kategória…"):
        subs_dict = ensure_node_scaffold(schema[cat_choice], "kategoria")["alkategóriák"]
        subs = ["(nincs)"] + sorted(list(subs_dict.keys()), key=lambda s: s.lower()) + ["+ Új alkategória…"]
        sub_choice = st.selectbox("Alkategória", subs, key="nav_sub")

        if sub_choice == "+ Új alkategória…":
            with st.form("form_new_sub", clear_on_submit=True):
                name = st.text_input("Új alkategória neve")
                submitted = st.form_submit_button("Hozzáadás")
                if submitted and name:
                    if name in subs_dict:
                        st.warning("Ilyen nevű alkategória már létezik.")
                    else:
                        subs_dict[name] = ensure_node_scaffold({}, "alkategoria")
                        schema[cat_choice]["alkategóriák"] = {k: subs_dict[k] for k in
                                                              sorted(subs_dict.keys(), key=lambda s: s.lower())}
                        st.session_state.schema = schema
                        st.success(f"Alkategória hozzáadva: {name}")
                        sub_choice = name

        if sub_choice and sub_choice not in ("(nincs)", "+ Új alkategória…"):
            subsub_dict = ensure_node_scaffold(schema[cat_choice]["alkategóriák"][sub_choice], "alkategoria")[
                "altípusok"]
            subsubs = ["(nincs)"] + sorted(list(subsub_dict.keys()), key=lambda s: s.lower()) + ["+ Új altípus…"]
            subsub_choice = st.selectbox("Altípus", subsubs, key="nav_subsub")

            if subsub_choice == "+ Új altípus…":
                with st.form("form_new_subsub", clear_on_submit=True):
                    name = st.text_input("Új altípus neve")
                    submitted = st.form_submit_button("Hozzáadás")
                    if submitted and name:
                        if name in subsub_dict:
                            st.warning("Ilyen nevű altípus már létezik.")
                        else:
                            subsub_dict[name] = ensure_node_scaffold({}, "altipus")
                            schema[cat_choice]["alkategóriák"][sub_choice]["altípusok"] = {
                                k: subsub_dict[k] for k in sorted(subsub_dict.keys(), key=lambda s: s.lower())
                            }
                            st.session_state.schema = schema
                            st.success(f"Altípus hozzáadva: {name}")
                            subsub_choice = name

with right:
    st.subheader("✏️ Kiválasztott elem szerkesztése")
    if cat_choice in (None, "(válassz)", "+ Új kategória…"):
        st.info("Válassz ki legalább egy kategóriát a bal oldalon.")
        st.stop()

    # Aktuális node és szint meghatározása
    level = "kategoria"
    if sub_choice and sub_choice not in ("(nincs)", "+ Új alkategória…"):
        level = "alkategoria"
    if subsub_choice and subsub_choice not in ("(nincs)", "+ Új altípus…"):
        level = "altipus"

    node = get_node(schema, cat_choice,
                    None if sub_choice in (None, "(nincs)", "+ Új alkategória…") else sub_choice,
                    None if subsub_choice in (None, "(nincs)", "+ Új altípus…") else subsub_choice)

    # ---------- Átnevezés / törlés ----------
    with st.expander("🔤 Átnevezés és törlés", expanded=False):
        colr1, colr2, colr3 = st.columns([2, 1, 1])
        current_name = subsub_choice if level == "altipus" else (sub_choice if level == "alkategoria" else cat_choice)
        new_name = colr1.text_input("Új név", value=current_name or "")
        if colr2.button("Átnevezés", type="primary"):
            try:
                if level == "kategoria":
                    rename_key(schema, cat_choice, new_name)
                    st.session_state.schema = sort_schema_rec(schema)
                    st.success("Kategória átnevezve.")
                    st.rerun()
                elif level == "alkategoria":
                    rename_key(schema[cat_choice]["alkategóriák"], sub_choice, new_name)
                    st.session_state.schema = sort_schema_rec(schema)
                    st.success("Alkategória átnevezve.")
                    st.rerun()
                else:
                    rename_key(schema[cat_choice]["alkategóriák"][sub_choice]["altípusok"], subsub_choice, new_name)
                    st.session_state.schema = sort_schema_rec(schema)
                    st.success("Altípus átnevezve.")
                    st.rerun()
            except Exception as e:
                st.error(str(e))

        if colr3.button("🗑️ Törlés", help="Az aktuális elemet törli"):
            delete_node(schema, cat_choice,
                        None if level == "kategoria" else sub_choice,
                        subsub_choice if level == "altipus" else None)
            st.session_state.schema = schema
            st.warning("Törölve.")
            st.rerun()

    # ---------- Tulajdonságok szerkesztése ----------
    st.markdown("### ⚙️ Tulajdonságok")


    def edit_prop_group(title: str, group_key: str):
        st.markdown(f"#### {title}")
        props: Dict[str, Any] = node["tulajdonságok"].get(group_key, {})

        # Meglévő tulajdonságok listája
        if not props:
            st.caption("(Nincs még tulajdonság.)")
        else:
            for prop_name in sorted(list(props.keys()), key=lambda s: s.lower()):
                val = props[prop_name]
                with st.expander(f"🧩 {prop_name}", expanded=False):
                    c1, c2 = st.columns([2, 1])
                    new_pname = c1.text_input("Tulajdonság neve", value=prop_name, key=f"{group_key}_pname_{prop_name}")
                    ptype = "Opciók" if isinstance(val, list) else "Bool"
                    new_ptype = c2.selectbox("Típus", ["Bool", "Opciók"], index=0 if ptype == "Bool" else 1,
                                             key=f"{group_key}_ptype_{prop_name}")

                    # Opciók szerkesztése
                    options_text = ""
                    if new_ptype == "Opciók":
                        current_opts = val if isinstance(val, list) else []
                        options_text = st.text_area("Opciók (soronként)", value="\n".join(current_opts),
                                                    key=f"{group_key}_opts_{prop_name}")

                    cc1, cc2, cc3 = st.columns(3)
                    if cc1.button("Mentés", key=f"{group_key}_save_{prop_name}"):
                        # Átnevezés + típusváltás + opciók mentése
                        if new_pname != prop_name and new_pname in props:
                            st.error("Már létezik ilyen nevű tulajdonság.")
                        else:
                            # típus és érték
                            new_val: Any
                            if new_ptype == "Opciók":
                                raw = [ln.strip() for ln in options_text.splitlines()]
                                new_opts = [x for x in raw if x]
                                new_val = sorted(list(dict.fromkeys(new_opts)), key=lambda s: s.lower())
                            else:
                                new_val = {}
                            # átnevezés
                            if new_pname != prop_name:
                                props[new_pname] = new_val
                                del props[prop_name]
                            else:
                                props[prop_name] = new_val
                            node["tulajdonságok"][group_key] = sort_properties(props)
                            st.session_state.schema = schema
                            st.success("Mentve.")
                    if cc2.button("🗑️ Törlés", key=f"{group_key}_del_{prop_name}"):
                        del props[prop_name]
                        node["tulajdonságok"][group_key] = sort_properties(props)
                        st.session_state.schema = schema
                        st.warning("Tulajdonság törölve.")
                    if cc3.button("↔️ Áthelyezés másik csoportba", key=f"{group_key}_move_{prop_name}"):
                        other_key = "egyedi" if group_key == "csoportos" else "csoportos"
                        # Az áthelyezés *definíciót* visz, jelentés változatlan (bool vs opciók)
                        node["tulajdonságok"].setdefault(other_key, {})
                        node["tulajdonságok"][other_key][prop_name] = val
                        del props[prop_name]
                        node["tulajdonságok"][group_key] = sort_properties(props)
                        node["tulajdonságok"][other_key] = sort_properties(node["tulajdonságok"][other_key])
                        st.session_state.schema = schema
                        st.info("Áthelyezve.")

        st.markdown("**Új tulajdonság hozzáadása**")
        with st.form(f"form_add_prop_{group_key}", clear_on_submit=True):
            pname = st.text_input("Név", key=f"new_{group_key}_name")
            ptype = st.selectbox("Típus", ["Bool", "Opciók"], key=f"new_{group_key}_type")
            opts_text = ""
            if ptype == "Opciók":
                opts_text = st.text_area("Opciók (soronként)", key=f"new_{group_key}_opts")
            submitted = st.form_submit_button("Hozzáadás")
            if submitted:
                if not pname:
                    st.warning("Adj meg egy nevet.")
                else:
                    if pname in node["tulajdonságok"].get(group_key, {}):
                        st.warning("Már létezik ilyen nevű tulajdonság ezen a szinten.")
                    else:
                        if ptype == "Opciók":
                            raw = [ln.strip() for ln in opts_text.splitlines()]
                            opts = [x for x in raw if x]
                            node["tulajdonságok"].setdefault(group_key, {})[pname] = sorted(list(dict.fromkeys(opts)),
                                                                                            key=lambda s: s.lower())
                        else:
                            node["tulajdonságok"].setdefault(group_key, {})[pname] = {}
                        node["tulajdonságok"][group_key] = sort_properties(node["tulajdonságok"][group_key])
                        st.session_state.schema = schema
                        st.success("Hozzáadva.")


    edit_prop_group("Egyedi (egymást kizáró) / bool jelzők", "egyedi")
    st.markdown("---")
    edit_prop_group("Csoportos (több egyszerre igaz lehet)", "csoportos")

# ---------- Mentés / export ----------

st.markdown("---")
st.subheader("💾 Mentés és export")
with st.form("form_save"):
    out_path = st.text_input("Célfájl (JSON)",
                             value=(st.session_state.loaded_from or "kategori_tulajdonsagok_szerkesztett.json"))
    do_save = st.form_submit_button("Mentés fájlba", type="primary")
    if do_save:
        try:
            # Végső rendezés írás előtt
            final = {k: sort_schema_rec(v) for k, v in st.session_state.schema.items()}
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(final, f, ensure_ascii=False, indent=2)
            st.success(f"Elmentve: {out_path}")
        except Exception as e:
            st.error(f"Mentési hiba: {e}")

final_text = json.dumps({k: sort_schema_rec(v) for k, v in st.session_state.schema.items()}, ensure_ascii=False,
                        indent=2)
st.download_button("⬇️ Letöltés JSON-ként", data=final_text.encode("utf-8"),
                   file_name="kategori_tulajdonsagok_szerkesztett.json", mime="application/json")

# ---------- Tipp / Súgó ----------
with st.expander("ℹ️ Súgó"):
    st.markdown(
        """
        **Mit jelentenek a típusok?**
        - **Bool**: egyszerű igen/nem jelző (például: `bio`, `hazai`). A sémában üres objektumként tárolódik (`{}`).
        - **Opciók**: felsorolt értékek közül *egy* (egyedi) vagy *több* (csoportos) lehet igaz a termékekre vonatkozóan. A sémában listaként tárolódik (`["piros", "sárga", ...]`).

        **Szintek:**
        - **Kategória** → `alkategóriák` → `altípusok` (mindegyikhez külön tulajdonság‑készlet tartozhat).

        **Rendezés:**
        - Mentés előtt a program minden kulcsot és opciólistát ABC‐rendbe állít, és kiszűri a duplikátumokat.
        """
    )
