# -*- coding: utf-8 -*-
"""6501-6600 kézi kategorizálása, kép+CSV alapján."""
import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
TREE = BASE / "kategoriak_2026-06-13.json"
CSV = BASE / "kategorizalatlan_termekek.csv"
ERED = BASE / "eredmeny.json"

AL = "Alapanyag, sütés-főzés"
FU = "Fűszer"


def kategoriak_hash(fok, al, alt, tul):
    key = f"{fok}|{al}|{alt}|{json.dumps(tul, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def add_vals(values, new_values):
    for value in new_values:
        if value not in values:
            values.append(value)


def extend_tree(tree):
    fuszer = tree[AL]["alkategóriák"][FU]
    add_vals(fuszer["tulajdonságok"]["egyedi"]["márka"], [
        "Kalocsai", "Univer", "Auchan Kedvenc", "THYMOS", "Konyhavarázs"
    ])
    add_vals(fuszer["tulajdonságok"]["csoportos"]["forma"], ["pehely"])
    add_vals(fuszer["tulajdonságok"]["csoportos"]["fűszerfajta"], [
        "rózsabors", "tarkabors", "fehér bors", "színesbors", "babérlevél",
        "borsikafű", "lestyán", "sáfrány", "sáfrányos szeklice", "koriander",
        "kurkuma", "mustármag", "szegfűszeg", "szegfűbors", "édeskömény",
        "római kömény", "zsálya", "szegfűszeg", "fűszerpaprika",
        "majoranna", "rozmaring"
    ])
    add_vals(fuszer["altípusok"]["Bors, chili"]["tulajdonságok"]["csoportos"]["fajta"], [
        "tarkabors", "fehér bors", "rózsabors", "citrombors", "fokhagymabors",
        "bors és tengeri só", "Birdseye chili"
    ])


D = []


def spice(i, alt, marka, forma, fajta, cel=None, csip="nem csípős", bio=False, kisz="tasak", extra=None):
    props = {
        "kiszerelés": kisz,
        "márka": marka,
        "bio": bio,
        "forma": forma,
        "fűszerfajta": fajta,
        "célétel / stílus": cel or ["egyéb"],
        "csípősség": [csip],
    }
    if extra:
        props.update(extra)
    D.append((i, AL, FU, alt, props))


def paprika(i, marka, csip="nem csípős", forma=None, fajta=None, kisz="tasak"):
    spice(i, "Őrölt paprika", marka, forma or ["őrölt"], fajta or ["paprika"], ["egyéb"], csip, False, kisz)


def bors(i, marka, forma, fajta, kisz="tasak", csip="nem csípős", bio=False):
    spice(i, "Bors, chili", marka, forma, ["bors"], ["egyéb"], csip, bio, kisz, {"fajta": fajta})


def herb(i, marka, forma, fajta, bio=False):
    spice(i, "Szárított fűszernövény", marka, forma, fajta, ["egyéb"], "nem csípős", bio, "tasak")


def basic(i, marka, forma, fajta, bio=False):
    spice(i, "Őrölt / egész fűszer", marka, forma, fajta, ["egyéb"], "nem csípős", bio, "tasak")


def mix(i, marka, forma, fajta, cel, csip="nem csípős", kisz="tasak", alt="Fűszerkeverék"):
    spice(i, alt, marka, forma, fajta, cel, csip, False, kisz)


# Paprika, chili, fűszersó
paprika(6500, "Szegedi", fajta=["fűszerpaprika"])
paprika(6501, "Szegedi")
paprika(6502, "Szegedi")
paprika(6503, "Szegedi", csip="csípős")
paprika(6504, "Kalocsai")
paprika(6505, "Kalocsai", fajta=["fűszerpaprika"])
paprika(6506, "Kalocsai", fajta=["fűszerpaprika"])
paprika(6507, "Böllér", fajta=["fűszerpaprika"])
paprika(6508, "Univer", csip="csípős", forma=["pehely"])
paprika(6509, "Szegedi")
paprika(6510, "Szegedi", fajta=["fűszerpaprika"])
mix(6511, "Kotányi", ["malmos"], ["chili"], ["egyéb"], "csípős", "üveg", "Fűszersó, pác")
paprika(6512, "Univer", csip="csípős")
bors(6513, "Kotányi", ["malmos"], ["Birdseye chili"], "üveg", "extra csípős")
paprika(6514, "Kalocsai", csip="csípős", fajta=["fűszerpaprika"])
paprika(6515, "Kalocsai", fajta=["fűszerpaprika"])
paprika(6516, "Lacikonyha", fajta=["fűszerpaprika"])
paprika(6517, "Kotányi")
paprika(6518, "Szegedi", fajta=["fűszerpaprika"])
paprika(6519, "Lacikonyha", fajta=["fűszerpaprika"])
paprika(6520, "Böllér", fajta=["fűszerpaprika"])
paprika(6521, "Böllér", fajta=["fűszerpaprika"])

