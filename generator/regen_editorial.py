#!/usr/bin/env python3
"""
regen_editorial.py — Sembuhkan ulasan boilerplate dalam trending_products.json
=============================================================================
Kenal pasti produk yang teksnya generic (tepat sama untuk semua produk
satu kategori), jana semula hook/verdict/who/pros/cons/faq/score dengan
modul editorial.py (spesifik ikut jenis + spesifikasi sebenar).

Guna:
  python3 generator/regen_editorial.py           # semak sahaja
  python3 generator/regen_editorial.py --apply   # tulis + rebuild + deploy
"""

import os
import sys
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "generator"))

import editorial  # noqa: E402
from auto_expand import PRODUCT_ALLOWLIST  # noqa: E402

PRODUCTS_FILE = os.path.join(BASE_DIR, "data", "trending_products.json")

GENERIC_WHO_PREFIX = "Pengguna yang memerlukan"
GENERIC_SKIP = "Pengguna yang sudah mempunyai model gred komersil"
GENERIC_PROS = {
    "Kualiti binaan kukuh dan tahan lasak.",
    "Prestasi terbukti dengan ulasan pembeli positif.",
    "Nilai belian praktikal.",
}
# Teks hook/verdict dari PRODUCT_ALLOWLIST = generic per kategori
GENERIC_HOOKS = {v[3] for v in PRODUCT_ALLOWLIST.values()}
GENERIC_VERDICTS = {v[4] for v in PRODUCT_ALLOWLIST.values()}


def is_generic(p):
    if p.get("who_is_it_for", "").startswith(GENERIC_WHO_PREFIX):
        return True
    if GENERIC_SKIP in p.get("who_should_skip", ""):
        return True
    if set(p.get("pros", [])) == GENERIC_PROS:
        return True
    if p.get("hook") in GENERIC_HOOKS and p.get("verdict") in GENERIC_VERDICTS:
        return True
    return False


def main():
    apply = "--apply" in sys.argv
    products = json.load(open(PRODUCTS_FILE, encoding="utf-8"))
    allowlist_keys = list(PRODUCT_ALLOWLIST.keys())

    regen = 0
    for p in products:
        if not is_generic(p):
            continue
        new = editorial.generate(
            name=p.get("name", ""),
            brand=p.get("brand", ""),
            price_num=p.get("price_num", 0),
            category=p.get("category", ""),
            group=p.get("group", ""),
            allowlist=allowlist_keys,
        )
        p.update(new)
        regen += 1
        print(f"  ↻ {p['name'][:55]}")

    print(f"\n{regen} produk dijana semula daripada {len(products)} total.")

    if not apply:
        print("Belum ditulis. Guna --apply untuk simpan + rebuild + deploy.")
        return

    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print("📦 Rebuild microsites...")
    b = subprocess.run([sys.executable, "generator/build_microsites.py"],
                       cwd=BASE_DIR, capture_output=True, text=True)
    if b.returncode != 0:
        print(b.stderr[-800:])
        raise SystemExit("Build gagal!")
    print(b.stdout[-300:])

    print("🚀 Deploy Cloudflare Pages...")
    d = subprocess.run([sys.executable, "generator/deploy_cf.py"],
                       cwd=BASE_DIR, capture_output=True, text=True)
    print("Deploy:", "OK" if d.returncode == 0 else d.stderr[-300:])
    print("✅ Selesai.")


if __name__ == "__main__":
    main()
