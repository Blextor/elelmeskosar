# -*- coding: utf-8 -*-
"""Batch 2200-2299 kézi besorolásának kiírása (zömében friss zöldség-gyümölcs +
magvak/aszalt). Döntések kéziek (kép+adat); kód csak szerializál + hiányzó értékek
felvétele + hash. Lásd apply_batch_2100.py."""
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
    # Gyümölcs > Magvak, csonthéjasok: Chia fajta
    add_vals(t["Gyümölcs"]["alkategóriák"]["Magvak, csonthéjasok"]["tulajdonságok"]["egyedi"]["fajta"],
             ["Chia"])
    # Édesség > Rágcsálnivaló magvak > Olajos magvak (snack): pekándió magfajta
    om = (t["Édesség, snack, rágcsálnivaló"]["alkategóriák"]["Rágcsálnivaló magvak (snack)"]
          ["altípusok"]["Olajos magvak (snack)"]["tulajdonságok"]["csoportos"]["magfajta"])
    add_vals(om, ["pekándió"])

# ---- KÉZI DÖNTÉSEK ----
ZO = "Zöldség"
GY = "Gyümölcs"
ED = "Édesség, snack, rágcsálnivaló"
AL = "Alapanyag, sütés-főzés"

D = []
def d(i, fok, al, alt, **ov): D.append((i, fok, al, alt, ov))

def veg(i, alk, kisz, feld="egész", meret="normál", hazai=True, bio=False, **ap):
    base = dict(bio=bio, hazai=hazai, kiszerelés=kisz)
    base["feldolgozottság"] = [feld]; base["méret"] = [meret]
    base.update(ap)
    d(i, ZO, alk, None, **base)

def fruit(i, alk, kisz, er="érett", feld="egész", meret="normál", hazai=False, bio=False, **ap):
    base = dict(bio=bio, hazai=hazai, kiszerelés=kisz)
    base["érettség"] = [er]; base["méret"] = [meret]; base["feldolgozottság"] = [feld]
    base.update(ap)
    d(i, GY, alk, None, **base)

def dried(i, gyum, tart, kisz="tasak", feld="egész"):
    fruit(i, "Aszalt, szárított, chips", kisz, er="egyéb", meret="egyéb", feld=feld,
          hazai=False, **{"gyümölcs": gyum, "tartósítás": tart})

def magvak_snack(i, magfajta, marka, izesites="natúr", sozott=False, porkolt=False,
                 hej_nelkul=False, sotlan=False):
    d(i, ED, "Rágcsálnivaló magvak (snack)", "Olajos magvak (snack)",
      márka=marka, vegán=True, sózott=sozott, pörkölt=porkolt,
      **{"héj nélküli": hej_nelkul}, sótlan=sotlan,
      **{"magfajta": [magfajta], "ízesítés": [izesites]})

# SHEET 1 (2200-2224)
veg(2200, "Burgonya", "lédig", fajta="Étkezési", **{"színe": "Sárga"})
veg(2201, "Hagymafélék", "csomagolt", fajta="Fokhagyma")
dried(2202, "Szilva", "Aszalt", feld="magozott")
magvak_snack(2203, "napraforgómag", "Snack Fun", izesites="sós", sozott=True, porkolt=True, hej_nelkul=True)
veg(2204, "Burgonya", "2 kg", fajta="Étkezési", **{"színe": "egyéb"})
veg(2205, "Csomagolt saláta, salátatál", "csomagolt", feld="mix", mosott=True, konyhakész=True,
    **{"saláta alap": ["salátakeverék"]})
veg(2206, "Csomagolt saláta, salátatál", "csomagolt", feld="mix", mosott=True, konyhakész=True,
    **{"saláta alap": ["salátakeverék"]})
d(2207, AL, "Olajos magvak, aszalt gyümölcs (natúr, sütéshez-főzéshez)", "Reszelt kókusz, mák",
  kiszerelés="tasak", **{"sótlan": True}, márka="Back Family", **{"fajta": ["mák"], "forma": ["darált"]})
