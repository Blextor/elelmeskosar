# LLM-alapú tömeges termékkategorizáló

A `kategorizalatlan_termekek.csv` backlog (~47 000 termék) gépi besorolása a
`kategoriak_2026-06-13.json` fa ellen, az Anthropic API-val. A kimenet
`eredmeny.json`-kompatibilis (`termek` + `fokategoria`/`alkategoria`/`altipus`/
`tulajdonsagok`/`kategoria_hash`/`statusz`), a hash **bitre** a `kat25.py` képletével.

## Miért hatékony

1. **Routing (ingyen):** minden termék előbb EGY főkategóriára kerül szabályalapon
   (bolti út + név token-egyezés). Így nem a teljes ~90k tokenes fát küldjük be,
   hanem **csak az adott ág részfáját**. Az LLM `fo_override`-ral felülbírálhat.
2. **Prompt caching:** az ág részfája cache-elt prefix → a 2.+ kérésnél ~0,1× ár.
3. **Batches API:** kötegelt feldolgozás **−50%** minden tokenen.
4. **Structured output:** az `alkategoria` ENUM-mal kötött a fa ágához.
5. **Determinisztikus utóvalidáció:** minden LLM-kimenetet a fa ellen ellenőrzünk
   (út + érték-listák), a tulajdonság-értékeket a megengedettre szűrjük, a hash-t
   újraszámoljuk. Ami nem fér be / `confidence=alacsony` → `review.json`.

## Modell és effort

| Réteg | Modell | Effort |
|---|---|---|
| Tömeg (bolti út döntő) | `claude-haiku-4-5` | – (Haiku nem fogad el effortot) |
| Fő réteg (alapértelmezett) | `claude-sonnet-4-6` | `medium` |
| Nehéz farok / képes eset | `claude-opus-4-8` | `high` |

Mind a `--model` és `--effort` kapcsolóval állítható.

## Használat

```bash
# 0) Függőség + kulcs
pip install anthropic
export ANTHROPIC_API_KEY=...    # Windows PowerShell: $env:ANTHROPIC_API_KEY="..."

# 1) Ingyenes ellenőrzés: routing-eloszlás (nem hív API-t)
python src/categories/llm_kategorizalo/pipeline.py route-stats --limit 3000

# 2) Élő próbafutás kis mintán (látja a tényleges besorolásokat)
python src/categories/llm_kategorizalo/pipeline.py sync --limit 20
#   + termékképpel:    ... sync --limit 20 --image
#   + más modell:      ... sync --limit 20 --model claude-haiku-4-5

# 3) Teljes köteg beküldése (Batches API)
python src/categories/llm_kategorizalo/pipeline.py batch-submit

# 4) Elkészült kötegek begyűjtése + validáció + eredmeny írás
python src/categories/llm_kategorizalo/pipeline.py batch-collect
```

Minden kimenet az `out/` almappába kerül; kézi adatot SOHA nem ír felül.

## Kimenetek (`out/`)

- `eredmeny_llm.json` – a kész, validált rekordok (eredmeny.json-kompatibilis).
- `review.json` – kétséges / `alacsony` magabiztosságú / ismeretlen alkategória.
- `masik_agba.json` – amit a modell `fo_override`-ral másik főkategóriába tett
  (a routing tévedett); futtasd rájuk újra a megfelelő ággal.
- `batch_ids.json`, `batch_routing_index.json` – a köteg-állapot (collect olvassa).
- `hibak.json` – sikertelen kérések (ha volt).

## Ajánlott munkamenet

1. `route-stats` → ránézés, jó-e az ágeloszlás.
2. `sync --limit 30` Sonnettel → minőség-ellenőrzés kézzel.
3. Ha jó: `batch-submit` (akár `--model claude-haiku-4-5` az olcsó tömegre),
   majd `batch-collect`.
4. `masik_agba.json` újrafuttatása; `review.json` kézi átnézése (3. fázis).
5. Az `eredmeny_llm.json` beolvasztása a fő `eredmeny.json`-ba (külön lépés,
   a validátor garantálja az út-/érték-/hash-helyességet).

## Megjegyzések

- A `--limit` minden parancsnál az első N termékre szűkít (próbához).
- A routing tévedéseit a `fo_override` + a validáció felfogja; a fa bővítése
  (ha egy érték hiányzik) a 2026-06-15 szabály szerint külön, kézi lépés marad.
- A szkript a `kategoriak_2026-06-13.json` és a `kategorizalatlan_termekek.csv`
  Claude_Opus-mappabeli példányát használja (a versenykörnyezeted szerint).
