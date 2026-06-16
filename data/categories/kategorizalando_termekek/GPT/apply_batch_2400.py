# -*- coding: utf-8 -*-
"""Batch 2400-2499: Auchan grill világ — grillkolbász, szalonna, pácolt grill húsok,
+ Tudatos táplálkozás: vegán húspótló (tofu/szejtán/vegli/bászka/burger), vegán szószok,
gluténmentes pékáru. Döntések kéziek (kép+adat)."""
import csv, json, os, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
TREE = os.path.join(BASE, "kategoriak_2026-06-13.json")
CSVP = os.path.join(BASE, "kategorizalatlan_termekek.csv")
ERED = os.path.join(BASE, "eredmeny.json")

def kategoriak_hash(fok, al, alt, tul):
    key = f"{fok}|{al}|{alt}|{json.dumps(tul, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def norm_blokk(blokk):
    out = {}
    if isinstance(blokk, dict) and ("egyedi" in blokk or "csoportos" in blokk):
        for nev, v in blokk.get("egyedi", {}).items():
            if isinstance(v, dict): out[nev] = {}
            elif isinstance(v, list): out[nev] = {"values": v, "type": "single"}
            elif isinstance(v, str): out[nev] = {"values": [v], "type": "single"}
            else: out[nev] = {}
        for nev, v in blokk.get("csoportos", {}).items():
            out[nev] = v if isinstance(v, list) else []
    return out

def schema(tree, fok, al, alt):
    res = {}
    c = tree[fok]
    res.update(norm_blokk(c.get("tulajdonságok", {})))
    alk = c["alkategóriák"][al]
    res.update(norm_blokk(alk.get("tulajdonságok", {})))
    if alt:
        res.update(norm_blokk(alk["altípusok"][alt].get("tulajdonságok", {})))
    return res

def add_vals(lst, vals):
    for v in vals:
        if v not in lst: lst.append(v)

def extend_tree(t):
    hh = t["Hús, hal, felvágott"]
    add_vals(hh["tulajdonságok"]["egyedi"]["márka"],
             ["TARAVIS", "Hajnal", "HAJDÚHÚS", "TERRA PANNONIA",
              "Vegan Grill", "Real Nature", "Well Well", "Bio ABC"])
    add_vals(hh["alkategóriák"]["Csirke"]["tulajdonságok"]["csoportos"]["ízesítés"],
             ["buffalo", "tandori", "sültcsirke", "dolce vita", "édes-csípős", "paradicsomos-salsa"])
    add_vals(hh["alkategóriák"]["Sertés"]["tulajdonságok"]["csoportos"]["ízesítés"],
             ["bbq", "sörös", "mustáros", "montreál", "zöldfűszeres", "egyéb"])
    add_vals(hh["alkategóriák"]["Szalonna, tepertő, zsiradék"]["tulajdonságok"]["csoportos"]["stílus"],
             ["egyéb", "császár"])
    add_vals(t["Tejtermékek és tojás"]["alkategóriák"]["Sajt"]["tulajdonságok"]["egyedi"]["márka"],
             ["Minus L"])
    al = t["Alapanyag, sütés-főzés"]["alkategóriák"]["Szószok, öntetek, dresszingek"]
    add_vals(al["tulajdonságok"]["egyedi"]["márka"], ["Hellmann's", "Condito"])
    ed = t["Édesség, snack, rágcsálnivaló"]["alkategóriák"]["Gumicukor, zselé, pillecukor"]
    add_vals(ed["tulajdonságok"]["egyedi"]["márka"], ["Demi"])
    pk = t["Pékáru"]["alkategóriák"]
    add_vals(pk["Kenyér"]["tulajdonságok"]["egyedi"]["márka"], ["Nutrifree"])
    add_vals(pk["Egyéb sós pékáru"]["tulajdonságok"]["egyedi"]["márka"], ["Nutrifree"])
    add_vals(pk["Hotdog buci és hamburger zsemle"]["tulajdonságok"]["egyedi"]["márka"], ["Balviten"])

HH = "Hús, hal, felvágott"; AL = "Alapanyag, sütés-főzés"
ED = "Édesség, snack, rágcsálnivaló"; TM = "Tejtermékek és tojás"; PK = "Pékáru"

