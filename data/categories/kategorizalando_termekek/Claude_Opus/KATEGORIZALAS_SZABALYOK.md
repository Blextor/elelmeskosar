# Kategorizálási szabályok (kötelező, mindig olvasd vissza)

Ez a fájl a termékkategorizálás kötelező szabályait rögzíti. **Minden batch elkezdése
előtt olvasd vissza.** A munka célja a `master_products`-hoz: minden terméknek legyen
helyes kategóriája ÉS a kategóriájához tartozó MINDEN tulajdonsága kitöltve.

Kapcsolódó fájlok:
- Fa: `kategoriak_2026-06-13.json` (ebben a mappában)
- Eredmény: `eredmeny.json` (rekordonként: `termek`, `fokategoria`, `alkategoria`,
  `altipus`, `tulajdonsagok`, `kategoria_hash`, `statusz`)
- Backlog: `kategorizalatlan_termekek.csv`
- Futtató/segédek: `src/categories/llm_kategorizalo/`

## 1. Teljes tulajdonság-kitöltés (LEGFONTOSABB)

A termék path-ja = fő kategória + alkategória + altípus. Az e path-on érvényes
ÖSSZES tulajdonságot ki kell tölteni (öröklődő fő-szintű + alkategória-szintű +
altípus-szintű együtt). Nem elég néhányat.

- **Flag (igaz/hamis):** MINDIG döntsd el — `true` vagy `false`. Soha ne hagyd ki.
- **Listás / választható:** legalább EGY értéket adj.
  - Ha nincs a termékre jellemző konkrét érték → válaszd az `"egyéb"`-et.
  - Ha a listában NINCS `"egyéb"` → előbb VEDD FEL az `"egyéb"`-et a listába, majd használd.
- **Egyedi (single) lista** → egy string érték; **csoportos (multi) lista** → legalább
  egy elemű lista.

## 2. Fa bővítése a hiányzók szerint

Ha a termékre jellemző adat nem fér be a fába, NE ejtsd `"egyéb"`-re csendben — bővíts:

- Hiányzó **érték** (pl. a márka neve nincs a márkalistában) → vedd fel a csoportba.
- Hiányzó **tulajdonságcsoport** (pl. nincs hova írni egy fontos jellemzőt) → vedd fel.
- Hiányzó **altípus / alkategória** (a termék külön altípust kíván) → vedd fel.

**Gondolkodj végig MINDEN jellemző tulajdonságot:** márka, íz/ízesítés, forma/alak,
szín, zsírtartalom, érzékenység (laktóz-/gluténmentes, bio) stb. — ami az adott termékre
jellemző. Ha a path-on nincs hozzá slot (pl. a joghurtnál sokáig NEM volt `márka`, a
Krémjoghurt/Skyr-en nem volt `íz`), az a fa hiányossága → előbb VEDD FEL (lehetőleg
alkategória-szinten, hogy az altípusok örököljék), majd töltsd ki. A `márka` egyedi lista
a konkrét márkákkal + `egyéb`; a márka a terméknévből kiolvasható (a `brand_name` mező
gyakran üres). FIGYELEM: új tulajdonság felvétele visszamenőleg hiányossá teszi a korábbi
rekordokat is arra a slotra → ld. 6. pont (backlog), az `audit.py` jelzi.

A bővítés a `kategoriak_2026-06-13.json`-ba megy; az `1005` fa richness-ét sosem
csökkentjük (MERGE, nem felülírás). A bővítés után a tulajdonságot ténylegesen töltsd ki.

## 3. Kép mindig kötelező

MINDEN terméknél nézd meg a termékképet (`local_image_paths`, a Read eszközzel).
Egyes infó (pontos kiszerelés, töltelék, márka, jelleg, töltött/marinált stb.) CSAK a
képen lehet. A bolti név/út félrevezető lehet — a kép + név + kiszerelés együtt dönt.

## 4. Besorolási elvek (összefoglaló)

- A bolti kategóriaút csak KIINDULÁS; a név, a kép és a kiszerelés együtt dönt.
- Bottom-up tulajdonság-elhelyezés (altípus → alkategória → fő).
- Fagyasztott → Fagyasztott áruk (kivéve fagyasztott péksütemény → Pékáru). A
  fagyasztott HAL külön ágban marad a Fagyasztott áruk alatt (2026-06-15 döntés).
