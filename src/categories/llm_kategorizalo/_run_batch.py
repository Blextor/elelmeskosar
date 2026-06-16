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

T='Tejtermékek és tojás'; HUS='Hús, hal, felvágott'; AL='Alapanyag, sütés-főzés'; PEK='Pékáru'; KE='Készétel'
TEJ='Tej'; UHT='UHT tartós tej'; TI='Tejital, jegeskávé'; NA='Növényi alternatíva'; NI='Növényi ital'
KAKAO='Kakaós tej'; JEG='Jegeskávé'; KAVE='Kávéital / latte / cappuccino'; EIT='Egyéb ízesített tejital'
HAL='Hal (friss, fagyasztott)'; RAK='Rák, garnéla, tenger gyümölcsei'; SUR='Surimi, halrúd'; LAZ='Lazac'
SE='Sertés'; MA='Marha, borjú'; VAD='Vad'; KZ='Konzerv, savanyúság, befőtt'; OBA='Olívabogyó, kapribogyó, eltett zöldség'
SZ='Szószok, öntetek, dresszingek'; EHS='Egyéb hideg szósz, dip'
HOT='Hotdog buci és hamburger zsemle'; PUFF='Puffasztott, lepény, golyók'
PR='protein / magas fehérje'; IZ='ízesített'; CM='cukormentes / hozzáadott cukor nélkül'; LM='laktózmentes'
def ni(a, **k): d={'vegán':True,'terméktípus':['növényi ital'],'alap':[a]}; d.update(k); return d
def tj(z, **k): d={'zsírtartalom':z,'kiszerelés':'doboz'}; d.update(k); return d
def tit(alt, iz, **k): d={IZ:True,'íz':[iz]}; d.update(k); return (T,TI,alt,d)

