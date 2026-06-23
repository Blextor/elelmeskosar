# Baba főkategória audit

Dátum: 2026-06-23 20:42:10

Források:
- `C:/Users/Bobo/Documents/GitHub/elelmeskosar2/data/categories/kategorizalando_termekek/GPT/kategoriak_2026-06-13.json`
- `C:/Users/Bobo/Documents/GitHub/elelmeskosar2/data/categories/kategorizalando_termekek/GPT/eredmeny.json`

## Összefoglaló

| Mérés | Darab |
| --- | --- |
| Baba termék | 645 |
| Baba alkategória | 7 |
| Baba altípus | 27 |
| Termékkel használt kategóriaút | 28 |
| Üres altípus | 0 |
| Hiányzó kategóriaút | 197 |
| Hiányzó tulajdonságdefiníció | 0 |
| Hiányzó értéklistás deklaráció | 0 |
| Kardinalitási gond | 0 |
| Nem használt közvetlen tulajdonságdefiníció | 8 |
| Pontos duplikált terméknévcsoport | 146 |
| Pontos duplikált terméksor | 318 |

## Javítási jelöltek

| Téma | Darab | Megjegyzés | Javaslat |
| --- | --- | --- | --- |
| Duplikált Baba-terméknevek | 146 | 318 terméksor érintett; 14 névcsoport több kategória/altípus között is szóródik. | Dedublikáció vagy egy forrásonkénti merge szabály kell, mert eltérő tulajdonságsémák is vannak ugyanarra a terméknévre. |
| Nem élelmiszer jellegű Baba-termékek | 25 | 25 Babaápolási eszköz; rossz élelmiszer-ágon maradt: 0. | Ha a Baba főkategória vegyes baba-termék kategória marad, ez így konzisztens. Ha csak élelmiszer legyen, ezt az egész ágat külön főkategóriába kellene vinni. |
| Hiányzó értéklistás deklarációk | 0 |  | A használt értékeket fel kell venni, vagy lazítani kell az adott tulajdonság értéklistáját. |
| Kiszerelés jelentése keveredik | 162 | csomagolástípus: 0, mennyiség: 160, egyéb: 2 | Érdemes szétválasztani `csomagolás` és `kiszerelés`/`nettó mennyiség` mezőkre. |
| Nem használt közvetlen tulajdonságdefiníciók | 8 | Főleg régi `korosztály`, `jellemzők`, `alapanyag` maradványok. | A régi kulcsokat össze kell vezetni az aktuális `életkor`, `jellemző`, `gabona` kulcsokkal, majd törölni a maradék deklarációkat. |
| Üres altípusok | 0 |  | Ha nincs tervezett termékfeltöltés, törölhető. |
| Közvetlen duplikált tulajdonságdefiníció | 0 |  | Egy mező csak `egyedi` vagy `csoportos` legyen ugyanazon a szinten. |
| Életkor értékformátum szóródik | 23 | 23 különböző életkorérték. | Egységes formátum javasolt, például `4 hó+`, `6 hó+`, `12 hó+`, `1-3 év`. |

## Kategóriaeloszlás

| Kategóriaút | Termék |
| --- | --- |
| Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré | 174 |
| Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek | 40 |
| Baba > Tápszer > Junior tápszer (1-3 év) | 32 |
| Baba > Tápszer > Gyermek italpor | 31 |
| Baba > Tejpép, gabonapép, kása > Tejpép | 30 |
| Baba > Bébi snack, keksz > Puffasztott snack, ropi | 24 |
| Baba > Tejpép, gabonapép, kása > Gabonapép | 20 |
| Baba > Tápszer > Követő tápszer (2-es) | 14 |
| Baba > Bébiital, víz > Gyümölcslé, gyerekital | 13 |
| Baba > Babaápolási eszköz > Baba cumi | 11 |
| Baba > Bébi snack, keksz > Bébikeksz | 10 |
| Baba > Tejpép, gabonapép, kása > Zabkása, instant kása | 8 |
| Baba > Tápszer > Speciális tápszer | 8 |
| Baba > Bébi snack, keksz > Gyümölcsfalat, rágóka | 7 |
| Baba > Bébiital, víz > Bébitea | 4 |
| Baba > Babaápolási eszköz > Baba rágóka | 3 |
| Baba > Babaápolási eszköz > Itatópohár | 3 |
| Baba > Bébiital, víz > Bébivíz | 3 |
| Baba > Tápszer > Követő tápszer (3-as) | 3 |
| Baba > Babaápolási eszköz > Baba fogkefe | 2 |
| Baba > Tápszer > Anyatej-helyettesítő (1-es) | 2 |
| Baba > Babaápolási eszköz > Baba evőeszköz | 1 |
| Baba > Babaápolási eszköz > Baba fürdetőszivacs | 1 |
| Baba > Babaápolási eszköz > Baba kanál | 1 |
| Baba > Babaápolási eszköz > Baba tányér | 1 |
| Baba > Babaápolási eszköz > Pelenkázó alátét | 1 |
| Baba > Babaápolási eszköz > Tanulópohár | 1 |

