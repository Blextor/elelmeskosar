# -*- coding: utf-8 -*-
"""Eldobható kötegfuttató – kézi tételenkénti döntések alkalmazása + validáció + mentés."""
import sys, os, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P

ERED = 'data/categories/kategorizalando_termekek/Claude_Opus/eredmeny.json'
tree = P.load_tree()
ered = json.load(open(ERED, encoding='utf-8'))
dk = {f"{r['termek'].get('store_name','')}|{r['termek'].get('store_product_id','')}" for r in ered}
full = list(csv.DictReader(open(P.BACKLOG_CSV, encoding='utf-8')))
undone = [{c: r.get(c, '') for c in P.TERMEK_COLS} for r in full
          if f"{r['store_name']}|{r['store_product_id']}" not in dk]

GY = 'Gyümölcs'; Z = 'Zöldség'; T = 'Tejtermékek és tojás'
ED = 'Édesség, snack, rágcsálnivaló'; RM = 'Rágcsálnivaló magvak (snack)'
AL = 'Alapanyag, sütés-főzés'; OM2 = 'Olajos magvak, aszalt gyümölcs (natúr, sütéshez-főzéshez)'
KZ = 'Konzerv, savanyúság, befőtt'; SZK = 'Szószok, öntetek, dresszingek'; HUMM = 'Szendvicskrém, hummusz, kenőkrém'
HUS = 'Hús, hal, felvágott'; NHP = 'Növényi húspótló'; NA = 'Növényi alternatíva'
CSAL = 'Csomagolt saláta, salátatál'; TOK = 'Tökféle, cukkini, padlizsán'; EGYZ = 'Egyéb zöldség'
GR = 'Grillsajt / halloumi / sütnivaló'; EGYG = 'Egyéb gyümölcs'

# --- fa-bővítés ---
def add_alk(fo, nev):
    tree[fo]['alkategóriák'].setdefault(nev, {'tulajdonságok': {'egyedi': {}, 'csoportos': {}}, 'altípusok': {}})
for nev in ['Sárgabarack', 'Őszibarack, nektarin', 'Cseresznye']:
    add_alk(GY, nev)
add_alk(Z, 'Spárga')
omarka = tree[AL]['alkategóriák'][OM2]['tulajdonságok']['egyedi'].setdefault('márka', [])
for m in ['Back Family', 'Happy Harvest']:
    if m not in omarka:
        omarka.insert(omarka.index('egyéb') if 'egyéb' in omarka else len(omarka), m)

