# Kedvezmények és promóciók

## Cél

A boltok akcióit nem érdemes csak a terméksorban tárolni, mert egy termékhez
több, eltérő szabályú kedvezmény is tartozhat. A termékajánlatban elég egy
rövid hivatkozás, a részletes szabály pedig külön promóciós táblába kerül.

## Kimenetek

`promotions_*.csv`: részletes promóciós tábla.

Fontosabb mezők:

- `promotion_id`: egyedi promóciósor-azonosító.
- `promotion_group_id`: összetartozó promóciósorok csoportja, például Metro
  mennyiségi ársávoknál.
- `store_name`, `store_product_id`, `product_name`: bolti ajánlat kapcsolása.
- `promotion_type`: normalizált kedvezménytípus.
- `required_program`: szükséges hűségprogram, például `tesco_clubcard`.
- `original_price`, `discounted_price`, `discount_percent`, `discount_amount`:
  árengedmény paraméterei.
- `min_quantity`, `buy_quantity`, `get_quantity`, `bundle_quantity`,
  `bundle_price`: darabszámhoz kötött kedvezmények paraméterei.
- `tier_quantity`, `tier_gross_price`, `tier_base_unit_price`,
  `tier_base_unit`: mennyiségi ársáv paraméterei.
- `promotion_params`: a nem üres numerikus és egységparaméterek kompakt JSON
  formában.
- `raw_data`: az eredeti bolti promóciós adat visszakereséshez.

`offers_with_promotions_*.csv`: a legfrissebb normalizált bolti ajánlatok
kiegészítve promócióhivatkozásokkal.

Új mezők:

- `has_promotion`: van-e promóciós hivatkozás.
- `promotion_count`: hány promóciósor kapcsolódik az ajánlathoz.
- `promotion_ids`: pontos promóciósorok azonosítói.
- `promotion_types`: az ajánlaton előforduló kedvezménytípusok.
- `promotion_required_programs`: szükséges hűségprogramok listája.

## Kedvezménytípusok

- `price_cut`: egyszerű aktuális ár és eredeti ár különbség.
- `percentage_discount`: százalékos kedvezmény.
- `amount_off`: fix forint kedvezmény.
- `loyalty_price_cut`: hűségprogramhoz kötött kedvezményes ár.
- `loyalty_percentage_discount`: hűségprogramhoz kötött százalékos kedvezmény.
- `loyalty_amount_off`: hűségprogramhoz kötött fix kedvezmény.
- `loyalty_quantity_discount`: hűségprogramhoz és darabszámhoz kötött
  kedvezmény.
- `loyalty_offer`: hűségprogramos ajánlat, ahol a forrásból még nem nyerhető ki
  biztosan minden árparaméter.
- `quantity_discount`: darabszámhoz kötött általános kedvezmény.
- `bundle_price`: adott darabszám együtt adott áron.
- `x_pay_y_get`: „X-et fizet, Y-t kap” típusú ajánlat.
- `quantity_price_tier`: mennyiségi ársáv, például Metro esetén több darabtól
  eltérő Ft/kg vagy Ft/db ár.
- `store_promotion`: bolti promóció jelölés, ahol nincs elég strukturált
  árparaméter.
- `unknown_promotion`: feldolgozott, de még nem besorolható promóció.

## Források

- Tesco: `tesco_filtered_data_*.csv` `promotions` mező. A Clubcard ajánlatok
  `required_program = tesco_clubcard` jelölést kapnak.
- Auchan: `auchan_filtered_data_*.csv` árengedmény, offline promóció és
  hűségár mezők.
- Metro: `metro_price_tiers_*.csv` mennyiségi ársávok.
- SPAR, Príma és egyéb boltok: a normalizált `is_discounted` és
  `original_unit_price` mezők alapján egyszerű `price_cut`, ha nincs gazdagabb
  promóciós forrás.

## Futtatás

```powershell
python src\markets\build_promotions.py
```

Csak a részletes promóciós tábla elkészítése:

```powershell
python src\markets\build_promotions.py --skip-offers
```
