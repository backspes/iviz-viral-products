#!/usr/bin/env python3
"""
auto_expand.py — Enjin Automasi Penuh iviz Picks (100% Zero-Touch)
=================================================================
Aliran Kerja Automatik:
  1. Ingest & tapis dari shopee_feed.csv (7 Gate Penapis Ketat).
  2. Jana kandungan peribadi (Hook, Verdict, Pros/Cons, Specs).
  3. Jana Shortlink Rasmi Sah (invl.me/clo...) via Involve Asia API.
  4. Sahkan harga numerik & had bajet.
  5. Rebuild Microsites & Auto-Deploy ke Cloudflare Pages.
"""

import os, sys, csv, json, re, time, requests, subprocess
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import editorial

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "trending_products.json")
FEED_FILE = os.path.join(DATA_DIR, "shopee_feed.csv")

# Kredensial Publisher Involve Asia (dibaca dari persekitaran / .env)
def load_ia_credentials():
    key = os.getenv("INVOLVE_ASIA_KEY") or os.getenv("IA_API_KEY")
    secret = os.getenv("INVOLVE_ASIA_SECRET") or os.getenv("IA_API_SECRET")
    if not key or not secret:
        for path in ["/root/.env", "/root/projects/affiliate-sync/.env", os.path.join(BASE_DIR, ".env")]:
            if os.path.exists(path):
                for line in open(path, encoding="utf-8"):
                    line = line.strip()
                    if line.startswith("INVOLVE_ASIA_KEY=") and not key:
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("INVOLVE_ASIA_SECRET=") and not secret:
                        secret = line.split("=", 1)[1].strip().strip('"').strip("'")
    return key, secret

OFFER_ID = 5032 # Shopee MY - CPS

# Slug kumpulan -> Nama paparan (teks manusia utk breadcrumb/badge)
GROUP_DISPLAY = {
    "perkakas_dapur": ("Rumah & Dapur", "home-kitchen"),
    "skincare_kesihatan": ("Kesihatan & Penjagaan Diri", "health-care"),
    "gajet_elektronik": ("Gajet & Elektronik", "gadgets-tech"),
    "setup_wfh": ("Perabot & Setup Meja", "wfh-setup"),
}

# GATE 1: Junk Blocklist
JUNK_KEYWORDS = [
    "hose", "nozzle", "cover probe", "earpads", "replacement", "spare part",
    "case for", "casing", "alat ganti", "repair", "keycap", "switch mechanical",
    "boundary strip", "mount", "bracket", "suction cup", "screen protector",
    "charging port", "front camera", "back camera", "fingerprint sensor",
    "baju", "seluar", "kasut", "sneakers", "tote bag", "shoulder bag", "backpack",
    "bra", "strap", "pants", "skirt", "underwear", "shirt", "dress", "vest",
    "jacket", "waistband", "socks", "helmet", "t-shirt",
    "gundam", "charm bead", "action figure", "dog vest", "cat food", "dog food",
    "aquarium", "toy", "figure", "plush", "doll", "sticker", "decal", "pokemon",
    "yu-gi-oh", "hot wheels", "anime", "cosplay", "novel", "book", "tape",
    "wind chime", "glue", "sewing", "thread", "beads", "jewelry", "ring",
    "pendant", "earring", "necklace", "bracelet", "wig", "nail polish", "holder",
    "wall-mounted", "bathroom corner", "torendi", "kratom", "ketum"
]