D = []
def d(i, fok, al, alt, **ov): D.append((i, fok, al, alt, ov))

def kolb(i, izes, marka, hus="sertés", forma="pár", alt="Főző-, grillkolbász", hazai=True):
    d(i, HH, "Felvágottak, húskészítmény", alt, **{"hazai/magyar": hazai}, márka=marka,
      **{"húsfajta": [hus], "forma": [forma], "ízesítés": izes,
         "hústartalom": ["egyéb"], "csomagolás": ["védőgázas"]})

def szalonna(i, marka, stilus, fustolt=True, pacolt=False, hazai=True):
    d(i, HH, "Szalonna, tepertő, zsiradék", "Szalonna (angol, kolozsvári)",
      **{"hazai/magyar": hazai}, márka=marka, füstölt=fustolt, **{"pácolt / érlelt": pacolt},
      **{"csomagolás": ["vákuumcsomagolt"], "alap": ["sertés"], "stílus": [stilus]})

def csirke(i, alt, izes, marka, elok, filee=True, csontos=False):
    d(i, HH, "Csirke", alt, **{"hazai/magyar": True}, márka=marka, filé=filee, csontos=csontos,
      **{"pácolt / fűszerezett": True}, **{"csomagolás": ["tálcás"], "előkészítés": [elok], "ízesítés": izes})

def sertes(i, alt, izes, marka, elok="szeletelt"):
    d(i, HH, "Sertés", alt, **{"hazai/magyar": True}, márka=marka, **{"pácolt / fűszerezett": True},
      **{"csomagolás": ["vákuumcsomagolt"], "előkészítés": [elok], "ízesítés": izes})

def darathus(i, alt, hus, marka, zsir="egyéb", csom="védőgázas"):
    d(i, HH, "Darált hús, fasírt", alt, **{"hazai/magyar": True}, márka=marka,
      **{"húsfajta": [hus], "csomagolás": [csom], "zsírtartalom": [zsir]})

def huspotlo(i, alt, alap, forma, marka, bio=False, csom="tálca"):
    d(i, HH, "Növényi húspótló", alt, bio=bio, **{"hazai/magyar": False}, márka=marka, vegán=True,
      **{"készítmény (növényi/kevert)": True}, **{"alap": [alap], "forma": [forma], "csomagolás": [csom]})

def grillsajt(i, izes, marka, fajta="egyéb", keszitmeny=False, forma="tömb", laktozmentes=False):
    d(i, TM, "Sajt", "Grillsajt / halloumi / sütnivaló", forma=forma, érlelt=True, laktózmentes=laktozmentes,
      **{"készítmény (növényi zsiradékkal)": keszitmeny}, kiszerelés="vákuumcsomagolt",
      márka=marka, **{"ízesítés": izes, "fajta": [fajta]})

def friss_sajt(i, marka, fajta, forma="tömb", laktozmentes=False, izes="natúr"):
    d(i, TM, "Sajt", "Friss / lágy sajt", forma=forma, érlelt=False, laktózmentes=laktozmentes,
      kiszerelés="vákuumcsomagolt", márka=marka, **{"ízesítés": [izes], "fajta": [fajta]})

def szosz(i, alt, marka, alap, iz, kisz="üveg", konyha="egyéb", csipos="csemege", gm=False, light=False, **extra):
    base = dict(márka=marka, gluténmentes=gm, light=light, kiszerelés=kisz)
    base["alap"] = alap; base["íz"] = iz; base["konyha / stílus"] = [konyha]; base["csípősség"] = [csipos]
    base.update(extra)
    d(i, AL, "Szószok, öntetek, dresszingek", alt, **base)

def hotdogbuci(i, marka, tipus, fajta="egyéb"):
    d(i, PK, "Hotdog buci és hamburger zsemle", None, márka=marka, gluténmentes=True, csomagolt=True,
      méret="normál", **{"fajta": [fajta], "típus": [tipus]})