OBA = 'Olívabogyó, kapribogyó, eltett zöldség'; KOK = 'Kókusztej, kókuszkrém, főzőalap'
HH = 'Happy Harvest'
D = [
 (0, AL, KZ, OBA, {'alapanyag': ['pfefferoni']}),
 (1, AL, KZ, OBA, {'alapanyag': ['pfefferoni']}),
 (2, AL, KZ, OBA, {'alapanyag': ['pfefferoni']}),
 (3, AL, KZ, KOK, {'márka': 'Asia Green Garden', 'alapanyag': ['kókusz']}),
 (4, AL, SZK, HUMM, {'vegán': True, 'íz': ['natúr']}),
 (5, AL, SZK, HUMM, {'vegán': True, 'íz': ['egyéb']}),
 (6, AL, SZK, HUMM, {'vegán': True, 'íz': ['egyéb']}),
 (7, T, NA, 'Növényi ital', {'vegán': True, 'terméktípus': ['növényi ital'], 'alap': ['zab']}),
 (8, AL, SZK, HUMM, {'vegán': True, 'alap': ['hummusz'], 'íz': ['egyéb']}),
 (9, AL, SZK, HUMM, {'vegán': True, 'alap': ['hummusz'], 'íz': ['egyéb']}),
 (10, AL, SZK, HUMM, {'vegán': True, 'alap': ['hummusz'], 'íz': ['egyéb']}),
 (11, HUS, NHP, 'Növényi virsli/kolbász', {'vegán': True, 'forma': ['virsli']}),
 (12, T, NA, 'Növényi főzőkrém / tejszín', {'vegán': True, 'terméktípus': ['habkrém']}),
 (13, HUS, NHP, 'Növényi falat/burger', {'vegán': True, 'forma': ['falat']}),
 (14, HUS, NHP, 'Növényi falat/burger', {'vegán': True, 'forma': ['falat']}),
 (15, HUS, NHP, 'Növényi falat/burger', {'vegán': True, 'forma': ['burger']}),
 (16, Z, 'Paradicsom', '', {'fajta': 'Koktél', 'fürtös': True}),
 (17, GY, 'Görögdinnye', '', {'kiszerelés': 'lédig'}),
 (18, Z, TOK, '', {}),
 (19, Z, 'Paprika', '', {'fajta': 'TV'}),
 (20, GY, 'Málna', '', {}),
 (21, ED, RM, 'Magkeverék (sós)', {'márka': HH, 'magfajta': ['magkeverék']}),
 (22, AL, OM2, 'Dió, mandula, mogyoró (sütőmag)', {'márka': 'Bella', 'fajta': ['mandula'], 'forma': ['egész']}),
 (23, Z, 'Burgonya', '', {'fajta': 'Étkezési', 'színe': 'Sárga', 'kiszerelés': 'lédig'}),
 (24, Z, 'Hagymafélék', '', {'fajta': 'Fokhagyma'}),
 (25, ED, RM, 'Aszalt gyümölcs (snack)', {'márka': HH}),
 (26, ED, RM, 'Olajos magvak (snack)', {'márka': 'Snack Fun', 'sózott': True, 'pörkölt': True, 'héj nélküli': True, 'magfajta': ['napraforgómag'], 'ízesítés': ['sós']}),
 (27, Z, 'Burgonya', '', {'fajta': 'Étkezési', 'kiszerelés': '2 kg'}),
 (28, Z, CSAL, '', {'saláta alap': ['salátakeverék']}),
 (29, Z, CSAL, '', {'saláta alap': ['salátakeverék']}),
 (30, AL, OM2, 'Reszelt kókusz, mák', {'márka': 'Back Family', 'fajta': ['mák'], 'forma': ['darált']}),
 (31, Z, 'Burgonya', '', {'fajta': 'Étkezési', 'színe': 'Sárga', 'kiszerelés': '2 kg'}),
 (32, ED, RM, 'Aszalt gyümölcs (snack)', {'márka': HH}),
 (33, AL, OM2, 'Mag- és gyümölcskeverék', {'márka': HH, 'fajta': ['egyéb'], 'forma': ['egész']}),
 (34, ED, RM, 'Aszalt gyümölcs (snack)', {'márka': HH}),
 (35, ED, RM, 'Aszalt gyümölcs (snack)', {'márka': HH}),
 (36, AL, OM2, 'Aszalt gyümölcs', {'márka': 'Back Family', 'fajta': ['mazsola'], 'forma': ['egész']}),
 (37, ED, RM, 'Olajos magvak (snack)', {'márka': HH, 'magfajta': ['dió']}),
 (38, ED, RM, 'Olajos magvak (snack)', {'márka': HH, 'magfajta': ['egyéb']}),
 (39, ED, RM, 'Olajos magvak (snack)', {'márka': HH, 'pörkölt': True, 'magfajta': ['kesudió']}),
 (40, ED, RM, 'Aszalt gyümölcs (snack)', {'márka': HH}),
 (41, Z, 'Paprika', '', {'erős, csípős': True, 'fajta': 'Sima'}),
 (42, Z, 'Hagymafélék', '', {'fajta': 'Fokhagyma'}),
 (43, Z, 'Káposzta', '', {'fajta': 'Fejeskáposzta'}),
 (44, Z, 'Hagymafélék', '', {'fajta': 'Vöröshagyma'}),
 (45, Z, 'Hagymafélék', '', {'fajta': 'Vöröshagyma', 'kiszerelés': '1 kg'}),
 (46, GY, 'Kiwi', '', {}),
 (47, Z, 'Káposzta', '', {'fajta': 'Fejeskáposzta'}),
 (48, GY, 'Alma', '', {'színe': ['piros']}),
 (49, Z, 'Uborka', '', {'fajta': 'Kígyúuborka'}),
 (50, Z, 'Hagymafélék', '', {'fajta': 'Lilahagyma'}),
 (51, Z, 'Hagymafélék', '', {'fajta': 'Újhagyma', 'kiszerelés': 'csomós'}),
 (52, Z, 'Karalábé', '', {}),
 (53, Z, 'Retekfélék', '', {'kiszerelés': 'csomós'}),
 (54, GY, 'Alma', '', {'típus': 'Golden', 'színe': ['sárga']}),
 (55, Z, 'Friss fűszernövény', '', {}),
 (56, Z, 'Paradicsom', '', {'fürtös': True}),
 (57, GY, 'Alma', '', {'típus': 'Jonagold'}),
 (58, GY, 'Alma', '', {'típus': 'Idared'}),
 (59, GY, 'Alma', '', {'típus': 'Gála'}),
 (60, Z, 'Retekfélék', '', {}),
 (61, Z, 'Salátafélék', '', {'fajta': 'Fejes'}),
 (62, Z, 'Paradicsom', '', {'fürtös': True}),
 (63, Z, 'Hagymafélék', '', {'fajta': 'Lilahagyma'}),
 (64, Z, 'Uborka', '', {'fajta': 'Kígyúuborka', 'bio': True}),
 (65, GY, 'Alma', '', {}),
 (66, GY, 'Körte', '', {}),
 (67, Z, 'Paradicsom', '', {'fajta': 'Koktél'}),
 (68, GY, 'Körte', '', {'típus': 'Conference'}),
 (69, Z, 'Paradicsom', '', {'fajta': 'Cherry', 'fürtös': True}),
 (70, Z, 'Sárgarépa', '', {'kiszerelés': '1 kg'}),
 (71, Z, 'Salátafélék', '', {'fajta': 'Római'}),
 (72, GY, 'Avokádó', '', {}),
 (73, Z, 'Zeller', '', {}),
 (74, Z, 'Sárgarépa', '', {}),
 (75, Z, 'Brokkoli', '', {}),
 (76, Z, 'Retekfélék', '', {}),
 (77, Z, 'Sárgarépa', '', {'kiszerelés': 'csomós'}),
 (78, Z, 'Zeller', '', {}),
 (79, Z, CSAL, '', {'saláta alap': ['rucola']}),
 (80, Z, 'Paradicsom', '', {'fajta': 'Koktél', 'fürtös': True}),
 (81, GY, 'Szőlő', '', {'magnélküli': True, 'színe': 'fehér'}),
 (82, Z, 'Friss fűszernövény', '', {}),
 (83, GY, 'Alma', '', {'típus': 'Crimson Snow'}),
 (84, Z, 'Friss fűszernövény', '', {}),
 (85, GY, 'Szőlő', '', {'magnélküli': True, 'színe': 'piros'}),
 (86, Z, 'Paradicsom', '', {'fajta': 'egyéb'}),
 (87, Z, EGYZ, '', {'kiszerelés': 'csomós'}),
 (88, GY, 'Narancs', '', {'kiszerelés': 'lédig'}),
 (89, Z, 'Káposzta', '', {'fajta': 'Kelkáposzta'}),
 (90, Z, 'Gomba', '', {'fajta': 'Csiperke', 'bio': True}),
 (91, Z, 'Hagymafélék', '', {'fajta': 'Vöröshagyma', 'kiszerelés': 'csomós'}),
 (92, GY, 'Banán', '', {'fajta / jelleg': ['sima']}),
 (93, Z, 'Salátafélék', '', {'fajta': 'Jég'}),
 (94, Z, 'Paradicsom', '', {'fajta': 'Koktél'}),
 (95, Z, 'Gomba', '', {'fajta': 'Laska'}),
 (96, Z, 'Paprika', '', {'fajta': 'Lecsó'}),
 (97, GY, 'Alma', '', {'típus': 'Pink Lady'}),
 (98, Z, 'Paradicsom', '', {'fajta': 'Cherry', 'fürtös': True}),
 (99, GY, 'Citrom', '', {'bio': True}),
 (100, Z, 'Burgonya', '', {'fajta': 'Újburgonya'}),
 (101, GY, 'Sárgadinnye', '', {}),
 (102, GY, 'Mangó', '', {}),
 (103, Z, 'Burgonya', '', {'fajta': 'Étkezési', 'kiszerelés': '1 kg'}),
 (104, Z, 'Paradicsom', '', {'fajta': 'egyéb'}),
 (105, Z, 'Paprika', '', {'fajta': 'Kápia'}),
 (106, GY, 'Passiógyümölcs', '', {}),
 (107, Z, 'Uborka', '', {'fajta': 'Fürtös'}),
 (108, GY, 'Málna', '', {}),
 (109, GY, 'Őszibarack, nektarin', '', {}),
 (110, GY, 'Sárgabarack', '', {}),
 (111, GY, 'Eper', '', {}),
 (112, Z, 'Burgonya', '', {'fajta': 'Édesburgonya'}),
 (113, GY, 'Áfonya', '', {}),
 (114, Z, TOK, '', {}),
 (115, GY, 'Banán', '', {'fajta / jelleg': ['sima'], 'bio': True}),
 (116, GY, 'Ananász', '', {}),
 (117, Z, 'Paprika', '', {'fajta': 'Kaliforniai', 'színe': 'Mix'}),
 (118, Z, 'Mix, vegyes', '', {'kiszerelés': '1 kg'}),
 (119, Z, TOK, '', {'kiszerelés': 'lédig'}),
 (120, Z, 'Hagymafélék', '', {'fajta': 'Vöröshagyma', 'bio': True, 'kiszerelés': '1 kg'}),
 (121, GY, 'Narancs', '', {}),
 (122, GY, 'Lime', '', {}),
 (123, GY, 'Citrom', '', {}),
 (124, Z, 'Paprika', '', {'fajta': 'egyéb'}),
 (125, Z, 'Karfiol', '', {'fajta': 'Sima'}),
 (126, GY, 'Szeder', '', {}),
 (127, GY, 'Áfonya', '', {'bio': True}),
 (128, GY, 'Avokádó', '', {'fajta / jelleg': ['hass']}),
 (129, Z, EGYZ, '', {}),
 (130, Z, 'Uborka', '', {'fajta': 'Kovászolni való', 'kiszerelés': 'lédig'}),
 (131, Z, 'Sárgarépa', '', {'bio': True, 'kiszerelés': '1 kg'}),
 (132, Z, 'Hagymafélék', '', {'fajta': 'Fokhagyma'}),
 (133, Z, 'Paprika', '', {'fajta': 'Kaliforniai'}),
 (134, GY, 'Cseresznye', '', {}),
 (135, GY, 'Őszibarack, nektarin', '', {'kiszerelés': 'lédig'}),
 (136, GY, 'Őszibarack, nektarin', '', {'kiszerelés': 'lédig'}),
 (137, GY, 'Őszibarack, nektarin', '', {}),
 (138, Z, 'Paradicsom', '', {'fajta': 'Cherry', 'fürtös': True, 'kiszerelés': 'lédig'}),
 (139, GY, 'Eper', '', {}),
 (140, Z, 'Gomba', '', {'fajta': 'Csiperke'}),
 (141, Z, 'Paradicsom', '', {'fajta': 'Koktél', 'kiszerelés': 'lédig'}),
 (142, Z, 'Spárga', '', {}),
 (143, Z, 'Gyömbér', '', {}),
 (144, T, 'Sajt', GR, {'ízesítés': ['chili-lime']}),
 (145, T, 'Sajt', GR, {'ízesítés': ['füstölt']}),
 (146, T, 'Sajt', GR, {'ízesítés': ['natúr']}),
 (147, T, 'Sajt', GR, {'ízesítés': ['füstölt']}),
 (148, T, 'Sajt', GR, {'ízesítés': ['natúr']}),
 (149, T, 'Sajt', GR, {'ízesítés': ['zöldfűszeres']}),
]

