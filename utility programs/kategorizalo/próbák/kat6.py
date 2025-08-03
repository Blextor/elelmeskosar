import tkinter as tk
from tkinter import ttk, messagebox
import json, hashlib, requests
from PIL import Image, ImageTk
from io import BytesIO
import os
import re
import unicodedata

### --- Segédfüggvények ---

def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9]+', '_', value).strip('_')
    return value

def termek_fajlnev(termek):
    nev = slugify(termek['nev'])
    kisz = slugify(termek.get('kiszereles', ''))
    hash_str = hashlib.md5(termek['kep_url'].encode('utf-8')).hexdigest()[:8]
    return f"{nev}_{kisz}_{hash_str}.jpg"

def kep_letolt(termek, kepek_dir="kepek"):
    os.makedirs(kepek_dir, exist_ok=True)
    fajlnev = termek_fajlnev(termek)
    utvonal = os.path.join(kepek_dir, fajlnev)
    if not os.path.exists(utvonal):
        try:
            resp = requests.get(termek['kep_url'], timeout=10)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content))
            img.save(utvonal)
        except Exception as e:
            print(f"Kép letöltési hiba: {e}")
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

def get_tulajdonsagok(kategoriak_dict, fokategoria, alkategoria, altipus):
    tulajd = {}
    if fokategoria:
        tulajd.update(kategoriak_dict[fokategoria].get('tulajdonságok', {}))
    if fokategoria and alkategoria:
        alk = kategoriak_dict[fokategoria]['alkategóriák'][alkategoria]
        tulajd.update(alk.get('tulajdonságok', {}))
        if altipus and 'altípusok' in alk and altipus in alk['altípusok']:
            tulajd.update(alk['altípusok'][altipus].get('tulajdonságok', {}))
    return tulajd

### --- Fő alkalmazás osztály ---