- Készétel = készen van, max mikrózni kell, főétel-jellegű (nem nyers tészta, nem snack,
  nem instant/bögrés leves). Friss töltött tészta (nem teljesen száraz) készétel.
- Olajos magvak: az egész, rágcsálható mag (sózott/pörkölt ÉS natúr) → Édesség >
  Rágcsálnivaló magvak; a darált/reszelt sütőforma → Alapanyag.
- Mentes/bio/vegán/laktóz-/gluténmentes/protein → a rokon ág megfelelő FLAG-jével,
  nem külön „Mentes" ágba (kivéve fehérjepor, vitamin, paleo).
- Hummusz/szendvicskrém → Alapanyag > Szószok; tofu/szejtán/vegán húspótló → Hús-hal >
  Növényi húspótló; növényi ital/krém/joghurt/sajt → Tejtermék > Növényi alternatíva.

## 5. Munkamenet és technikai szabályok

- Kimenet: `eredmeny.json`-kompatibilis rekord; a `kategoria_hash` BITRE a `kat25.py`
  képletével: `sha256("fok|al|alt|json(tul, sort_keys=True, ensure_ascii=False)")`.
- Determinisztikus utóvalidáció: minden rekord út-/érték-helyességét a fa ellen
  ellenőrizni, a hash-t újraszámolni. (A validátort bővíteni kell úgy, hogy a KI NEM
  töltött path-tulajdonságokat is jelezze, ne csak az érvénytelen értékeket.)
- Köteges futtatás explicit indexszel (0..N-1 hiánytalanság-ellenőrzéssel), nem
  pozíció-számolással.
- Token-takarékosság: a logika a futtatóscriptbe; minimális dump/lista/próza. De a
  takarékosság NEM mehet a teljes kitöltés, a képvizsgálat és a fa-bővítés rovására →
  inkább kisebb, alaposabb adagok.
- Nincs `.bak` fájl (a felhasználónak saját verziókövetése van).

## 6. Visszamenőleges teendő

A korábbi saját besorolások (kb. az `eredmeny.json` 1700. indexétől felfelé) hiányosan
vannak kitöltve (kihagyott flagek, üres listák, fába fel nem vett márkák, kép nélkül).
Ezeket e szabályok szerint utólag át kell nézni és pótolni.

## 7. Montázs-munkamenet (a pótlás módja) + haladás

A felülvizsgálat 25-ös csoportokban megy, montázzsal (hatékony képnézés):

1. `python src/categories/llm_kategorizalo/_montage.py START 25` → létrejön
   `_montage.png` (5×5 rács, cellánként `#index` felirat) + `_lst.txt`
   (tételenként: név, kiszerelés, PATH, és a path ÖSSZES megengedett tulajdonsága
   `[flag]/[single]/[multi]` jelöléssel + a listák értékei).
2. Read-del megnézni a `_montage.png`-t (egy kép = 25 termék) és a `_lst.txt`-t.
3. Eldobható fix-script (/tmp/fix.py): minden tételhez a TELJES `tulajdonsagok` dict
   (minden flag true/false, minden lista ≥1 érték), szükség szerint fa-bővítés
   (hiányzó márka/érték/csoport a `kategoriak_2026-06-13.json`-ba), majd
   `coerce_tulajdonsagok` + hash-újraszámolás, és mentés az `eredmeny.json`-ba.
4. **A hiány-ellenőrzést a `coerce` UTÁNI (clean) értéken kell futtatni**, nem a
   bemeneten — különben a fa listájába nem illő érték (amit a coerce eldob) hiányként
   átcsúszik. Tipikus eldobások: Krémsajt kiszerelés `tégely` (a Sajt-listában nincs →
   `doboz`); Margarin kiszerelés `papír` (nincs → `doboz`); Túró kiszerelés `pohár`
   (nincs → `tégely`). Sok altípusnak van rejtett `íz`/`fajta` listája (pl. Vajkrém íz,
   Joghurt-Gyümölcsös íz, Túró Rudi íz, Sajt-altípusok fajta) — ezeket is ki kell tölteni.
5. Ellenőrzés: `python src/categories/llm_kategorizalo/audit.py [START]` (az 1700-tól
   számolt hiánytalan/hiányos darabszám; a fix-scriptbeli `fld()` ezzel azonos logika)
   és a hash-validátor. Az audit/fix `fld()`: flag=bool kész, lista≥1 kész, string≠'' kész.

