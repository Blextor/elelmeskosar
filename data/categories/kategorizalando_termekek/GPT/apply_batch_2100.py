# -*- coding: utf-8 -*-
"""Batch 2100-2199 kézi besorolásának kiírása.
A kategória-DÖNTÉSEK kézi (kép+adat alapján), itt csak szerializálás + a fa
hiányzó ÉRTÉKEINEK felvétele (rules.txt 9-19) + hash-számítás. Nincs auto-besorolás."""
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

# ---- 1) FA-BŐVÍTÉSEK (hiányzó értékek/márkák) ----
def add_vals(lst, vals):
    for v in vals:
        if v not in lst: lst.append(v)

def extend_tree(t):
    tt = t["Tejtermékek és tojás"]["alkategóriák"]
    # Tejdesszert: vödör kiszerelés + íz-értékek
    td = tt["Tejdesszert, puding"]["tulajdonságok"]
    add_vals(td["egyedi"]["kiszerelés"], ["vödör"])
    add_vals(td["egyedi"]["márka"], ["Milfina"])
    add_vals(td["csoportos"]["íz"], ["áfonyás", "őszibarackos", "cseresznyés", "maracuja"])
    # Krémtúró: stracciatella íz
    add_vals(tt["Krémtúró, túródesszert"]["tulajdonságok"]["csoportos"]["íz"], ["stracciatella"])
    # Gyümölcsös/ízesített joghurt: kekszes íz
    jog = tt["Joghurt"]["altípusok"]["Gyümölcsös/ízesített joghurt"]["tulajdonságok"]["csoportos"]["íz"]
    add_vals(jog, ["kekszes"])
    # Sajt: Leerdammer márka + medvehagymás ízesítés
    sajt = tt["Sajt"]["tulajdonságok"]["egyedi"]
    add_vals(sajt["márka"], ["Leerdammer"])
    add_vals(tt["Sajt"]["tulajdonságok"]["csoportos"]["ízesítés"], ["medvehagymás"])
    # Növényi alternatíva: márkák
    add_vals(tt["Növényi alternatíva"]["tulajdonságok"]["egyedi"]["márka"],
             ["Dr. Oetker", "Violife", "Hulala"])
    # Hús-hal főkat márka: MyVay
    add_vals(t["Hús, hal, felvágott"]["tulajdonságok"]["egyedi"]["márka"], ["MyVay"])
    # Alapanyag > Szószok > Szendvicskrém: márkák
    sk = (t["Alapanyag, sütés-főzés"]["alkategóriák"]["Szószok, öntetek, dresszingek"]
          ["altípusok"]["Szendvicskrém, hummusz, kenőkrém"]["tulajdonságok"]["egyedi"]["márka"])
    add_vals(sk, ["MyVay", "Yummy Dip"])
    # Édesség > Rágcsálnivaló magvak > Olajos magvak (snack): Bella márka
    om = (t["Édesség, snack, rágcsálnivaló"]["alkategóriák"]["Rágcsálnivaló magvak (snack)"]
          ["altípusok"]["Olajos magvak (snack)"]["tulajdonságok"]["egyedi"]["márka"])
    add_vals(om, ["Bella"])

# ---- 2) KÉZI DÖNTÉSEK: (csv_index, fok, al, alt, overrides) ----
TM = "Tejtermékek és tojás"
AL = "Alapanyag, sütés-főzés"
HH = "Hús, hal, felvágott"
ED = "Édesség, snack, rágcsálnivaló"
ZO = "Zöldség"
GY = "Gyümölcs"

D = []
def d(i, fok, al, alt, **ov): D.append((i, fok, al, alt, ov))

# --- SHEET 1 (2100-2124) ---
d(2100, TM, "Sajt", "Penészes sajt", forma="korong", érlelt=True, kiszerelés="doboz",
  márka="Roi de Trefle", **{"ízesítés":["fűszeres"], "fajta":["brie"]})
for i, izf, fajta in [(2101,["paradicsomos-bazsalikomos"],["egyéb"]),
                      (2102,["natúr"],["gouda"]),
                      (2103,["csípős paprikás"],["egyéb"])]:
    d(i, TM, "Sajt", "Grillsajt / halloumi / sütnivaló", forma="tömb",
      **{"készítmény (növényi zsiradékkal)":True}, kiszerelés="vákuumcsomagolt",
      márka="BBQ", **{"ízesítés":izf, "fajta":fajta})
