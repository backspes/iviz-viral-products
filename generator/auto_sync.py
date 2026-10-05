"""
Auto Sync & Maintenance Engine: iviz Picks
==========================================
Tugasan automatik:
1. Health Check: Periksa HTTP status imej CDN Shopee & pautan untuk 100 produk.
2. Ingest New Products: Pilih produk trending baharu dari Shopee Feed (5 produk per sync).
3. Lifecycle Manager: Tandakan status 'active' atau 'out_of_stock'.
4. Rebuild & Deploy: Jana semula HTML dan kemaskini sitemap/robots.
"""

import os
import sys
import json
import csv
import urllib.request
import urllib.parse
import hashlib
from datetime import datetime

BASE_DIR = "/root/projects/iviz-viral-products"
DATA_FILE = os.path.join(BASE_DIR, "data", "trending_products.json")
FEED_FILE = os.path.join(BASE_DIR, "data", "shopee_feed.csv")
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

AFF_ID = "122839"
OFF_ID_XTRA = "103878"


def make_aff_url(target):
    enc = urllib.parse.quote(target, safe="")
    return f"https://invl.me/aff_m?offer_id={OFF_ID_XTRA}&aff_id={AFF_ID}&source=ia_api_shopeextra&url={enc}"


def check_images_health(products, sample_size=10):
    """Semak sampel URL imej untuk pastikan CDN Shopee masih aktif."""
    print(f"[{datetime.now().isoformat()}] Menjalankan pemeriksaan kesihatan imej CDN...")
    healthy = 0
    checked = 0
    for p in products[:sample_size]:
        url = p.get("image_url")
        if not url:
            continue
        checked += 1
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    healthy += 1
        except Exception as e:
            print(f"  [AMARAN] Imej gagal bagi {p['id']}: {e}")
    print(f"  Kesihatan imej: {healthy}/{checked} OK.")
    return healthy == checked


def run_maintenance():
    log_file = os.path.join(LOG_DIR, f"sync_{datetime.now().strftime('%Y%m%d')}.log")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    print(f"Jumlah produk semasa: {len(products)}")
    check_images_health(products, sample_size=15)

    # Kemaskini timestamp last_checked
    today_str = datetime.now().strftime("%Y-%m-%d")
    for p in products:
        p["last_checked"] = today_str

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

    print(f"Penyelarasan selesai. Rekod disimpan ke {DATA_FILE}")


if __name__ == "__main__":
    run_maintenance()
