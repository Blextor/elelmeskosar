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

## Besorolások ellenőrzése

A fejléc **Besorolások ellenőrzése** hivatkozása megnyitja az [ellenőrzőoldalt](http://127.0.0.1:8765/ellenorzes/). A bal oldali listában névre, kategóriára és bolti azonosítóra kereshetsz. A **Kivételek** szűrő mutatja az indoklással ellátott tételeket. A kiválasztott termék fotója nagyítható. A jobb oldalon a két teljes kategóriaútvonal és a tulajdonságok értékenkénti összevetése látható. A **Csak eltérések** kikapcsolásával az azonos értékek is megjelennek.

- **Korábbi munka átnézése.** A jegyzékválasztó az `analysis/reports/*/termekenkenti_besorolas.csv` fájlokat kínálja fel. A fagyasztott termékek jegyzéke tartalmazza az újrabesorolás előtti és utáni tulajdonságokat. Más jegyzékekben a `regi_tulajdonsagok` és az `uj_tulajdonsagok` oszlopba JSON-objektum kerülhet. Ha a régi oszlop hiányzik, az oldal ezt jelzi.
- **Új javaslat átnézése a csere előtt.** A **Tervezet megnyitása** gombbal válassz az `eredmeny.json` szerkezetét követő terméklistát. A teljes lista és egyetlen ág rekordjait tartalmazó tömb is használható. Az ellenőrző a jelenlegi helyi eredményekkel veti össze a tervezetben szereplő rekordokat bolt és bolti termékazonosító alapján. A listába az új termékek és az eltérések kerülnek.
- **Ellenőrzési állapot.** A **Rendben** és a **Javítandó** jelöléseket a böngésző az adott összevetéshez menti. Az aktív gomb újbóli megnyomásával visszaállíthatod az ellenőrizetlen állapotot. A termékadatok cseréje külön művelet.

## Felhasználói folyamat

A **Részfa-tervező** a fejlécből vagy közvetlenül a [helyi részfa-tervezőben](http://127.0.0.1:8765/reszfa/) érhető el. Az alábbi műveletekhez a tervezőben nyiss meg egy ágat.

- A főkategóriát, alkategóriát és altípust hozzáadhatod, átnevezheted és törölheted. Az alkategória és az altípus másik szülőhöz is áthelyezhető a teljes ágával együtt. Az örökölt tulajdonságok az új szülő útvonalát követik.
- A **Saját tulajdonságok** között szerkeszthető a név, a típus és a lehetséges értékek. A fix lehetőségeket soronként add meg. A többválasztós listához megjegyzést is írhatsz. Az örökölt tulajdonságot a deklaráló felmenőn szerkesztheted.
- A **Részfa letöltése** név szerinti JSON-objektumot ad a kijelölt csomóponttal, saját tulajdonságaival és összes leszármazottjával. A felmenők definíciói a felmenőkön maradnak. A lista értékei a megszokott `tulajdonságok.csoportos` mezőben vannak. A hozzájuk tartozó szöveg a csomópont `tulajdonságmegjegyzések` mezőjében szerepel, a tulajdonság nevével kulcsolva. A **Teljes fa** nézetben az összes módosított ág együtt exportálható.
- A vázlat ugyanazon a böngészőlapon újratöltés után is elérhető. Bezárás előtt töltsd le a kívánt JSON-t. A **Vázlat elvetése** a megnyitáskor betöltött forrásfát állítja vissza. Az eredeti kategóriafájl és a termékbesorolások szerkesztése a régi felületen történik.

### Műveletek az eredeti kategóriafán

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

- **Összevonás (tulajdonság-térkép)** — *ez az elsődleges összevonó művelet.* Kijelölsz egy
  **Forrás** és egy **Cél** node-ot (azonos szintűek). A felület kétoldalt kirajzolja a két node
  tulajdonságait pöttyökkel (a fán deklaráltakat ÉS a termékeken ténylegesen előfordulókat is).
  Húzd össze őket: kattints egy **bal** (forrás) pöttyre, majd egy **jobb** (cél) pöttyre.
  - Összekötött forrás-tulajdonság → **beolvad** a cél-tulajdonságba (értékek uniója).
  - Be **nem** kötött **forrás**-tulajdonság → **törlődik** (pirossal, áthúzva jelölve).
  - Be nem kötött **cél**-tulajdonság → marad, nem történik vele semmi.
  - Az **azonos nevűek előre összekötve** indulnak; forrás-pöttyre kattintva bontod a kötést.
  - Alkalmazáskor a **forrás node és termékei a célba olvadnak** (a forrás megszűnik), a
    tulajdonságok a térkép szerint képződnek le. Az Előnézet pontosan listázza, mi köt össze és mi törlődik.
  - **Öröklés:** a pöttyök közt a **felmenők** (fő-/alkategória) tulajdonságai is megjelennek
    (`örökölt: <szülő>` címke, dőlten), érték-listák **unióval** (nem felülírással). Így a
    Citromlé altípusnál a Citromlé alkategória teljes márkalistája is látszik.
  - **Eltérő szint is összevonható:** a forrás és a cél lehet különböző mélységű. Ekkor a forrás
    termékei a **cél szintjére** kerülnek; ha a cél sekélyebb, a mélyebb szint(ek) kiürülnek
    (pl. altípus → alkategória = feloldás térképpel).
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