# Borsok
bors(6522, "Horváth Rozi", ["egész"], ["fekete bors"])
bors(6523, "Horváth Rozi", ["őrölt"], ["fekete bors"])
bors(6524, "Lucullus", ["egész"], ["fekete bors"])
bors(6525, "Lucullus", ["őrölt"], ["fekete bors"])
bors(6526, "Auchan Kedvenc", ["egész"], ["tarkabors"])
bors(6527, "Lucullus", ["őrölt"], ["fehér bors"])
bors(6528, "Horváth Rozi", ["őrölt"], ["citrombors"])
bors(6529, "Lucullus", ["egész"], ["rózsabors"])
bors(6530, "Kotányi", ["őrölt"], ["fekete bors"])
bors(6531, "THYMOS", ["egész"], ["színes bors"])
bors(6532, "Ízmester", ["őrölt"], ["fekete bors"], bio=True)
bors(6533, "Horváth Rozi", ["őrölt"], ["fekete bors"])
bors(6534, "Horváth Rozi", ["egész"], ["fekete bors"])
bors(6535, "Kotányi", ["egész"], ["tarkabors"])
bors(6536, "THYMOS", ["őrölt"], ["fekete bors"])
bors(6537, "Lucullus", ["őrölt"], ["fekete bors"])
bors(6538, "Kotányi", ["malmos"], ["bors és tengeri só"], "üveg")
bors(6539, "Kotányi", ["malmos"], ["fekete bors"], "üveg")
bors(6540, "Kotányi", ["malmos"], ["tarkabors"], "üveg")
bors(6541, "Horváth Rozi", ["őrölt"], ["fokhagymabors"])

# Zöldfűszerek
herb(6542, "Auchan Tipp", ["morzsolt"], ["majoranna"])
herb(6543, "Auchan Kedvenc", ["morzsolt"], ["bazsalikom"])
herb(6544, "Horváth Rozi", ["morzsolt"], ["majoranna"])
herb(6545, "Horváth Rozi", ["őrölt"], ["majoranna"])
herb(6546, "Lucullus", ["morzsolt"], ["majoranna"])
herb(6547, "Auchan Tipp", ["egész"], ["babérlevél"])
herb(6548, "Horváth Rozi", ["morzsolt"], ["bazsalikom"])
herb(6549, "Horváth Rozi", ["morzsolt"], ["oregánó"])
herb(6550, "Horváth Rozi", ["szeletelt"], ["petrezselyem"])
herb(6551, "Lucullus", ["morzsolt"], ["oregánó"])
herb(6552, "Lucullus", ["szeletelt"], ["kapor"])
herb(6553, "Lucullus", ["szeletelt"], ["petrezselyem"])
herb(6554, "Kotányi", ["morzsolt"], ["majoranna"])
herb(6555, "Horváth Rozi", ["szeletelt"], ["rozmaring"])
herb(6556, "Lucullus", ["morzsolt"], ["borsikafű"])
herb(6557, "Lucullus", ["morzsolt"], ["lestyán"])
herb(6558, "Lucullus", ["morzsolt"], ["tárkony"])
herb(6559, "Lucullus", ["szeletelt"], ["metélőhagyma"])
herb(6560, "Kotányi", ["egész"], ["babérlevél"])
herb(6561, "Horváth Rozi", ["őrölt"], ["sáfrányos szeklice"])
herb(6562, "Kotányi", ["morzsolt"], ["bazsalikom"], bio=True)
herb(6563, "Kotányi", ["szeletelt"], ["petrezselyem"], bio=True)
herb(6564, "Kotányi", ["morzsolt"], ["bazsalikom"])
herb(6565, "Kotányi", ["morzsolt"], ["kakukkfű"])
herb(6566, "Kotányi", ["morzsolt"], ["oregánó"])
herb(6567, "Kotányi", ["szeletelt"], ["kapor"])
herb(6568, "Kotányi", ["szeletelt"], ["petrezselyem"])
herb(6569, "Kotányi", ["őrölt"], ["rozmaring"])
basic(6570, "Kotányi", ["egész"], ["sáfrány"])

