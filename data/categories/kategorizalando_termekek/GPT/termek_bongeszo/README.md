# Termék-böngésző

Egyszerű webes felület a kategorizált termékek böngészéséhez és szűréséhez.

## Indítás

```bash
cd data/categories/kategorizalando_termekek/GPT/termek_bongeszo
python server.py
```

Majd nyisd meg a böngészőben: **http://localhost:8765**

Másik port: `PORT=9000 python server.py`

Nincs külső függőség, csak Python 3 (stdlib).

## Mit tud

- **Kategória szerinti szűrés** — főkategória → alkategória → altípus legördülők (terméksZámmal).
- **Tulajdonság (fazetta) szűrés** — a bal oldali panelen a kiválasztott halmazban
  ténylegesen előforduló tulajdonságok és értékeik jelennek meg, darabszámmal.
  Egy tulajdonságon belül több érték is választható (VAGY kapcsolat),
  több tulajdonság között ÉS kapcsolat. Sok értékű tulajdonságnál (pl. márka)
  van helyben kereső.
- **Névre keresés** — a felső keresőmező (ékezet- és kisbetű-érzéketlen, részszó).
- **Rendezés** név vagy ár szerint, lapozással.
- Termékképek megjelenítése a repó `local_image_paths` mezője alapján.

## Adatforrás

- `../eredmeny.json` — a kategorizált termékek (47 030 db).
- A kategóriafa és a fazetták magából a termékhalmazból épülnek, így mindig csak
  olyan szűrő jelenik meg, amihez van termék.

A szűrés és lapozás szerveroldalon történik, ezért a 41 MB-os JSON nem kerül
a böngészőbe — a felület nagy adathalmazon is gyors marad.
