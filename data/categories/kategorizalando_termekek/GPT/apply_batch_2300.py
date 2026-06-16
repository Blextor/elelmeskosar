# -*- coding: utf-8 -*-
"""Batch 2300-2399: maradék Aldi zöldség-gyümölcs + Auchan grillsajtok/különleges
sajtok + sok grillkolbász/debreceni/leberkäse. Döntések kéziek (kép+adat)."""
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
    tt = t["Tejtermékek és tojás"]["alkategóriák"]
    add_vals(tt["Sajt"]["tulajdonságok"]["egyedi"]["márka"],
             ["Auchan Kedvenc", "Hochland", "Ízes Erdély"])
    fv = (t["Hús, hal, felvágott"]["alkategóriák"]["Felvágottak, húskészítmény"]
          ["tulajdonságok"]["csoportos"]["ízesítés"])
    add_vals(fv, ["hagymás", "bajor", "sonkás", "káposztás"])
    add_vals(t["Hús, hal, felvágott"]["tulajdonságok"]["egyedi"]["márka"], ["Hízóföld"])

ZO = "Zöldség"; GY = "Gyümölcs"; TM = "Tejtermékek és tojás"; HH = "Hús, hal, felvágott"

D = []
def d(i, fok, al, alt, **ov): D.append((i, fok, al, alt, ov))

def veg(i, alk, kisz, feld="egész", meret="normál", hazai=True, bio=False, **ap):
    base = dict(bio=bio, hazai=hazai, kiszerelés=kisz)
    base["feldolgozottság"] = [feld]; base["méret"] = [meret]; base.update(ap)
    d(i, ZO, alk, None, **base)

def fruit(i, alk, kisz, er="érett", feld="egész", meret="normál", hazai=False, bio=False, **ap):
    base = dict(bio=bio, hazai=hazai, kiszerelés=kisz)
    base["érettség"] = [er]; base["méret"] = [meret]; base["feldolgozottság"] = [feld]; base.update(ap)
    d(i, GY, alk, None, **base)

def grillsajt(i, izes, marka, fajta="egyéb", keszitmeny=False, forma="tömb"):
    d(i, TM, "Sajt", "Grillsajt / halloumi / sütnivaló", forma=forma, érlelt=True,
      **{"készítmény (növényi zsiradékkal)": keszitmeny}, kiszerelés="vákuumcsomagolt",
      márka=marka, **{"ízesítés": izes, "fajta": [fajta]})

def friss_sajt(i, marka, fajta, forma="tömb", light=False, izes="natúr"):
    d(i, TM, "Sajt", "Friss / lágy sajt", forma=forma, érlelt=False,
      **{"light / csökkentett zsír": light}, kiszerelés="vákuumcsomagolt", márka=marka,
      **{"ízesítés": [izes], "fajta": [fajta]})

def kolb(i, izes, marka, hus="sertés", forma="pár", alt="Főző-, grillkolbász", hazai=True):
    d(i, HH, "Felvágottak, húskészítmény", alt, **{"hazai/magyar": hazai}, márka=marka,
      **{"húsfajta": [hus], "forma": [forma], "ízesítés": izes,
         "hústartalom": ["egyéb"], "csomagolás": ["védőgázas"]})

def leberkase(i, izes, marka="Hízóföld"):
    kolb(i, [izes], marka, hus="sertés", forma="tömb", alt="Párizsi, felvágott")

def debreceni(i, izes, marka, hazai=True):
    kolb(i, izes, marka, hus="sertés", forma="pár", alt="Virsli, debreceni", hazai=hazai)

# SHEET 1 (2300-2324): produce 2300-2320 + grill cheese 2321-2324
fruit(2300, "Citrom", "lédig")
veg(2301, "Paprika", "csomagolt", **{"erős, csípős": False}, fajta="egyéb", **{"színe": "Piros"})
veg(2302, "Karfiol", "darabra", fajta="Sima")
fruit(2303, "Szeder", "csomagolt", er="fogyasztásra kész", hazai=True)
fruit(2304, "Áfonya", "csomagolt", er="fogyasztásra kész", bio=True)
fruit(2305, "Avokádó", "csomagolt", **{"fajta / jelleg": ["hass"]})
veg(2306, "Egyéb zöldség", "lédig")
veg(2307, "Uborka", "lédig", fajta="Kovászolni való")
veg(2308, "Sárgarépa", "1 kg", bio=True)
veg(2309, "Hagymafélék", "lédig", fajta="Fokhagyma")
veg(2310, "Paprika", "lédig", **{"erős, csípős": False}, fajta="Kaliforniai", **{"színe": "Mix"})
fruit(2311, "Cseresznye", "csomagolt", hazai=True)
fruit(2312, "Őszibarack, nektarin", "lédig", hazai=True)
fruit(2313, "Őszibarack, nektarin", "lédig", hazai=True)
fruit(2314, "Őszibarack, nektarin", "csomagolt", hazai=True)
veg(2315, "Paradicsom", "lédig", fajta="Cherry", fürtös=True, **{"színe": "Piros"})
fruit(2316, "Eper", "csomagolt", er="fogyasztásra kész", hazai=True)
veg(2317, "Gomba", "lédig", fajta="Csiperke")
veg(2318, "Paradicsom", "lédig", fajta="Koktél", fürtös=True, **{"színe": "Piros"})
veg(2319, "Spárga", "csomagolt")
veg(2320, "Gyömbér", "lédig", hazai=False)
grillsajt(2321, ["chili-lime"], "Hajdú")
grillsajt(2322, ["füstölt"], "Hajdú", fajta="parenyica")
grillsajt(2323, ["natúr"], "Hajdú")
grillsajt(2324, ["füstölt"], "Auchan Kedvenc")