# Egyéb fűszerek, pácok, keverékek
basic(6571, "Auchan Kedvenc", ["őrölt"], ["fahéj"])
basic(6572, "Horváth Rozi", ["egész"], ["kömény"])
basic(6573, "Horváth Rozi", ["egész"], ["koriander"])
basic(6574, "Horváth Rozi", ["őrölt"], ["kömény"])
basic(6575, "Horváth Rozi", ["őrölt"], ["kurkuma"])
herb(6576, "Auchan Kedvenc", ["morzsolt"], ["tárkony"])
basic(6577, "Horváth Rozi", ["mag"], ["mustármag"])
basic(6578, "Lucullus", ["őrölt"], ["fahéj"])
basic(6579, "Lucullus", ["mag"], ["mustármag"])
basic(6580, "Lucullus", ["egész"], ["kömény"])
basic(6581, "Lucullus", ["egész"], ["koriander"])
basic(6582, "Auchan Tipp", ["granulátum"], ["fokhagyma"])
basic(6583, "Horváth Rozi", ["granulátum"], ["fokhagyma"])
basic(6584, "Auchan Kedvenc", ["őrölt"], ["szegfűszeg"])
basic(6585, "Lucullus", ["őrölt"], ["kömény"])
basic(6586, "Lucullus", ["granulátum"], ["fokhagyma"])
herb(6587, "Horváth Rozi", ["egész"], ["babérlevél"])
basic(6588, "Horváth Rozi", ["őrölt"], ["fahéj"])
herb(6589, "Horváth Rozi", ["őrölt"], ["babérlevél"])
basic(6590, "Horváth Rozi", ["egész"], ["szegfűbors"])
basic(6591, "THYMOS", ["mag"], ["édeskömény"])
herb(6592, "THYMOS", ["morzsolt"], ["zsálya"])
basic(6593, "Horváth Rozi", ["egész"], ["szegfűszeg"])
mix(6594, "Horváth Rozi", ["por"], ["fokhagymás"], ["grill"], "nem csípős", "tasak", "Fűszersó, pác")
basic(6595, "Lucullus", ["őrölt"], ["kurkuma"])
basic(6596, "Lucullus", ["őrölt"], ["római kömény"])
basic(6597, "Horváth Rozi", ["egész"], ["római kömény"])
mix(6598, "Konyhavarázs", ["por"], ["sült krumpli"], ["sült krumpli"], "nem csípős", "tasak", "Fűszerkeverék")
basic(6599, "Lucullus", ["egész"], ["szegfűszeg"])


def main():
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    extend_tree(tree)
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    assert len(D) == 100, len(D)
    new = []
    for i, fok, alk, alt, props in D:
        new.append({
            "termek": rows[i],
            "fokategoria": fok,
            "alkategoria": alk,
            "altipus": alt,
            "tulajdonsagok": props,
            "kategoria_hash": kategoriak_hash(fok, alk, alt, props),
            "statusz": "kesz",
        })
    done_keys = {(rows[i]["store_name"], rows[i]["store_product_id"]) for i, *_ in D}
    ered = json.loads(ERED.read_text(encoding="utf-8"))
    ered = [
        r for r in ered
        if (r.get("termek", {}).get("store_name"), r.get("termek", {}).get("store_product_id")) not in done_keys
    ]
    ered.extend(new)
    TREE.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    ERED.write_text(json.dumps(ered, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(f"saved {len(new)} records; eredmeny length={len(ered)}")


if __name__ == "__main__":
    main()