# ---- SHEET 1 (2400-2424) ----
kolb(2400, ["egyéb"], "Master Good", hus="csirke")
kolb(2401, ["sajtos"], "Master Good", hus="csirke")
kolb(2402, ["egyéb"], "Wiesbauer", hus="vegyes", hazai=False)
kolb(2403, ["magyaros", "hot-dog"], "Pick")
kolb(2404, ["sajtos", "hot-dog"], "Pick")
kolb(2405, ["egyéb"], "Wiesbauer", hus="vegyes", hazai=False)
kolb(2406, ["hot-dog", "mozzarella"], "Pick")
kolb(2407, ["egyéb"], "Kaiser", hus="vegyes", hazai=False)
szalonna(2408, "Hegedűs", "egyéb")
szalonna(2409, "Sarudi", "egyéb")
szalonna(2410, "Hegedűs", "egyéb")
kolb(2411, ["frankfurti"], "Gierlinger", forma="pár", alt="Virsli, debreceni", hazai=False)
szalonna(2412, "Hegedűs", "egyéb")
kolb(2413, ["lecsó"], "Kometa")
szalonna(2414, "Sarudi", "császár")
darathus(2415, "Csevapcsicsa", "sertés-marha mix", "Hízóföld")
kolb(2416, ["egyéb"], "Auchan Prémium", hus="vegyes")
szalonna(2417, "Sarudi", "kolozsvári")
szalonna(2418, "Privát Hús", "császár")
szalonna(2419, "Privát Hús", "kolozsvári")
kolb(2420, ["sajtos", "jalapeno"], "Gierlinger", hazai=False)
kolb(2421, ["mozzarella"], "Gierlinger", hazai=False)
kolb(2422, ["magyaros"], "Kometa")
kolb(2423, ["sajtos"], "Gierlinger", hazai=False)
kolb(2424, ["klasszikus", "hot-dog"], "Pick")

# ---- SHEET 2 (2425-2449) ----
csirke(2425, "Csirkeszárny", ["buffalo"], "Master Good", "egész", filee=False, csontos=True)
kolb(2426, ["bajor"], "Kometa")
csirke(2427, "Csirkecomb", ["buffalo"], "Master Good", "combfilé")
csirke(2428, "Csirkecomb", ["fokhagymás-zöldfűszeres"], "Master Good", "combfilé")
csirke(2429, "Csirkecomb", ["magyaros"], "Master Good", "combfilé")
csirke(2430, "Csirkecomb", ["paradicsomos-salsa"], "TARAVIS", "felsőcomb")
csirke(2431, "Csirkemell", ["édes-csípős"], "TARAVIS", "filézett")
csirke(2432, "Csirkemell", ["buffalo"], "Master Good", "filézett")
csirke(2433, "Csirkemell", ["magyaros"], "Master Good", "filézett")
csirke(2434, "Csirkemell", ["sültcsirke"], "Master Good", "filézett")
csirke(2435, "Csirkemell", ["dolce vita"], "Master Good", "filézett")
csirke(2436, "Csirkemell", ["mézes-mustáros"], "TARAVIS", "filézett")
sertes(2437, "Tarja", ["magyaros"], "Kometa")
sertes(2438, "Tarja", ["zöldfűszeres", "fokhagymás"], "Kometa")
szalonna(2439, "Hajnal", "császár", fustolt=False, pacolt=True)
sertes(2440, "Karaj", ["bbq"], "Hajnal")
sertes(2441, "Tarja", ["sörös"], "Hajnal")
sertes(2442, "Tarja", ["mustáros"], "Hajnal")
sertes(2443, "Tarja", ["bbq"], "Hajnal")
csirke(2444, "Csirkemell", ["dolce vita"], "Master Good", "filézett")
sertes(2445, "Karaj", ["magyaros"], "Hajnal")
sertes(2446, "Karaj", ["montreál"], "Hajnal")
sertes(2447, "Karaj", ["mustáros"], "Hajnal")
sertes(2448, "Tarja", ["egyéb"], "HAJDÚHÚS")
darathus(2449, "Darált hús", "marha", "Auchan Kedvenc", zsir="20% alatt")