new, prob = [], []
for i, fo, alk, alt, raw in D:
    t = undone[i]
    if alk not in tree[fo]['alkategóriák']:
        prob.append(f"  #{i} ROSSZ ALK: {fo} > {alk}")
        continue
    altmap = tree[fo]['alkategóriák'][alk].get('altípusok', {})
    if alt and alt not in altmap:
        prob.append(f"  #{i} ROSSZ ALT: {alk} > {alt}  (elerheto: {list(altmap.keys())})")
        continue
    allowed = P.props_for_path(tree, fo, alk, alt)
    clean = P.coerce_tulajdonsagok(allowed, raw)
    for k, v in raw.items():
        if k not in clean:
            prob.append(f"  #{i} [{t['product_name'][:24]}] ELDOBVA {k}={v!r}")
    new.append({'termek': t, 'fokategoria': fo, 'alkategoria': alk, 'altipus': alt,
                'tulajdonsagok': clean, 'kategoria_hash': P.kategoriak_hash(fo, alk, alt, clean),
                'statusz': 'kesz'})

print("Minoseg:")
print('\n'.join(prob) if prob else "  OK - nincs eldobott ertek / rossz ut")
if not any('ROSSZ' in p for p in prob):
    json.dump(tree, open(P.TREE_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    ered.extend(new)
    json.dump(ered, open(ERED, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"Uj: {len(new)} | eredmeny most: {len(ered)}")
else:
    print("ROSSZ UT talalva -> NEM mentettem.")
