# ÚJ séma támogatás + javítások:
# - Egyválasztós (radio) tulajdonságoknál az első opció automatikusan kiválasztódik.
# - "Mentés és következő": kategóriák mellett a TULAJDONSÁGOKAT is viszi a következő termékre,
#   ha a következő termék még nincs kategorizálva.
#
# A JSON tulajdonság séma támogatott formái:
#   ÚJ séma:
#   "tulajdonságok": {
#       "egyedi": {      # {} = boolean; ["a","b"] = single (rádió – első opció alapból)
#           "bio": {},
#           "színe": ["piros","fehér","kék"]
#       },
#       "csoportos": {   # csak listák -> többválasztós (checkbox-csoport)
#           "tájegység": ["Dél","Észak","Kelet"]
#       }
#   }
#
#   RÉGI séma is működik (visszafelé kompatibilis):
#     {} -> boolean
#     ["a","b"] -> többválasztós
#     {"values":[...],"type":"single"} -> rádió
#     {"values":[...]} -> többválasztós

import tkinter as tk
from tkinter import ttk, messagebox, font
import json, hashlib, requests, csv, ast
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
import os
import re
import unicodedata

def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9]+', '_', value).strip('_')
    return value

def termek_fajlnev(termek, extension=".jpg"):
    nev = slugify(termek.get('product_name'))
    marka = slugify(termek.get('brand_name', ''))
    hash_str = hashlib.md5(termek.get('kep_url', '').encode('utf-8')).hexdigest()[:8]
    return f"{nev}_{marka}_{hash_str}{extension}"

def kep_letolt(termek, kepek_dir="kepek"):
    os.makedirs(kepek_dir, exist_ok=True)
    url = termek.get('kep_url', '')
    extension = ".jpg"
    if url.lower().endswith('.png'):
        extension = ".png"
    fajlnev = termek_fajlnev(termek, extension)
    utvonal = os.path.join(kepek_dir, fajlnev)
    if not os.path.exists(utvonal):
        if url:
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                content_type = resp.headers.get('Content-Type', '').lower()
                if 'png' in content_type or url.lower().endswith('.png'):
                    extension = '.png'
                elif 'jpeg' in content_type or 'jpg' in content_type or url.lower().endswith('.jpg'):
                    extension = '.jpg'
                fajlnev = termek_fajlnev(termek, extension)
                utvonal = os.path.join(kepek_dir, fajlnev)
                img = Image.open(BytesIO(resp.content))
                img.save(utvonal)
            except Exception:
                return None
    return utvonal

def kategoriak_hash(fok, al, alt, tul):
    key = f"{fok}|{al}|{alt}|{json.dumps(tul, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def get_alkategoriak(kategoriak_dict, fokategoria):
    if not fokategoria: return []
    return list(kategoriak_dict[fokategoria]['alkategóriák'].keys())

def get_altipusok(kategoriak_dict, fokategoria, alkategoria):
    if not (fokategoria and alkategoria): return []
    return list(kategoriak_dict[fokategoria]['alkategóriák'][alkategoria].get('altípusok', {}).keys())

# --- ÚJ: tulajdonság normalizáló az új sémához + visszafelé kompatibilitás ---
def _normalize_tulajdonsag_blokk(blokk):
    """
    Bemenet: a JSON 'tulajdonságok' blokkja ÚJ (egyedi/csoportos) VAGY RÉGI sémában.
    Kimenet: egységesített dict: kulcs -> spec
      - {}                               -> boolean
      - ["a","b"]                        -> multi (checkbox)
      - {"values":[...],"type":"single"} -> single (radio)
      - {"values":[...]}                 -> multi (checkbox)
    """
    out = {}

    # ÚJ séma
    if isinstance(blokk, dict) and ("egyedi" in blokk or "csoportos" in blokk):
        egyedi = blokk.get("egyedi", {})
        csoportos = blokk.get("csoportos", {})

        # egyedi: {} (boolean) vagy lista (single)
        if isinstance(egyedi, dict):
            for nev, v in egyedi.items():
                if isinstance(v, dict):
                    out[nev] = {}
                elif isinstance(v, list):
                    out[nev] = {"values": v, "type": "single"}  # single-choice -> rádió
                elif isinstance(v, str):
                    out[nev] = {"values": [v], "type": "single"}
                else:
                    out[nev] = {}

        # csoportos: listák -> multi
        if isinstance(csoportos, dict):
            for nev, v in csoportos.items():
                if isinstance(v, list):
                    out[nev] = v
                elif isinstance(v, dict) and "values" in v:
                    out[nev] = {"values": v.get("values", [])} if "type" not in v else v
                else:
                    out[nev] = []
        return out

    # RÉGI séma
    if isinstance(blokk, dict):
        for nev, v in blokk.items():
            if isinstance(v, dict):
                if "values" in v:
                    out[nev] = v
                else:
                    out[nev] = {}
            elif isinstance(v, list):
                out[nev] = v
            else:
                out[nev] = {}
        return out

    return out