D=[
 (0,AL,KZ,OBA,{'alapanyag':['olívabogyó']}),(1,AL,SZ,EHS,{}),
 (2,HUS,HAL,SUR,{}),(3,HUS,HAL,SUR,{}),(4,AL,KZ,OBA,{'alapanyag':['paprika']}),(5,AL,KZ,OBA,{'alapanyag':['paprika']}),
 (6,HUS,HAL,LAZ,{}),(7,HUS,HAL,LAZ,{}),(8,HUS,HAL,RAK,{}),(9,HUS,HAL,LAZ,{}),(10,HUS,HAL,LAZ,{}),
 (11,HUS,HAL,RAK,{}),(12,HUS,HAL,RAK,{}),(13,HUS,HAL,RAK,{}),(14,HUS,HAL,RAK,{}),
 (15,KE,'Saláta, hidegtál','',{}),(16,AL,KZ,OBA,{'alapanyag':['olívabogyó']}),(17,HUS,HAL,RAK,{}),
 (18,HUS,HAL,RAK,{}),(19,AL,KZ,OBA,{'alapanyag':['paprika']}),(20,HUS,HAL,RAK,{}),(21,HUS,HAL,LAZ,{}),
 (22,PEK,'Fánk','',{'fajta':['natúr']}),(23,PEK,'Fánk','',{'fajta':['natúr']}),(24,PEK,HOT,'',{'fajta':['natúr']}),
 (25,PEK,'Bagett','',{}),(26,PEK,PUFF,'',{'típus':'pita'}),(27,PEK,'Kenyér','',{'fajta':['egyéb']}),
 (28,PEK,HOT,'',{'fajta':['szezámos']}),(29,PEK,HOT,'',{'fajta':['egyéb']}),(30,PEK,'Tortilla lap','',{'fajta':['fehér']}),
 (31,PEK,HOT,'',{'fajta':['szezámos']}),(32,AL,'Sütési alapanyag','Pizzaalap, pizzatészta',{}),
 (33,HUS,SE,'Köröm, fej',{'csontos':True}),(34,HUS,SE,'Lapocka',{'előkészítés':['gulyáshús']}),
 (35,HUS,SE,'Csülök',{}),(36,HUS,SE,'Lapocka',{'előkészítés':['kockázott']}),
 (37,HUS,MA,'Pörköltnek való',{'előkészítés':['gulyáshús']}),(38,HUS,MA,'Lábszár',{'előkészítés':['darabolt']}),
 (39,HUS,VAD,'Vaddisznó',{'előkészítés':['darabolt']}),
 (40,T,TI,EIT,{PR:True,IZ:True,'íz':['vaníliás']}),(41,T,NA,NI,ni('rizs')),(42,T,NA,NI,ni('zab')),
 (43,T,NA,NI,ni('zab')),(44,T,NA,NI,ni('kókusz')),(45,T,NA,NI,ni('kókusz')),(46,T,NA,NI,ni('mandula',**{CM:True})),
 (47,T,NA,NI,ni('szója',**{IZ:True})),(48,T,NA,NI,ni('szója')),(49,T,NA,NI,ni('zab')),
 (50,T,NA,NI,ni('szója',**{IZ:True})),(51,T,NA,NI,ni('kókusz',**{CM:True})),(52,T,NA,NI,ni('zab',**{CM:True})),
 (53,T,NA,NI,ni('kókusz')),(54,T,NA,NI,ni('szója',**{IZ:True})),(55,T,NA,NI,ni('zab')),
 (56,T,NA,NI,ni('mandula',**{CM:True})),(57,T,NA,NI,ni('mandula')),(58,T,NA,NI,ni('mandula')),
 (59,T,NA,NI,ni('rizs')),(60,T,NA,NI,ni('zab',bio=True)),(61,T,NA,NI,ni('zab',**{CM:True})),
 (62,T,NA,NI,ni('zab',**{CM:True})),(63,T,NA,NI,ni('zab',bio=True)),(64,T,NA,NI,ni('zab',bio=True)),
 (65,T,NA,NI,ni('mandula',bio=True,**{CM:True,'gluténmentes':True})),(66,T,NA,NI,ni('rizs',bio=True,**{'gluténmentes':True})),
 (67,T,NA,NI,ni('rizs',bio=True)),(68,T,NA,NI,ni('rizs',bio=True,**{IZ:True,'gluténmentes':True})),
 (69,T,NA,NI,ni('zab',bio=True,**{'gluténmentes':True})),(70,T,NA,NI,ni('kókusz',bio=True,**{'gluténmentes':True})),
 (71,T,NA,NI,ni('egyéb')),(72,T,NA,NI,ni('mandula',**{IZ:True})),(73,T,TI,EIT,{PR:True,IZ:True,'íz':['kakaós']}),
 (74,T,NA,NI,ni('rizs',bio=True)),(75,T,NA,NI,ni('rizs',bio=True,**{'gluténmentes':True})),
 (76,T,NA,NI,ni('zab',bio=True)),(77,T,NA,NI,ni('rizs',bio=True,**{'gluténmentes':True})),
 (78,T,TEJ,UHT,tj('teljes 3,5%')),(79,T,TEJ,UHT,tj('félzsíros 2,8%')),(80,T,TEJ,UHT,tj('zsírszegény 1,5%',**{LM:True})),
 (81,T,TEJ,UHT,tj('félzsíros 2,8%')),(82,T,TEJ,UHT,tj('zsírszegény 1,5%')),(83,T,TEJ,UHT,tj('félzsíros 2,8%')),
 (84,T,TEJ,UHT,tj('félzsíros 2,8%')),(85,T,TEJ,UHT,tj('teljes 3,5%')),(86,T,TEJ,UHT,tj('zsírszegény 1,5%')),
 (87,T,TEJ,UHT,tj('zsírszegény 1,5%')),(88,T,TEJ,UHT,tj('félzsíros 2,8%')),(89,T,TEJ,UHT,tj('0,1%')),
 (90,T,TEJ,UHT,tj('zsírszegény 1,5%')),
 tit(KAKAO,'kakaós'),tit(JEG,'kávés'),tit(JEG,'kávés'),tit(JEG,'kávés'),tit(JEG,'kávés'),tit(JEG,'kávés'),
 tit(KAVE,'egyéb'),tit(KAVE,'kávés'),tit(KAVE,'kávés'),tit(KAVE,'kávés'),tit(KAVE,'kávés'),tit(KAVE,'kávés'),
 tit(KAVE,'kávés'),tit(KAVE,'kávés'),tit(KAVE,'kávés'),tit(KAKAO,'kakaós'),
 (107,T,TI,EIT,{PR:True,LM:True,IZ:True,'íz':['vaníliás']}),tit(KAKAO,'kakaós'),tit(EIT,'vaníliás'),tit(EIT,'kakaós'),
 (111,T,TI,KAKAO,{IZ:True,LM:True,'íz':['kakaós']}),tit(EIT,'epres'),tit(KAKAO,'kakaós'),tit(KAVE,'kávés'),
 tit(KAKAO,'kakaós'),tit(JEG,'kávés'),tit(JEG,'kávés'),tit(JEG,'kávés'),tit(JEG,'kávés'),
 tit(EIT,'banános'),tit(EIT,'kakaós'),tit(EIT,'egyéb'),tit(EIT,'epres'),tit(EIT,'egyéb'),tit(EIT,'egyéb'),
 (126,T,TI,EIT,{IZ:True,CM:True,'íz':['kakaós']}),tit(EIT,'egyéb'),tit(EIT,'egyéb'),
 (129,T,TI,KAKAO,{IZ:True,CM:True,'íz':['kakaós']}),tit(KAKAO,'kakaós'),tit(KAKAO,'kakaós'),tit(EIT,'vaníliás'),
 tit(EIT,'egyéb'),(134,T,TI,EIT,{IZ:True,LM:True,'íz':['vaníliás']}),tit(KAVE,'kávés'),
 (136,T,TI,EIT,{PR:True,CM:True}),(137,T,NA,NI,ni('mandula',bio=True,**{'gluténmentes':True})),
 tit(KAKAO,'kakaós'),tit(KAVE,'kávés'),tit(KAVE,'kávés'),tit(KAVE,'kávés'),tit(JEG,'kávés'),tit(JEG,'kávés'),
 tit(JEG,'kávés'),tit(JEG,'kávés'),tit(KAVE,'kávés'),tit(KAVE,'kávés'),tit(EIT,'egyéb'),tit(JEG,'kávés'),
]
# tit() tételek nem hordoznak indexet -> sorszám szerint töltjük ki a hiányzókat
D2=[]; auto=iter(range(150))
for d in D:
    if len(d)==4 and isinstance(d[0],str): D2.append((None,)+d)
    else: D2.append(d)
