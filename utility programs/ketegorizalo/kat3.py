import tkinter as tk
from tkinter import ttk
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

def kategoriak_hash(kategoria):
    szuro_lista = sorted([f"{sz['nev']}|{sz['tipus']}" for sz in kategoria['szurok']])
    s = "|".join(szuro_lista)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def get_kategoria_by_name(kategoriak, nev):
    for k in kategoriak:
        if k['nev'] == nev:
            return k
    return None

def get_kategoria_hash_map(kategoriak):
    return {k['nev']: kategoriak_hash(k) for k in kategoriak}

### ----------- Fő alkalmazás osztály -----------

class TermekTagger:
    def __init__(self, master, termekek, kategoriak, eredmenyek):
        self.master = master
        self.termekek = termekek
        self.kategoriak = kategoriak
        self.eredmenyek = eredmenyek
        self.kategoria_hash_map = get_kategoria_hash_map(kategoriak)

        # Státusz és eredmény leképezése terméknévre
        self.statusz_map = {}
        self.eredmeny_map = {}
        for eredmeny in self.eredmenyek:
            termeknev = eredmeny['termek']['nev']
            self.eredmeny_map[termeknev] = eredmeny
            katnev = eredmeny.get('kategoria', '')
            regi_hash = eredmeny.get('kategoria_hash', None)
            uj_hash = self.kategoria_hash_map.get(katnev, '')
            if regi_hash is None:
                self.statusz_map[termeknev] = 'folyamatban'
            elif regi_hash != uj_hash:
                self.statusz_map[termeknev] = 'elavult'
            else:
                self.statusz_map[termeknev] = 'kesz'
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

        # ---- Bal panel: termék szerkesztő ----
        self.nev_label = tk.Label(self.left_frame, text="", font=('Arial', 16))
        self.nev_label.pack(pady=5)
        self.kep_label = tk.Label(self.left_frame)
        self.kep_label.pack(pady=5)

        self.kategoria_var = tk.StringVar()
        self.kategoria_combo = ttk.Combobox(self.left_frame, textvariable=self.kategoria_var, values=[k["nev"] for k in kategoriak], state='readonly')
        self.kategoria_combo.pack(pady=3)
        self.kategoria_combo.bind("<<ComboboxSelected>>", self.frissit_szurok)

        self.szurok_frame = tk.Frame(self.left_frame)
        self.szurok_frame.pack(pady=5, fill=tk.X)
        self.szurok_entries = {}

        self.save_button = tk.Button(self.left_frame, text="Mentés", command=self.mentes)
        self.save_button.pack(pady=2)
        self.kovetkezo_button = tk.Button(self.left_frame, text="Következő", command=self.kovetkezo)
        self.kovetkezo_button.pack(pady=2)

        # ---- Jobb panel: szűrők + terméklista ----
        self.filter_frame = tk.Frame(self.right_frame)
        self.filter_frame.pack(side=tk.TOP, fill=tk.X, padx=3, pady=2)

        tk.Label(self.filter_frame, text="Név keresés:").grid(row=0, column=0, sticky='w')
        self.nev_filter_var = tk.StringVar()
        self.nev_filter_entry = tk.Entry(self.filter_frame, textvariable=self.nev_filter_var)
        self.nev_filter_entry.grid(row=0, column=1, sticky='ew')
        self.nev_filter_entry.bind('<KeyRelease>', self.filter_frissit)

        tk.Label(self.filter_frame, text="Kategória:").grid(row=1, column=0, sticky='w')
        self.kategoria_filter_var = tk.StringVar()
        kategoria_lista = [""] + [k["nev"] for k in self.kategoriak]
        self.kategoria_filter_combo = ttk.Combobox(self.filter_frame, textvariable=self.kategoria_filter_var, values=kategoria_lista, state='readonly')
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

        # Frissítések
        self.termek_lista_frissit()

    ### ------ Adatkezelés & UI ------

    def filter_frissit(self, event=None):
        self.termek_lista_frissit()

    def termek_lista_frissit(self):
        self.termek_lista.delete(0, tk.END)
        nev_filter = self.nev_filter_var.get().lower()
        kat_filter = self.kategoria_filter_var.get()
        csak_nem_kateg = self.nem_kateg_cb_var.get()

        self.filtered_termekek = []
        for i, termek in enumerate(self.termekek):
            nev = termek['nev']
            statusz = self.statusz_map[nev]
            eredm = self.eredmeny_map.get(nev, {})
            katnev = eredm.get('kategoria', "")

            # Szűrés
            if nev_filter and nev_filter not in nev.lower():
                continue
            if kat_filter and katnev != kat_filter:
                continue
            if csak_nem_kateg and statusz not in ('nincs', 'elavult'):
                continue

            self.filtered_termekek.append((i, termek))

        for j, (idx, termek) in enumerate(self.filtered_termekek):
            nev = termek['nev']
            statusz = self.statusz_map[nev]
            self.termek_lista.insert(tk.END, nev)
            self.termek_lista.itemconfig(j, {'fg': self.statusz_color[statusz]})

        # Ha nincs találat, ürítjük a szerkesztő panelt!
        if not self.filtered_termekek:
            self.nev_label.config(text="")
            self.kep_label.config(image='')
            self.kategoria_var.set("")
            self.frissit_szurok()
            self.statusz_label.config(text="")
        else:
            # Automatikusan az első elemre ugrunk
            self.termek_lista.selection_clear(0, tk.END)
            self.termek_lista.selection_set(0)
            idx = self.filtered_termekek[0][0]
            self.termek_betoltes(idx)

    def termek_betoltes(self, idx):
        self.kivalasztott_index = idx
        termek = self.termekek[idx]
        self.nev_label.config(text=f"{termek['nev']} ({termek['kiszereles']})")

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

        # Előző értékek visszatöltése
        eredm = self.eredmeny_map.get(termek['nev'], {})
        katnev = eredm.get('kategoria', '')
        self.kategoria_var.set(katnev)
        self.frissit_szurok()
        # Szűrők kitöltése
        tul = eredm.get('tulajdonsagok', {})
        for nev, entry in self.szurok_entries.items():
            entry.delete(0, tk.END)
            if nev in tul:
                entry.insert(0, tul[nev])

        self.statusz_label.config(text=f"Státusz: {self.statusz_map[termek['nev']]}")

    def frissit_szurok(self, event=None):
        for widget in self.szurok_frame.winfo_children():
            widget.destroy()
        kategoria = get_kategoria_by_name(self.kategoriak, self.kategoria_var.get())
        self.szurok_entries = {}
        if kategoria:
            for szuro in kategoria["szurok"]:
                lbl = tk.Label(self.szurok_frame, text=szuro["nev"])
                lbl.pack(anchor='w', padx=2)
                # Típus-specifikus input (itt egyszerűen csak Entry, de bővíthető)
                entry = tk.Entry(self.szurok_frame)
                entry.pack(fill=tk.X, padx=2, pady=1)
                self.szurok_entries[szuro["nev"]] = entry

    def lista_katt(self, event):
        if not self.termek_lista.curselection():
            return
        j = self.termek_lista.curselection()[0]
        if 0 <= j < len(self.filtered_termekek):
            idx = self.filtered_termekek[j][0]
            self.termek_betoltes(idx)

    def mentes(self):
        if not self.filtered_termekek:
            return
        termek = self.termekek[self.kivalasztott_index]
        valasztott_kategoria = self.kategoria_var.get()
        kategoria_hash = self.kategoria_hash_map.get(valasztott_kategoria, '')
        szuro_ertekek = {nev: entry.get() for nev, entry in self.szurok_entries.items()}
        eredm = {
            "termek": termek,
            "kategoria": valasztott_kategoria,
            "kategoria_hash": kategoria_hash,
            "tulajdonsagok": szuro_ertekek
        }
        self.eredmeny_map[termek['nev']] = eredm

        # Státusz update
        if valasztott_kategoria and all(v for v in szuro_ertekek.values()):
            self.statusz_map[termek['nev']] = 'kesz'
        else:
            self.statusz_map[termek['nev']] = 'folyamatban'
        self.termek_lista_frissit()

        # Eredmény mentése
        with open('eredmeny.json', 'w', encoding='utf-8') as f:
            json.dump(list(self.eredmeny_map.values()), f, ensure_ascii=False, indent=2)
        self.statusz_label.config(text=f"Státusz: {self.statusz_map[termek['nev']]}")

    def kovetkezo(self):
        # A szűrt listában léptetünk!
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

### ------------ FŐ PROGRAM FUTTATÁS ------------

if __name__ == '__main__':
    os.makedirs('kepek', exist_ok=True)
    with open('kategoria.json', 'r', encoding='utf-8') as f:
        kategoriak = json.load(f)
    with open('termekek.json', 'r', encoding='utf-8') as f:
        termekek = json.load(f)
    if os.path.exists('eredmeny.json'):
        with open('eredmeny.json', 'r', encoding='utf-8') as f:
            eredmenyek = json.load(f)
    else:
        eredmenyek = []

    root = tk.Tk()
    root.title("Termék kategorizáló és tulajdonság-kezelő")
    root.geometry("900x540")
    app = TermekTagger(root, termekek, kategoriak, eredmenyek)
    root.mainloop()