# ---- SHEET 3 (2450-2474) ----
darathus(2450, "Húspogácsa, hamburgerhús", "sertés-marha mix", "Kometa")
darathus(2451, "Csevapcsicsa", "sertés-marha mix", "Kometa")
csirke(2452, "Csirkemell", ["fokhagymás-zöldfűszeres"], "Master Good", "filézett")
csirke(2453, "Csirkecomb", ["mézes-mustáros"], "Master Good", "combfilé")
csirke(2454, "Csirkemell", ["tandori"], "Master Good", "filézett")
darathus(2455, "Húspogácsa, hamburgerhús", "marha", "TERRA PANNONIA")
sertes(2456, "Tarja", ["magyaros"], "Kometa")
sertes(2457, "Lapocka", ["magyaros"], "Kometa", elok="kockázott")
sertes(2458, "Karaj", ["sörös"], "Hajnal")
huspotlo(2459, "Tofu, seitan, tempeh", "tofu", "egyéb", "Lunter", csom="vákuumcsomagolt")
szosz(2460, "Egyéb hideg szósz, dip", "egyéb", ["joghurt"], ["fokhagymás"], kisz="doboz", konyha="balkáni")
huspotlo(2461, "Tofu, seitan, tempeh", "tofu", "egyéb", "Lunter", csom="vákuumcsomagolt")
huspotlo(2462, "Tofu, seitan, tempeh", "tofu", "egyéb", "Lunter", csom="vákuumcsomagolt")
d(2463, PK, "Tortilla lap", None, márka="Dijo", **{"fajta": ["fehér"], "íz": ["natúr"]})
szosz(2464, "Paradicsomos / főzőszósz (kész)", "Condito", ["paradicsom"], ["paradicsomos"],
      konyha="olasz", gm=True)
d(2465, ED, "Gumicukor, zselé, pillecukor", "Pillecukor, hab", márka="Demi",
  **{"forma": ["pillecukor"], "íz": ["egyéb"]})
huspotlo(2466, "Növényi falat/burger", "szója", "falat", "Vegan Grill")
grillsajt(2467, ["natúr"], "Hajdú", laktozmentes=True)
hotdogbuci(2468, "Nutrifree", "hamburgerzsemle")
huspotlo(2469, "Növényi felvágott/szelet", "borsófehérje", "felvágott", "Vegan Grill")
huspotlo(2470, "Növényi felvágott/szelet", "borsófehérje", "felvágott", "Vegan Grill")
huspotlo(2471, "Növényi virsli/kolbász", "szója", "kolbász", "Vegan Grill")
d(2472, ED, "Snack", "Chips, Nachos, Pufi", gluténmentes=True, alak="szirom", márka="Lorenz",
  **{"egyéb jellemzők": ["egyéb"], "íz": ["BBQ"], "alapanyag": ["burgonya"], "kiszerelés / csomagolás": ["egyéb"]})
d(2473, ED, "Snack", "Chips, Nachos, Pufi", gluténmentes=True, alak="szirom", márka="Lorenz",
  **{"egyéb jellemzők": ["egyéb"], "íz": ["egyéb"], "alapanyag": ["burgonya"], "kiszerelés / csomagolás": ["egyéb"]})
friss_sajt(2474, "Minus L", "feta", laktozmentes=True)

# ---- SHEET 4 (2475-2499) ----
hotdogbuci(2475, "Nutrifree", "hot-dog kifli")
szosz(2476, "Majonéz", "egyéb", ["majonéz"], ["natúr"], light=True, kisz="üveg",
      **{"tojás nélküli": True, "zsírtartalom": ["egyéb"]})
d(2477, PK, "Kenyér", None, márka="Nutrifree", gluténmentes=True, **{"fajta": ["fehér"]})
hotdogbuci(2478, "Balviten", "hamburgerzsemle", fajta="magvas")
huspotlo(2479, "Növényi felvágott/szelet", "egyéb", "felvágott", "Bio ABC", bio=True)
huspotlo(2480, "Növényi felvágott/szelet", "egyéb", "felvágott", "Bio ABC", bio=True)
hotdogbuci(2481, "Nutrifree", "hamburgerzsemle")
huspotlo(2482, "Növényi virsli/kolbász", "szója", "kolbász", "Vegan Grill")
huspotlo(2483, "Tofu, seitan, tempeh", "seitan", "egyéb", "Vegan Grill")
huspotlo(2484, "Növényi virsli/kolbász", "szója", "virsli", "Well Well")
szosz(2485, "Egyéb hideg szósz, dip", "Condito", ["zöldség"], ["hagymás"], gm=True)
huspotlo(2486, "Tofu, seitan, tempeh", "seitan", "egyéb", "Vegan Grill")
szosz(2487, "Mustár", "Condito", ["mustár"], ["mild"], kisz="flakon", gm=True, csipos="enyhe")
szosz(2488, "Majonéz", "Hellmann's", ["majonéz"], ["natúr"], kisz="flakon",
      **{"tojás nélküli": True, "zsírtartalom": ["egyéb"]})
