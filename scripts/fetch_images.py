#!/usr/bin/env python3
"""Copy every photo the site uses from the current theakosart.gr media library
into assets/img, so the new site no longer depends on the old one.

Run from the repo root on your own computer:
    python3 scripts/fetch_images.py
    python3 build.py
Files that do not exist on the old server are skipped (the pages fall back
to the smaller version automatically).
"""
import os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.theakosart.gr/wp-content/uploads/"
out = os.path.join(ROOT, "assets", "img")
os.makedirs(out, exist_ok=True)
ok = miss = 0
for line in open(os.path.join(ROOT, "scripts", "images.txt"), encoding="utf-8"):
    path = line.strip()
    if not path:
        continue
    dest = os.path.join(out, path.replace("/", "_"))
    if os.path.exists(dest):
        ok += 1
        continue
    try:
        req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            f.write(r.read())
        ok += 1
        print("saved  ", path)
    except Exception as err:
        miss += 1
        print("skipped", path, "(%s)" % err)
print("%d photos in assets/img, %d skipped" % (ok, miss))
