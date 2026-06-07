# elírt termékek

Kézi javítólisták a Wolt alapú normalizáláshoz.

## Szerepe

Ezek a fájlok olyan termékneveket tartalmaznak, ahol a kiszerelés a névben vagy
az API mezőkben hibásan, félreérthetően vagy egymásnak ellentmondó módon
szerepel.

## Használat

A `normalize_data_prima.py` innen olvassa a kivétellistákat, és ezek alapján
dönt egyes vitás kiszereléseknél.

## Megjegyzés

Ez a mappa a SPAR pipeline-ból lett átvéve, mert a normalizáló ugyanazt a
mechanizmust használja. A bejegyzések pontos terméknév-egyezéssel működnek, így
a SPAR-specifikus sorok Prima termékekre nem hatnak, amíg nincs pontos egyezés.
