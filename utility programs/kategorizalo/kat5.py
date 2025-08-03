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

        # --- Státusz és eredmény ---
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

        # --- UI Layout ---
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(master)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Bal panel: termék szerkesztő ---
        self.nev_label = tk.Label(self.left_frame, text="", font=('Arial', 16))
        self.nev_label.pack(pady=5)
        self.kep_label = tk.Label(self.left_frame)
        self.kep_label.pack(pady=5)

        # --- Radio kategóriaválasztók ---
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

        # --- Jobb panel: szűrők + terméklista ---
        self.filter_frame = tk.LabelFrame(self.right_frame, text="Szűrés")
        self.filter_frame.pack(side=tk.TOP, fill=tk.X, padx=3, pady=2)

        # Kategória szűrő: radio főkategória
        tk.Label(self.filter_frame, text="Főkategória:").grid(row=0, column=0, sticky='w')
        self.filter_fokategoria_var = tk.StringVar()
        self.filter_fokategoria_radio_frame = tk.Frame(self.filter_frame)
        self.filter_fokategoria_radio_frame.grid(row=0, column=1, sticky='w')
        for fokat in [""] + list(self.kategoriak_dict.keys()):
            rb = tk.Radiobutton(self.filter_fokategoria_radio_frame, text=fokat if fokat else "Mind", variable=self.filter_fokategoria_var, value=fokat, command=self.filter_frissit)
            rb.pack(side=tk.LEFT)

        tk.Label(self.filter_frame, text="Kategória:").grid(row=1, column=0, sticky='w')
        self.filter_alkategoria_var = tk.StringVar()
        self.filter_alkategoria_radio_frame = tk.Frame(self.filter_frame)
        self.filter_alkategoria_radio_frame.grid(row=1, column=1, sticky='w')

        tk.Label(self.filter_frame, text="Altípus:").grid(row=2, column=0, sticky='w')
        self.filter_altipus_var = tk.StringVar()
        self.filter_altipus_radio_frame = tk.Frame(self.filter_frame)
        self.filter_altipus_radio_frame.grid(row=2, column=1, sticky='w')

        # Státuszok szűrője
        tk.Label(self.filter_frame, text="Státusz:").grid(row=3, column=0, sticky='w')
        self.filter_statusz_vars = {}
        statuszok = ['kesz', 'folyamatban', 'elavult', 'nincs']
        self.filter_statusz_frame = tk.Frame(self.filter_frame)
        self.filter_statusz_frame.grid(row=3, column=1, sticky='w')
        for sz in statuszok:
            v = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.filter_statusz_frame, text=sz.capitalize(), variable=v, command=self.filter_frissit)
            cb.pack(side=tk.LEFT)
            self.filter_statusz_vars[sz] = v

        # Név kereső
        tk.Label(self.filter_frame, text="Név keresés:").grid(row=4, column=0, sticky='w')
        self.nev_filter_var = tk.StringVar()
        self.nev_filter_entry = tk.Entry(self.filter_frame, textvariable=self.nev_filter_var)
        self.nev_filter_entry.grid(row=4, column=1, sticky='ew')
        self.nev_filter_entry.bind('<KeyRelease>', self.filter_frissit)

        self.filter_frame.grid_columnconfigure(1, weight=1)

        self.termek_lista = tk.Listbox(self.right_frame)
        self.termek_lista.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2)
        self.termek_lista.bind('<<ListboxSelect>>', self.lista_katt)

        self.statusz_label = tk.Label(self.right_frame, text="")
        self.statusz_label.pack(side=tk.BOTTOM, pady=3)

        self.update_filter_kategoria_radios()
        self.termek_lista_frissit()

    ### ------ Szűrőpanelen a radio csoportok frissítése ------
    def update_filter_kategoria_radios(self):
        # Alkategóriák radio gombjai
        for widget in self.filter_alkategoria_radio_frame.winfo_children():
            widget.destroy()
        fok = self.filter_fokategoria_var.get()
        if fok and fok in self.kategoriak_dict:
            alkats = [""] + get_alkategoriak(self.kategoriak_dict, fok)
        else:
            alkats = [""]
        for alk in alkats:
            rb = tk.Radiobutton(self.filter_alkategoria_radio_frame, text=alk if alk else "Mind", variable=self.filter_alkategoria_var, value=alk, command=self.filter_frissit)
            rb.pack(side=tk.LEFT)
        # Altípus radio
        for widget in self.filter_altipus_radio_frame.winfo_children():
            widget.destroy()
        fok = self.filter_fokategoria_var.get()
        alk = self.filter_alkategoria_var.get()
        if fok and alk and fok in self.kategoriak_dict and alk in self.kategoriak_dict[fok]['alkategóriák']:
            alts = [""] + get_altipusok(self.kategoriak_dict, fok, alk)
        else:
            alts = [""]
        for alt in alts:
            rb = tk.Radiobutton(self.filter_altipus_radio_frame, text=alt if alt else "Mind", variable=self.filter_altipus_var, value=alt, command=self.filter_frissit)
            rb.pack(side=tk.LEFT)

    ### ------ Jobb oldal: szűrés ------
    def filter_frissit(self, event=None):
        self.update_filter_kategoria_radios()
        self.termek_lista_frissit()

    def termek_lista_frissit(self):
        self.termek_lista.delete(0, tk.END)
        nev_filter = self.nev_filter_var.get().lower()
        fokat_filter = self.filter_fokategoria_var.get()
        alk_filter = self.filter_alkategoria_var.get()
        alt_filter = self.filter_altipus_var.get()
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
            if fokat_filter and fokat != fokat_filter:
                continue
            if alk_filter and alk != alk_filter:
                continue
            if alt_filter and alt != alt_filter:
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

    ### ------ Bal oldali kategória radio kezelők ------
    def fokategoria_valtozott(self):
        for widget in self.alkategoria_radio_frame.winfo_children():
            widget.destroy()
        self.alkategoria_radios = {}
        fok = self.fokategoria_var.get()
        alkats = get_alkategoriak(self.kategoriak_dict, fok) if fok else []
        for alk in alkats:
            rb = tk.Radiobutton(self.alkategoria_radio_frame, text=alk, variable=self.alkategoria_var, value=alk, command=self.alkategoria_valtozott)
            rb.pack(anchor='w')
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
        for alt in alts:
            rb = tk.Radiobutton(self.altipus_radio_frame, text=alt, variable=self.altipus_var, value=alt, command=self.frissit_tulajdonsagok)
            rb.pack(anchor='w')
            self.altipus_radios[alt] = rb
        self.altipus_var.set('')
        self.frissit_tulajdonsagok()

    ### ------ Tulajdonság mezők ------
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
            if isinstance(val, dict):  # Egyszerű checkbox
                var = tk.BooleanVar()
                if mentett_ertekek and nev in mentett_ertekek:
                    var.set(bool(mentett_ertekek[nev]))
                cb = tk.Checkbutton(keret, variable=var)
                cb.pack(side=tk.LEFT)
                self.tulajdonsagok_widgets[nev] = var
            elif isinstance(val, list):
                csoport = []
                for v in val:
                    var = tk.BooleanVar()
                    if mentett_ertekek and nev in mentett_ertekek and v in mentett_ertekek[nev]:
                        var.set(True)
                    cb = tk.Checkbutton(keret, text=v, variable=var)
                    cb.pack(side=tk.LEFT)
                    csoport.append((v, var))
                self.tulajdonsagok_widgets[nev] = csoport

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

### --- FŐ FUTTATÁS ---

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
    root.geometry("1150x680")
    app = TermekTagger(root, termekek, kategoriak_dict, eredmenyek)
    root.mainloop()