huspotlo(2489, "Tofu, seitan, tempeh", "seitan", "egyéb", "Vegan Grill")
huspotlo(2490, "Tofu, seitan, tempeh", "seitan", "egyéb", "Vegan Grill")
szosz(2491, "Ketchup", "Condito", ["paradicsom"], ["natúr"], kisz="flakon", gm=True)
d(2492, PK, "Egyéb sós pékáru", None, márka="Nutrifree", csomagolt=True,
  fajta="focaccia", **{"íz": ["natúr"]})
huspotlo(2493, "Növényi falat/burger", "szója", "burger", "Vegan Grill")
huspotlo(2494, "Növényi virsli/kolbász", "szója", "kolbász", "Vegan Grill")
huspotlo(2495, "Tofu, seitan, tempeh", "tofu", "egyéb", "Real Nature", csom="vákuumcsomagolt")
huspotlo(2496, "Tofu, seitan, tempeh", "tofu", "egyéb", "Real Nature", csom="vákuumcsomagolt")
huspotlo(2497, "Tofu, seitan, tempeh", "tofu", "egyéb", "Real Nature", csom="vákuumcsomagolt")
huspotlo(2498, "Növényi falat/burger", "tofu", "burger", "Real Nature")
huspotlo(2499, "Növényi virsli/kolbász", "tofu", "virsli", "Real Nature")

# ---- ÉPÍTÉS + VALIDÁCIÓ ----
def build(tree, rows):
    out = []
    for i, fok, al, alt, ov in D:
        sch = schema(tree, fok, al, alt)
        tul = {}
        for key, spec in sch.items():
            if spec == {}:
                v = ov.get(key, False)
                assert isinstance(v, bool), f"{i} {key}: flag nem bool ({v})"
                tul[key] = v
            elif isinstance(spec, dict) and spec.get("type") == "single":
                assert key in ov, f"{i}: hiányzó single '{key}' ({fok}>{al}>{alt})"
                assert ov[key] in spec["values"], f"{i} {key}: '{ov[key]}' nincs {spec['values']}"
                tul[key] = ov[key]
            elif isinstance(spec, list):
                assert key in ov, f"{i}: hiányzó lista '{key}' ({fok}>{al}>{alt})"
                v = ov[key]
                assert isinstance(v, list) and v, f"{i} {key}: nem nemüres lista ({v})"
                for x in v:
                    assert x in spec, f"{i} {key}: '{x}' nincs {spec}"
                tul[key] = v
        for k in ov:
            assert k in sch, f"{i}: ismeretlen override '{k}' ({fok}>{al}>{alt})"
        row = rows[i]
        out.append({
            "termek": dict(row),
            "fokategoria": fok, "alkategoria": al, "altipus": (alt or ""),
            "tulajdonsagok": tul,
            "kategoria_hash": kategoriak_hash(fok, al, (alt or ""), tul),
            "statusz": "kesz",
        })
    return out

def main():
    tree = json.load(open(TREE, encoding="utf-8"))
    extend_tree(tree)
    rows = list(csv.DictReader(open(CSVP, encoding="utf-8")))
    new = build(tree, rows)
    assert len(new) == 100, f"vártam 100 (2400-2499), kaptam {len(new)}"
    def save(path, data):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))
    save(TREE, tree)
    ered = json.load(open(ERED, encoding="utf-8"))
    done_keys = set((rows[i]["store_name"], rows[i]["store_product_id"]) for i, _, _, _, _ in D)
    ered = [r for r in ered if (r.get("termek", {}).get("store_name"),
                                r.get("termek", {}).get("store_product_id")) not in done_keys]
    ered.extend(new)
    save(ERED, ered)
    print(f"OK: {len(new)} új rekord, eredmeny.json össz: {len(ered)}")

if __name__ == "__main__":
    main()
