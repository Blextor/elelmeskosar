# Ital kategóriafa átalakítása – 2026-07-23

## Eredmény

- Ital-termékek: **12876 → 12810**
- Használt Ital-útvonalak: **89 → 41**
- Második szintű Ital-kategóriák: **18 → 8**
- Minden Ital-termék név szerinti harmadik szintű levélen van.
- A szénsavasság, alkoholstátusz, sör-/bor-/teatípus, célcsoport és növényi alap tulajdonságként marad meg.
- A kategóriafa, a termékutak, az értékalakok, az engedélyezett értékek és a termékhash-ek paritása ellenőrzött.

## Új kategóriafa

- **Víz és vízalapú italok**
  - Ízesítetlen palackozott víz: 420
  - Ízesített víz: 93
- **Alkoholos italok és alkoholmentes alternatívák**
  - Bor és boralapú ital: 2128
  - Pezsgő, habzóbor és gyöngyözőbor: 560
  - Sör, radler és malátaital: 1015
  - Cider: 73
  - Likőr: 601
  - Whisky és bourbon: 241
  - Gin: 135
  - Rum: 120
  - Tequila: 21
  - Vodka: 188
  - Pálinka: 133
  - Brandy: 41
  - Vermut és aperitif: 33
  - Egyéb szeszes ital: 86
  - Koktél és előre kevert ital: 125
- **Üdítőitalok**
  - Kóla: 349
  - Tonik: 87
  - Jegestea: 482
  - Limonádé: 93
  - Aloe vera ital: 21
  - Gyömbér- és gyökéralapú üdítőital: 57
  - Kombucha: 17
  - Egyéb ízesített üdítőital: 689
- **Gyümölcs- és zöldségitalok**
  - Lé: 463
  - Nektár: 81
  - Gyümölcsital: 765
  - Smoothie és püréital: 86
- **Funkcionális és teljesítményitalok**
  - Energiaital: 341
  - Sport- és izotóniás ital: 86
  - Vitamin- és wellnessital: 155
  - Egyéb funkcionális ital: 147
- **Növényi italok**
  - Egynövényes ital: 200
  - Kevert növényi ital: 31
- **Kávé-, tea- és kakaótermékek**
  - Kávé: 1301
  - Tea: 760
  - Kakaó és forró csokoládé: 138
  - Kávé- és teaadalék: 24
- **Italkészítési alapok**
  - Italszirup és folyékony koncentrátum: 395
  - Italpor és tabletta: 29

## Kikerült hibás vagy nem italjellegű termékek

- 65 citruslé/citrusízesítő → `Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Citruslé és citrusízesítő`
- Nesquik kakaós szirup (`209545089`) → `Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Desszertszósz, topping`

## Ellenőrzés

- Belső candidate-validáció: `ok`
- Független ellenőrző: `ok`
- Forrásút-lefedés: `89/89`
- Futtatás módja: `source-migration`
- Utólagos idempotenciakorrekció: 37, név szerint „enyhén szénsavas” Apenta-termék
  szénsavassága `szénsavas` helyett `enyhén szénsavas`; ismételt száraz futásban
  elvárt változás: **0 termék**.

## Automatikusan feloldott ellentmondások

Összesen 175 eset. A teljes lista a gépi audit JSON-ban található.
