# -*- coding: utf-8 -*-
"""Kép-URL átírása a LEGNAGYOBB (eredeti) elérhető méretre.

A boltok CDN-jei alapból kicsinyített képet adnak (méret a path-ban vagy query-ben).
Ez a függvény bolt/CDN szerint az eredeti méretű URL-re ír át. Idempotens: egy már
teljes méretű URL-t változatlanul hagy. Ismeretlen hostot érintetlenül hagy.
"""
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


def to_full_size(url):
    if not url or not isinstance(url, str) or not url.lower().startswith("http"):
        return url
    try:
        parts = urlsplit(url)
    except Exception:
        return url
    host = parts.netloc.lower()
    path, query = parts.path, parts.query

    # Auchan (Magento kép-cache): /cache/product_<méret>/ -> product_large (a legnagyobb)
    if "azurefd.net" in host and "/cache/product_" in path:
        path = re.sub(r"/cache/product_[^/]+/", "/cache/product_large/", path)
        return urlunsplit((parts.scheme, parts.netloc, path, query, parts.fragment))

    # Tesco GHS media: a h/w méret-paramétereket elhagyva a natív (eredeti) méret jön
    if "digitalcontent.api.tesco.com" in host and query:
        kept = [(k, v) for k, v in parse_qsl(query, keep_blank_values=True)
                if k.lower() not in ("h", "w")]
        return urlunsplit((parts.scheme, parts.netloc, path, urlencode(kept), parts.fragment))

    # Wolt imageproxy (Spar, Prima): nagyobb szélesség kérése
    if "imageproxy.wolt.com" in host:
        q = dict(parse_qsl(query, keep_blank_values=True))
        if q.get("w", "0").isdigit() and int(q.get("w", "0")) >= 2000:
            return url
        q["w"] = "2000"
        return urlunsplit((parts.scheme, parts.netloc, path, urlencode(q), parts.fragment))

    return url