# SHEET 2 (2325-2349)
grillsajt(2325, ["natúr"], "Auchan Kedvenc")
grillsajt(2326, ["zöldfűszeres"], "Auchan Kedvenc")
grillsajt(2327, ["gyros"], "Hajdú")
grillsajt(2328, ["natúr"], "Karaván", keszitmeny=True, forma="korong")
grillsajt(2329, ["zöldfűszeres"], "Karaván", keszitmeny=True, forma="korong")
grillsajt(2330, ["natúr"], "Auchan Kedvenc")
grillsajt(2331, ["natúr"], "Président", fajta="camembert")
friss_sajt(2332, "Président", "feta")
friss_sajt(2333, "Président", "feta")
friss_sajt(2334, "egyéb", "egyéb")
friss_sajt(2335, "Hochland", "feta", forma="kocka", izes="fűszeres")
friss_sajt(2336, "Hochland", "feta", light=True)
friss_sajt(2337, "Ízes Erdély", "feta")
grillsajt(2338, ["füstölt"], "Karaván", forma="rudacska")
kolb(2339, ["füstölt"], "Gierlinger", hus="sertés", forma="szeletelt", alt="Bacon", hazai=False)
kolb(2340, ["bajor"], "Privát Hús")
kolb(2341, ["borsos-fokhagymás"], "Privát Hús")
kolb(2342, ["sajtos"], "Kaiser", hazai=False)
kolb(2343, ["fokhagymás"], "Kaiser", hazai=False)
kolb(2344, ["egyéb"], "Kaiser", hus="vegyes", hazai=False)
kolb(2345, ["hagymás"], "Kaiser", hazai=False)
kolb(2346, ["magyaros", "csípős"], "Privát Hús")
kolb(2347, ["sajtos"], "Privát Hús")
kolb(2348, ["egyéb"], "Régimódi")
kolb(2349, ["sajtos"], "Régimódi")

# SHEET 3 (2350-2374)
kolb(2350, ["pritaminpaprikás"], "Régimódi")
kolb(2351, ["chilis"], "Régimódi")
kolb(2352, ["káposztás"], "Régimódi")
kolb(2353, ["sajtos"], "Régimódi")
kolb(2354, ["egyéb"], "Pápai Hús")
kolb(2355, ["barbecue"], "Wiesbauer", hazai=False)
kolb(2356, ["borsos"], "Wiesbauer", hazai=False)
kolb(2357, ["mézes", "fokhagymás"], "Wiesbauer", hazai=False)
kolb(2358, ["paprikás"], "Wiesbauer", hazai=False)
kolb(2359, ["sajtos"], "Wiesbauer", hazai=False)
kolb(2360, ["magyaros"], "Auchan Collection")
kolb(2361, ["mézes", "mustáros"], "Auchan Collection")
kolb(2362, ["barbecue"], "Auchan Prémium")
kolb(2363, ["chilis"], "Auchan Prémium")
kolb(2364, ["jalapeno"], "Auchan Prémium")
kolb(2365, ["hagymás"], "Auchan Prémium")
kolb(2366, ["szárított paradicsom"], "Auchan Prémium")
kolb(2367, ["borsos-fokhagymás"], "Kometa")
kolb(2368, ["egyéb"], "Wiesbauer", hazai=False)
leberkase(2369, "chilis")
leberkase(2370, "natúr")
leberkase(2371, "natúr")
kolb(2372, ["chilis"], "Nádudvari")
kolb(2373, ["sajtos"], "Nádudvari")
debreceni(2374, ["csemege"], "Nádudvari")

# SHEET 4 (2375-2399)
debreceni(2375, ["sajtos", "csemege"], "Nádudvari")
debreceni(2376, ["csípős"], "Nádudvari")
kolb(2377, ["fokhagymás"], "Nádudvari")
kolb(2378, ["egyéb"], "Nádudvari", hus="vegyes")
kolb(2379, ["klasszikus"], "Nádudvari")
kolb(2380, ["pikáns"], "Régimódi")
debreceni(2381, ["csemege"], "Auchan Kedvenc")
debreceni(2382, ["csípős"], "Auchan Kedvenc")
kolb(2383, ["sajtos", "chilis", "füstölt"], "Wiesbauer", hazai=False)
kolb(2384, ["egyéb"], "Bogádi", hus="vegyes")
kolb(2385, ["bajor"], "Bogádi")
kolb(2386, ["csípős", "paprikás"], "Bogádi")
kolb(2387, ["paprikás"], "Bogádi")
kolb(2388, ["bajor"], "Bogádi")
kolb(2389, ["csípős"], "Bogádi")
kolb(2390, ["paprikás"], "Bogádi")
kolb(2391, ["sonkás"], "Bogádi")
kolb(2392, ["barbecue"], "Wiesbauer", hazai=False)
kolb(2393, ["csípős"], "Wiesbauer", hazai=False)
kolb(2394, ["mustáros"], "Wiesbauer", hazai=False)
kolb(2395, ["egyéb"], "Wiesbauer", hazai=False)
kolb(2396, ["sajtos"], "Wiesbauer", hazai=False)
kolb(2397, ["csípős"], "Auchan Collection", hus="marha")
kolb(2398, ["sajtos"], "Auchan Collection", hus="marha")
kolb(2399, ["magyaros"], "Master Good", hus="csirke")

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
    assert len(new) == 100, f"vártam 100 (2300-2399), kaptam {len(new)}"
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