## Hiányzó értéklistás deklarációk

### Tulajdonság szerint

| Tulajdonság | Darab |
| --- | --- |
| - | - |

### Kategóriaút és tulajdonság szerint

| Kategóriaút | Tulajdonság | Darab |
| --- | --- | --- |
| - | - |

### Konkrét hiányzó értékek

| Tulajdonság | Érték | Darab |
| --- | --- | --- |
| - | - |

## Kardinalitási gondok

| Index | Kategóriaút | Tulajdonság | Gond | Érték | Termék |
| --- | --- | --- | --- | --- | --- |
| - | - |

## Nem használt közvetlen tulajdonságdefiníciók

| Kategóriaút | Tulajdonság |
| --- | --- |
| Baba > Bébiétel, bébimenü (sós) | bio |
| Baba > Bébiétel, bébimenü (sós) | márka |
| Baba > Bébiétel, bébimenü (sós) | állag |
| Baba > Bébiétel, bébimenü (sós) | hús/tej |
| Baba > Bébiétel, bébimenü (sós) | Íz / alapanyag |
| Baba > Bébiétel, bébimenü (sós) | életkor |
| Baba > Tápszer > Gyermek italpor | gabona |
| Baba > Bébiital, víz > Bébivíz | életkor |

## Speciális tulajdonságkulcsok használata

| Tulajdonság | Termékdarab |
| --- | --- |
| életkor | 580 |
| kiszerelés | 216 |
| hús/tej | 200 |
| gabona | 55 |

## Életkor értékek

| Érték | Darab |
| --- | --- |
| 6 hó+ | 179 |
| 4 hó+ | 104 |
| 12 hó+ | 88 |
| 8 hó+ | 76 |
| 5 hó+ | 33 |
| 10 hó+ | 28 |
| 2 év+ | 22 |
| 7 hó+ | 8 |
| 0 hó+ | 8 |
| 11 hó+ | 6 |
| 3 év+ | 6 |
| 6-36 hó | 4 |
| 16 hó+ | 4 |
| 9 hó+ | 3 |
| 6-12 hó | 2 |
| 24 hó+ | 2 |
| 1-3 év | 1 |
| 0-2 év | 1 |
| 6/9 hó+ | 1 |
| 36 hó+ | 1 |
| 2-6 hó | 1 |
| 2 hó+ | 1 |
| 0-3 hó | 1 |

## Nem élelmiszer jellegű Baba-termékek