class TermekTagger:
    def __init__(self, master, termekek, kategoriak_dict, eredmenyek):
        self.master = master
        self.termekek = termekek
        self.kategoriak_dict = kategoriak_dict
        self.eredmenyek = eredmenyek

        self.statusz_map = {}
        self.eredmeny_map = {}
        for eredmeny in self.eredmenyek:
            termeknev = eredmeny['termek']['nev']
            self.eredmeny_map[termeknev] = eredmeny
            self.statusz_map[termeknev] = eredmeny.get('statusz', 'folyamatban')
        for t in termekek:
            if t['nev'] not in self.statusz_map:
                self.statusz_map[t['nev']] = 'nincs'

        self.statusz_color = {
            'kesz': 'green', 'folyamatban': 'orange', 'elavult': 'red', 'nincs': 'gray'
        }

        self.kivalasztott_index = 0
        self.filtered_termekek = []

        # --- Bal panel: termék szerkesztő ---
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.nev_label = tk.Label(self.left_frame, text="", font=('Arial', 16))
        self.nev_label.pack(pady=5)
        self.kep_label = tk.Label(self.left_frame)
        self.kep_label.pack(pady=5)

        self.fokategoria_var = tk.StringVar()
        self.alkategoria_var = tk.StringVar()
        self.altipus_var = tk.StringVar()

        tk.Label(self.left_frame, text="Főkategória:").pack(anchor='w', padx=4)
        self.fokategoria_radio_frame = tk.Frame(self.left_frame)
        self.fokategoria_radio_frame.pack(anchor='w', padx=6)
        self.fokategoria_radios = {}
        for fokat in kategoriak_dict.keys():
            rb = tk.Radiobutton(self.fokategoria_radio_frame, text=fokat, variable=self.fokategoria_var, value=fokat, command=self.fokategoria_valtozott)
            rb.pack(anchor='w', side=tk.TOP)
            self.fokategoria_radios[fokat] = rb

        tk.Label(self.left_frame, text="Kategória:").pack(anchor='w', padx=4)
        self.alkategoria_radio_frame = tk.Frame(self.left_frame)
        self.alkategoria_radio_frame.pack(anchor='w', padx=6)
        self.alkategoria_radios = {}

        tk.Label(self.left_frame, text="Altípus:").pack(anchor='w', padx=4)
        self.altipus_radio_frame = tk.Frame(self.left_frame)
        self.altipus_radio_frame.pack(anchor='w', padx=6)
        self.altipus_radios = {}

        self.tulajdonsagok_frame = tk.LabelFrame(self.left_frame, text="Tulajdonságok")
        self.tulajdonsagok_frame.pack(pady=5, fill=tk.X, padx=4)
        self.tulajdonsagok_widgets = {}

        self.save_button = tk.Button(self.left_frame, text="Mentés", command=self.mentes)
        self.save_button.pack(pady=2)
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

        # Főkategória szűrő (checkbox csoport)
        tk.Label(self.filter_frame, text="Főkategória:").pack(anchor='w')
        self.filter_fokategoria_vars = {}
        self.filter_fokategoria_checkboxes = {}
        self.filter_fokategoria_box = tk.Frame(self.filter_frame)
        self.filter_fokategoria_box.pack(anchor='w')
        self._build_checkbox_row(self.filter_fokategoria_box, list(self.kategoriak_dict.keys()), self.filter_fokategoria_vars, self.filter_fokategoria_checkboxes, self.on_fokategoria_filter_change)

        # Mind gomb külön sorban
        self.filter_fokategoria_mind_var = tk.BooleanVar()
        mind_row = tk.Frame(self.filter_frame)
        mind_row.pack(anchor='w')
        cb_mind = tk.Checkbutton(mind_row, text="Mind", variable=self.filter_fokategoria_mind_var, command=lambda: self.on_mind_checkbox(self.filter_fokategoria_vars, self.filter_fokategoria_mind_var))
        cb_mind.pack(side=tk.LEFT)

        # Alkategória szűrő (csak akkor, ha egy főkategória van pipálva)
        tk.Label(self.filter_frame, text="Kategória:").pack(anchor='w')
        self.filter_alkategoria_vars = {}
        self.filter_alkategoria_checkboxes = {}
        self.filter_alkategoria_box = tk.Frame(self.filter_frame)
        self.filter_alkategoria_box.pack(anchor='w')
        self.filter_alkategoria_mind_var = tk.BooleanVar()
        mind_row2 = tk.Frame(self.filter_frame)
        mind_row2.pack(anchor='w')
        cb_mind2 = tk.Checkbutton(mind_row2, text="Mind", variable=self.filter_alkategoria_mind_var, command=lambda: self.on_mind_checkbox(self.filter_alkategoria_vars, self.filter_alkategoria_mind_var))
        cb_mind2.pack(side=tk.LEFT)

        # Altípus szűrő (csak akkor, ha egy kategória van pipálva)
        tk.Label(self.filter_frame, text="Altípus:").pack(anchor='w')
        self.filter_altipus_vars = {}
        self.filter_altipus_checkboxes = {}
        self.filter_altipus_box = tk.Frame(self.filter_frame)
        self.filter_altipus_box.pack(anchor='w')
        self.filter_altipus_mind_var = tk.BooleanVar()
        mind_row3 = tk.Frame(self.filter_frame)
        mind_row3.pack(anchor='w')
        cb_mind3 = tk.Checkbutton(mind_row3, text="Mind", variable=self.filter_altipus_mind_var, command=lambda: self.on_mind_checkbox(self.filter_altipus_vars, self.filter_altipus_mind_var))
        cb_mind3.pack(side=tk.LEFT)

        # Státuszok szűrője (checkbox, többszörös)
        tk.Label(self.filter_frame, text="Státusz:").pack(anchor='w')
        self.filter_statusz_vars = {}
        self.filter_statusz_frame = tk.Frame(self.filter_frame)
        self.filter_statusz_frame.pack(anchor='w')
        for sz in ['kesz', 'folyamatban', 'elavult', 'nincs']:
            v = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.filter_statusz_frame, text=sz.capitalize(), variable=v, command=self.filter_frissit)
            cb.pack(side=tk.LEFT)
            self.filter_statusz_vars[sz] = v

        self.termek_lista = tk.Listbox(self.right_frame)
        self.termek_lista.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2)
        self.termek_lista.bind('<<ListboxSelect>>', self.lista_katt)

        self.statusz_label = tk.Label(self.right_frame, text="")
        self.statusz_label.pack(side=tk.BOTTOM, pady=3)

        self.filter_frissit()

    ### --- Checkbox panel építő ---
    def _build_checkbox_row(self, parent, options, var_dict, cb_dict, command, max_per_row=5):
        # Először töröl
        for widget in parent.winfo_children():
            widget.destroy()
        var_dict.clear()
        cb_dict.clear()
        row = None
        for i, opt in enumerate(options):
            if i % max_per_row == 0:
                row = tk.Frame(parent)
                row.pack(anchor='w')
            var = tk.BooleanVar()
            cb = tk.Checkbutton(row, text=opt, variable=var, command=command)
            cb.pack(side=tk.LEFT)
            var_dict[opt] = var
            cb_dict[opt] = cb

    ### --- "Mind" checkbox logika ---
    def on_mind_checkbox(self, var_dict, mind_var):
        v = mind_var.get()
        for var in var_dict.values():
            var.set(v)
        self.filter_frissit()

    ### --- Főkategória szűrő változás ---
    def on_fokategoria_filter_change(self):
        # Ha bármi más változott, a "Mind" menjen ki
        if any(v.get() for k, v in self.filter_fokategoria_vars.items()):
            self.filter_fokategoria_mind_var.set(False)
        self.filter_frissit()

    def on_alkategoria_filter_change(self):
        if any(v.get() for v in self.filter_alkategoria_vars.values()):
            self.filter_alkategoria_mind_var.set(False)
        self.filter_frissit()

    def on_altipus_filter_change(self):
        if any(v.get() for v in self.filter_altipus_vars.values()):
            self.filter_altipus_mind_var.set(False)
        self.filter_frissit()

    ### --- Főkategória pipáláskor, alkategória/altípus szűrőpanel frissül ---
    def filter_frissit(self, event=None):
        # Főkategória opciók alapján alkategória panelt épít
        fokats = [k for k,v in self.filter_fokategoria_vars.items() if v.get()]
        if len(fokats) == 1:
            alkats = get_alkategoriak(self.kategoriak_dict, fokats[0])
        else:
            alkats = []
        self._build_checkbox_row(self.filter_alkategoria_box, alkats, self.filter_alkategoria_vars, self.filter_alkategoria_checkboxes, self.on_alkategoria_filter_change)
        self.filter_alkategoria_mind_var.set(False)

        # Alkategória alapján altípus panelt épít
        alkats_selected = [k for k,v in self.filter_alkategoria_vars.items() if v.get()]
        if len(fokats) == 1 and len(alkats_selected) == 1:
            altipusok = get_altipusok(self.kategoriak_dict, fokats[0], alkats_selected[0])
        else:
            altipusok = []
        self._build_checkbox_row(self.filter_altipus_box, altipusok, self.filter_altipus_vars, self.filter_altipus_checkboxes, self.on_altipus_filter_change)
        self.filter_altipus_mind_var.set(False)

        self.termek_lista_frissit()

    ### --- Terméklista frissítés, szűrés ---
    def termek_lista_frissit(self):
        self.termek_lista.delete(0, tk.END)
        nev_filter = self.nev_filter_var.get().lower()
        fokats = [k for k,v in self.filter_fokategoria_vars.items() if v.get()]
        alkats = [k for k,v in self.filter_alkategoria_vars.items() if v.get()]
        altipusok = [k for k,v in self.filter_altipus_vars.items() if v.get()]
        statuszok = [k for k,v in self.filter_statusz_vars.items() if v.get()]

        self.filtered_termekek = []
        for i, termek in enumerate(self.termekek):
            nev = termek['nev']
            statusz = self.statusz_map[nev]
            eredm = self.eredmeny_map.get(nev, {})
            fokat = eredm.get('fokategoria', "")
            alk = eredm.get('alkategoria', "")
            alt = eredm.get('altipus', "")

            if nev_filter and nev_filter not in nev.lower():
                continue
            if fokats and fokat not in fokats:
                continue
            if alkats and alk not in alkats:
                continue
            if altipusok and alt not in altipusok:
                continue
            if statusz not in statuszok:
                continue

            self.filtered_termekek.append((i, termek))

        for j, (idx, termek) in enumerate(self.filtered_termekek):
            nev = termek['nev']
            statusz = self.statusz_map[nev]
            self.termek_lista.insert(tk.END, nev)
            self.termek_lista.itemconfig(j, {'fg': self.statusz_color[statusz]})

        if not self.filtered_termekek:
            self.nev_label.config(text="")
            self.kep_label.config(image='')
            self.clear_kategoria_radios()
            self.frissit_tulajdonsagok()
            self.statusz_label.config(text="")
        else:
            self.termek_lista.selection_clear(0, tk.END)
            self.termek_lista.selection_set(0)
            idx = self.filtered_termekek[0][0]
            self.termek_betoltes(idx)

    ### ------ Termék betöltése & szerkesztőpanel ------
    def termek_betoltes(self, idx):
        self.kivalasztott_index = idx
        termek = self.termekek[idx]
        self.nev_label.config(text=f"{termek['nev']} ({termek.get('kiszereles','')})")

        kep_path = kep_letolt(termek)
        if kep_path and os.path.exists(kep_path):
            try:
                img = Image.open(kep_path)
                img.thumbnail((220,220))
                self.tk_img = ImageTk.PhotoImage(img)
                self.kep_label.config(image=self.tk_img)
            except Exception as e:
                self.kep_label.config(image='')
        else:
            self.kep_label.config(image='')

        eredm = self.eredmeny_map.get(termek['nev'], {})
        self.set_kategoria_radios(eredm.get('fokategoria', ''), eredm.get('alkategoria', ''), eredm.get('altipus', ''))
        self.frissit_tulajdonsagok(eredm.get('tulajdonsagok', {}))

        self.statusz_label.config(text=f"Státusz: {self.statusz_map[termek['nev']]}")

    def clear_kategoria_radios(self):
        for var in [self.fokategoria_var, self.alkategoria_var, self.altipus_var]:
            var.set('')
        for frame in [self.alkategoria_radio_frame, self.altipus_radio_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

    def set_kategoria_radios(self, fokat, alk, alt):
        self.fokategoria_var.set(fokat)
        self.fokategoria_valtozott()
        self.alkategoria_var.set(alk)
        self.alkategoria_valtozott()
        self.altipus_var.set(alt)

    ### --- Bal oldali szerkesztőpanel radio kezelők ---
    def fokategoria_valtozott(self):
        for widget in self.alkategoria_radio_frame.winfo_children():
            widget.destroy()
        self.alkategoria_radios = {}
        fok = self.fokategoria_var.get()
        alkats = get_alkategoriak(self.kategoriak_dict, fok) if fok else []
        for i, alk in enumerate(alkats):
            if i % 5 == 0:
                row = tk.Frame(self.alkategoria_radio_frame)
                row.pack(anchor='w')
            rb = tk.Radiobutton(row, text=alk, variable=self.alkategoria_var, value=alk, command=self.alkategoria_valtozott)
            rb.pack(side=tk.LEFT)
            self.alkategoria_radios[alk] = rb
        self.alkategoria_var.set('')
        self.alkategoria_valtozott()

    def alkategoria_valtozott(self):
        for widget in self.altipus_radio_frame.winfo_children():
            widget.destroy()
        self.altipus_radios = {}
        fok = self.fokategoria_var.get()
        alk = self.alkategoria_var.get()
        alts = get_altipusok(self.kategoriak_dict, fok, alk) if fok and alk else []
        for i, alt in enumerate(alts):
            if i % 5 == 0:
                row = tk.Frame(self.altipus_radio_frame)
                row.pack(anchor='w')
            rb = tk.Radiobutton(row, text=alt, variable=self.altipus_var, value=alt, command=self.frissit_tulajdonsagok)
            rb.pack(side=tk.LEFT)
            self.altipus_radios[alt] = rb
        self.altipus_var.set('')
        self.frissit_tulajdonsagok()

    ### --- Tulajdonság mezők (mindig checkbox csoport) ---
    def frissit_tulajdonsagok(self, mentett_ertekek=None):
        for widget in self.tulajdonsagok_frame.winfo_children():
            widget.destroy()
        self.tulajdonsagok_widgets = {}

        fok = self.fokategoria_var.get()
        alk = self.alkategoria_var.get()
        alt = self.altipus_var.get()
        tulajd = get_tulajdonsagok(self.kategoriak_dict, fok, alk, alt)

        if not tulajd:
            return

        for nev, val in tulajd.items():
            keret = tk.Frame(self.tulajdonsagok_frame)
            keret.pack(anchor='w', fill=tk.X, padx=2, pady=1)
            tk.Label(keret, text=nev + ':', anchor='w').pack(side=tk.LEFT)
            if isinstance(val, dict):
                var = tk.BooleanVar()
                if mentett_ertekek and nev in mentett_ertekek:
                    var.set(bool(mentett_ertekek[nev]))
                cb = tk.Checkbutton(keret, variable=var)
                cb.pack(side=tk.LEFT)
                self.tulajdonsagok_widgets[nev] = var
            elif isinstance(val, list):
                csoport = []
                row = None
                for i, v in enumerate(val):
                    if i % 5 == 0:
                        row = tk.Frame(keret)
                        row.pack(anchor='w')
                    var = tk.BooleanVar()
                    if mentett_ertekek and nev in mentett_ertekek and v in mentett_ertekek[nev]:
                        var.set(True)
                    cb = tk.Checkbutton(row, text=v, variable=var)
                    cb.pack(side=tk.LEFT)
                    csoport.append((v, var))
                self.tulajdonsagok_widgets[nev] = csoport

    ### --- Terméklista kattintás -----
    def lista_katt(self, event):
        if not self.termek_lista.curselection():
            return
        j = self.termek_lista.curselection()[0]
        if 0 <= j < len(self.filtered_termekek):
            idx = self.filtered_termekek[j][0]
            self.termek_betoltes(idx)

    ### --- Mentés -----
    def mentes(self):
        if not self.filtered_termekek:
            return
        termek = self.termekek[self.kivalasztott_index]
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
        self.eredmeny_map[termek['nev']] = eredm
        self.statusz_map[termek['nev']] = statusz
        self.termek_lista_frissit()
        with open('eredmeny.json', 'w', encoding='utf-8') as f:
            json.dump(list(self.eredmeny_map.values()), f, ensure_ascii=False, indent=2)
        self.statusz_label.config(text=f"Státusz: {self.statusz_map[termek['nev']]}")

    def lekerdezes_tulajdonsagok(self):
        eredm = {}
        for nev, widget in self.tulajdonsagok_widgets.items():
            if isinstance(widget, tk.BooleanVar):
                eredm[nev] = bool(widget.get())
            elif isinstance(widget, list):
                vals = [v for v, var in widget if var.get()]
                eredm[nev] = vals
        return eredm

    def kovetkezo(self):
        if not self.filtered_termekek:
            return
        cur = None
        for j, (idx, t) in enumerate(self.filtered_termekek):
            if idx == self.kivalasztott_index:
                cur = j
                break
        if cur is not None and cur+1 < len(self.filtered_termekek):
            next_idx = self.filtered_termekek[cur+1][0]
            self.termek_betoltes(next_idx)
            self.termek_lista.selection_clear(0, tk.END)
            self.termek_lista.selection_set(cur+1)

if __name__ == '__main__':
    os.makedirs('kepek', exist_ok=True)
    with open('kategori_tulajdonsagok.json', 'r', encoding='utf-8') as f:
        kategoriak_dict = json.load(f)
    with open('termekek.json', 'r', encoding='utf-8') as f:
        termekek = json.load(f)
    if os.path.exists('eredmeny.json'):
        with open('eredmeny.json', 'r', encoding='utf-8') as f:
            eredmenyek = json.load(f)
    else:
        eredmenyek = []

    root = tk.Tk()
    root.title("Termék kategorizáló és tulajdonság-kezelő")
    root.geometry("1200x720")
    app = TermekTagger(root, termekek, kategoriak_dict, eredmenyek)
    root.mainloop()