# index hozzárendelés: a sorrend MEGEGYEZIK a tételek sorrendjével (0..149)
final=[]
for idx,d in enumerate(D2):
    i = d[0] if d[0] is not None else idx
    final.append((i, d[1], d[2], d[3], d[4]))

new, prob = [], []
for i, fo, alk, alt, raw in final:
    t = undone[i]
    if alk not in tree[fo]['alkategóriák']: prob.append(f"#{i} ROSSZ ALK {fo}>{alk}"); continue
    altmap = tree[fo]['alkategóriák'][alk].get('altípusok', {})
    if alt and alt not in altmap: prob.append(f"#{i} ROSSZ ALT {alk}>{alt}"); continue
    allowed = P.props_for_path(tree, fo, alk, alt); clean = P.coerce_tulajdonsagok(allowed, raw)
    for k, v in raw.items():
        if k not in clean: prob.append(f"#{i} ELDOB {k}")
    new.append({'termek': t, 'fokategoria': fo, 'alkategoria': alk, 'altipus': alt, 'tulajdonsagok': clean,
                'kategoria_hash': P.kategoriak_hash(fo, alk, alt, clean), 'statusz': 'kesz'})
print('\n'.join(prob) if prob else "OK")
if not any('ROSSZ' in p for p in prob) and len(final)==150:
    ered.extend(new); json.dump(ered, open(ERED, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"Uj:{len(new)} ossz:{len(ered)}")
else: print(f"NEM mentve (db={len(final)})")
