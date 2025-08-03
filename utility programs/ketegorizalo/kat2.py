import tkinter as tk
from tkinter import ttk, messagebox
import json, hashlib, requests
from PIL import Image, ImageTk
from io import BytesIO
import os

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

class TermekTagger:
    def __init__(self, master, termekek, kategoriak, eredmenyek):
        self.master = master
        self.termekek = termekek
        self.kategoriak = kategoriak
        self.eredmenyek = eredmenyek  # régi eredmény
        self.kategoria_hash_map = get_kategoria_hash_map(kategoriak)

        # státusz beállítása minden termékre
        self.statusz_map = {}
        self.eredmeny_map = {}
        for eredmeny in self.eredmenyek:
            termeknev = eredmeny['termek']['nev']
            self.eredmeny_map[termeknev] = eredmeny
            katnev = eredmeny['kategoria']
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

        # UI elemek
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # bal panel
        self.nev_label = tk.Label(self.left_frame, text="", font=('Arial', 16))
        self.nev_label.pack()
        self.kep_label = tk.Label(self.left_frame)
        self.kep_label.pack()
        self.kategoria_var = tk.StringVar()
        self.kategoria_combo = ttk.Combobox(self.left_frame, textvariable=self.kategoria_var, values=[k["nev"] for k in kategoriak])
        self.kategoria_combo.pack()
        self.kategoria_combo.bind("<<ComboboxSelected>>", self.frissit_szurok)
        self.szurok_frame = tk.Frame(self.left_frame)
        self.szurok_frame.pack()
        self.save_button = tk.Button(self.left_frame, text="Mentés", command=self.mentes)
        self.save_button.pack()
        self.kovetkezo_button = tk.Button(self.left_frame, text="Következő", command=self.kovetkezo)
        self.kovetkezo_button.pack()

        # jobb panel – termék lista státusszal
        self.termek_lista = tk.Listbox(self.right_frame)
        self.termek_lista.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.termek_lista.bind('<<ListboxSelect>>', self.lista_katt)
        self.statusz_color = {
            'kesz': 'green', 'folyamatban': 'orange', 'elavult': 'red', 'nincs': 'gray'
        }
        self.statusz_label = tk.Label(self.right_frame, text="")
        self.statusz_label.pack(side=tk.BOTTOM)

        self.szurok_entries = {}
        self.kivalasztott_index = 0
        self.termek_lista_frissit()
        self.termek_betoltes(self.kivalasztott_index)

    def termek_lista_frissit(self):
        self.termek_lista.delete(0, tk.END)
        for i, termek in enumerate(self.termekek):
            nev = termek['nev']
            statusz = self.statusz_map[nev]
            self.termek_lista.insert(tk.END, nev)
            self.termek_lista.itemconfig(i, {'fg': self.statusz_color[statusz]})

    def termek_betoltes(self, idx):
        self.kivalasztott_index = idx
        termek = self.termekek[idx]
        self.nev_label.config(text=f"{termek['nev']} ({termek['kiszereles']})")
        # Kép betöltés (helyi cache!)
        kep_path = f"kepek/{os.path.basename(termek['kep_url'])}"
        if not os.path.exists(kep_path):
            try:
                response = requests.get(termek['kep_url'])
                with open(kep_path, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                kep_path = None
        if kep_path and os.path.exists(kep_path):
            img = Image.open(kep_path)
            img.thumbnail((200,200))
            self.tk_img = ImageTk.PhotoImage(img)
            self.kep_label.config(image=self.tk_img)
        else:
            self.kep_label.config(image='')

        # Előző értékek betöltése ha vannak
        eredm = self.eredmeny_map.get(termek['nev'], {})
        katnev = eredm.get('kategoria', '')
        self.kategoria_var.set(katnev)
        self.frissit_szurok()
        # Tulajdonságok visszatöltése
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
                lbl.pack()
                entry = tk.Entry(self.szurok_frame)
                entry.pack()
                self.szurok_entries[szuro["nev"]] = entry

    def lista_katt(self, event):
        if not self.termek_lista.curselection():
            return
        idx = self.termek_lista.curselection()[0]
        self.termek_betoltes(idx)

    def mentes(self):
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
        # státusz update
        if valasztott_kategoria and all(v for v in szuro_ertekek.values()):
            self.statusz_map[termek['nev']] = 'kesz'
        else:
            self.statusz_map[termek['nev']] = 'folyamatban'
        self.termek_lista_frissit()
        # eredmény mentése
        with open('eredmeny.json', 'w', encoding='utf-8') as f:
            json.dump(list(self.eredmeny_map.values()), f, ensure_ascii=False, indent=2)
        self.statusz_label.config(text=f"Státusz: {self.statusz_map[termek['nev']]}")

    def kovetkezo(self):
        if self.kivalasztott_index + 1 < len(self.termekek):
            self.termek_betoltes(self.kivalasztott_index + 1)

# --- fő futás ---
if __name__ == '__main__':
    # Könyvtárak létrehozása, fájlok betöltése
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
    app = TermekTagger(root, termekek, kategoriak, eredmenyek)
    root.mainloop()
