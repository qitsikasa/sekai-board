#!/usr/bin/env python3
"""Genera web/js/data.js desde los assets locales + master DBs de sekai.
Requisitos: master DBs descargadas en /tmp/opencode/ (cards, events, musics,
character2ds, characterProfiles) — o rutas vía env SEKAI_DB.
Uso: python3 tools/gen_data.py
"""
import json, os, hashlib

ROOT = os.path.expanduser("~/Proyectos/prograweb/projectSekai")
DB = os.environ.get("SEKAI_DB", "/tmp/opencode")

man = json.load(open(ROOT + "/manifest.json"))
cards = {c["id"]: c for c in json.load(open(f"{DB}/cards.json"))}
events = {e["id"]: e for e in json.load(open(f"{DB}/events.json"))}
musics = {m["id"]: m for m in json.load(open(f"{DB}/musics.json"))}
c2 = json.load(open(f"{DB}/character2ds.json"))

NAMES = {1: "Ichika Hoshino", 2: "Saki Tenma", 3: "Honami Mochizuki", 4: "Shiho Hinomori",
         5: "Minori Hanasato", 6: "Haruka Kiritani", 7: "Airi Momoi", 8: "Shizuku Hinomori",
         9: "Kohane Azusawa", 10: "An Shiraishi", 11: "Akito Shinonome", 12: "Toya Aoyagi",
         13: "Tsukasa Tenma", 14: "Emu Otori", 15: "Nene Kusanagi", 16: "Rui Kamishiro",
         17: "Kanade Yoisaki", 18: "Mafuyu Asahina", 19: "Ena Shinonome", 20: "Mizuki Akiyama",
         21: "Hatsune Miku", 22: "Kagamine Rin", 23: "Kagamine Len", 24: "Megurine Luka",
         25: "MEIKO", 26: "KAITO"}
# ids = valores reales de character2ds.unit
UNITS = [
    {"id": "light_sound", "name": "Leo/need", "tag": "band", "color": "#00C2C7", "logo": "../logos/Leoneed logo.png"},
    {"id": "idol", "name": "MORE MORE JUMP!", "tag": "idol", "color": "#FF4D8D", "logo": "../logos/MORE MORE JUMP! logo.png"},
    {"id": "street", "name": "Vivid BAD SQUAD", "tag": "street", "color": "#4D7CFE", "logo": "../logos/Vivid BAD SQUAD logo.png"},
    {"id": "theme_park", "name": "Wonderlands × Showtime", "tag": "teatro", "color": "#FFB13D", "logo": "../logos/Wonderlands×Showtime logo.png"},
    {"id": "school_refusal", "name": "25:00 (Nightcord)", "tag": "night", "color": "#8B5CF6", "logo": "../logos/25-ji, Nightcord de. logo.png"},
    {"id": "piapro", "name": "Virtual Singer", "tag": "vocaloid", "color": "#33B1FF", "logo": "../logos/VIRTUAL SINGER logo.png"},
]
seen = {}
for c in c2:
    if c.get("characterType") == "game_character" and c["characterId"] not in seen:
        seen[c["characterId"]] = c
chars = []
for cid in range(1, 27):
    a = seen[cid]
    n = NAMES[cid]
    chars.append({"id": cid, "name": n, "first": n.split()[0], "unit": a["unit"],
                  "portrait": f"../characters/portraits/chr_tl_{cid:02d}.webp"})
ev_items = []
for e in man["event_banners"][::-1][:12]:
    meta = events.get(e["id"], {})
    ev_items.append({"id": e["id"], "name": meta.get("name", f'Evento #{e["id"]}'),
                     "banner": "../" + e["file"], "start": meta.get("startAt"),
                     "end": meta.get("closedAt"), "type": meta.get("eventType", "")})
song_items = []
for s in man["songs"][::46][:16]:
    meta = musics.get(s["id"], {})
    song_items.append({"id": s["id"], "title": meta.get("title", f'Song #{s["id"]}'),
                       "jacket": "../" + s["file"]})
booru = []
def favs(seed):
    return int(hashlib.md5(seed.encode()).hexdigest(), 16) % 2400 + 40
pool = man["cards_trained"][::-1]
sel = pool[:30]
# garantiza cobertura mínima de Miku (21) y Emu (14) en la galería
for need_cid, need_n in ((21, 4), (14, 4)):
    have = [e for e in sel if cards.get(e["id"], {}).get("characterId") == need_cid]
    for e in pool[30:]:
        if len(have) >= need_n:
            break
        if cards.get(e["id"], {}).get("characterId") == need_cid:
            sel.append(e)
            have.append(e)

def card_tags(ch, meta):
    parts = ["card", meta.get("attr", ""), ch["first"].lower(),
             ch["name"].split()[-1].lower(), ch["unit"]]
    out = []
    for t in parts:
        if t and t not in out:
            out.append(t)
    return out

for e in sel:
    meta = cards.get(e["id"], {})
    cid = meta.get("characterId", 1)
    ch = next(c for c in chars if c["id"] == cid)
    booru.append({"src": "../" + e["file"], "type": "card", "attr": meta.get("attr", ""),
                  "char": ch["first"],
                  "tags": card_tags(ch, meta),
                  "favs": favs(e["file"]), "w": 2338, "h": 1440})
for s in man["songs"][::70][:10]:
    booru.append({"src": "../" + s["file"], "type": "live", "tags": ["live", "music"],
                  "favs": favs(s["file"]), "w": 800, "h": 800})
for e in man["event_banners"][::-1][:8]:
    booru.append({"src": "../" + e["file"], "type": "event", "tags": ["event"],
                  "favs": favs(e["file"]), "w": 2338, "h": 1440})
data = {"units": UNITS, "characters": chars, "events": ev_items, "songs": song_items, "booru": booru}
out = "window.SEKAI = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n"
open(ROOT + "/web/js/data.js", "w").write(out)
missing = []
for it in booru + [{"src": s["jacket"]} for s in song_items] + [{"src": e["banner"]} for e in ev_items] + [{"src": c["portrait"]} for c in chars]:
    p = os.path.join(ROOT, it["src"].replace("../", ""))
    if not os.path.exists(p):
        missing.append(p)
print(f"data.js -> {len(out)} bytes; booru={len(booru)} events={len(ev_items)} missing={len(missing)}")