| Index | Kategóriaút | Termék |
| --- | --- | --- |
| 38939 | Baba > Babaápolási eszköz > Pelenkázó alátét | Fred & Flo eldobható pelenkázó alátét 60 x 60 cm 10 db |
| 46901 | Baba > Babaápolási eszköz > Baba fürdetőszivacs | Fred & Flo állat alakú szivacs |
| 46925 | Baba > Babaápolási eszköz > Baba fogkefe | Tesco Pro Formula Oral Care Baby Steps fogkefe gyermekeknek 0-2 éves korig |
| 46952 | Baba > Babaápolási eszköz > Baba cumi | MAM Original Night szilikon cumi 16+ hónap 2 db |
| 46958 | Baba > Babaápolási eszköz > Baba fogkefe | MAM Baba fogkefe 6+ hónap |
| 46969 | Baba > Babaápolási eszköz > Baba cumi | MAM Original szilikon cumi 16+ hónap 2 db |
| 46971 | Baba > Babaápolási eszköz > Baba cumi | MAM Original Start szilikon cumi 0+ hónap |
| 46972 | Baba > Babaápolási eszköz > Baba cumi | MAM Original Night szilikon cumi 2-6 hónap |
| 46975 | Baba > Babaápolási eszköz > Tanulópohár | MAM Trainer tanulópohár 220 ml 4+ hónap |
| 46980 | Baba > Babaápolási eszköz > Baba cumi | MAM Original szilikon cumi 16+ hónap |
| 46981 | Baba > Babaápolási eszköz > Baba rágóka | MAM Cooler hűtőrágóka 4+ hónap |
| 46985 | Baba > Babaápolási eszköz > Baba cumi | MAM Air szilikon cumi 16+ hónap |
| 46987 | Baba > Babaápolási eszköz > Baba kanál | MAM Hőérzékelős kanál védőtokkal |
| 46988 | Baba > Babaápolási eszköz > Baba cumi | MAM Original Start szilikon cumi 0+ hónap 2 db |
| 46989 | Baba > Babaápolási eszköz > Baba cumi | MAM Original Night szilikon cumi 6+ hónap 2 db |
| 46990 | Baba > Babaápolási eszköz > Baba cumi | MAM Air szilikon cumi 6+ hónap |
| 46991 | Baba > Babaápolási eszköz > Baba rágóka | MAM Bite & Relax 1. mini rágóka 2+ hónap |
| 46992 | Baba > Babaápolási eszköz > Baba cumi | MAM Comfort szilikon cumi 0-3 hónap |
| 47000 | Baba > Babaápolási eszköz > Baba tányér | Petite&Mars Take&Match szilikon tányér tapadókoronggal |
| 47001 | Baba > Babaápolási eszköz > Baba evőeszköz | Petite&Mars Take&Match Misty Green szilikon evőeszközök 6+, 14 x 3,5 cm |
| 47002 | Baba > Babaápolási eszköz > Baba rágóka | Petite&Mars Take&Match Dusty Rose szilikon rágóka 0+, 7 x 7 cm |
| 47012 | Baba > Babaápolási eszköz > Baba cumi | MAM Original Start Night szilikon cumi 0+ hónap 2 db |
| 47017 | Baba > Babaápolási eszköz > Itatópohár | Philips Avent pohár puha itatófejjel 300 ml 9+ hó |
| 47018 | Baba > Babaápolási eszköz > Itatópohár | MAM Sports Cup ivópohár 33 0ml 12+ hónap |
| 47019 | Baba > Babaápolási eszköz > Itatópohár | MAM Starter ivópohár 150 ml 4+ hónap |

## Duplikált terméknevek

### Több kategória/altípus között is szóródó pontos egyezések

| Darab | Indexek | Termék | Kategóriautak |
| --- | --- | --- | --- |
| 3 | 12351, 37577, 46909 | Nestlé Pizsama Hami UHT gyümölcsös folyékony gabonás bébiétel 6 hónapos kortól 2 x 200 ml (400 ml) | Baba > Tejpép, gabonapép, kása > Gabonapép; Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12429, 37578 | Beba Optipro 3 Junior tejalapú anyatej-kiegészítő tápszer 12. hó+ 2 x 500 g (1000 g) | Baba > Tápszer > Junior tápszer (1-3 év); Baba > Tápszer > Követő tápszer (3-as) |
| 2 | 12430, 46996 | Beba SupremePro 3 Junior tejalapú italpor fehérje-hidrolizátumból 12 hó+ 800 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12315, 46948 | Gerber bio banán-mangó gyümölcspüré fermentált tejkészítménnyel és gabonával, 6 hónapos kortól 80 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré; Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12314, 46930 | Gerber bio banán-áfonya gyümölcspüré fermentált tejkészítménnyel és gabonával, 6 hónapos kortól 80 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré; Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12416, 46986 | Lactogen 3 Junior Vaníliás ízű Tejalapú italpor vitaminokkal és ásványi anyagokkal 12 hó+ 500 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12417, 46939 | Lactogen 4 Junior Vaníliás ízű Tejalapú italpor vitaminokkal és ásványi anyagokkal 2 év+ 500 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12432, 46982 | Milumil 4 Junior vaníliaízű tejalapú italpor 2 év+ 3 x 500 g (1,5 kg) | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12423, 46979 | Milumil 4 Junior vaníliaízű tejalapú italpor 2 év+ 500 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12438, 46978 | Milupa natúr tejes ital 2 év+ 2 x 500 g (1000 g) | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12418, 46959 | Milupa natúr tejes ital tejalapú anyatej-kiegészítő tápszer 12 hó+ 500 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12425, 46942 | Milupa natúr tejes ital tejalapú anyatej-kiegészítő tápszer 12. hó+ 2 x 500 g (1000 g) | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12426, 46929 | Milupa vaníliaízű tejes ital 12 hó+ 2 x 500 g (1000 g) | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12419, 46908 | Milupa vaníliaízű tejes ital 12 hó+ 500g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |

