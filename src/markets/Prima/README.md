# Prima

Prima termekadatok lekeresenek, szuresenek es normalizalasanak mappaja.

## Szerepe

Ez a pipeline a Wolt Consumer API-n keresztul tolti le az Online Prima Expressz
Corvin termekeit, a SPAR adatfolyammal azonos haromlepcsos felosztasban:

1. `get_all_data_prima.py`: indulasnal frissiti a Wolt aktualis kategoriafajat,
   majd kategorialapuan letolti a termekeket.
2. `filter_data_prima.py`: eltavolitja a nem hasznalt oszlopokat.
3. `normalize_data_prima.py`: egyseges termeksemara alakitja az adatokat.

## Alapertelmezett Wolt venue

- Webes URL: `https://wolt.com/hu/hun/budapest/venue/online-prima-expressz-corvin`
- Venue slug: `online-prima-expressz-corvin`

Masik Prima/Wolt venue futtatasahoz hasznalhato:

```powershell
python get_all_data_prima.py --venue-slug masik-venue-slug
```

Vagy kornyezeti valtozoval:

```powershell
$env:PRIMA_VENUE_SLUG = "masik-venue-slug"
python main_prima.py
```

## Kimenetek

A scriptek mappanev alapjan generalnak fajlnevet, ezert ebbol a mappabol futtatva
a kimenetek a `data/markets_data/` mappaba kerulnek:

- `prima_categories_*.csv`
- `prima_all_data_*.csv`
- `prima_filtered_data_*.csv`
- `prima_normalized_data_*.csv`

## Hasznos opciok

- `python get_all_data_prima.py --refresh-categories-only`: csak a kategoriakat
  frissiti.
- `python get_all_data_prima.py --no-category-refresh`: explicit modon a helyi
  `kategoriak.txt` alapjan tolt le.
- `python get_all_data_prima.py --allow-stale-categories`: ha a
  kategoriafrissites hibazik, engedi a helyi kategoriafajl hasznalatat.
- `python get_all_data_prima.py --allow-partial-download`: engedi, hogy nehany
  sikertelen kategoria mellett is keszuljon `all_data` CSV.
- `python get_all_data_prima.py --category-delay 1.0`: lassitja a kategoriak
  kozti lekerdezest, ha a Wolt 429 rate limitet ad.

Alapertelmezett teljes futasnal friss kategoriafa szukseges, es sikertelen
kategorialekeres eseten a script nem ir hianyos `all_data` fajlt. A Prima
letolto a SPAR-hoz kepest ovatosabb alapbeallitast hasznal: 5 retry, 3 masodperc
alap retry-delay es 0.5 masodperc kategoria-delay.