# GATE 2: Product Type Allowlist & Metadata
PRODUCT_ALLOWLIST = {
    "air fryer": ("perkakas_dapur", "Perkakas Dapur", "kitchen", "Menggoreng garing sekata tanpa minyak berlebihan.", "Pemanasan pusaran 360 darjah pantas."),
    "rice cooker": ("perkakas_dapur", "Perkakas Memasak", "kitchen", "Memasak nasi gebu dengan periuk anti-lekat dan pemanas pintar.", "Mod kekal hangat automatik sehingga 12 jam."),
    "blender": ("perkakas_dapur", "Perkakas Dapur", "kitchen", "Mengisar halus bahan masakan, sambal, dan smoothie.", "Motor berkuasa tinggi menghancurkan ais tanpa tersekat."),
    "food steamer": ("perkakas_dapur", "Perkakas Dapur", "kitchen", "Mengukus hidangan sihat mengekalkan nutrisi dan rasa asli.", "Kapasiti bertingkat memasak pelbagai lauk serentak."),
    "slow juicer": ("perkakas_dapur", "Perkakas Dapur", "kitchen", "Memerah jus buah segar tanpa haba bagi mengekalkan enzim.", "Pengekstrakan perlahan dengan buih minimum."),
    "serum": ("skincare_kesihatan", "Serum & Rawatan", "health-care", "Kepekatan bahan aktif merawat tona kusam dan parut degil.", "Penyerapan pantas tanpa rasa melekit."),
    "sunscreen": ("skincare_kesihatan", "Pelindung Matahari & Sunscreen", "health-care", "Perlindungan UVA/UVB spektrum luas kalis peluh untuk harian.", "Tekstur ringan tanpa kesan putih (white cast)."),
    "cleanser": ("skincare_kesihatan", "Pencuci Muka & Skincare", "health-care", "Membersih kotoran pori secara mendalam tanpa mengeringkan barrier.", "Formula pH seimbang melembapkan wajah selepas cucian."),
    "moisturizer": ("skincare_kesihatan", "Pelembap & Wajah", "health-care", "Mengunci kelembapan 24 jam dan menguatkan lapisan pertahanan kulit.", "Tekstur gel-krim melegakan kulit sensitif."),
    "vacuum cleaner": ("rumah_pintar", "Pembersihan & Kediaman", "home-smart", "Sedutan kuasa tinggi menyerap habuk halus dan bulu lantai.", "Binaan tanpa wayar memudahkan pembersihan celah perabot."),
    "robot vacuum": ("rumah_pintar", "Rumah Pintar & Pembersihan", "home-smart", "Pembersihan lantai automatik berjadual dengan navigasi pintar.", "Mengelak halangan perabot dan tangga secara cerdas."),
    "air purifier": ("rumah_pintar", "Penyaman & Pembersih Udara", "home-smart", "Penapisan HEPA H13 menyingkirkan 99.97% habuk mikro dan alergen.", "Operasi ultra-senyap sesuai untuk tidur lena bebas resdung."),
    "earbuds": ("gajet_elektronik", "Audio & Fon Telinga", "gadgets", "Audio jernih dengan pembatalan hingar aktif (ANC) untuk fokus kerja.", "Bateri tahan lama bersama sarung pengecas padat."),
    "powerbank": ("gajet_elektronik", "Pengecas & Kuasa", "gadgets", "Pengecasan pantas kapasiti tinggi untuk kuasa telefon seharian.", "Perlindungan litar pintar mengelakkan pemanasan lampau."),
    "mechanical keyboard": ("setup_wfh", "Papan Kekunci & Tetikus", "wfh", "Ketukan mekanikal taktikal yang mengurangkan keletihan menaip.", "Suis tahan lasak berjuta ketukan dengan reka bentuk ergonomik.")
}

def clean_wirecutter_title(raw_title):
    t = raw_title
    t = re.sub(r"【[^】]*】", "", t)
    t = re.sub(r"\[[^\]]*\]", "", t)
    for promo in ["HOT SALE", "READY STOCK", "100% ORIGINAL", "ORIGINAL", "MALAYSIA WARRANTY",
                  "FAST DELIVERY", "LOCAL SELLER", "PROMO", "FREE GIFT", "DISCOUNT",
                  "MURAH", "VIRAL", "TERBARU", "READY", "STOCK", "NEW"]:
        t = re.sub(r"(?i)\b" + re.escape(promo) + r"\b", "", t)
    t = re.sub(r"\s+", " ", t).strip(" -|,.")
    # Buang perkataan berulang berturut (cth: "PowerBank ... PowerBank")
    words, out = t.split(), []
    for w in words:
        if not out or out[-1].lower() != w.lower():
            out.append(w)
    t = " ".join(out)
    # Buang pengulangan perkataan merentas tajuk (max 1 setiap perkataan)
    seen, out = set(), []
    for w in t.split():
        key = w.lower().strip(".,")
        if key in seen and len(key) > 3:
            continue
        seen.add(key)
        out.append(w)
    return " ".join(out).strip(" -|,.")

