# Metro

Metro saját webes adatfolyam a `termekek.metro.hu` termékkatalógushoz.

## Szerepe

Ez a mappa a Metro élelmiszer kategóriájának termékadatait tölti le, szűri és
alakítja át a többi bolt által is használt közös `*_normalized_data_*.csv`
sémára.

## Fontos eltérések

- A megadott Metro oldal már az élelmiszer gyökérkategória:
  `https://termekek.metro.hu/shop/category/%C3%A9lelmiszer`.
- A Metro kereső API a gyökér `category:élelmiszer` listán kb. 3000 találat után
  400-as hibát ad, ezért a teljes letöltő alapból az élelmiszer ág
  levélkategóriáin megy végig, majd termékazonosító alapján deduplikál.
- A terméklista kétlépcsős:
  1. `/searchdiscover/articlesearch/search`: termékazonosítók, találati sorrend,
     elérhetőség és keresőár.
  2. `/evaluate.article.v1/betty-variants`: a termékek részletes adatai,
     kategóriái, képei, vonalkódjai, csomagolása és árai.
- A kategóriafa a `/searchdiscover/articlesearch/mainCategories` végpontról
  jön, ebből csak az `élelmiszer` ág kerül a `kategoriak.txt` fájlba.
- Az alap áruház a Metro HU frontend konfigurációja szerinti `00010`.

## Kiszerelés és ár

A normalizáló elsődlegesen a Metro strukturált mezőire támaszkodik:

1. `bundle.basePriceContent` és `bundle.basePriceContentMeasureUnit`.
2. `bundle.contentData.netPieceWeight`.
3. `bundle.weightPerPiece`.
4. Terméknév parser csak tartalék.

Térfogati termékeknél a Metro base-price tartalom az elsődleges, mert a
`netPieceWeight` sok italnál csak tömeget adna vissza. Néhány grammos terméknél
a Metro `GR` + törtérték formában küldi a base mezőt, ilyenkor a normalizáló a
megbízhatóbb `contentData.netPieceWeight` értékre vált.

Az `unit_price` mezőbe a termék bruttó ára kerül. Ha a Metro külön
visszaváltási vagy göngyöleg díjat küld az `emptiesGross` mezőben, az a közös
séma `secondary_unit_price` mezőjébe kerül, hogy ne torzítsa az alap
ár-összehasonlítást.

Ha a Metro mennyiségi kedvezményt küld (`isBuyMorePayLessArticle`,
`price.summaryDnrInfo`), a normalizált fájl `unit_price` mezője továbbra is az
alap, egy egységre vonatkozó bruttó ár marad. A mennyiségi ársávok külön
`metro_price_tiers_*.csv` fájlba kerülnek, mert egy termékhez több érvényes ár
tartozhat a vásárolt mennyiségtől függően.

Az ársávos fájlban a `tier_final_gross_price` az adott mennyiségi sávban
érvényes bruttó termékár, a `product_unit_step` és `product_unit_type` pedig a
normalizált kiszerelés. Összehasonlítható egységárat ezekből érdemes számolni.
A Metro saját `tier_base_unit_price` mezője megmarad ellenőrzésre, de nem ez az
elsődleges összehasonlítási alap.

Fontos: a Metro részletes API-válaszában az EAN/GTIN mezők jelen vannak, de a
mostani lekérdezésekben üresek. A vonalkódot ezért a PDF-es termékadatlapokból
érdemes pótolni, ha pontos termékpárosításra is szükség van.

## PDF-es termékadatlapok

A Metro termékoldalai több élelmiszernél FIR PDF-adatlapra hivatkoznak. Ezekben
megtalálható lehet a GTIN/EAN vonalkód, az összetevőlista, a tápérték, a
tárolási információ, a jogi terméknév és a felelős vállalkozás adata.

A PDF-link a letöltött termékadatok `bundle.displayId` mezőjéből építhető:

```text
https://cdn.metro-group.com/hu/hu_fir_{bundle.displayId}_hu.pdf
```

Ezt a `get_product_facts_metro.py` dolgozza fel. A szkript a legfrissebb
`metro_filtered_data_*.csv` fájlból indul, letölti vagy cache-ből olvassa a
PDF-eket, majd `metro_product_facts_*.csv` fájlba írja a kinyert adatokat. A PDF
fájlok a `data/markets_data/metro_product_facts_pdfs/` mappába kerülnek, így egy
megszakított vagy ismételt futásnál nem kell mindent újra letölteni.

A normalizáló a legfrissebb `metro_product_facts_*.csv` fájlt automatikusan
beolvassa, és ha a Metro API saját EAN/GTIN mezője üres, akkor ebből pótolja a
`barcode` mezőt.

## Fájlok

- `main_metro.py`: a teljes Metro folyamat belépési pontja.
- `get_all_data_metro.py`: kategóriafa, keresőtalálatok és részletes termékadatok
  letöltése.
- `filter_data_metro.py`: a nyers Metro CSV fontosabb oszlopainak megtartása.
- `get_product_facts_metro.py`: Metro FIR PDF-adatlapok letöltése és a vonalkód,
  összetevők, tápértékek, tárolási adatok kinyerése.
- `normalize_data_metro.py`: Metro mezők átalakítása a közös 18 oszlopos
  `*_normalized_data_*.csv` sémára.
- `kategoriak.txt`: a legutóbb felfedezett Metro élelmiszer kategóriafa.

## Kimenetek

A szkriptek a `data/markets_data/` mappába írnak:

- `metro_categories_*.csv`: friss Metro élelmiszer kategóriafa.
- `metro_all_data_*.csv`: nyers, részletezett Metro termékadatok.
- `metro_failed_requests_*.csv`: sikertelen keresőoldalak vagy részlet batch-ek.
- `metro_filtered_data_*.csv`: lényegesebb nyers oszlopokra szűkített CSV.
- `metro_product_facts_*.csv`: PDF-adatlapokból kinyert vonalkód, összetevő,
  tápérték és további termékinformáció.
- `metro_normalized_data_*.csv`: SPAR/Príma/Tesco/Auchan azonos kimeneti séma.
- `metro_price_tiers_*.csv`: Metro mennyiségi kedvezményes ársávok, ha az adott
  letöltés tartalmaz `price.summaryDnrInfo` adatot.

## Futtatás

```powershell
cd src\markets\Metro
python main_metro.py
```

Gyors próba:

```powershell
python get_all_data_metro.py --category-limit 3 --page-limit 1 --max-detail-ids 25 --allow-partial-download
python filter_data_metro.py
python normalize_data_metro.py
```

Teljes élelmiszer letöltés részletes haladással:

```powershell
python get_all_data_metro.py --allow-partial-download --rows 500 --detail-batch-size 25
python filter_data_metro.py
python normalize_data_metro.py
```

Egy konkrét termék PDF-adatlapjának feldolgozása:

```powershell
python get_product_facts_metro.py --product-id BTY-X13888900320021 --allow-partial-download
python normalize_data_metro.py
```

Teljes PDF-adatlap feldolgozás a legfrissebb szűrt Metro terméklistára:

```powershell
python get_product_facts_metro.py --allow-partial-download --delay 0.1
python normalize_data_metro.py
```

Ez a lépés várhatóan jóval lassabb, mint az alap terméklista letöltése, mert
termékenként külön PDF-et kér le. Ezért nincs bekötve a `main_metro.py` alap
folyamatába; akkor érdemes futtatni, amikor a vonalkód, összetevő vagy tápérték
adatokra is szükség van.
