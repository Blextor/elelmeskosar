# Auchan hibás kategóriaoldalak vizsgálata

Vizsgálat időpontja: `2026-06-08`

## Rövid következtetés

Az Auchan hibák nem kategóriafa-, jogosultsági vagy rate limit problémának
tűnnek. Ugyanazzal az anon tokennel és delivery-area beállítással a hibás
oldalak közvetlen szomszédai `200 OK` választ adnak, miközben egy-egy konkrét
termékpozíció minden lekérdezésben `500` hibát okoz.

A legvalószínűbb ok: néhány termékrekordot az Auchan backend nem tud
összerakni vagy JSON-ná alakítani a terméklista válaszban. Ez szerveroldali
adat- vagy indexhiba.

## API-válasz

A hibás oldalak válasza egységes:

```json
{
  "message": "A művelet végrehajtása sikertelen!",
  "itemReferences": null,
  "constraintViolations": null,
  "debug": null,
  "scope": "api_general"
}
```

HTTP státusz: `500`

Content-Type: `application/problem+json; charset=utf-8`

Az API nem ad vissza termékazonosítót, vonalkódot vagy részletes hibát, ezért a
hibás rekord pontos azonosítója a lista végpontról nem olvasható ki.

## Érintett kategóriák

| Kategória | Termékszám | Hibás pozíció alap rendezéssel | Eredmény |
| --- | ---: | ---: | --- |
| `6243` Natúr és görög joghurt | 22 | 16 | 21 termék kérhető le |
| `6551` Zsírszegény, sovány túró | 3 | 1 | 2 termék kérhető le |
| `7269` Hűtött tejtermékek- joghurt, kefir, vaj | 48 | 40 | 47 listaelem kérhető le |

Szülőkategóriás fallback esetén ugyanazok a hibás rekordok más pozícióban
jelennek meg:

| Szülőkategória | Fallback for | Hibás pozíció |
| --- | --- | ---: |
| `5669` Joghurtok | `6243` | 52 |
| `5677` Túró, tejszín | `6551` | 9 |
| `5595` Laktózmentes termékek | `7269` | 70 |

Ez megerősíti, hogy a hiba nem a levélkategória ID-jából fakad: ugyanaz a
termékrekord a szülőkategória listájában is elhasal.

## Szomszédos termékek

### `6243` Natúr és görög joghurt

Alap rendezésnél:

- 15. oldal: Danone Activia élőflórás, krémes natúr joghurt 4 x 125 g
- 16. oldal: `500`
- 17. oldal: Real Nature 2% görög joghurt 1 kg

### `6551` Zsírszegény, sovány túró

Alap rendezésnél:

- 1. oldal: `500`
- 2. oldal: Nádudvari Fitness sovány túró 250 g
- 3. oldal: Nádudvari zsírszegény túró 250 g

A kategória filter-meta márkái: `Nádudvari`, `Real Nature`.
A lekérhető termékek csak `Nádudvari` márkájúak, ezért a kieső rekord nagy
valószínűséggel `Real Nature`.

### `7269` Hűtött tejtermékek- joghurt, kefir, vaj

Alap rendezésnél:

- 39. oldal: Riska laktózmentes élőflórás tejföl 20% 800 g
- 40. oldal: `500`
- 41. oldal: Magic Milk UHT laktózmentes főzőtejszín 20% 0,5 l

A kategória filter-meta márkái között szerepel `Real Nature`, de a lekérhető
`categoryId = 7269` termékek között nincs `Real Nature` márkájú termék. A
kieső rekord nagy valószínűséggel itt is `Real Nature`.

## Rendezéses ellenőrzés

Több rendezéssel is végig lett járva a három kategória:

- alap rendezés
- `name ASC`
- `name DESC`
- `price ASC`
- `price DESC`
- `unit_price ASC`
- `unit_price DESC`

Minden rendezésnél ugyanannyi elem hiányzott, csak a hibás rekord pozíciója
változott. Például a `6243` kategóriában:

| Rendezés | Hibás oldal |
| --- | ---: |
| alap | 16 |
| `name ASC` | 16 |
| `name DESC` | 4 |
| `price ASC` | 16 |
| `price DESC` | 4 |
| `unit_price ASC` | 19 |
| `unit_price DESC` | 1 |

A több rendezés uniója sem adott több terméket:

| Kategória | Elvárt termékszám | Több rendezés uniója |
| --- | ---: | ---: |
| `6243` | 22 | 21 |
| `6551` | 3 | 2 |
| `7269` | 48 | 47 |

Ez azt jelenti, hogy a hibás rekord önmagában okozza a szerverhibát, nem csak
egy adott rendezés vagy lapméret.

## Mit jelent ez a letöltőre nézve?

A jelenlegi Auchan letöltő helyes irányban kezeli ezt:

- nagy lapméretről kisebb lapméretre vált vissza,
- 1-es lapméretnél csak a konkrét hibás oldalt hagyja ki,
- szülőkategóriával is próbálkozik,
- a hibás oldalakat `auchan_failed_categories_*.csv` fájlban naplózza,
- a többi terméket nem dobja el.

Jelen állapotban a hibás rekordok teljes kinyerése a lista API-ból nem látszik
megoldhatónak. Érdemes ezeket későbbi futásokban újrapróbálni, mert ha az
Auchan javítja vagy újraindexeli az érintett termékeket, a mostani letöltő
automatikusan be fogja húzni őket.
