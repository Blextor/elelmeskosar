# Mestertermékek és bolti ajánlatok

## Cél

A SPAR, Príma és Tesco letöltésekből egy olyan közös terméktáblát kell építeni,
ahol ugyanaz a termék csak egyszer szerepel. Ehhez külön kell választani a
termékazonosságot és a bolti ajánlatot:

- `master_products`: egyedi, boltfüggetlen termékek.
- `master_offers`: bolti előfordulások, árak, elérhetőség, kiszerelés és bolti
  azonosítók.

Így egy termékhez több bolti ajánlat tartozhat, és boltonként látható marad,
hogy mennyiért, milyen kiszerelésben és milyen forrásazonosítóval jelent meg.

## Javasolt mester tábla

`master_products`:

- `master_product_id`: belső, stabil mesterazonosító.
- `canonical_name`: emberileg olvasható fő név.
- `representative_name`: a kiválasztott forrásnév változtatás nélkül.
- `primary_barcode`: leggyakoribb normalizált vonalkód.
- `barcodes`: a csoportban látott vonalkódok.
- `representative_image_url`: első használható termékkép.
- `image_keys`: normalizált képlink-kulcsok.
- `stores_count`: hány boltban jelent meg.
- `stores`: boltok felsorolása.
- `offers_count`: hány bolti sor tartozik hozzá.
- `match_methods`: milyen szabályok kötötték össze a sorokat.
- `needs_review`: kézi vagy szabályalapú ellenőrzést igényel-e.
- `review_reason`: miért gyanús a csoport.

`master_offers`:

- `master_product_id`: hivatkozás a mestertermékre.
- `store_name`: bolt neve.
- `store_product_id`: bolti termékazonosító.
- `product_name`: bolti terméknév.
- `brand_name`: márka, ha van.
- `barcode`: eredeti vonalkód.
- `barcode_norm`: vezető nullák nélküli vonalkódkulcs.
- `unit_price`: bolti darab/csomag ár.
- `unit_type`: normalizált kiszerelési egység (`g`, `ml`, `db`).
- `unit_step`: normalizált kiszerelési mennyiség.
- `base_price`: összehasonlítható alapár (`Ft/kg`, `Ft/l`, `Ft/db`).
- `base_unit`: alapár egysége (`kg`, `l`, `db`).
- `available`: elérhetőség.
- `is_discounted`: akciós jelölés.
- `original_unit_price`: eredeti ár akció esetén.
- `image_urls`: forrás képlinkek.
- `image_key`: normalizált első képkulcs.
- `categories`: bolti kategóriaút.
- `name_key`: normalizált teljes név.
- `name_core`: kiszerelési részek nélküli gyengébb névkulcs.

## Párosítási jelek

A párosítás nem egyetlen mezőre támaszkodik, hanem több jelből épít gráfot. A
termékek akkor kerülnek egy mestertermékbe, ha legalább egy erős vagy több
összhangban lévő gyengébb jel összeköti őket.

Erős jelek:

- Azonos normalizált vonalkód. A vezető nullákat levágjuk, mert a Tesco sok
  GTIN-t 14 jegyűre egészít ki.
- Azonos képkulcs, ha a név is kellően hasonló.
- Azonos normalizált teljes név különböző boltok között.

Gyengébb jel:

- Azonos `name_core`, vagyis a kiszereléstől megtisztított név. Ezt csak akkor
  érdemes automatikusan összevonni, ha a kiszerelési egység és mennyiség is
  kompatibilis. Így a `125 g` és a `4 x 125 g` jellegű termékek nem olvadnak
  össze vakon.

## Ellenőrzést igénylő esetek

A mestertermék-képzés után külön listába kell tenni a gyanús csoportokat:

- több eltérő vonalkód ugyanabban a mestertermékben;
- ugyanazon boltból több ajánlat került ugyanabba a mestertermékbe;
- nagy névváltozatosság;
- azonos vonalkód mellett eltérő kiszerelés;
- azonos név mellett eltérő kiszerelés;
- azonos kép mellett eltérő vonalkód.

Ezek nem feltétlenül hibák. Sokszor a forrásadatban van bruttó/nettó tömeg,
lecsöpögtetett tömeg, multipack vagy címhiba, de összehasonlítás előtt jelölni
kell őket.

## Tesco kiszerelési sorrend

A Tesco esetén a névben lévő kiszerelés csak végső tartalék legyen. Ha a Tesco
értelmesen küldi a strukturált adatot, azt kell használni:

1. `catchWeightList`: lédig vagy változó súlyú termékek kosárba tehető lépése.
2. `details.packSize`: a részletes termék API strukturált kiszerelése.
3. `details.netContents`, `details.drainedWeight`, `details.boxContents`:
   szöveges, de részletes termékadatból származó mennyiségek.
4. `price.actual / price.unitPrice`: visszaszámolt kiszerelés, ha az egységár
   megbízható.
5. Terméknév parser: csak végső fallback.

Ez javítja az olyan eseteket, ahol a Tesco címében elcsúszik a tizedes vagy
hiányzik egy nulla, például `40 g` a valós `400 g` helyett.

## Következő lépések

- A teljes Tesco letöltést újra kell futtatni részletes termékadat gazdagítással.
- A SPAR és Príma multipack parserét javítani kell, különösen a `6 x 51 g
  (306 g)` és `10 x 9 db` típusú termékeknél.
- A mestertermék script `review_candidates.csv` listáját kézzel vagy további
  szabályokkal át kell nézni.
- Később a képlink helyett érdemes valódi kép-hasht használni, mert boltok
  között ugyanaz a termék gyakran más CDN URL-en jelenik meg.