**Eddigi fa-bővítések (példák):** Hotdog márka←Azon Melegében; Egyéb édes márka←egyéb;
Tortilla íz←chilis/kukoricás/natúr/egyéb; Tejdesszert íz←natúr; Joghurt-Gyümölcsös
íz←sárgabarackos/ananászos; Joghurt-Gyümölcsös íz←mézes-diós/almás-fahéjas/mangós;
Túró Rudi jellegű íz←kekszes/karamellás/mazsolás; Müzliszelet forma←szelet, íz/hozzáadott←gránátalma.
**Márka-slot felvéve** (alkat-szinten) a Joghurt/Sajt/Krémtúró/Tejdesszert-puding/
Ivójoghurt ágba; **íz-slot felvéve** a Krémjoghurt és Skyr altípusra (+gránátalmás/narancsos).
**2. kör (1912–1986):** márka-slot a Tejszín/Margarin/Vaj/Tej/Tejital-jegeskávé/Tejföl/
Sajtkrém-szendvicskrém/Túró ágba is; márkák bővítve (Kokárdás/Ammerländer/Cserpes/Milli/
Milsani/Zott/Hell/Hajdú/Nádudvari/Riska/Tolle/Delma/Bellasan/Barissimo); íz-slot a Krémtúró
alkat-szintre; íz-értékek: Joghurt←körte, Ivójoghurt←maracuja, Tejdesszert←meggyes/fahéjas,
Tejital←sós karamellás; Sajt fajta←parenyica, ízesítés←fokhagymás/szalámis; Szendvicskrém
íz←magyaros/fokhagymás; Tejföl zsírtartalom←25%; Csokoládé szelet hozzáadott darabok←puffasztott rizs.

**Altipus-javítás (példa):** Kokárdás ízesített túródesszert (kekszes/mazsolás/karamellás/
vanília) → „Natúr krémtúró" helyett „Túró Rudi jellegű túródesszert" (van íz-slot).

**3. kör (1987–2036):** új márkák (Mizo/Vénusz/Milram/Lyttos/Bio Natura/Desira/Hofburger/
Cucina/FARM/Globetti); márka-slot felvéve a Tojás ágba is; íz-bővítés Joghurtnál
(narancsos/mézes/szilvás/gabonapelyhes/stracciatella), Krémtúrónál (mangós), Tejdesszertnél
(mogyorós); Sajt ízesítés←tejszínes/snidlinges/gyümölcsös/borsos, fajta←ömlesztett/egyéb/cheddar;
Szendvicskrém íz←snidlinges/kapros/csípős paprikás; Tejföl zsírtartalom←15%.

**4. kör (2037–2136):** sok sajt + hummusz + növényi krém + tojás. Új márkák
(Wonnemeyer/Goldland/Roi de Trefle/Tihany/Lyttos/Cucina/Cucina Nobile/Hajdú/Regione che vai/
BBQ/Meine Käsetheke/Tolle/Bonlà/Milli/MyVay); márka-slot a Növényi alternatíva ágba is.
Új fajták: feta/kecskesajt (Friss/lágy), maasdam/butterkäse/kecskesajt (Félkemény),
grana padano/gruyère (Kemény); új ízesítés: chilis/gombás/fűszeres/bazsalikomos/
paradicsomos-bazsalikomos; íz: Görög joghurt-slot felvéve, Túró Rudi←pisztáciás,
Gyümölcsös joghurt←maracuja/kiwis; hummusz íz←pesztós/paprikás/fenyőmagos/avokádós.
**Altipus-javítás:** #2042 „Krémfehér sajt" (Hirtenkäse=feta) → Friss/lágy sajt.
**Javítás:** Ömlesztett sajt fajta-listájába ömlesztett/egyéb (addig csak parenyica).

**HALADÁS (frissítendő minden kör után):** az `eredmeny.json` indexei közül a
**1700–2136** tartomány már TELJESEN kitöltve (kép-vizsgálva, márkával). A következő
feldolgozandó index: **2137**. Az 1700 alatti (0–1699) rekordok a GPT/verseny-korpusz, nem
ide tartoznak. (A pontos állást bármikor újraszámolja az `audit.py`.)

**Backlog (márka-slot miatt):** mivel a márka-tulajdonságot több tejtermék-ágba utólag
vettük fel, a korábbi (1700–1911) és a még feldolgozatlan (1987+) rekordok azokon az
ágakon márka nélkül maradtak → ezeket a soron következő körökben pótolni kell (6. pont).
