# Kategória-szerkesztő

Helyi webes eszköz a termék-kategorizálás tisztításához. A **kategóriafát**
(`kategoriak_*.json`) **és** a **termékeket** (`eredmeny.json`) szinkronban tartja.

## Indítás

```bash
cd data/categories/kategorizalando_termekek/GPT
python kategoria_szerkeszto.py
```

Megnyílik a böngésző: <http://127.0.0.1:8765> (ha nem, nyisd meg kézzel).
Leállítás: `Ctrl+C`. Függőség nincs, csak Python 3.

> A `kategoriak_*.json` közül automatikusan a **legfrissebb dátumozottat** használja.

## Felhasználói folyamat

1. A bal oldali fában keress/böngéssz. Minden node mutatja a termékszámot
   (mélységgel együtt), az alkategóriáknál a „közvetlen" (altípus nélküli) számot is.
2. A node sorára húzva a kurzort jelöld ki **Forrás**nak vagy **Cél**nak.
3. Válassz műveletet a fülek közül, töltsd ki az űrlapot.
4. **Előnézet** — kiszámolja, mi változna (semmit nem ír).
5. **Alkalmaz** — megerősítés után **felülírja** a két JSON-t (atomi mentés, `.bak` nélkül).

A „Talált gondok" doboz a duplikált (azonos nevű szülő+altípus, pl. Citromlé→Citromlé)
és az **árva besorolásokat** (olyan termék-hármas, amihez nincs fa-node) listázza; rákattintva
a forrásnak jelöli.

## Műveletek

- **Node áthelyezés + összeolvasztás** — egy fő-/al-/altípust áthelyez egy másik helyre.
  Ha a célon már van azonos nevű node, **összeolvad** vele (tulajdonság-listák uniója,
  altípusok egyesítése). A forrás alatti termékek besorolása átíródik.
  - *Összeolvasztáshoz* a forrással **azonos szintű** célt jelölj ki.
  - *Új helyre tételhez* **egy szinttel feljebbi** célt (oda kerül új gyerekként), és add meg a nevet.
- **Altípus feloldása** — az altípus (vagy alkategória) megszűnik: tulajdonságai a
  szülőbe olvadnak, termékei közvetlenül a szülőhöz kerülnek (a megfelelő szint kiürül).
  Ez a Citromlé→Citromlé eset megoldása.
- **Tulajdonság áthelyezés/átnevezés** — egy tulajdonságot (vagy egyetlen értéket)
  átnevez/áthelyez/összevon node-ok közt, a termékek tulajdonságaival együtt.
  Lista-tulajdonságnál a chipre kattintva megadhatsz **egyetlen értéket** is.
- **Új tulajdonság** — új `egyedi`/`csoportos`, `flag` vagy `lista` tulajdonság a node-on.

## Fontos tudnivalók

- A termékek besorolása a `(fokategoria, alkategoria, altipus)` hármason alapul; az
  illesztés is ez alapján megy. A `termek.*` mezők szándékosan üresek.
- A fa-node-on **nem feltétlen van deklarálva** minden tulajdonság, ami a termékeken
  szerepel. A tulajdonság-műveletek ezt kezelik: a termék-szintű módosítás akkor is
  megtörténik, és a ténylegesen mozgatott értékekkel a fa-lista feltöltődik.
- **Egyszerre csak egy írót.** Ha közben fut a batch-kategorizálás (`apply_batch_*.py`),
  ne nyomj **Alkalmaz**t — előbb állítsd le, hogy ne írjatok egyszerre a fájlokba.
- A mentés atomi (`temp` + `os.replace`), de visszavonás nincs: a verziókövetésedre
  (git) támaszkodj, ha vissza akarsz lépni.
