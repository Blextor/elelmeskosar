import tkinter as tk
from tkinter import ttk
import json
import requests
from PIL import Image, ImageTk
from io import BytesIO

# JSON betöltés
with open('kategoria.json', 'r', encoding='utf-8') as f:
    kategoriak = json.load(f)
with open('termekek.json', 'r', encoding='utf-8') as f:
    termekek = json.load(f)

class TermekTagger:
    def __init__(self, master, termekek, kategoriak):
        self.master = master
        self.termekek = termekek
        self.kategoriak = kategoriak
        self.aktualis_index = 0
        self.eredmeny = []

        # UI elemek
        self.nev_label = tk.Label(master, text="")
        self.nev_label.pack()

        self.kep_label = tk.Label(master)
        self.kep_label.pack()

        self.kategoria_var = tk.StringVar()
        self.kategoria_combo = ttk.Combobox(master, textvariable=self.kategoria_var, values=[k["nev"] for k in kategoriak])
        self.kategoria_combo.pack()
        self.kategoria_combo.bind("<<ComboboxSelected>>", self.frissit_szurok)

        self.szurok_frame = tk.Frame(master)
        self.szurok_frame.pack()

        self.kovetkezo_button = tk.Button(master, text="Következő", command=self.kovetkezo)
        self.kovetkezo_button.pack()

        self.termek_betoltes()

    def termek_betoltes(self):
        termek = self.termekek[self.aktualis_index]
        self.nev_label.config(text=f"{termek['nev']} ({termek['kiszereles']})")
        # Kép letöltés
        response = requests.get(termek['kep_url'])
        img = Image.open(BytesIO(response.content))
        img.thumbnail((200,200))
        self.tk_img = ImageTk.PhotoImage(img)
        self.kep_label.config(image=self.tk_img)
        self.kategoria_var.set("")
        self.frissit_szurok()

    def frissit_szurok(self, event=None):
        for widget in self.szurok_frame.winfo_children():
            widget.destroy()
        kategoria = next((k for k in self.kategoriak if k["nev"] == self.kategoria_var.get()), None)
        self.szurok_entries = {}
        if kategoria:
            for szuro in kategoria["szurok"]:
                lbl = tk.Label(self.szurok_frame, text=szuro["nev"])
                lbl.pack()
                entry = tk.Entry(self.szurok_frame)
                entry.pack()
                self.szurok_entries[szuro["nev"]] = entry

    def kovetkezo(self):
        termek = self.termekek[self.aktualis_index]
        valasztott_kategoria = self.kategoria_var.get()
        szuro_ertekek = {nev: entry.get() for nev, entry in self.szurok_entries.items()}
        self.eredmeny.append({
            "termek": termek,
            "kategoria": valasztott_kategoria,
            "tulajdonsagok": szuro_ertekek
        })
        self.aktualis_index += 1
        if self.aktualis_index < len(self.termekek):
            self.termek_betoltes()
        else:
            with open('eredmeny.json', 'w', encoding='utf-8') as f:
                json.dump(self.eredmeny, f, ensure_ascii=False, indent=2)
            self.master.quit()

root = tk.Tk()
app = TermekTagger(root, termekek, kategoriak)
root.mainloop()