d(2104, TM, "Sajt", "Félkemény sajt", forma="tömb", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Ammerländer", **{"ízesítés":["natúr"], "fajta":["egyéb"]})
d(2105, TM, "Joghurt", "Skyr / proteinjoghurt", **{"protein / magas fehérje":True},
  **{"ízesített":True}, zsírtartalom="sovány", kiszerelés="pohár", márka="Milsani", **{"íz":["vaníliás"]})
d(2106, TM, "Joghurt", "Skyr / proteinjoghurt", **{"protein / magas fehérje":True},
  **{"ízesített":True}, zsírtartalom="sovány", kiszerelés="pohár", márka="Milsani", **{"íz":["epres"]})
d(2107, TM, "Sajt", "Félkemény sajt", forma="tömb", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Milsani", **{"ízesítés":["natúr"], "fajta":["maasdam"]})
d(2108, TM, "Tejdesszert, puding", "Egyéb tejdesszert", **{"ízesített":True},
  kiszerelés="vödör", márka="Milsani", **{"íz":["csokoládés","mogyorós"]})
d(2109, TM, "Tejdesszert, puding", "Tejberizs", kiszerelés="vödör", márka="Milsani", **{"íz":["natúr"]})
d(2110, TM, "Tejdesszert, puding", "Puding", kiszerelés="vödör", márka="Milsani", **{"íz":["natúr"]})
d(2111, TM, "Sajt", "Félkemény sajt", forma="szeletelt", érlelt=True, laktózmentes=True,
  kiszerelés="vákuumcsomagolt", márka="Milsani", **{"ízesítés":["natúr"], "fajta":["maasdam","gouda"]})
d(2112, TM, "Sajt", "Félkemény sajt", forma="szeletelt", érlelt=True, laktózmentes=True,
  kiszerelés="vákuumcsomagolt", márka="Milsani", **{"ízesítés":["natúr"], "fajta":["edami","butterkäse"]})
d(2113, TM, "Tojás", "Tyúktojás", méret="S", tartás="egyéb", hazai=True, kiszerelés="tálca",
  márka="Kokárdás", **{"fajta":["tyúktojás"]})
d(2114, TM, "Tojás", "Tyúktojás", méret="S", tartás="egyéb", hazai=True, kiszerelés="tálca",
  márka="FARM", **{"fajta":["tyúktojás"]})
for i in (2115, 2116):
    d(i, TM, "Sajt", "Penészes sajt", forma="gerezd", érlelt=True, kiszerelés="vákuumcsomagolt",
      márka="Cucina Nobile", **{"ízesítés":["natúr"], "fajta":["kékpenészes"]})
d(2117, TM, "Sajt", "Grillsajt / halloumi / sütnivaló", forma="tömb",
  **{"készítmény (növényi zsiradékkal)":True}, kiszerelés="vákuumcsomagolt", márka="Lyttos",
  **{"ízesítés":["chilis"], "fajta":["egyéb"]})
d(2118, TM, "Sajt", "Grillsajt / halloumi / sütnivaló", forma="tömb",
  kiszerelés="vákuumcsomagolt", márka="Lyttos", **{"ízesítés":["natúr"], "fajta":["egyéb"]})
d(2119, TM, "Sajt", "Grillsajt / halloumi / sütnivaló", forma="tömb",
  **{"készítmény (növényi zsiradékkal)":True}, kiszerelés="vákuumcsomagolt", márka="Lyttos",
  **{"ízesítés":["bazsalikomos"], "fajta":["egyéb"]})
def turorudi(i, iz, **extra):
    ov = dict(bevonatos=True, **{"ízesített":True}, kiszerelés="multipack", márka="Pöttyös",
              **{"íz":iz, "bevonat típusa":["tejbevonó"]})
    ov.update(extra)
    d(i, TM, "Krémtúró, túródesszert", "Túró Rudi jellegű túródesszert", **ov)
turorudi(2120, ["csokoládés"], **{"cukormentes / hozzáadott cukor nélkül":True})
turorudi(2121, ["natúr"], **{"cukormentes / hozzáadott cukor nélkül":True})
turorudi(2122, ["natúr"])
turorudi(2123, ["pisztáciás"])
turorudi(2124, ["natúr"], laktózmentes=True)

# --- SHEET 2 (2125-2149) ---
d(2125, TM, "Sajt", "Kemény sajt", forma="gerezd", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Cucina", **{"ízesítés":["natúr"], "fajta":["grana padano"]})
d(2126, TM, "Sajt", "Félkemény sajt", forma="tömb", érlelt=True, kiszerelés="egyéb",
  márka="Kokárdás", **{"ízesítés":["natúr"], "fajta":["trappista"]})
d(2127, TM, "Sajt", "Félkemény sajt", forma="tömb", érlelt=True, laktózmentes=True,
  kiszerelés="vákuumcsomagolt", márka="Milsani", **{"ízesítés":["natúr"], "fajta":["gouda"]})
d(2128, TM, "Sajt", "Félkemény sajt", forma="tömb", érlelt=True, laktózmentes=True,
  kiszerelés="vákuumcsomagolt", márka="Milsani", **{"ízesítés":["natúr"], "fajta":["gouda"]})
d(2129, TM, "Sajt", "Kemény sajt", forma="gerezd", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Meine Käsetheke", **{"ízesítés":["natúr"], "fajta":["egyéb"]})
d(2130, TM, "Sajt", "Kemény sajt", forma="gerezd", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Meine Käsetheke", **{"ízesítés":["natúr"], "fajta":["egyéb"]})
d(2131, TM, "Sajt", "Kemény sajt", forma="gerezd", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Meine Käsetheke", **{"ízesítés":["natúr"], "fajta":["gruyère"]})
d(2132, TM, "Sajt", "Félkemény sajt", forma="tömb", érlelt=True, kiszerelés="egyéb",
  márka="Tolle", **{"ízesítés":["natúr"], "fajta":["trappista"]})
d(2133, TM, "Sajt", "Félkemény sajt", forma="tömb", érlelt=True, laktózmentes=True,
  kiszerelés="vákuumcsomagolt", márka="Milsani", **{"ízesítés":["natúr"], "fajta":["kecskesajt"]})
d(2134, TM, "Sajt", "Kemény sajt", forma="tömb", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Bonlà", **{"ízesítés":["natúr"], "fajta":["grana padano"]})
d(2135, TM, "Joghurt", "Gyümölcsös/ízesített joghurt", zsírtartalom="sovány",
  **{"ízesített":True, "light / csökkentett zsír":True, "cukormentes / hozzáadott cukor nélkül":True},
  kiszerelés="pohár", márka="Zott", **{"íz":["meggyes"]})
d(2136, TM, "Joghurt", "Gyümölcsös/ízesített joghurt", zsírtartalom="sovány",
  **{"ízesített":True, "light / csökkentett zsír":True, "cukormentes / hozzáadott cukor nélkül":True},
  kiszerelés="pohár", márka="Zott", **{"íz":["epres"]})
def milsjog(i, iz):
    d(i, TM, "Joghurt", "Gyümölcsös/ízesített joghurt", zsírtartalom="egyéb",
      **{"ízesített":True}, kiszerelés="pohár", márka="Milsani", **{"íz":iz})
milsjog(2137, ["őszibarackos","maracuja"])
milsjog(2138, ["meggyes"])
milsjog(2139, ["kiwis"])
milsjog(2140, ["epres"])
milsjog(2141, ["málnás"])
milsjog(2142, ["vaníliás"])
milsjog(2143, ["kekszes"])
milsjog(2144, ["málnás"])
milsjog(2145, ["epres"])
d(2146, TM, "Tejdesszert, puding", "Puding", **{"ízesített":True}, kiszerelés="pohár",
  márka="Milfina", **{"íz":["fahéjas"]})
d(2147, TM, "Tejdesszert, puding", "Puding", kiszerelés="pohár", márka="Milfina", **{"íz":["natúr"]})
d(2148, TM, "Krémtúró, túródesszert", "Natúr krémtúró", **{"ízesített":True}, kiszerelés="pohár",
  márka="Milsani", **{"íz":["vaníliás"]})
d(2149, TM, "Krémtúró, túródesszert", "Natúr krémtúró", **{"ízesített":True}, kiszerelés="pohár",
  márka="Milsani", **{"íz":["stracciatella"]})

# --- SHEET 3 (2150-2174) ---
d(2150, TM, "Krémtúró, túródesszert", "Gyümölcsös krémtúró", **{"ízesített":True}, kiszerelés="pohár",
  márka="Milsani", **{"íz":["epres"]})
d(2151, TM, "Tej", "UHT tartós tej", zsírtartalom="félzsíros 2,8%", laktózmentes=True,
  kiszerelés="doboz", márka="Milsani")
def milfdessz(i, iz):
    d(i, TM, "Tejdesszert, puding", "Egyéb tejdesszert", **{"ízesített":True}, kiszerelés="pohár",
      márka="Milfina", **{"íz":iz})
milfdessz(2152, ["epres"])
milfdessz(2153, ["őszibarackos","maracuja"])
milfdessz(2154, ["áfonyás"])
milfdessz(2155, ["cseresznyés"])
d(2156, TM, "Sajt", "Félkemény sajt", forma="szeletelt", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Leerdammer", **{"ízesítés":["natúr"], "fajta":["maasdam"]})
d(2157, TM, "Sajt", "Félkemény sajt", forma="szeletelt", érlelt=True,
  **{"light / csökkentett zsír":True}, kiszerelés="vákuumcsomagolt",
  márka="Leerdammer", **{"ízesítés":["natúr"], "fajta":["maasdam"]})
d(2158, TM, "Sajt", "Félkemény sajt", forma="szeletelt", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Milfina", **{"ízesítés":["medvehagymás"], "fajta":["egyéb"]})
d(2159, TM, "Sajt", "Félkemény sajt", forma="szeletelt", érlelt=True, kiszerelés="vákuumcsomagolt",
  márka="Milfina", **{"ízesítés":["csípős paprikás"], "fajta":["egyéb"]})
d(2160, TM, "Vaj", "Teavaj, márkázott vaj", bio=True, kiszerelés="papír", márka="egyéb",
  zsírtartalom="82%")
def alpro_ital(i, alap, cukm=False, gm=True, iz=None):
    zj = ["cukormentes"] if cukm else ["egyéb"]
    d(i, TM, "Növényi alternatíva", "Növényi ital", vegán=True, laktózmentes=True, gluténmentes=gm,
      **{"cukormentes / hozzáadott cukor nélkül":cukm}, kiszerelés="doboz", márka="Alpro",
      **{"terméktípus":["növényi ital"], "alap":alap, "zsírtartalom / jelleg":zj,
         "dúsítás":["kalcium"], "íz":(iz or ["natúr"])})
alpro_ital(2161, ["rizs"])
alpro_ital(2162, ["kókusz"])
alpro_ital(2163, ["mandula"])
alpro_ital(2164, ["kókusz"], cukm=True)
alpro_ital(2165, ["mandula"], cukm=True)
alpro_ital(2166, ["egyéb"], cukm=True)
def tofu(i):
    d(i, HH, "Növényi húspótló", "Tofu, seitan, tempeh", vegán=True,
      **{"készítmény (növényi/kevert)":True}, márka="MyVay",
      **{"alap":["tofu"], "forma":["egyéb"], "csomagolás":["vákuumcsomagolt"]})
tofu(2167); tofu(2168); tofu(2169)
d(2170, TM, "Növényi alternatíva", "Növényi főzőkrém / tejszín", vegán=True, laktózmentes=True,
  kiszerelés="tégely", márka="Dr. Oetker",
  **{"terméktípus":["főzőkrém"], "alap":["növényi olaj"], "zsírtartalom / jelleg":["egyéb"],
     "dúsítás":["egyéb"], "íz":["natúr"]})
d(2171, TM, "Növényi alternatíva", "Növényi sajt", vegán=True, laktózmentes=True, gluténmentes=True,
  kiszerelés="tálca", márka="Violife",
  **{"terméktípus":["sajt alternatíva"], "alap":["kókusz"], "zsírtartalom / jelleg":["egyéb"],
     "dúsítás":["egyéb"], "íz":["natúr"]})
def myvay_ital(i, alap, bio=False, cukm=False, gm=False, iz=None):
    zj = ["cukormentes"] if cukm else ["egyéb"]
    d(i, TM, "Növényi alternatíva", "Növényi ital", vegán=True, laktózmentes=True, gluténmentes=gm,
      bio=bio, **{"cukormentes / hozzáadott cukor nélkül":cukm}, kiszerelés="doboz", márka="MyVay",
      **{"terméktípus":["növényi ital"], "alap":alap, "zsírtartalom / jelleg":zj,
         "dúsítás":["egyéb"], "íz":(iz or ["natúr"])})
myvay_ital(2172, ["zab"], bio=True)
myvay_ital(2173, ["rizs","kókusz"], bio=True)
d(2174, AL, "Szószok, öntetek, dresszingek", "Szendvicskrém, hummusz, kenőkrém",
  kiszerelés="tégely", márka="Wonnemeyer", gluténmentes=True, vegán=True, vegetáriánus=True,
  laktózmentes=True, **{"alap":["hummusz"], "íz":["egyéb"],
  "konyha / stílus":["egyéb"], "csípősség":["csemege"]})

# --- SHEET 4 (2175-2199) ---
def hummus(i, iz, csipos=False, marka="Wonnemeyer"):
    d(i, AL, "Szószok, öntetek, dresszingek", "Szendvicskrém, hummusz, kenőkrém",
      kiszerelés="tégely", márka=marka, gluténmentes=True, vegán=True, vegetáriánus=True,
      laktózmentes=True, csípős=csipos, **{"alap":["hummusz"], "íz":iz,
      "konyha / stílus":["egyéb"], "csípősség":(["csípős"] if csipos else ["csemege"])})
def alpro_jog(i, iz):
    d(i, TM, "Növényi alternatíva", "Növényi joghurt", vegán=True, laktózmentes=True,
      gluténmentes=True, **{"ízesített":True}, kiszerelés="pohár", márka="Alpro",
      **{"terméktípus":["fermentált készítmény"], "alap":["szója"], "zsírtartalom / jelleg":["egyéb"],
         "dúsítás":["kalcium"], "íz":iz})
def myvay_spread(i, iz):
    d(i, AL, "Szószok, öntetek, dresszingek", "Szendvicskrém, hummusz, kenőkrém",
      kiszerelés="tégely", márka="MyVay", gluténmentes=True, vegán=True, vegetáriánus=True,
      laktózmentes=True, **{"alap":["egyéb"], "íz":iz,
      "konyha / stílus":["egyéb"], "csípősség":["csemege"]})
def myvay_huspotlo(i, forma, alap="szója"):
    d(i, HH, "Növényi húspótló",
      {"virsli":"Növényi virsli/kolbász","falat":"Növényi falat/burger",
       "burger":"Növényi falat/burger"}[forma],
      vegán=True, **{"készítmény (növényi/kevert)":True}, márka="MyVay",
      **{"alap":[alap], "forma":[forma], "csomagolás":["tálca"]})

hummus(2175, ["natúr"])                              # WONNEMEYER Natúr hummus
hummus(2176, ["csípős"], csipos=True)                # WONNEMEYER Pikáns hummus
myvay_ital(2177, ["mandula"], bio=True, cukm=True, gm=True)  # MYVAY Bio Mandulaital cukormentes
alpro_jog(2178, ["egyéb"])                           # ALPRO Szójagurt barackos
alpro_jog(2179, ["áfonya"])                          # ALPRO Szójagurt kékáfonyás
d(2180, AL, "Konzerv, savanyúság, befőtt", "Kókusztej, kókuszkrém, főzőalap",  # ASIA GREEN GARDEN
  kiszerelés="doboz", márka="Asia Green Garden",
  **{"alapanyag":["kókusz"], "lé / közeg":["egyéb"], "darabolás":["egyéb"], "típus":["light"]})
myvay_spread(2181, ["natúr"])                        # MYVAY natúr szendvicskrém
myvay_spread(2182, ["egyéb"])                        # MYVAY szendvicskrém zöldfűszerekkel
myvay_spread(2183, ["paprikás"])                     # MYVAY szendvicskrém paprikával
myvay_ital(2184, ["zab"])                            # MYVAY Barista zabital
hummus(2185, ["csípős"], csipos=True, marka="Yummy Dip")  # YUMMY DIP Hummusz pikáns
hummus(2186, ["egyéb"], marka="Yummy Dip")           # YUMMY DIP Hummusz currys
hummus(2187, ["natúr"], marka="Yummy Dip")           # YUMMY DIP Hummusz natúr
myvay_huspotlo(2188, "virsli")                       # MYVAY Vegán frankfurti
d(2189, TM, "Növényi alternatíva", "Növényi főzőkrém / tejszín", vegán=True, laktózmentes=True,  # HULALA habalapanyag
  kiszerelés="doboz", márka="Hulala",
  **{"terméktípus":["habkrém"], "alap":["növényi olaj"], "zsírtartalom / jelleg":["egyéb"],
     "dúsítás":["egyéb"], "íz":["natúr"]})
myvay_huspotlo(2190, "falat")                        # MYVAY falatok döner
myvay_huspotlo(2191, "falat")                        # MYVAY falatok csirke
myvay_huspotlo(2192, "burger")                       # MYVAY Vegán burger
d(2193, ZO, "Paradicsom", None, kiszerelés="csomagolt", **{"feldolgozottság":["egész"],  # Paradicsom koktél
  "méret":["normál"]}, fajta="Koktél", fürtös=True, **{"színe":"Piros"})
d(2194, GY, "Görögdinnye", None, kiszerelés="lédig", **{"érettség":["érett"], "méret":["normál"],  # Görögdinnye
  "feldolgozottság":["egész"]})
d(2195, ZO, "Tökféle, cukkini, padlizsán", None, kiszerelés="lédig",  # Padlizsán
  **{"feldolgozottság":["egész"], "méret":["normál"]})
d(2196, ZO, "Paprika", None, kiszerelés="lédig", **{"feldolgozottság":["egész"], "méret":["normál"]},  # Paprika TV
  fajta="TV", **{"színe":"Fehér"})
d(2197, GY, "Málna", None, kiszerelés="csomagolt", **{"érettség":["fogyasztásra kész"],  # Málna
  "méret":["normál"], "feldolgozottság":["egész"]})
d(2198, ED, "Rágcsálnivaló magvak (snack)", "Magkeverék (sós)", sótlan=True, vegán=True,  # Diákcsemege
  márka="Happy Harvest", **{"magfajta":["magkeverék"], "ízesítés":["natúr"]})
d(2199, ED, "Rágcsálnivaló magvak (snack)", "Olajos magvak (snack)", sótlan=True, vegán=True,  # BELLA Mandula
  márka="Bella", **{"magfajta":["mandula"], "ízesítés":["natúr"]})

# ---- 3) ÉPÍTÉS + VALIDÁCIÓ ----
def build(tree, rows):
    out = []
    for i, fok, al, alt, ov in D:
        sch = schema(tree, fok, al, alt)
        tul = {}
        for key, spec in sch.items():
            if spec == {}:  # flag
                v = ov.get(key, False)
                assert isinstance(v, bool), f"{i} {key}: flag nem bool ({v})"
                tul[key] = v
            elif isinstance(spec, dict) and spec.get("type") == "single":
                assert key in ov, f"{i}: hiányzó single '{key}' ({fok}>{al}>{alt})"
                v = ov[key]
                assert v in spec["values"], f"{i} {key}: '{v}' nincs az opciók közt {spec['values']}"
                tul[key] = v
            elif isinstance(spec, list):
                assert key in ov, f"{i}: hiányzó lista '{key}' ({fok}>{al}>{alt})"
                v = ov[key]
                assert isinstance(v, list) and v, f"{i} {key}: nem nemüres lista ({v})"
                for x in v:
                    assert x in spec, f"{i} {key}: '{x}' nincs az opciók közt {spec}"
                tul[key] = v
        # ellenőrzés: minden override kulcs valós séma-kulcs
        for k in ov:
            assert k in sch, f"{i}: ismeretlen tulajdonság override '{k}' ({fok}>{al}>{alt})"
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
    assert len(new) == 100, f"vártam 100 (2100-2199), kaptam {len(new)}"
    # mentés (indent=2 + LF, az eredeti formátum szerint)
    def save(path, data):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))
    save(TREE, tree)
    ered = json.load(open(ERED, encoding="utf-8"))
    # idempotencia: töröljük az esetleg már meglévő 2100-2195 indexű rekordokat
    done_keys = set((rows[i]["store_name"], rows[i]["store_product_id"]) for i,_,_,_,_ in D)
    ered = [r for r in ered if (r.get("termek",{}).get("store_name"),
                                r.get("termek",{}).get("store_product_id")) not in done_keys]
    ered.extend(new)
    save(ERED, ered)
    print(f"OK: {len(new)} új rekord, eredmeny.json össz: {len(ered)}")

if __name__ == "__main__":
    main()