veg(2208, "Burgonya", "2 kg", fajta="Étkezési", **{"színe": "Sárga"})
dried(2209, "Szilva", "Aszalt", feld="magozott")
fruit(2210, "Magvak, csonthéjasok", "tasak", er="egyéb", meret="egyéb", fajta="Chia")
dried(2211, "Vörösáfonya", "Aszalt")
dried(2212, "Mangó", "Aszalt", feld="szeletelt")
dried(2213, "Szőlő / Mazsola", "Aszalt")
magvak_snack(2214, "dió", "Happy Harvest", sotlan=True)
magvak_snack(2215, "pekándió", "Happy Harvest", sotlan=True)
magvak_snack(2216, "kesudió", "Happy Harvest", porkolt=True, sotlan=True)
dried(2217, "Alma", "Chips", feld="szeletelt")
veg(2218, "Paprika", "darabra", **{"erős, csípős": True}, fajta="egyéb", **{"színe": "Zöld"})
veg(2219, "Hagymafélék", "darabra", fajta="Fokhagyma")
veg(2220, "Káposzta", "lédig", fajta="Fejeskáposzta")
veg(2221, "Hagymafélék", "lédig", fajta="Vöröshagyma")
veg(2222, "Hagymafélék", "1 kg", fajta="Vöröshagyma")
fruit(2223, "Kiwi", "darabra", **{"fajta / jelleg": ["zöld"]})
veg(2224, "Káposzta", "lédig", fajta="Fejeskáposzta")

# SHEET 2 (2225-2249)
fruit(2225, "Alma", "lédig", hazai=True, típus="egyéb", **{"színe": ["piros"]})
veg(2226, "Uborka", "darabra", fajta="Kígyúuborka")
veg(2227, "Hagymafélék", "csomagolt", fajta="Lilahagyma")
veg(2228, "Hagymafélék", "csomós", fajta="Újhagyma")
veg(2229, "Karalábé", "darabra")
veg(2230, "Retekfélék", "csomós")
fruit(2231, "Alma", "lédig", hazai=True, típus="Golden", **{"színe": ["sárga"]})
veg(2232, "Friss fűszernövény", "csomagolt")
veg(2233, "Paradicsom", "csomagolt", fajta="Sima", fürtös=True, **{"színe": "Piros"})
fruit(2234, "Alma", "lédig", hazai=True, típus="Jonagold", **{"színe": ["piros"]})
fruit(2235, "Alma", "lédig", hazai=True, típus="Idared", **{"színe": ["piros"]})
fruit(2236, "Alma", "lédig", hazai=True, típus="Gála", **{"színe": ["piros"]})
veg(2237, "Retekfélék", "csomagolt")
veg(2238, "Salátafélék", "darabra", fajta="Fejes")
veg(2239, "Paradicsom", "lédig", fajta="Sima", fürtös=True, **{"színe": "Piros"})
veg(2240, "Hagymafélék", "lédig", fajta="Lilahagyma")
veg(2241, "Uborka", "darabra", bio=True, fajta="Kígyúuborka")
fruit(2242, "Alma", "csomagolt", hazai=True, típus="egyéb", **{"színe": ["piros", "zöld"]})
fruit(2243, "Körte", "csomagolt", hazai=True, típus="egyéb")
veg(2244, "Paradicsom", "csomagolt", fajta="Koktél", fürtös=False, **{"színe": "Piros"})
fruit(2245, "Körte", "lédig", hazai=True, típus="Conference")
veg(2246, "Paradicsom", "csomagolt", fajta="Cherry", fürtös=True, **{"színe": "Piros"})
veg(2247, "Sárgarépa", "1 kg")
veg(2248, "Salátafélék", "darabra", fajta="Római")
fruit(2249, "Avokádó", "darabra", **{"fajta / jelleg": ["hass"]})

# SHEET 3 (2250-2274)
veg(2250, "Zeller", "lédig")
veg(2251, "Sárgarépa", "lédig")
veg(2252, "Brokkoli", "csomagolt")
veg(2253, "Retekfélék", "darabra")
veg(2254, "Sárgarépa", "csomós")
veg(2255, "Zeller", "darabra")
veg(2256, "Csomagolt saláta, salátatál", "csomagolt", feld="mosott", mosott=True, konyhakész=True,
    **{"saláta alap": ["rucola"]})
