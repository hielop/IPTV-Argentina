import json, os, shutil
from urllib.parse import quote

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "site")
PREFIX = "argtv_"
SITE_URL = "https://hielop.github.io/tv-ar"

# Cada canal puede tener varios streams: el primero es el principal, el resto son respaldo.
# ("hls", url) se reproduce en la app | ("yt", url) abre el en vivo de YouTube
CHANNELS = [
    ("eltrece", "El Trece", "https://i.imgur.com/ZK7AQFg.png", [
        ("hls", "https://livetrx01.vodgc.net/eltrecetv/index.m3u8"),
    ]),
    ("telefe", "Telefe", "https://i.imgur.com/wrZfMXn.png", [
        ("hls", "http://45.173.231.22:8000/play/a053/index.m3u8"),
        ("hls", "http://45.134.141.161:2200/ARG/TELEFE_HD/index.m3u8"),
    ]),
    ("tn", "TN Todo Noticias", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/TN_todo_noticias_logo.svg/250px-TN_todo_noticias_logo.svg.png", [
        ("hls", "http://158.172.155.130:8000/play/a0dp/index.m3u8"),
        ("yt", "https://www.youtube.com/c/todonoticias/live"),
    ]),
    ("america", "América", "https://i.imgur.com/Jt7dOQm.png", [
        ("hls", "https://prepublish.f.qaotic.net/a07/americahls-100056/playlist_720p.m3u8"),
    ]),
    ("elnueve", "El Nueve", "https://i.imgur.com/EtcVSm4.png", [
        ("hls", "http://15.204.246.24:8080/elnueveHD/index.m3u8"),
        ("hls", "http://45.226.28.9:8085/Live/18e292ea93b66c65c76707f07c489d61/local-canal9.playlist.m3u8"),
    ]),
    ("tvpublica", "Televisión Pública", "https://i.imgur.com/4hYYpiu.png", [
        ("hls", "http://190.128.214.97:64333/play/a008/index.m3u8"),
        ("yt", "https://www.youtube.com/user/TVPublicaArgentina/live"),
    ]),
    ("a24", "A24", "https://i.imgur.com/OdhF7ym.png", [
        ("hls", "http://138.59.227.20:8000/play/a05u/index.m3u8"),
        ("yt", "https://www.youtube.com/c/A24com/live"),
    ]),
    ("c5n", "C5N", "https://i.imgur.com/E3pamA5.png", [
        ("yt", "https://www.youtube.com/c/c5n/live"),
    ]),
    ("lnmas", "LN+", "https://i.imgur.com/vJYzGt1.png", [
        ("yt", "https://www.youtube.com/c/LaNacionMas/live"),
    ]),
    ("cronica", "Crónica TV", "https://i.imgur.com/k2Ku8Ib.png", [
        ("yt", "https://www.youtube.com/c/cronicatv/live"),
    ]),
    ("canal26", "Canal 26", "https://i.imgur.com/5pAaVih.png", [
        ("hls", "https://stream-gtlc.telecentro.net.ar/hls/canal26hls/main.m3u8"),
    ]),
    ("deportv", "DeporTV", "https://i.imgur.com/iyYLNRt.png", [
        ("hls", "http://158.172.155.130:8000/play/a09y/index.m3u8"),
        ("hls", "https://5fb24b460df87.streamlock.net/live-cont.ar/deportv/playlist.m3u8"),
    ]),
    ("cinear", "Cine.AR", "https://i.imgur.com/RPLyrIC.png", [
        ("hls", "https://5fb24b460df87.streamlock.net/live-cont.ar/cinear/playlist.m3u8"),
    ]),
]

def square(url):
    # Pasa el logo por un resizer: lo deja cuadrado, entero (sin recortar) y con fondo blanco
    return "https://wsrv.nl/?url=" + quote(url, safe="") + "&w=400&h=400&fit=contain&cbg=white&output=png"

def w(path, data):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

w("manifest.json", {
    "id": "ar.daniel.tvargentina.v2",
    "version": "2.1.0",
    "name": "TV Argentina (principales)",
    "description": "Canales de aire argentinos: El Trece, Telefe, TN, América y más.",
    "resources": ["catalog", "meta", "stream"],
    "types": ["tv"],
    "idPrefixes": [PREFIX],
    "catalogs": [{"type": "tv", "id": "tvar", "name": "TV Argentina"}],
})

metas = []
for cid, name, logo, streams in CHANNELS:
    mid = PREFIX + cid
    meta = {"id": mid, "type": "tv", "name": name, "poster": f"{SITE_URL}/logos/{cid}.png?v=3", "logo": f"{SITE_URL}/logos/{cid}.png?v=3",
            "posterShape": "square", "description": f"{name} en vivo"}
    metas.append(meta)
    w(f"meta/tv/{mid}.json", {"meta": meta})
    out = []
    n_hls = 0
    for kind, url in streams:
        if kind == "hls":
            n_hls += 1
            out.append({"name": name, "title": f"En vivo (opción {n_hls})" if sum(1 for k,_ in streams if k=='hls') > 1 else "En vivo", "url": url})
        else:
            out.append({"name": name, "title": "En vivo (abre YouTube)", "externalUrl": url})
    w(f"stream/tv/{mid}.json", {"streams": out})

w("catalog/tv/tvar.json", {"metas": metas})
open(os.path.join(OUT, ".nojekyll"), "w").close()
if os.path.isdir(os.path.join(BASE, "logos")):
    shutil.copytree(os.path.join(BASE, "logos"), os.path.join(OUT, "logos"))
print("OK", len(metas), "canales")
