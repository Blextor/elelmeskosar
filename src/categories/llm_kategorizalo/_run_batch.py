# -*- coding: utf-8 -*-
import sys, os, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P
ERED = 'data/categories/kategorizalando_termekek/Claude_Opus/eredmeny.json'
tree = P.load_tree(); ered = json.load(open(ERED, encoding='utf-8'))
dk = {f"{r['termek'].get('store_name','')}|{r['termek'].get('store_product_id','')}" for r in ered}
full = list(csv.DictReader(open(P.BACKLOG_CSV, encoding='utf-8')))
undone = [{c: r.get(c, '') for c in P.TERMEK_COLS} for r in full
          if f"{r['store_name']}|{r['store_product_id']}" not in dk]
T='Tejtermékek és tojás'
FL='Friss / lágy sajt'; FK='Félkemény sajt'; KM='Kemény sajt'; OM='Ömlesztett sajt'; PE='Penészes sajt'; KS='Krémsajt / kenhető sajt'
LIGHT='light / csökkentett zsír'; LM='laktózmentes'; IZ='ízesített'
def E(i,fo,alk,alt,d): return (i,fo,alk,alt,d)
def s(i,alt,forma=None,iz='natúr',**k):
    d={'ízesítés':[iz]}
    if forma: d['forma']=forma
    d.update(k); return (i,T,'Sajt',alt,d)
def tj(i,alt,z,**k): d={'zsírtartalom':z,'kiszerelés':'doboz'}; d.update(k); return (i,T,'Tej',alt,d)
def to(i,meret=None,**k):
    d={'fajta':['tyúktojás']}
    if meret: d['méret']=meret
    d.update(k); return (i,T,'Tojás','Tyúktojás',d)
def sk(i,iz='natúr',**k): d={'íz':[iz]}; d.update(k); return (i,T,'Sajtkrém, szendvicskrém','',d)
UHT='UHT tartós tej'; ESL='ESL tej'; FRT='Friss tej'