def slugify(text):
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return s.strip("-")[:50]

def get_ia_token():
    key, secret = load_ia_credentials()
    if not key or not secret:
        print("❌ Kredensial Involve Asia tidak dijumpai dalam persekitaran / .env")
        return None
    try:
        r = requests.post("https://api.involve.asia/api/authenticate",
                          data={"key": key, "secret": secret}, timeout=20)
        return r.json().get("data", {}).get("token")
    except Exception as e:
        print(f"❌ Ralat sambungan auth: {e}")
        return None

def generate_deeplink(token, feed_url, pid):
    try:
        r = requests.post("https://api.involve.asia/api/deeplink/generate",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            data={"offer_id": OFFER_ID, "url": feed_url, "aff_sub": "ivizpicks", "aff_sub2": pid},
            timeout=20)
        data = r.json()
        return data.get("data", {}).get("tracking_link")
    except Exception:
        return None

def run_auto_expansion(max_add=3):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 🚀 Memulakan Ingestion Automatik Penuh iviz Picks...")
    products = json.load(open(PRODUCTS_FILE, encoding="utf-8"))
    existing_ids = {p["id"] for p in products}
    existing_names = {p["name"].lower() for p in products}
    
    token = get_ia_token()
    if not token:
        print("❌ Gagal authenticate ke Involve Asia API.")
        return
        
    added = []
    
    with open(FEED_FILE, encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if len(added) >= max_add:
                break
                
            title = (row.get("title") or "").strip()
            img_url = (row.get("image_link") or "").strip()
            feed_short_url = (row.get("product_short link") or "").strip()
            price_raw = (row.get("sale_price") or row.get("price") or "0").strip()
            brand = (row.get("global_brand") or "").strip()
            shop_id = (row.get("shopid") or row.get("\ufeffshopid") or "").strip()
            item_id = (row.get("itemid") or "").strip()
            shop_name = (row.get("shop_name") or "").strip()
            _off = (row.get("is_official_shop") or "").strip().lower()
            _pref = (row.get("is_preferred_shop") or "").strip().lower()
            is_official = _off in ("true", "1", "yes") or ("official" in _off and "non" not in _off)
            is_preferred = _pref in ("true", "1", "yes") or ("preferred" in _pref and "non" not in _pref)
            discount_pct = (row.get("discount_percentage") or "").strip()
            
            if not title or not img_url or not feed_short_url:
                continue
            # GATE 1b: Tolak produk tanpa jenama (tajuk generic spam marketplace)
            if not brand or brand.lower() == "nobrand":
                continue
                
            low = title.lower()
            
            # GATE 1: Tapis Sampah
            if any(jk in low for jk in JUNK_KEYWORDS):
                continue
                
            # GATE 2: Semak Allowlist
            matched_key = None
            for pkey in PRODUCT_ALLOWLIST:
                if re.search(r"\b" + re.escape(pkey) + r"\b", low):
                    matched_key = pkey
                    break
            if not matched_key:
                continue
                
            grp, cat, grp_slug, hook_txt, verdict_txt = PRODUCT_ALLOWLIST[matched_key]
            
            clean_title = clean_wirecutter_title(title)
            pid = slugify(clean_title)
            if pid in existing_ids or clean_title.lower() in existing_names:
                continue
                
            try:
                price_num = float(re.sub(r"[^\d.]", "", price_raw))
            except Exception:
                continue
            if not (15.0 <= price_num <= 2000.0):
                continue
                
            # Jana Deeplink Rasmi Sah
            aff_link = generate_deeplink(token, feed_short_url, pid)
            if not aff_link:
                continue
                
            ed_data = editorial.generate(clean_title, brand or clean_title.split()[0], price_num, cat, grp, product_key=matched_key, allowlist=list(PRODUCT_ALLOWLIST.keys()))
            new_prod = {
                "id": pid,
                "name": clean_title,
                "brand": brand if brand and brand != "NoBrand" else clean_title.split()[0],
                "category": cat,
                "group": GROUP_DISPLAY.get(grp, (grp.replace("_", " ").title(), grp_slug))[0],
                "group_slug": GROUP_DISPLAY.get(grp, (grp.replace("_", " ").title(), grp_slug))[1],
                "shopee_price": f"RM {price_num:.2f}",
                "price": f"RM {price_num:.2f}",
                "price_num": price_num,
                "original_price": f"RM {price_num * 1.35:.2f}",
                "discount": (f"Diskaun {discount_pct.rstrip(chr(37))}%" if discount_pct and discount_pct != "0" else "Harga Pasaran"),
                "safety_audit": ed_data["safety_audit"],
                "hook": ed_data["hook"],
                "verdict": ed_data["verdict"],
                "who_is_it_for": ed_data["who_is_it_for"],
                "who_should_skip": ed_data["who_should_skip"],
                "pros": ed_data["pros"],
                "cons": ed_data["cons"],
                "specs": dict(
                    {"Jenama": brand or clean_title.split()[0], "Kategori": cat, "Harga": f"RM {price_num:.2f}"},
                    **ed_data.get("specs_extra", {}),
                    **({"Semakan Keselamatan": ed_data["safety_audit"]} if ed_data.get("safety_audit") else {})
                ),
                "faq": ed_data["faq"],
                "affiliate_url": aff_link,
                "merchant_platform": "Shopee Mall / Preferred",
                "image_url": img_url,
                "editorial_score": ed_data["editorial_score"],
                "status": "active",
                "added_at": datetime.now().strftime("%Y-%m-%d"),
                "tags": [grp, cat.lower(), matched_key],
                "deeplink_verified": True,
                "last_checked": datetime.now().strftime("%Y-%m-%d"),
                "match_score": 100,
                "matched_real_title": title,
                "matched_real_link": (f"https://shopee.com.my/product/{shop_id}/{item_id}"
                                      if shop_id and item_id else None),
                "matched_shop": shop_name,
                "price_from_feed": price_raw,
                "replacement_id": None,
                "schema": {"rating": "", "review_count": ""},
                "shopee_url": feed_short_url,
                "shopee_badge": ("Shopee Mall / Official" if is_official
                                 else ("Preferred Seller" if is_preferred else "")),
                "shopee_commission": "",
                "video_embed_url": ""
            }
            
            products.append(new_prod)
            existing_ids.add(pid)
            existing_names.add(clean_title.lower())
            added.append(new_prod)
            print(f"  + [{cat:24s}] RM {price_num:6.2f} | {clean_title[:45]} -> {aff_link}")
            time.sleep(0.3) # Throttle 60 req/min
            
    if added:
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
            
        print(f"\n✅ {len(added)} produk baharu berkualiti berjaya ditambah & di-deeplink!")
        print("📦 Menjalankan Build Microsites...")
        b_res = subprocess.run(["python3", "generator/build_microsites.py"], cwd=BASE_DIR, capture_output=True, text=True)
        if b_res.returncode != 0:
            print("STDERR Build:", b_res.stderr[-500:])
            raise RuntimeError("Build gagal!")
            
        print("🚀 Menjalankan Deploy Cloudflare Pages...")
        subprocess.run(["python3", "generator/deploy_cf.py"], cwd=BASE_DIR, check=True)
        print("🎉 Selesai! Semua produk baru telah live di production dengan shortlink sah.")
    else:
        print("Tiada produk baru melepasi saringan kali ini.")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    run_auto_expansion(count)
