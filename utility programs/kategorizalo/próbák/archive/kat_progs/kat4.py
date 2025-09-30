import tkinter as tk
from tkinter import ttk, messagebox
import json, hashlib, requests
from PIL import Image, ImageTk
from io import BytesIO
import os
import re
import unicodedata

### ----------- Segédfüggvények -----------

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

### ----------- Kategória fa kezelő -----------

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

### ----------- Fő alkalmazás osztály -----------

class TermekTagger:
    def __init__(self, master, termekek, kategoriak_dict, eredmenyek):
        self.master = master
        self.termekek = termekek
        self.kategoriak_dict = kategoriak_dict
        self.eredmenyek = eredmenyek

        # --- Státusz- és eredménykezelés ---
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

        # ---- UI Layout ----
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Bal panel: termék szerkesztő ---
        self.nev_label = tk.Label(self.left_frame, text="", font=('Arial', 16))
        self.nev_label.pack(pady=5)
        self.kep_label = tk.Label(self.left_frame)
        self.kep_label.pack(pady=5)

        # --- Kategória választók ---
        self.fokategoria_var = tk.StringVar()
        self.alkategoria_var = tk.StringVar()
        self.altipus_var = tk.StringVar()

        tk.Label(self.left_frame, text="Főkategória:").pack(anchor='w', padx=4)
        self.fokategoria_combo = ttk.Combobox(self.left_frame, textvariable=self.fokategoria_var, values=list(kategoriak_dict.keys()), state='readonly')
        self.fokategoria_combo.pack(fill=tk.X, padx=4, pady=2)
        self.fokategoria_combo.bind("<<ComboboxSelected>>", self.fokategoria_valtozott)

        tk.Label(self.left_frame, text="Kategória:").pack(anchor='w', padx=4)
        self.alkategoria_combo = ttk.Combobox(self.left_frame, textvariable=self.alkategoria_var, state='readonly')
        self.alkategoria_combo.pack(fill=tk.X, padx=4, pady=2)
        self.alkategoria_combo.bind("<<ComboboxSelected>>", self.alkategoria_valtozott)

        tk.Label(self.left_frame, text="Altípus:").pack(anchor='w', padx=4)
        self.altipus_combo = ttk.Combobox(self.left_frame, textvariable=self.altipus_var, state='readonly')
        self.altipus_combo.pack(fill=tk.X, padx=4, pady=2)
        self.altipus_combo.bind("<<ComboboxSelected>>", self.frissit_tulajdonsagok)

        self.tulajdonsagok_frame = tk.LabelFrame(self.left_frame, text="Tulajdonságok")
        self.tulajdonsagok_frame.pack(pady=5, fill=tk.X, padx=4)
        self.tulajdonsagok_widgets = {}

        self.save_button = tk.Button(self.left_frame, text="Mentés", command=self.mentes)
        self.save_button.pack(pady=2)
        self.kovetkezo_button = tk.Button(self.left_frame, text="Következő", command=self.kovetkezo)
        self.kovetkezo_button.pack(pady=2)

        # --- Jobb panel: szűrők + terméklista ---
        self.filter_frame = tk.Frame(self.right_frame)
        self.filter_frame.pack(side=tk.TOP, fill=tk.X, padx=3, pady=2)

        tk.Label(self.filter_frame, text="Név keresés:").grid(row=0, column=0, sticky='w')
        self.nev_filter_var = tk.StringVar()
        self.nev_filter_entry = tk.Entry(self.filter_frame, textvariable=self.nev_filter_var)
        self.nev_filter_entry.grid(row=0, column=1, sticky='ew')
        self.nev_filter_entry.bind('<KeyRelease>', self.filter_frissit)

        tk.Label(self.filter_frame, text="Főkategória:").grid(row=1, column=0, sticky='w')
        self.kategoria_filter_var = tk.StringVar()
        filter_fokategorias = [""] + list(self.kategoriak_dict.keys())
        self.kategoria_filter_combo = ttk.Combobox(self.filter_frame, textvariable=self.kategoria_filter_var, values=filter_fokategorias, state='readonly')
        self.kategoria_filter_combo.grid(row=1, column=1, sticky='ew')
        self.kategoria_filter_combo.bind("<<ComboboxSelected>>", self.filter_frissit)

        self.nem_kateg_cb_var = tk.BooleanVar()
        self.nem_kateg_cb = tk.Checkbutton(self.filter_frame, text="Csak nem kategorizált", variable=self.nem_kateg_cb_var, command=self.filter_frissit)
        self.nem_kateg_cb.grid(row=2, column=0, columnspan=2, sticky='w')

        self.filter_frame.grid_columnconfigure(1, weight=1)

        self.termek_lista = tk.Listbox(self.right_frame)
        self.termek_lista.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2)
        self.termek_lista.bind('<<ListboxSelect>>', self.lista_katt)

        self.statusz_label = tk.Label(self.right_frame, text="")
        self.statusz_label.pack(side=tk.BOTTOM, pady=3)

        # Frissítés
        self.termek_lista_frissit()

    ### ------ Szűrés & lista ------
    def filter_frissit(self, event=None):
        self.termek_lista_frissit()

    def termek_lista_frissit(self):
        self.termek_lista.delete(0, tk.END)
        nev_filter = self.nev_filter_var.get().lower()
        fokat_filter = self.kategoria_filter_var.get()
        csak_nem_kateg = self.nem_kateg_cb_var.get()

        self.filtered_termekek = []
        for i, termek in enumerate(self.termekek):
            nev = termek['nev']
            statusz = self.statusz_map[nev]
            eredm = self.eredmeny_map.get(nev, {})
            fokat = eredm.get('fokategoria', "")

            if nev_filter and nev_filter not in nev.lower():
                continue
            if fokat_filter and fokat != fokat_filter:
                continue
            if csak_nem_kateg and statusz not in ('nincs', 'elavult'):
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
            self.clear_kategoria_comboboxes()
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
        # Visszatöltés a kategória választókba
        self.fokategoria_var.set(eredm.get('fokategoria', ''))
        self.fokategoria_valtozott()
        self.alkategoria_var.set(eredm.get('alkategoria', ''))
        self.alkategoria_valtozott()
        self.altipus_var.set(eredm.get('altipus', ''))
        self.frissit_tulajdonsagok(eredm.get('tulajdonsagok', {}))

        self.statusz_label.config(text=f"Státusz: {self.statusz_map[termek['nev']]}")

    def clear_kategoria_comboboxes(self):
        self.fokategoria_var.set('')
        self.alkategoria_var.set('')
        self.altipus_var.set('')
        self.alkategoria_combo['values'] = []
        self.altipus_combo['values'] = []

    ### ------ Kategória választók kezelése ------
    def fokategoria_valtozott(self, event=None):
        fok = self.fokategoria_var.get()
        if fok:
            alkats = get_alkategoriak(self.kategoriak_dict, fok)
            self.alkategoria_combo['values'] = alkats
            if self.alkategoria_var.get() not in alkats:
                self.alkategoria_var.set('')
            self.alkategoria_valtozott()
        else:
            self.alkategoria_combo['values'] = []
            self.altipus_combo['values'] = []
            self.alkategoria_var.set('')
            self.altipus_var.set('')
            self.frissit_tulajdonsagok()

    def alkategoria_valtozott(self, event=None):
        fok = self.fokategoria_var.get()
        alk = self.alkategoria_var.get()
        if fok and alk:
            alts = get_altipusok(self.kategoriak_dict, fok, alk)
            self.altipus_combo['values'] = alts
            if self.altipus_var.get() not in alts:
                self.altipus_var.set('')
            self.frissit_tulajdonsagok()
        else:
            self.altipus_combo['values'] = []
            self.altipus_var.set('')
            self.frissit_tulajdonsagok()

    ### ------ Tulajdonság mezők ------
    def frissit_tulajdonsagok(self, mentett_ertekek=None):
        # Előzőek törlése
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
            if isinstance(val, dict):  # Üres dict: egyszerű checkbox (pl. "bio")
                var = tk.BooleanVar()
                if mentett_ertekek and nev in mentett_ertekek:
                    var.set(bool(mentett_ertekek[nev]))
                cb = tk.Checkbutton(keret, variable=var)
                cb.pack(side=tk.LEFT)
                self.tulajdonsagok_widgets[nev] = var
            elif isinstance(val, list):
                # Ha rövid (kevesebb, mint 6 érték): checkbox csoport
                if len(val) <= 6:
                    csoport = []
                    for v in val:
                        var = tk.BooleanVar()
                        if mentett_ertekek and nev in mentett_ertekek and v in mentett_ertekek[nev]:
                            var.set(True)
                        cb = tk.Checkbutton(keret, text=v, variable=var)
                        cb.pack(side=tk.LEFT)
                        csoport.append((v, var))
                    self.tulajdonsagok_widgets[nev] = csoport
                else:
                    # Sokanál: többválasztós Listbox
                    lb = tk.Listbox(keret, selectmode='multiple', height=min(len(val), 6), exportselection=False)
                    for item in val:
                        lb.insert(tk.END, item)
                    if mentett_ertekek and nev in mentett_ertekek:
                        for i, item in enumerate(val):
                            if item in mentett_ertekek[nev]:
                                lb.selection_set(i)
                    lb.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    self.tulajdonsagok_widgets[nev] = lb

    ### ------ Terméklista kattintás ------
    def lista_katt(self, event):
        if not self.termek_lista.curselection():
            return
        j = self.termek_lista.curselection()[0]
        if 0 <= j < len(self.filtered_termekek):
            idx = self.filtered_termekek[j][0]
            self.termek_betoltes(idx)

    ### ------ Mentés ------
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
            # Egyszerű checkbox
            if isinstance(widget, tk.BooleanVar):
                eredm[nev] = bool(widget.get())
            # Csoportos checkbox
            elif isinstance(widget, list):
                vals = [v for v, var in widget if var.get()]
                eredm[nev] = vals
            # Listbox (többválasztós)
            elif isinstance(widget, tk.Listbox):
                vals = [widget.get(i) for i in widget.curselection()]
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

### ------------ FŐ PROGRAM ------------

if __name__ == '__main__':
    os.makedirs('kepek', exist_ok=True)
    with open('archive/kategoriak_json/kategori_tulajdonsagok.json', 'r', encoding='utf-8') as f:
        kategoriak_dict = json.load(f)
    with open('archive/etc/termekek.json', 'r', encoding='utf-8') as f:
        termekek = json.load(f)
    if os.path.exists('eredmeny.json'):
        with open('eredmeny.json', 'r', encoding='utf-8') as f:
            eredmenyek = json.load(f)
    else:
        eredmenyek = []

    root = tk.Tk()
    root.title("Termék kategorizáló és tulajdonság-kezelő")
    root.geometry("1050x620")
    app = TermekTagger(root, termekek, kategoriak_dict, eredmenyek)
    root.mainloop()