### Összes pontos duplikált terméknévcsoport

| Darab | Indexek | Termék | Kategóriautak |
| --- | --- | --- | --- |
| 5 | 12231, 25904, 30729, 37541, 39106 | Univer Disney Baby bio alma-őszibarack bébidesszert 4 hónapos kortól 163 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 5 | 12166, 25909, 30724, 37527, 38707 | Univer alma-banán csirkehússal bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 5 | 12172, 25907, 30727, 37528, 39170 | Univer sütőtökpüré csirkehússal bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 4 | 12175, 30726, 37526, 38780 | Univer zsenge zöldborsófőzelék csirkehússal bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 3 | 12384, 37556, 46899 | Detki bio babakeksz 6+ hónapos kortól 150 g | Baba > Bébi snack, keksz > Bébikeksz |
| 3 | 12254, 30732, 31215 | HiPP HiPPiS BIO eper-banán almában gyümölcspép 4 hónapos kortól 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 3 | 12328, 30738, 37535 | Kecskeméti brokkolis csirkehús tésztával és sajttal bébiétel 8 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 3 | 12185, 30735, 37525 | Kecskeméti sütőtök almával és csirkehússal bébiétel 5 hónapos kortól 190 g | Baba > Bébiétel, bébimenü (sós) >  |
| 3 | 12343, 30739, 37524 | Kecskeméti vadas marhahús rizzsel bébiétel 8 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 3 | 12408, 37579, 46956 | Lactogen 2 Tejalapú anyatej-kiegészítő tápszer 6 hó 500 g | Baba > Tápszer > Követő tápszer (2-es) |
| 3 | 12351, 37577, 46909 | Nestlé Pizsama Hami UHT gyümölcsös folyékony gabonás bébiétel 6 hónapos kortól 2 x 200 ml (400 ml) | Baba > Tejpép, gabonapép, kása > Gabonapép; Baba > Tejpép, gabonapép, kása > Tejpép |
| 3 | 12371, 37546, 46902 | Nestlé kekszes tejpép 6 hónapos kortól 250 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 3 | 12232, 25905, 39135 | Univer Disney Baby bio sütőtök-körte-alma bébidesszert 4 hónapos kortól 163 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 3 | 12229, 25906, 39031 | Univer bio sütőtök-alma bébidesszert 4 hónapos kortól 163 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 3 | 12333, 25912, 38812 | Univer bio zöldséges, vadas marhahús rizzsel bébiétel, 10 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 3 | 12334, 25911, 38801 | Univer körtés, zöldséges pulykahús rizzsel bébiétel 10 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 3 | 12212, 25908, 39202 | Univer vegyes zöldfőzelék csirkehússal bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 3 | 12174, 30722, 39151 | Univer zsenge sárgarépa főzelék csirkehússal bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 3 | 12322, 30728, 38902 | Univer zöldséges rizottó csirkemellel bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12424, 46918 | Beba ExpertPro HA 3 Junior tejalapú anyatej-kiegészítő tápszer 12. hó+ 600 g | Baba > Tápszer > Speciális tápszer |
| 2 | 12429, 37578 | Beba Optipro 3 Junior tejalapú anyatej-kiegészítő tápszer 12. hó+ 2 x 500 g (1000 g) | Baba > Tápszer > Junior tápszer (1-3 év); Baba > Tápszer > Követő tápszer (3-as) |
| 2 | 12430, 46996 | Beba SupremePro 3 Junior tejalapú italpor fehérje-hidrolizátumból 12 hó+ 800 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12262, 37550 | FruchtBar BIO bébidesszert körte almával és kölessel 6 hónapos kortól 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12381, 46999 | Gerber Chewing Wheels banános bio gabonasnack, 10 hónapos kortól 28 g | Baba > Bébi snack, keksz > Puffasztott snack, ropi |
| 2 | 12236, 46932 | Gerber bio alma gyümölcspüré, 4 hónapos kortól 80 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12315, 46948 | Gerber bio banán-mangó gyümölcspüré fermentált tejkészítménnyel és gabonával, 6 hónapos kortól 80 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré; Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12314, 46930 | Gerber bio banán-áfonya gyümölcspüré fermentált tejkészítménnyel és gabonával, 6 hónapos kortól 80 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré; Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12388, 46934 | Gerber bio banános gabonasnack, 8 hónapos kortól 35 g | Baba > Bébi snack, keksz > Puffasztott snack, ropi |
| 2 | 12387, 46914 | Gerber bio banános és málnás gabonasnack, 8 hónapos kortól 35 g | Baba > Bébi snack, keksz > Puffasztott snack, ropi |
| 2 | 12374, 46915 | Gerber bio banános és málnás gabonasnack, 8 hónapos kortól 7 g | Baba > Bébi snack, keksz > Puffasztott snack, ropi |
| 2 | 12237, 46927 | Gerber bio körte gyümölcspüré, 4 hónapos kortól 80 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12238, 46933 | Gerber bio mangó gyümölcspüré, 4 hónapos kortól 80 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12278, 37538 | HiPP BIO alma-banán babakeksszel bébidesszert 4 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12205, 37562 | HiPP BIO sárgarépa rizzsel és pulykahússal bébiétel 8 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12288, 37539 | HiPP BIO őszibarackos banános alma bébidesszert 4 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12403, 37553 | HiPP Bio Tea + Gyümölcslé piros gyümölcslé ital csipkebogyóteával 4 hónapos kortól 0,5 l | Baba > Bébiital, víz > Gyümölcslé, gyerekital |
| 2 | 12294, 37545 | HiPP Gyümölcs Duett BIO őszibarack-sárgabarack túrókrémmel bébidesszert 7 hónapos kortól 160 g | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12295, 37560 | HiPP Gyümölcs Gabonával BIO banános alma teljes kiőrlésű gabonával bébidesszert 6 hónap 190 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12251, 37565 | HiPP HiPPiS BIO alma-banán-málna gyümölcspép teljes kiőrlésű gabonával 6 hónapos kortól 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12252, 30733 | HiPP HiPPiS BIO alma-banán-őszibarack keksszel gyümölcskészítmény 1 éves kortól 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12253, 30731 | HiPP HiPPiS BIO alma-körte-banán gyümölcspép 4 hónapos kortól 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12256, 31214 | HiPP HiPPiS BIO szilva-feketeribizli körtében gyümölcspép 6 hónapos kortól 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12273, 37537 | HiPP Jó Éjt Papi BIO almás-babakekszes tejbegríz bébidesszert 6 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12274, 37559 | HiPP Jó Éjt Papi BIO almás-őszibarackos tejbegríz bébidesszert 6 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12275, 37544 | HiPP Jó Éjt Papi BIO banános-kakaós tejbegríz bébidesszert 6 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12390, 37557 | HiPP bio babakeksz 6 hónapos kortól 4 x 45 g (180 g) | Baba > Bébi snack, keksz > Bébikeksz |
| 2 | 12280, 37552 | HiPP bio gyümölcskészítmény alma áfonyával bébidesszert 5 hónapos kortól 160 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12201, 37533 | HiPP bio sütőtök almával és pulykahússal bébiétel 5 hónapos kortól 190 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12202, 37563 | HiPP sárgarépa burgonyával és vadlazaccal bébiétel 5 hónapos kortól 190 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12266, 30736 | Kecskeméti alma-sárgabarack keksszel bébidesszert 6 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12189, 37536 | Kecskeméti alma-őszibarack csirkehússal bébiétel 8 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12265, 37570 | Kecskeméti alma-őszibarack rizzsel bébidesszert 4 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12183, 30734 | Kecskeméti almaszósz csirkehússal bébiétel 5 hónapos kortól 190 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12327, 30737 | Kecskeméti bolognai spagetti bébiétel 8 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12329, 37532 | Kecskeméti cukkini csirkehússal és rizzsel bébiétel 8 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12392, 37567 | Kecskeméti málna-csipkebogyó babatea 6 hónapos kortól 200 g | Baba > Bébiital, víz > Bébitea |
| 2 | 12330, 37566 | Kecskeméti spenótos tészta csirkehússal bébiétel 11 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12249, 37542 | Kecskeméti szilva bébidesszert 4 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12331, 37531 | Kecskeméti tengeri hal rizzsel joghurtos mártásban bébiétel 11 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12188, 37534 | Kecskeméti zöldséges spagetti pulykahússal bébiétel 6 hónapos kortól 190 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12247, 37540 | Kecskeméti őszibarack bébidesszert 4 hónapos kortól 190 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12401, 37554 | Kecskeméti őszibarack ital 4 hónapos kortól 0,2 l | Baba > Bébiital, víz > Gyümölcslé, gyerekital |
| 2 | 12184, 37530 | Kecskeméti őszibarack pulykahússal bébiétel 5 hónapos kortól 190 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 26194, 44180 | Kubu 100% alma-őszibarack-banán-sárgarépa püré C-vitaminnal 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 26231, 37572 | Kubu Immuno alma-körte-sárgarépa-banán-acerola-bodzabogyó püré, C-vitaminnal, cinkkel 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 25902, 44250 | Kubu Tízórai alma püré rizzsel, fahéjjal és C-vitaminnal 100 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12427, 46910 | Lactogen 3 Junior Tejalapú anyatej-kiegészítő tápszer 12. hó+ 1000 g | Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12415, 46957 | Lactogen 3 Junior Tejalapú anyatej-kiegészítő tápszer 12. hó+ 500 g | Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12416, 46986 | Lactogen 3 Junior Vaníliás ízű Tejalapú italpor vitaminokkal és ásványi anyagokkal 12 hó+ 500 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12417, 46939 | Lactogen 4 Junior Vaníliás ízű Tejalapú italpor vitaminokkal és ásványi anyagokkal 2 év+ 500 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12413, 46966 | Milumil 2 tejalapú anyatej-kiegészítő tápszer 6-12 hó között 1000 g | Baba > Tápszer > Követő tápszer (2-es) |
| 2 | 12428, 46926 | Milumil 3 Junior tejalapú anyatej-kiegészítő tápszer 12. hónapos kortól 1000 g | Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12432, 46982 | Milumil 4 Junior vaníliaízű tejalapú italpor 2 év+ 3 x 500 g (1,5 kg) | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12423, 46979 | Milumil 4 Junior vaníliaízű tejalapú italpor 2 év+ 500 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12412, 46977 | Milumil Cesar-Biotik 2 tejalapú anyatej-kiegészítő tápszer 6 hó+ 400 g | Baba > Tápszer > Követő tápszer (2-es) |
| 2 | 12409, 46944 | Milupa 3 tejalapú anyatej-kiegészítő tápszer 9 hó+ 500 g | Baba > Tápszer > Követő tápszer (3-as) |
| 2 | 12355, 46923 | Milupa Finom falatok banános tejpép 4 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12356, 46922 | Milupa Finom falatok gyümölcsös kaland tejpép 6 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12357, 46906 | Milupa Finom falatok sztracsatellás tejpép 8 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12358, 46920 | Milupa Finom falatok vaníliaízű tejbegríz 4 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12359, 46916 | Milupa Finom falatok vaníliaízű tejberizs 6 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12309, 39298 | Milupa Frutapura alma-banán 100% gyümölcspüré 4 hó+ 4 x 100 g (400 g) | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12310, 39397 | Milupa Frutapura alma-szilva 100% gyümölcspüré 6 hó+ 4 x 100 g (400 g) | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12360, 46919 | Milupa Jó reggelt! almás zabkása 6 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Zabkása, instant kása |
| 2 | 12361, 46946 | Milupa Jó reggelt! bogyós-gyümölcsös zabkasa 6 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Zabkása, instant kása |
| 2 | 12362, 46903 | Milupa Jó reggelt! gyümölcsduó zabkása 6 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Zabkása, instant kása |
| 2 | 12373, 46937 | Milupa Jó reggelt! pirosgyümölcsös zabkása 6 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Zabkása, instant kása |
| 2 | 12363, 46924 | Milupa Natúr 7-gabonás kása 8 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Gabonapép |
| 2 | 12364, 46951 | Milupa Natúr rizskása 4 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Gabonapép |
| 2 | 12365, 46904 | Milupa Szép álmokat! 7-gabonás kekszes tejpép 6 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12366, 46913 | Milupa Szép álmokat! eper-banánízű 7-gabonás tejpép 8 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12367, 46905 | Milupa Szép álmokat! zamatos gyümölcsös 7-gabonás tejpép 8 hó+ 225 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12438, 46978 | Milupa natúr tejes ital 2 év+ 2 x 500 g (1000 g) | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12418, 46959 | Milupa natúr tejes ital tejalapú anyatej-kiegészítő tápszer 12 hó+ 500 g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12425, 46942 | Milupa natúr tejes ital tejalapú anyatej-kiegészítő tápszer 12. hó+ 2 x 500 g (1000 g) | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12426, 46929 | Milupa vaníliaízű tejes ital 12 hó+ 2 x 500 g (1000 g) | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12419, 46908 | Milupa vaníliaízű tejes ital 12 hó+ 500g | Baba > Tápszer > Gyermek italpor; Baba > Tápszer > Junior tápszer (1-3 év) |
| 2 | 12368, 46950 | Nestlé 8 gabonás pép 8 hónapos kortól 250 g | Baba > Tejpép, gabonapép, kása > Gabonapép |
| 2 | 12349, 46940 | Nestlé Junior Cereals 3-gyümölcsös gabonapép 12 hónapos kortól 200 g | Baba > Tejpép, gabonapép, kása > Gabonapép |
| 2 | 12369, 46954 | Nestlé Jó éjszakát 5 gyümölcsös tejpép 8 hónapos kortól 250 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12350, 46911 | Nestlé Pizsama Hami UHT gluténmentes banános folyékony gabonás bébiétel 6 hónap+ 2 x 200 ml (400 ml) | Baba > Tejpép, gabonapép, kása > Gabonapép |
| 2 | 12352, 46912 | Nestlé Pizsama Hami UHT kakaós folyékony gabonás bébiétel 6 hónapos kortól 2 x 200 ml (400 ml) | Baba > Tejpép, gabonapép, kása > Gabonapép |
| 2 | 12353, 46907 | Nestlé Pizsama Hami UHT kekszes folyékony gabonás bébiétel 6 hónapos kortól 2 x 200 ml (400 ml) | Baba > Tejpép, gabonapép, kása > Gabonapép |
| 2 | 12354, 46900 | Nestlé Pizsama Hami UHT vaníliás ízű folyékony gabonás bébiétel 6 hónapos kortól 2 x 200 ml (400 ml) | Baba > Tejpép, gabonapép, kása > Gabonapép |
| 2 | 12300, 39300 | Nestlé Yogolino kakaós babapuding 6+ hó 4 x 100 g (400 g) | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12301, 39263 | Nestlé Yogolino kekszes babapuding 6-36 hónapos korig 4 x 100 g (400 g) | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12302, 39372 | Nestlé Yogolino tejalapú banános bébidesszert 6+ hó 4 x 100 g (400 g) | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12304, 39262 | Nestlé Yogolino vaníliás ízű babapuding 6+ hó 4 x 100 g (400 g) | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12305, 39048 | Nestlé Yogolino vaníliás ízű grízes babapuding 6+ hó 4 x 100 g (400 g) | Baba > Gyümölcspüré, bébidesszert > Tejes, grízes desszertek |
| 2 | 12348, 47003 | Nestlé banános tejberizspép 6 hónapos kortól 200 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12370, 46928 | Nestlé kakaós tejberizspép 10 hónapos kortól 230 g | Baba > Tejpép, gabonapép, kása > Tejpép |
| 2 | 12414, 47009 | Nestlé kakaós, gabona alapú ízesítő italpor 8 hónapos kortól 400 g | Baba > Tápszer > Gyermek italpor |
| 2 | 31446, 31448 | SPAR Natur*pur Bio extrudált gluténmentes kukorica-snack 12 hónapos kortól 30 g | Baba > Bébi snack, keksz > Puffasztott snack, ropi |
| 2 | 26196, 44518 | Sió Vitatigris alma-szőlő-banán gyümölcspüré 90 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 26197, 44376 | Sió Vitatigris alma-szőlő-eper gyümölcspüré 90 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 26239, 45028 | Sió Vitatigris almás gyümölcspüré 90 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 26240, 44658 | Sió Vitatigris barackos gyümölcspüré 90 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12234, 39293 | Univer Disney Baby bio alma-banán-édesburgonya zabpehellyel bébidesszert 8 hónapos kortól 163 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 30725, 39326 | Univer Disney Baby bio cukkini sertéshússal, rizzsel bébiétel 8 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12235, 39338 | Univer Disney Baby bio szilva-banán zabpehellyel bébidesszert 8 hónapos kortól 163 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12344, 39611 | Univer Disney Baby bio sárgarépa-brokkoli tésztával bébiétel, 12 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 25910, 38764 | Univer Disney Baby bio sárgarépás rizottó csirkehússal bébiétel 10 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12149, 39343 | Univer Disney Baby bio zsenge sárgarépa főzelék 4 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12153, 39391 | Univer Disney Baby bio zöldséges lasagne bébiétel 8 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 37569, 38686 | Univer Disney Baby bio édesburgonyás csirke zöldségekkel, rizzsel bébiétel 10 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12179, 39168 | Univer Disney Baby édesburgonya pulykával bébiétel 8 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12167, 38821 | Univer almaszósz csirkehússal bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12323, 38832 | Univer bio bolognai mártás spagettivel bébiétel 8 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12192, 39791 | Univer bio lencsefőzelék sertéshússal bébiétel, 10 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12193, 39008 | Univer bio mexikói zöldségek sertéshússal bébiétel 10 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12148, 39390 | Univer bio paradicsom-burgonya zöldségpüré a bébinek 4 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12230, 39038 | Univer bio szilva-alma bébidesszert 4 hónapos kortól 163 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12168, 38652 | Univer bio sütőtökpüré marhahússal bébiétel, 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12151, 39337 | Univer bio vegyes zöldfőzelék zöldségpüré a bébinek, 4 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12152, 39260 | Univer bio zsenge zöldborsófőzelék bébiétel, 4 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12194, 39043 | Univer bio zöldbab-burgonya marhahússal bébiétel, 10 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12332, 39023 | Univer bio zöldborsós marharagu rizzsel bébiétel, 10 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12324, 39167 | Univer bio zöldséges rizs marhahússal bébiétel, 8 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12228, 39009 | Univer bio őszibarack-alma-banán bébidesszert 4 hónapos kortól 163 g | Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré |
| 2 | 12176, 39340 | Univer burgonyafőzelék pulykahússal bébiétel 8 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12170, 38653 | Univer körte-őszibarack pulykahússal bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12171, 39599 | Univer spenót-burgonya pulykahússal bébiétel, 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12150, 30723 | Univer sütőtökpüré zöldségpüré a bébinek 4 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12335, 39883 | Univer trópusi gyümölcsös rizs csirkehússal bébiétel, 12 hónapos kortól 220 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12165, 39266 | Univer zöldbabpüré csirkehússal bébiétel 6 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |
| 2 | 12325, 38795 | Univer zöldséges rizottó sertésmájjal bébiétel 8 hónapos kortól 163 g | Baba > Bébiétel, bébimenü (sós) >  |

## Kategória-összevonási jelöltek

| Jelölt | Darab | Javasolt cél |
| --- | --- | --- |
| Baba > Gyümölcspüré, bébidesszert > Gyümölcs-gabona püré | 0 | Baba > Gyümölcspüré, bébidesszert > Gyümölcs-gabona készítmény |
| Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré gabonával | 0 | Baba > Gyümölcspüré, bébidesszert > Gyümölcs-gabona készítmény |
| Baba > Bébi snack, keksz > Babapiskóta | 0 | törlés, ha nincs tervezett termék |
| Baba > Egyéb babaélelmiszer > Pelenkázó alátét | 0 | Baba > Babaápolási eszköz > Pelenkázó alátét, ha Baba vegyes baba-termék kategória marad |
