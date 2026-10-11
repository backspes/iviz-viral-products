#!/usr/bin/env python3
"""
Auto-heal affiliate_url: jana deeplink Involve Asia untuk produk yang masih
kosong affiliate_url (drip-feed baharu). Dipanggil dari auto_update.sh
SEBELUM build — kalau API IA down (500), langkau senyap; build tetap jalan
dengan fallback matched_real_link (lihat get_outbound_url dalam build_microsites).

Usage: python3 generator/refresh_affiliate_links.py
"""
import json, os, sys, time, csv, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODS_FILE = os.path.join(ROOT, "data", "trending_products.json")
FEED_FILE = os.path.join(ROOT, "data", "shopee_feed.csv")
OFFER_ID = 5032  # Shopee MY - CPS

def main():
    prods = json.load(open(PRODS_FILE))
    todo = [p for p in prods
            if p.get("status") == "active" and not str(p.get("affiliate_url", "")).strip()]
    if not todo:
        print("  🔗 Affiliate links: semua produk sudah ada tracking link.")
        return 0
    print(f"  🔗 Affiliate links: {len(todo)} produk tanpa tracking link...")

    sys.path.insert(0, os.path.join(ROOT, "docs", "involve-asia"))
    try:
        from generate_deeplink import load_creds, authenticate, generate
    except Exception as e:
        print(f"  ⚠️  Affiliate links: helper IA tak boleh dimuat ({e}) — langkau.")
        return 0
    try:
        key, secret = load_creds()
        token = authenticate(key, secret)
    except SystemExit:
        print("  ⚠️  Affiliate links: kredensial tiada — langkau.")
        return 0
    except Exception as e:
        print(f"  ⚠️  Affiliate links: auth gagal ({e}) — langkau.")
        return 0

    # peta shopid/itemid -> URL feed asal (syarat API: url mesti dari domain whitelist)
    feed_map = {}
    if os.path.exists(FEED_FILE):
        with open(FEED_FILE, encoding="utf-8", errors="ignore") as fh:
            for r in csv.DictReader(fh):
                sid = r.get("shopid") or r.get("\ufeffshopid")
                iid = r.get("itemid")
                if not sid or not iid:
                    continue
                link = r.get("product_short link") or r.get("product_link") or ""
                if "an_redir" in link:
                    feed_map[f"{sid}/{iid}"] = link

    from urllib.parse import quote
    ok = fail = 0
    for p in todo:
        m = re.search(r"/product/(\d+)/(\d+)", p.get("matched_real_link", ""))
        if not m:
            fail += 1
            continue
        url = feed_map.get(f"{m.group(1)}/{m.group(2)}") or \
              f"https://shope.ee/an_redir?origin_link={quote(p['matched_real_link'], safe='')}"
        try:
            status, body = generate(token, OFFER_ID, url, aff_sub=p["id"])
        except Exception:
            status, body = 0, {}
        if status == 200 and body.get("status") == "success":
            p["affiliate_url"] = body["data"]["tracking_link"]
            ok += 1
            print(f"    ✅ {p['id']} -> {p['affiliate_url']}")
        else:
            fail += 1
        time.sleep(1.2)  # hormat rate limit 60 req/min
        if ok >= 3 and fail >= 3:
            # API nampak down merentas beberapa percubaan — jangan bazir masa
            print("    ⚠️  API nampak bermasalah berterusan — henti percubaan, cuba lagi run seterusnya.")
            break

    if ok:
        json.dump(prods, open(PRODS_FILE, "w"), indent=2, ensure_ascii=False)
    print(f"  🔗 Affiliate links: {ok} berjaya, {fail} berbaki (akan dicuba lagi run seterusnya).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
