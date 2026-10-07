#!/usr/bin/env python3
"""
Involve Asia Publisher API — helper.

Guna untuk:
  - Semak status akaun (auth + bilangan offer).
  - Jana deeplink yang dijejak ke akaun publisher (aff_id).

Kredensial dibaca dari /root/.env (INVOLVE_ASIA_KEY, INVOLVE_ASIA_SECRET).
JANGAN cetak kredensial ke output.

Rujuk skill.md / llms.txt dalam folder ini untuk dokumentasi penuh.
"""
import argparse
import os
import sys
import json
import requests

API = "https://api.involve.asia/api"
ENV_CANDIDATES = ["/root/.env", "/root/projects/affiliate-sync/.env"]


def load_creds():
    key = secret = None
    for path in ENV_CANDIDATES:
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line.startswith("INVOLVE_ASIA_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("INVOLVE_ASIA_SECRET="):
                secret = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key or not secret:
        sys.exit("Kredensial Involve Asia tidak dijumpai dalam .env")
    return key, secret


def authenticate(key, secret):
    r = requests.post(f"{API}/authenticate",
                      data={"key": key, "secret": secret},
                      headers={"Accept": "application/json"}, timeout=20)
    r.raise_for_status()
    return r.json()["data"]["token"]


def generate(token, offer_id, url, aff_sub=None, aff_sub2=None):
    payload = {"offer_id": offer_id, "url": url}
    if aff_sub:
        payload["aff_sub"] = aff_sub
    if aff_sub2:
        payload["aff_sub2"] = aff_sub2
    r = requests.post(f"{API}/deeplink/generate",
                      headers={"Authorization": f"Bearer {token}",
                               "Accept": "application/json"},
                      data=payload, timeout=20)
    return r.status_code, r.json()


def main():
    ap = argparse.ArgumentParser(description="Involve Asia deeplink helper")
    ap.add_argument("--offer-id")
    ap.add_argument("--url")
    ap.add_argument("--aff-sub", default="ivizpicks")
    ap.add_argument("--aff-sub2")
    ap.add_argument("--check", action="store_true", help="Semak status akaun sahaja")
    args = ap.parse_args()

    key, secret = load_creds()
    token = authenticate(key, secret)

    if args.check or not args.url:
        r = requests.post(f"{API}/offers/all",
                          headers={"Authorization": f"Bearer {token}",
                                   "Accept": "application/json"},
                          data={"limit": 200}, timeout=30)
        offers = r.json().get("data", {}).get("data", [])
        shopee = [o for o in offers if "shopee" in str(o.get("offer_name", "")).lower()]
        print(f"✅ Auth berjaya. {len(offers)} offer boleh akses.")
        print("Offer Shopee:")
        for o in shopee:
            print(f"  - {o.get('offer_id')} | {o.get('offer_name')}")
        return

    status, body = generate(token, args.offer_id, args.url, args.aff_sub, args.aff_sub2)
    if status == 200 and body.get("status") == "success":
        print("✅ Deeplink:", body["data"]["tracking_link"])
    else:
        # 500 pada Shopee = ralat kekal, jangan retry (lihat gotchas skill.md)
        print(f"❌ HTTP {status}: {body.get('message')!r}")
        sys.exit(1)


if __name__ == "__main__":
    main()