def get_tulajdonsagok(kategoriak_dict, fokategoria, alkategoria, altipus):
    """
    Tulajdonságok összeolvasztása: főkategória -> alkategória -> altípus
    Az alacsonyabb szint felülírja a felsőbb szintek azonos nevű mezőit.
    """
    res = {}

    if fokategoria and fokategoria in kategoriak_dict:
        blokk = kategoriak_dict[fokategoria].get('tulajdonságok', {})
        res.update(_normalize_tulajdonsag_blokk(blokk))

        alk_map = kategoriak_dict[fokategoria].get('alkategóriák', {})
        if alkategoria and alkategoria in alk_map:
            alk = alk_map[alkategoria]
            blokk = alk.get('tulajdonságok', {})
            res.update(_normalize_tulajdonsag_blokk(blokk))

            alt_map = alk.get('altípusok', {})
            if altipus and altipus in alt_map:
                alt_blokk = alt_map[altipus].get('tulajdonságok', {})
                res.update(_normalize_tulajdonsag_blokk(alt_blokk))

    return res

def get_group_width(options, font_obj):
    if not options:
        return 70
    return max([font_obj.measure(str(opt)) for opt in options]) + 24

def beolvas_termekek_csv(csv_path):
    termekek = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_url = ""
            image_urls_raw = row.get('image_urls', '')
            if image_urls_raw:
                try:
                    if image_urls_raw.strip().startswith('['):
                        urls = ast.literal_eval(image_urls_raw)
                    else:
                        urls = image_urls_raw.split(';')
                    if isinstance(urls, list) and urls and urls[0].strip():
                        img_url = urls[0].strip()
                except Exception:
                    img_url = ""
            row['kep_url'] = img_url

            cats = row.get('categories', '')
            try:
                if cats and cats.strip().startswith('['):
                    cats_val = ast.literal_eval(cats)
                    row['categories__show'] = ', '.join(str(x) for x in cats_val) if isinstance(cats_val, list) else str(cats_val)
                else:
                    row['categories__show'] = cats
            except:
                row['categories__show'] = str(cats)
            termekek.append(row)
    return termekek