veg(2257, "Paradicsom", "csomagolt", fajta="Koktél", fürtös=True, **{"színe": "Piros"})
fruit(2258, "Szőlő", "csomagolt", hazai=True, **{"magnélküli": True, "színe": "fehér"})
veg(2259, "Friss fűszernövény", "darabra")
fruit(2260, "Alma", "lédig", hazai=True, típus="Crimson Snow", **{"színe": ["piros"]})
veg(2261, "Friss fűszernövény", "csomagolt")
fruit(2262, "Szőlő", "csomagolt", hazai=True, **{"magnélküli": True, "színe": "piros"})
veg(2263, "Paradicsom", "lédig", fajta="Sima", fürtös=False, **{"színe": "Piros"})
veg(2264, "Egyéb zöldség", "csomós")
fruit(2265, "Narancs", "lédig", fajta="egyéb")
veg(2266, "Káposzta", "lédig", fajta="Kelkáposzta")
veg(2267, "Gomba", "csomagolt", bio=True, fajta="Csiperke")
veg(2268, "Hagymafélék", "csomós", fajta="Fehérhagyma")
fruit(2269, "Banán", "lédig", **{"fajta / jelleg": ["sima"]})
veg(2270, "Salátafélék", "darabra", fajta="Jég")
veg(2271, "Paradicsom", "csomagolt", fajta="Koktél", fürtös=False, **{"színe": "Piros"})
veg(2272, "Gomba", "csomagolt", fajta="Laska")
veg(2273, "Paprika", "csomagolt", **{"erős, csípős": False}, fajta="Lecsó", **{"színe": "Fehér"})
fruit(2274, "Alma", "lédig", hazai=True, típus="Pink Lady", **{"színe": ["piros"]})

# SHEET 4 (2275-2299)
veg(2275, "Paradicsom", "csomagolt", fajta="Cherry", fürtös=True, **{"színe": "Piros"})
fruit(2276, "Citrom", "csomagolt", bio=True, **{"kezeletlen héjú": True})
veg(2277, "Burgonya", "lédig", fajta="Újburgonya", **{"színe": "egyéb"})
fruit(2278, "Sárgadinnye", "darabra", típus="Cantaloupe")
fruit(2279, "Mangó", "darabra")
veg(2280, "Burgonya", "1 kg", fajta="Étkezési", **{"színe": "Piros"})
veg(2281, "Paradicsom", "csomagolt", fajta="egyéb", fürtös=False, **{"színe": "Piros"})
veg(2282, "Paprika", "csomagolt", **{"erős, csípős": False}, fajta="Kápia", **{"színe": "Piros"})
fruit(2283, "Passiógyümölcs", "csomagolt")
veg(2284, "Uborka", "lédig", fajta="Fürtös")
fruit(2285, "Málna", "csomagolt", er="fogyasztásra kész", hazai=True)
fruit(2286, "Őszibarack, nektarin", "csomagolt", hazai=True)
fruit(2287, "Sárgabarack", "csomagolt", hazai=True)
fruit(2288, "Eper", "csomagolt", er="fogyasztásra kész", hazai=True)
veg(2289, "Burgonya", "lédig", fajta="Édesburgonya", hazai=False, **{"színe": "egyéb"})
fruit(2290, "Áfonya", "csomagolt", er="fogyasztásra kész")
veg(2291, "Tökféle, cukkini, padlizsán", "lédig")
fruit(2292, "Banán", "lédig", bio=True, **{"fajta / jelleg": ["sima"]})
fruit(2293, "Ananász", "lédig", **{"fajta / jelleg": ["egész"]})
veg(2294, "Paprika", "csomagolt", **{"erős, csípős": False}, fajta="Kaliforniai", **{"színe": "Mix"})
veg(2295, "Mix, vegyes", "1 kg")
veg(2296, "Tökféle, cukkini, padlizsán", "lédig")
veg(2297, "Hagymafélék", "1 kg", bio=True, fajta="Vöröshagyma")
fruit(2298, "Narancs", "hálós", fajta="egyéb")
fruit(2299, "Lime", "csomagolt")

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
                v = ov[key]
                assert v in spec["values"], f"{i} {key}: '{v}' nincs {spec['values']}"
                tul[key] = v
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
    assert len(new) == 100, f"vártam 100 (2200-2299), kaptam {len(new)}"
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