D=[
 E(0,T,'Tejital, jegeskávé','Egyéb ízesített tejital',{IZ:True,'íz':['kakaós']}),
 E(1,T,'Egyéb tejtermék','',{}),
 tj(2,UHT,'zsírszegény 1,5%'),tj(3,ESL,'zsírszegény 1,5%'),tj(4,ESL,'félzsíros 2,8%'),
 tj(5,ESL,'félzsíros 2,8%',kiszerelés='flakon'),tj(6,ESL,'zsírszegény 1,5%',kiszerelés='flakon'),tj(7,ESL,'teljes 3,5%'),
 tj(8,FRT,'félzsíros 2,8%'),tj(9,FRT,'zsírszegény 1,5%'),tj(10,FRT,'félzsíros 2,8%'),
 to(11,'M'),to(12,'M'),to(13,'M'),to(14,'M'),to(15,'XL'),to(16),to(17,**{'tartás':'szabadtartású'}),to(18,'M'),to(19,'M'),
 to(20,**{'tartás':'mélyalmos'}),to(21,'M'),to(22,'M'),to(23,'L'),to(24,**{'tartás':'ketreces'}),to(25,'M'),
 E(26,T,'Tojás','Egyéb tojás (fürj, stb.)',{'fajta':['fürjtojás']}),
 s(27,KS,'kenhető'),s(28,FL),s(29,FL,'reszelt'),s(30,FL),s(31,FK,'reszelt'),s(32,FL),s(33,FK,'tömb'),s(34,FK,'tömb'),
 s(35,KM,'tömb',érlelt=True),s(36,FK,'szeletelt'),s(37,FK,'szeletelt'),s(38,OM,'szeletelt','füstölt'),s(39,OM,iz='egyéb'),
 s(40,OM,iz='sonkás'),s(41,OM,'szeletelt'),s(42,OM,'szeletelt'),s(43,OM,'szeletelt'),s(44,FK,'szeletelt'),
 s(45,FK,'szeletelt','füstölt'),s(46,FL,'szeletelt'),s(47,FK,'szeletelt','füstölt'),s(48,FK,'szeletelt'),
 s(49,FK,'szeletelt'),s(50,FK,'szeletelt'),s(51,FK,'szeletelt'),s(52,FK,'szeletelt'),s(53,FK,'szeletelt'),s(54,KM,'szeletelt'),
 s(55,OM,'szeletelt'),s(56,OM,'szeletelt'),s(57,FK,'szeletelt'),s(58,OM,'szeletelt'),s(59,FL,'szeletelt'),
 s(60,FL,'szeletelt'),s(61,FL,'szeletelt','füstölt'),s(62,OM,'szeletelt'),s(63,FK,'szeletelt'),s(64,OM,'szeletelt'),
 s(65,OM,'szeletelt','sonkás'),s(66,OM,'szeletelt'),s(67,FK,'szeletelt'),s(68,FK,'szeletelt'),s(69,FK,'szeletelt'),
 s(70,FK,'szeletelt'),s(71,OM,'szeletelt'),s(72,FK,'szeletelt'),s(73,FK,'szeletelt',**{LIGHT:True,LM:True}),
 s(74,FK,'szeletelt',**{LM:True}),s(75,OM,'szeletelt','füstölt'),s(76,PE,'szeletelt'),s(77,FK,'szeletelt',**{LIGHT:True}),
 s(78,KM,'szeletelt'),s(79,FK,'szeletelt'),s(80,FK,'szeletelt'),s(81,FK,'szeletelt'),s(82,KM,'szeletelt'),
 s(83,FK,'szeletelt'),s(84,FK,'szeletelt'),s(85,FK,'kocka'),s(86,OM),s(87,FL,'szeletelt',**{LIGHT:True}),
 s(88,FK,'szeletelt'),s(89,FK,'szeletelt'),s(90,FK,'szeletelt'),s(91,FK,'szeletelt'),s(92,FK,'szeletelt'),
 s(93,FK,'szeletelt'),s(94,FK,'szeletelt'),s(95,FK,'szeletelt',**{LIGHT:True}),s(96,OM,'szeletelt'),s(97,FK,'reszelt'),
 s(98,OM),s(99,KM,'reszelt',érlelt=True),s(100,KM,'reszelt'),s(101,KM,'reszelt'),s(102,FK,'reszelt'),s(103,FK,'reszelt'),
 s(104,KM,'tömb',érlelt=True),s(105,KM,'tömb',érlelt=True),s(106,KM,'reszelt'),s(107,KM,'reszelt'),s(108,KM,'reszelt'),
 s(109,KM,iz='natúr',érlelt=True),s(110,KM,'reszelt'),s(111,FK,'reszelt'),s(112,KM,'reszelt'),s(113,KM,'reszelt',érlelt=True),
 sk(114,'natúr'),sk(115,'sonkás',**{IZ:True}),sk(116,'fűszeres',**{IZ:True}),
 s(117,OM,'kenhető','paprikás'),s(118,OM,'kenhető','zöldfűszeres'),s(119,OM,'kenhető','sonkás'),s(120,OM,'kenhető'),
 s(121,OM,'kenhető',**{LIGHT:True}),s(122,OM,'kenhető','paprikás'),s(123,OM,'kenhető','egyéb'),s(124,OM,'kenhető','zöldfűszeres'),
 s(125,OM,'kenhető'),s(126,OM,'kenhető'),s(127,OM,'kenhető'),
 sk(128,'sonkás',**{IZ:True}),sk(129,'fűszeres',**{IZ:True}),
 s(130,OM,'kenhető'),s(131,KS,'kenhető'),s(132,FL,'golyó'),s(133,OM,'kenhető','füstölt'),s(134,OM,'kenhető'),
 s(135,OM,'kenhető','sonkás'),s(136,OM,'kenhető'),s(137,OM,'kenhető','egyéb'),s(138,OM,'kenhető'),
 s(139,FL,'golyó',**{LIGHT:True}),s(140,FL,'golyó'),s(141,OM),
 sk(142,'fűszeres',**{IZ:True}),sk(143,'natúr',**{LIGHT:True}),sk(144,'natúr'),sk(145,'fűszeres',**{IZ:True}),
 s(146,FL,'golyó','zöldfűszeres'),sk(147,'natúr'),sk(148,'egyéb',**{IZ:True}),s(149,FL,'golyó',**{LIGHT:True}),
]
idxs=[d[0] for d in D]
new, prob = [], []
for i,fo,alk,alt,raw in D:
    t = undone[i]
    if alk not in tree[fo]['alkategóriák']: prob.append(f"#{i} ROSSZ ALK {fo}>{alk}"); continue
    altmap = tree[fo]['alkategóriák'][alk].get('altípusok', {})
    if alt and alt not in altmap: prob.append(f"#{i} ROSSZ ALT {alk}>{alt}"); continue
    allowed = P.props_for_path(tree, fo, alk, alt); clean = P.coerce_tulajdonsagok(allowed, raw)
    for k, v in raw.items():
        if k not in clean: prob.append(f"#{i} ELDOB {k}")
    new.append({'termek': t, 'fokategoria': fo, 'alkategoria': alk, 'altipus': alt, 'tulajdonsagok': clean,
                'kategoria_hash': P.kategoriak_hash(fo, alk, alt, clean), 'statusz': 'kesz'})
ok = sorted(idxs)==list(range(150))
print(f"db={len(D)} indexek_okek={ok}"); print('\n'.join(p for p in prob if 'ROSSZ' in p) or "utak OK")
if ok and not any('ROSSZ' in p for p in prob):
    ered.extend(new); json.dump(ered, open(ERED, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"Uj:{len(new)} ossz:{len(ered)}")
else: print("NEM mentve")