class TermekTagger:
    def __init__(self, master, termekek, kategoriak_dict, eredmenyek):
        self.master = master
        self.termekek = termekek
        self.kategoriak_dict = kategoriak_dict
        self.eredmenyek = eredmenyek
        self.cur = 0

        self.statusz_map = {}
        self.eredmeny_map = {}
        for eredmeny in self.eredmenyek:
            termek_hash = self._termek_hash(eredmeny['termek'])
            self.eredmeny_map[termek_hash] = eredmeny
            self.statusz_map[termek_hash] = eredmeny.get('statusz', 'folyamatban')
        for t in termekek:
            t_hash = self._termek_hash(t)
            if t_hash not in self.statusz_map:
                self.statusz_map[t_hash] = 'nincs'

        self.statusz_color = {
            'kesz': 'green', 'folyamatban': 'orange', 'elavult': 'red', 'nincs': 'gray'
        }

        self.kivalasztott_index = 0
        self.filtered_termekek = []

        # --- UI ---
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.nev_label = tk.Label(self.left_frame, text="", font=('Arial', 13, "bold"))
        self.nev_label.pack(pady=2)
        self.marka_label = tk.Label(self.left_frame, text="", font=('Arial', 11))
        self.marka_label.pack(pady=2)
        self.kategoria_label = tk.Label(self.left_frame, text="", font=('Arial', 10), wraplength=340, justify='left')
        self.kategoria_label.pack(pady=2)
        self.kep_label = tk.Label(self.left_frame)
        self.kep_label.pack(pady=5)

        self.fokategoria_var = tk.StringVar()
        self.alkategoria_var = tk.StringVar()
        self.altipus_var = tk.StringVar()

        tk.Label(self.left_frame, text="Főkategória:").pack(anchor='w', padx=4)
        self.fokategoria_radio_frame = tk.Frame(self.left_frame)
        self.fokategoria_radio_frame.pack(anchor='w', padx=6)
        tk.Label(self.left_frame, text="Kategória:").pack(anchor='w', padx=4)
        self.alkategoria_radio_frame = tk.Frame(self.left_frame)
        self.alkategoria_radio_frame.pack(anchor='w', padx=6)
        tk.Label(self.left_frame, text="Altípus:").pack(anchor='w', padx=4)
        self.altipus_radio_frame = tk.Frame(self.left_frame)
        self.altipus_radio_frame.pack(anchor='w', padx=6)

        self.tulajdonsagok_frame = tk.LabelFrame(self.left_frame, text="Tulajdonságok")
        self.tulajdonsagok_frame.pack(pady=5, fill=tk.X, padx=4)
        self.tulajdonsagok_widgets = {}

        self.save_button = tk.Button(self.left_frame, text="Mentés", command=self.mentes)
        self.save_button.pack(pady=2)
        self.save_next_button = tk.Button(self.left_frame, text="Mentés és következő", command=self.mentes_es_kovetkezo)
        self.save_next_button.pack(pady=2)
        self.kovetkezo_button = tk.Button(self.left_frame, text="Következő", command=self.kovetkezo)

        self.kovetkezo_button.pack(pady=2)

        # --- Szűrőpanel (jobb oldal teteje) ---
        self.filter_frame = tk.LabelFrame(self.right_frame, text="Szűrés")
        self.filter_frame.pack(side=tk.TOP, fill=tk.X, padx=3, pady=2)

        self.nev_filter_var = tk.StringVar()
        tk.Label(self.filter_frame, text="Név keresés:").pack(anchor='w')
        self.nev_filter_entry = tk.Entry(self.filter_frame, textvariable=self.nev_filter_var)
        self.nev_filter_entry.pack(fill=tk.X, padx=2)
        self.nev_filter_entry.bind('<KeyRelease>', self.filter_frissit)

        tk.Label(self.filter_frame, text="Főkategória:").pack(anchor='w')
        self.filter_fokategoria_vars = {}
        self.filter_fokategoria_box = tk.Frame(self.filter_frame)
        self.filter_fokategoria_box.pack(anchor='w')
        self.filter_fokategoria_mind_var = tk.BooleanVar()
        self._build_checkbox_grid(self.filter_fokategoria_box, list(self.kategoriak_dict.keys()),
                                 self.filter_fokategoria_vars, self.on_fokategoria_filter_change,
                                 mind_var=self.filter_fokategoria_mind_var, mind_text="Mind")

        tk.Label(self.filter_frame, text="Kategória:").pack(anchor='w')
        self.filter_alkategoria_vars = {}
        self.filter_alkategoria_box = tk.Frame(self.filter_frame)
        self.filter_alkategoria_box.pack(anchor='w')
        self.filter_alkategoria_mind_var = tk.BooleanVar()

        tk.Label(self.filter_frame, text="Altípus:").pack(anchor='w')
        self.filter_altipus_vars = {}
        self.filter_altipus_box = tk.Frame(self.filter_frame)
        self.filter_altipus_box.pack(anchor='w')
        self.filter_altipus_mind_var = tk.BooleanVar()

        tk.Label(self.filter_frame, text="Státusz:").pack(anchor='w')
        self.filter_statusz_vars = {}
        self.filter_statusz_frame = tk.Frame(self.filter_frame)
        self.filter_statusz_frame.pack(anchor='w')
        for sz in ['kesz', 'folyamatban', 'elavult', 'nincs']:
            v = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.filter_statusz_frame, text=sz.capitalize(), variable=v, command=self.filter_frissit, font=('Arial', 9))
            cb.pack(side=tk.LEFT)
            self.filter_statusz_vars[sz] = v
        self.statusz_stats_label = tk.Label(self.filter_frame, text="", font=('Arial', 10))
        self.statusz_stats_label.pack(anchor='w', padx=2, pady=(2, 6))

        lista_frame = tk.Frame(self.right_frame)
        lista_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2)
        self.termek_lista = tk.Listbox(lista_frame)
        self.termek_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.termek_lista_scroll = tk.Scrollbar(lista_frame, orient="vertical", command=self.termek_lista.yview)
        self.termek_lista_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.termek_lista.config(yscrollcommand=self.termek_lista_scroll.set)
        self.termek_lista.bind('<<ListboxSelect>>', self.lista_katt)

        self.statusz_label = tk.Label(self.right_frame, text="")
        self.statusz_label.pack(side=tk.BOTTOM, pady=3)

        self.fokategoria_radios = {}
        self.alkategoria_radios = {}
        self.altipus_radios = {}

        self.suppress_select = False
        self.advanced_due_to_save = False  # mentés miatti automatikus előrelépés jele

        self.build_left_radios()
        self.filter_frissit()

    def frissit_statusz_kimutatas(self):
        statusz_sorrend = ['kesz', 'folyamatban', 'elavult', 'nincs']
        ossz = len(self.termekek)
        stat = {k: 0 for k in statusz_sorrend}
        for t in self.termekek:
            t_hash = self._termek_hash(t)
            st = self.statusz_map.get(t_hash, 'nincs')
            if st not in stat: st = 'nincs'
            stat[st] += 1
        s = "   ".join([f"{st.capitalize()}: {stat[st]} db" for st in statusz_sorrend])
        if hasattr(self, 'statusz_stats_label'):
            self.statusz_stats_label.config(text=s)

    def _termek_hash(self, termek):
        return (
            str(termek.get("product_name", "")) + "|" +
            str(termek.get("store_name", "")) + "|" +
            str(termek.get("brand_name", "")) + "|" +
            str(termek.get("kep_url", ""))
        )

    def build_radio_group(self, parent, options, var, command, radios_dict, max_per_row=5):
        for widget in parent.winfo_children():
            widget.destroy()
        font_radio = font.Font(family="Arial", size=9)
        width = get_group_width(options, font_radio)
        row = None
        for i, opt in enumerate(options):
            if i % max_per_row == 0:
                row = tk.Frame(parent)
                row.pack(anchor='w')
            rb = tk.Radiobutton(row, text=opt, variable=var, value=opt, indicatoron=0, font=font_radio,
                                command=command, anchor='w', justify='left', padx=4)
            rb.pack(side=tk.LEFT, padx=0, pady=0, ipadx=0, ipady=0)
            rb.config(width=width//8)
            radios_dict[opt] = rb

    def build_left_radios(self):
        self.build_radio_group(self.fokategoria_radio_frame, list(self.kategoriak_dict.keys()),
                              self.fokategoria_var, self.fokategoria_valtozott, self.fokategoria_radios)

    def fokategoria_valtozott(self):
        options = get_alkategoriak(self.kategoriak_dict, self.fokategoria_var.get()) if self.fokategoria_var.get() else []
        self.build_radio_group(self.alkategoria_radio_frame, options, self.alkategoria_var, self.alkategoria_valtozott, self.alkategoria_radios)
        self.alkategoria_var.set('')
        self.alkategoria_valtozott()

    def alkategoria_valtozott(self):
        options = get_altipusok(self.kategoriak_dict, self.fokategoria_var.get(), self.alkategoria_var.get()) if self.fokategoria_var.get() and self.alkategoria_var.get() else []
        self.build_radio_group(self.altipus_radio_frame, options, self.altipus_var, self.frissit_tulajdonsagok, self.altipus_radios)
        self.altipus_var.set('')
        self.frissit_tulajdonsagok()

    def rebuild_kategoria_radios_with_current(self):
        self.build_radio_group(self.fokategoria_radio_frame, list(self.kategoriak_dict.keys()),
                               self.fokategoria_var, self.fokategoria_valtozott, self.fokategoria_radios)
        alk_options = get_alkategoriak(self.kategoriak_dict, self.fokategoria_var.get()) if self.fokategoria_var.get() else []
        self.build_radio_group(self.alkategoria_radio_frame, alk_options,
                               self.alkategoria_var, self.alkategoria_valtozott, self.alkategoria_radios)
        alt_options = get_altipusok(self.kategoriak_dict, self.fokategoria_var.get(), self.alkategoria_var.get()) if self.alkategoria_var.get() else []
        self.build_radio_group(self.altipus_radio_frame, alt_options,
                               self.altipus_var, self.frissit_tulajdonsagok, self.altipus_radios)

    def _build_checkbox_grid(self, parent, options, var_dict, command, mind_var=None, mind_text=None, max_per_row=5):
        old_vals = {k: v.get() for k, v in var_dict.items()}
        for widget in parent.winfo_children():
            widget.destroy()
        var_dict.clear()
        font_cb = font.Font(family="Arial", size=9)
        if mind_var is not None and mind_text is not None:
            mind_row = tk.Frame(parent)
            mind_row.pack(anchor='w')
            cb_mind = tk.Checkbutton(mind_row, text=mind_text, variable=mind_var, font=font_cb,
                                     command=lambda: self.on_mind_checkbox(var_dict, mind_var, command), padx=4)
            cb_mind.pack(side=tk.LEFT, padx=0, pady=0)
        width = get_group_width(options, font_cb)
        row = None
        for i, opt in enumerate(options):
            if i % max_per_row == 0:
                row = tk.Frame(parent)
                row.pack(anchor='w')
            var = tk.BooleanVar(value=old_vals.get(opt, False))
            cb = tk.Checkbutton(row, text=opt, variable=var, font=font_cb, anchor='w', justify='left', padx=4, command=command)
            cb.pack(side=tk.LEFT, padx=0, pady=0)
            cb.config(width=width//8)
            var_dict[opt] = var

    def on_mind_checkbox(self, var_dict, mind_var, change_command):
        v = mind_var.get()
        for var in var_dict.values():
            var.set(v)
        change_command()
        self.master.after(10, lambda: mind_var.set(all(var.get() for var in var_dict.values())))

    def on_fokategoria_filter_change(self):
        self.filter_frissit()
    def on_alkategoria_filter_change(self):
        self.filter_frissit()
    def on_altipus_filter_change(self):
        self.filter_frissit()

    def filter_frissit(self, event=None):
        fokats = [k for k,v in self.filter_fokategoria_vars.items() if v.get()]
        if len(fokats) == 1:
            alkats = get_alkategoriak(self.kategoriak_dict, fokats[0])
        else:
            alkats = []
        self._build_checkbox_grid(self.filter_alkategoria_box, alkats, self.filter_alkategoria_vars, self.on_alkategoria_filter_change, mind_var=self.filter_alkategoria_mind_var, mind_text="Mind")

        alkats_selected = [k for k,v in self.filter_alkategoria_vars.items() if v.get()]
        if len(fokats) == 1 and len(alkats_selected) == 1:
            altipusok = get_altipusok(self.kategoriak_dict, fokats[0], alkats_selected[0])
        else:
            altipusok = []
        self._build_checkbox_grid(self.filter_altipus_box, altipusok, self.filter_altipus_vars, self.on_altipus_filter_change, mind_var=self.filter_altipus_mind_var, mind_text="Mind")
        self.termek_lista_frissit()
        self.frissit_statusz_kimutatas()

    def termek_lista_frissit(self):
        self.termek_lista.delete(0, tk.END)
        nev_filter = self.nev_filter_var.get().lower()
        fokats = [k for k,v in self.filter_fokategoria_vars.items() if v.get()]
        alkats = [k for k,v in self.filter_alkategoria_vars.items() if v.get()]
        altipusok = [k for k,v in self.filter_altipus_vars.items() if v.get()]
        statuszok = [k for k,v in self.filter_statusz_vars.items() if v.get()]
        if not statuszok:
            self.filtered_termekek = []
            return
        self.filtered_termekek = []
        for i, termek in enumerate(self.termekek):
            nev = termek.get('product_name', '')
            t_hash = self._termek_hash(termek)
            statusz = self.statusz_map[t_hash]
            eredm = self.eredmeny_map.get(t_hash, {})
            fokat = eredm.get('fokategoria', "")
            alk = eredm.get('alkategoria', "")
            alt = eredm.get('altipus', "")

            if not statusz == "kész":
                if statusz in statuszok:
                    self.filtered_termekek.append((i, termek))
                    continue

            if nev_filter not in nev.lower():
                continue
            if not fokat == "" and not fokats == [] and fokat not in fokats:
                continue
            if not alk == "" and not alkats == [] and alk not in alkats:
                continue
            if not alt == "" and not altipusok == [] and alt not in altipusok:
                continue
            if statusz not in statuszok:
                continue

            self.filtered_termekek.append((i, termek))

        for j, (idx, termek) in enumerate(self.filtered_termekek):
            nev = termek.get('product_name', '')
            t_hash = self._termek_hash(termek)
            statusz = self.statusz_map[t_hash]
            self.termek_lista.insert(tk.END, nev)
            self.termek_lista.itemconfig(j, {'fg': self.statusz_color[statusz]})

        if not self.filtered_termekek:
            self.nev_label.config(text="")
            self.marka_label.config(text="")
            self.kategoria_label.config(text="")
            self.kep_label.config(image='')
            self.clear_kategoria_radios()
            self.frissit_tulajdonsagok()
            self.statusz_label.config(text="")
        else:
            if self.suppress_select:
                return
            if not self.termek_lista.curselection():
                self.termek_lista.selection_clear(0, tk.END)
                self.termek_lista.selection_set(0)
                idx = self.filtered_termekek[0][0]
                self.termek_betoltes(idx)

    def termek_betoltes(self, idx, keep_kat=False, clear_props=False, prefill_props=None):
        self.kivalasztott_index = idx
        termek = self.termekek[idx]
        uzlet = termek.get('store_name', '')
        nev = termek.get('product_name', '')
        marka = termek.get('brand_name', '')
        kategoriak = termek.get('categories__show', '')
        self.nev_label.config(text=f"{uzlet} | {nev}")
        self.marka_label.config(text=f"Márka: {marka}")
        self.kategoria_label.config(text=f"Kategóriák: {kategoriak}")

        kep_path = kep_letolt(termek)
        if kep_path and os.path.exists(kep_path):
            try:
                img = Image.open(kep_path)
                img = ImageOps.contain(img, (300, 500), Image.LANCZOS)
                self.tk_img = ImageTk.PhotoImage(img)
                self.kep_label.config(image=self.tk_img)
            except Exception:
                self.kep_label.config(image='')
        else:
            self.kep_label.config(image='')

        t_hash = self._termek_hash(termek)
        eredm = self.eredmeny_map.get(t_hash, {})

        if keep_kat:
            self.rebuild_kategoria_radios_with_current()
            if prefill_props is not None:
                self.frissit_tulajdonsagok(prefill_props)   # PREFILL a hozott tulajdonságokkal
            elif clear_props:
                self.frissit_tulajdonsagok({})
            else:
                self.frissit_tulajdonsagok()
        else:
            self.fokategoria_var.set(eredm.get('fokategoria', ''))
            self.fokategoria_valtozott()
            self.alkategoria_var.set(eredm.get('alkategoria', ''))
            self.alkategoria_valtozott()
            self.altipus_var.set(eredm.get('altipus', ''))
            self.frissit_tulajdonsagok(eredm.get('tulajdonsagok', {}))

        self.statusz_label.config(text=f"Státusz: {self.statusz_map[t_hash]}")

    def clear_kategoria_radios(self):
        for var in [self.fokategoria_var, self.alkategoria_var, self.altipus_var]:
            var.set('')
        for frame in [self.alkategoria_radio_frame, self.altipus_radio_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

    def frissit_tulajdonsagok(self, mentett_ertekek=None):
        """
        Megjelenítés az egységesített spec alapján:
        - {}                               -> boolean (checkbox)
        - [ "a", "b", ... ]                -> többválasztós (checkboxok)
        - {"values":[...], "type":"single"}-> egyválasztós (rádió)  <-- első opció ALAPBÓL kijelölve
        - {"values":[...]}                 -> többválasztós (checkboxok)
        """
        for widget in self.tulajdonsagok_frame.winfo_children():
            widget.destroy()
        self.tulajdonsagok_widgets = {}

        fok = self.fokategoria_var.get()
        alk = self.alkategoria_var.get()
        alt = self.altipus_var.get()
        tulajd = get_tulajdonsagok(self.kategoriak_dict, fok, alk, alt)

        font_cb = font.Font(family="Arial", size=9)
        for nev, spec in tulajd.items():
            keret = tk.Frame(self.tulajdonsagok_frame)
            keret.pack(anchor='w', fill=tk.X, padx=2, pady=1)
            tk.Label(keret, text=nev + ':', anchor='w').pack(side=tk.LEFT)

            # BOOLEAN
            if isinstance(spec, dict) and 'values' not in spec and len(spec) == 0:
                var = tk.BooleanVar()
                if mentett_ertekek and nev in mentett_ertekek:
                    var.set(bool(mentett_ertekek[nev]))
                cb = tk.Checkbutton(keret, variable=var, font=font_cb)
                cb.pack(side=tk.LEFT)
                self.tulajdonsagok_widgets[nev] = var
                continue

            # LISTA / 'values'
            if isinstance(spec, list) or (isinstance(spec, dict) and 'values' in spec):
                if isinstance(spec, dict):
                    values = spec.get('values', [])
                    is_single = spec.get('type') == 'single' or spec.get('unique') is True
                else:
                    values = spec
                    is_single = False  # plain lista -> multi

                # EGYVÁLASZTÓS (RADIO) – alapértelmezetten az első opció kijelölése
                if is_single:
                    var = tk.StringVar()
                    preset = None
                    if mentett_ertekek and nev in mentett_ertekek and isinstance(mentett_ertekek[nev], str):
                        preset = mentett_ertekek[nev]
                    if not preset and values:
                        preset = values[0]  # <-- első opció
                    if preset:
                        var.set(preset)
                    width = get_group_width(values, font_cb)
                    row = None
                    for i, v in enumerate(values):
                        if i % 5 == 0:
                            row = tk.Frame(keret)
                            row.pack(anchor='w')
                        rb = tk.Radiobutton(row, text=v, variable=var, value=v, font=font_cb, anchor='w', padx=4, indicatoron=0)
                        rb.pack(side=tk.LEFT, padx=0, pady=0)
                        rb.config(width=width//8)
                    self.tulajdonsagok_widgets[nev] = ('single', var)
                else:
                    # TÖBBVÁLASZTÓS (CHECKBOXOK)
                    csoport = []
                    width = get_group_width(values, font_cb)
                    row = None
                    preset_list = []
                    if mentett_ertekek and nev in mentett_ertekek:
                        me = mentett_ertekek[nev]
                        if isinstance(me, list):
                            preset_list = me
                        elif isinstance(me, str):
                            preset_list = [me]
                    for i, v in enumerate(values):
                        if i % 5 == 0:
                            row = tk.Frame(keret)
                            row.pack(anchor='w')
                        var = tk.BooleanVar(value=(v in preset_list))
                        cb = tk.Checkbutton(row, text=v, variable=var, font=font_cb, anchor='w', padx=4)
                        cb.pack(side=tk.LEFT, padx=0, pady=0)
                        cb.config(width=width//8)
                        csoport.append((v, var))
                    self.tulajdonsagok_widgets[nev] = csoport
                continue

            # Fallback -> boolean
            var = tk.BooleanVar()
            if mentett_ertekek and nev in mentett_ertekek:
                var.set(bool(mentett_ertekek[nev]))
            cb = tk.Checkbutton(keret, variable=var, font=font_cb)
            cb.pack(side=tk.LEFT)
            self.tulajdonsagok_widgets[nev] = var

    def lista_katt(self, event):
        if getattr(self, 'suppress_select', False):
            return
        if not self.termek_lista.curselection():
            return
        j = self.termek_lista.curselection()[0]
        if 0 <= j < len(self.filtered_termekek):
            idx = self.filtered_termekek[j][0]
            self.cur = j
            self.termek_betoltes(idx)

    def mentes(self, for_kov=False, return_payload=False):
        """
        Mentés. Ha for_kov=True, nem renderelünk új terméket azonnal (a caller intézi).
        Ha return_payload=True, (advanced_due_to_save, eredm) tuple-t ad vissza.
        """
        if not self.filtered_termekek:
            return (False, None) if return_payload else False
        cur_index = self.termek_lista.curselection()[0] if self.termek_lista.curselection() else 0

        termek = self.termekek[self.kivalasztott_index]
        t_hash = self._termek_hash(termek)
        fok = self.fokategoria_var.get()
        alk = self.alkategoria_var.get()
        alt = self.altipus_var.get()
        tul = self.lekerdezes_tulajdonsagok()
        h = kategoriak_hash(fok, alk, alt, tul)
        statusz = "kesz" if fok and alk else "folyamatban"
        eredm = {
            "termek": termek,
            "fokategoria": fok,
            "alkategoria": alk,
            "altipus": alt,
            "tulajdonsagok": tul,
            "kategoria_hash": h,
            "statusz": statusz
        }
        self.eredmeny_map[t_hash] = eredm
        self.statusz_map[t_hash] = statusz

        # Lista frissítés, kijelölés kézben tartása
        self.suppress_select = True
        self.termek_lista_frissit()

        def _hash_in_filtered(hsh):
            for i, _t in self.filtered_termekek:
                if self._termek_hash(self.termekek[i]) == hsh:
                    return True
            return False

        still_in = _hash_in_filtered(t_hash)

        if still_in:
            new_j = None
            for j, (i, _t) in enumerate(self.filtered_termekek):
                if self._termek_hash(self.termekek[i]) == t_hash:
                    new_j = j
                    break
            if new_j is None:
                new_j = 0
        else:
            if self.filtered_termekek:
                new_j = min(cur_index, len(self.filtered_termekek) - 1)
            else:
                new_j = None

        self.termek_lista.selection_clear(0, tk.END)
        if new_j is not None:
            self.termek_lista.selection_set(new_j)
            self.termek_lista.see(new_j)
            self.cur = new_j
            self.kivalasztott_index = self.filtered_termekek[new_j][0]
        self.suppress_select = False

        with open('eredmeny.json', 'w', encoding='utf-8') as f:
            json.dump(list(self.eredmeny_map.values()), f, ensure_ascii=False, indent=2)
        self.statusz_label.config(text=f"Státusz: {self.statusz_map[t_hash]}")
        self.frissit_statusz_kimutatas()

        self.advanced_due_to_save = not still_in

        if not for_kov and self.filtered_termekek and (new_j is not None):
            idx = self.kivalasztott_index
            self.termek_betoltes(idx, keep_kat=False, clear_props=False)

        if return_payload:
            return (self.advanced_due_to_save, eredm)
        return self.advanced_due_to_save

    def lekerdezes_tulajdonsagok(self):
        eredm = {}
        for nev, widget in self.tulajdonsagok_widgets.items():
            if isinstance(widget, tuple) and widget[0] == 'single':
                eredm[nev] = widget[1].get()
            elif isinstance(widget, tk.BooleanVar):
                eredm[nev] = bool(widget.get())
            elif isinstance(widget, list):
                vals = [v for v, var in widget if var.get()]
                eredm[nev] = vals
        return eredm

    def kovetkezo(self, keep_kat=True, prefill_props=None):
        if not self.filtered_termekek:
            return
        next_j = self.cur + 1
        if next_j >= len(self.filtered_termekek):
            return

        next_idx = self.filtered_termekek[next_j][0]
        self.kivalasztott_index = next_idx

        self.suppress_select = True
        self.termek_lista.selection_clear(0, tk.END)
        self.termek_lista.selection_set(next_j)
        self.termek_lista.see(next_j)
        self.suppress_select = False

        self.cur = next_j

        next_t = self.termekek[next_idx]
        next_saved = self.eredmeny_map.get(self._termek_hash(next_t), {})
        has_saved_cat = bool(next_saved.get('fokategoria') and next_saved.get('alkategoria'))

        if keep_kat and not has_saved_cat:
            # Kategóriák + (új) TULAJDONSÁGOK továbbvitele
            self.termek_betoltes(next_idx, keep_kat=True, clear_props=False, prefill_props=prefill_props or {})
        else:
            self.termek_betoltes(next_idx, keep_kat=False, clear_props=False)

    def mentes_es_kovetkezo(self):
        # Mentsünk, és kérjük vissza a most mentett payloadot (benne a tulajdonságokkal)
        advanced, payload = self.mentes(for_kov=True, return_payload=True)
        if not self.filtered_termekek or payload is None:
            return

        prev_tul = payload.get("tulajdonsagok", {})

        if advanced:
            # A szűrés miatt már a "következő" van kijelölve -> NE léptessünk még egyszer,
            # viszont vigyük át a kategóriákat és a tulajdonságokat is.
            next_idx = self.kivalasztott_index
            next_t = self.termekek[next_idx]
            next_saved = self.eredmeny_map.get(self._termek_hash(next_t), {})
            has_saved_cat = bool(next_saved.get('fokategoria') and next_saved.get('alkategoria'))
            if not has_saved_cat:
                self.termek_betoltes(next_idx, keep_kat=True, clear_props=False, prefill_props=prev_tul)
            else:
                self.termek_betoltes(next_idx, keep_kat=False, clear_props=False)
        else:
            # Normál eset: most léptessünk egyet, és adjuk át a tulajdonságokat is
            self.kovetkezo(keep_kat=True, prefill_props=prev_tul)

if __name__ == '__main__':
    os.makedirs('kepek', exist_ok=True)
    with open('archive/kategoriak_json/kategori_tulajdonsagok_uj_sorted.json', 'r', encoding='utf-8') as f:
        kategoriak_dict = json.load(f)
    termekek = beolvas_termekek_csv('archive/etc/termekek_spar.csv')
    if os.path.exists('eredmeny.json'):
        with open('eredmeny.json', 'r', encoding='utf-8') as f:
            eredmenyek = json.load(f)
    else:
        eredmenyek = []

    root = tk.Tk()
    root.title("Termék kategorizáló és tulajdonság-kezelő")
    root.geometry("1200x750")
    app = TermekTagger(root, termekek, kategoriak_dict, eredmenyek)
    root.mainloop()
