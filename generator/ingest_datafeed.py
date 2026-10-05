"""
Ingest Involve Asia Datafeed CSV -> parse real product image URLs, real prices, real deeplinks.
Zero images saved to VM disk: HTML links directly to Involve/merchant image CDN URL.

Usage:
    python3 generator/ingest_datafeed.py <path_to_csv>
"""

import sys
import os
import csv
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "trending_products.json")


def inspect_feed(csv_path):
    """Detect dialect, delimiter, and map column headers."""
    # Check encoding (utf-8, utf-8-sig, latin-1)
    for enc in ["utf-8-sig", "utf-8", "latin-1"]:
        try:
            with open(csv_path, "r", encoding=enc) as f:
                header_line = f.readline()
                dialect = csv.Sniffer().sniff(header_line)
                delim = dialect.delimiter
                f.seek(0)
                reader = csv.reader(f, delimiter=delim)
                headers = [h.strip() for h in next(reader)]
                return enc, delim, headers
        except Exception:
            continue
    raise RuntimeError(f"Could not parse CSV: {csv_path}")


def map_columns(headers):
    """Fuzzy-map standard affiliate feed columns to canonical names."""
    h_lower = {h.lower(): h for h in headers}

    def find_match(*candidates):
        for c in candidates:
            for k in h_lower:
                if c in k:
                    return h_lower[k]
        return None

    mapping = {
        "title": find_match("product_name", "product name", "title", "name", "item_name"),
        "image_url": find_match("image_url", "image url", "image", "img_url", "picture"),
        "price": find_match("sale_price", "saleprice", "price", "current_price"),
        "original_price": find_match("original_price", "retail_price", "regular_price", "was_price", "strike"),
        "deeplink": find_match("affiliate_url", "affiliate_link", "tracking_url", "deeplink", "url", "link"),
        "product_url": find_match("product_url", "landing_url", "target_url"),
        "brand": find_match("brand", "manufacturer"),
        "category": find_match("category", "category_name", "dept"),
        "sku": find_match("sku", "product_id", "item_id", "id"),
        "currency": find_match("currency"),
    }
    return mapping


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generator/ingest_datafeed.py <datafeed.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        sys.exit(1)

    print(f"Inspecting feed: {csv_path}")
    enc, delim, headers = inspect_feed(csv_path)
    print(f"Encoding: {enc} | Delimiter: {repr(delim)} | Total columns: {len(headers)}")

    mapping = map_columns(headers)
    print("Column mapping detected:")
    for k, v in mapping.items():
        print(f"  {k:15}: {v}")

    if not mapping["title"] or not mapping["image_url"]:
        print("ERROR: Could not detect title or image_url column.")
        sys.exit(1)

    # Load existing trending_products.json to match by name/brand
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        existing = json.load(f)

    print(f"\nExisting products to update: {len(existing)}")

    # Read feed rows
    updated_count = 0
    with open(csv_path, "r", encoding=enc) as f:
        reader = csv.DictReader(f, delimiter=delim)
        all_rows = list(reader)

    print(f"Feed rows parsed: {len(all_rows)}")

    # Match each existing product against feed
    for prod in existing:
        prod_name_norm = prod["name"].lower()
        prod_brand_norm = prod.get("brand", "").lower()

        best_match = None
        best_score = 0

        for row in all_rows:
            feed_title = (row.get(mapping["title"]) or "").strip()
            if not feed_title:
                continue

            feed_title_norm = feed_title.lower()

            # Word overlap score
            words_prod = set(re.findall(r"\w+", prod_name_norm))
            words_feed = set(re.findall(r"\w+", feed_title_norm))
            overlap = len(words_prod & words_feed)

            # Extra weight if brand is explicitly in title
            if prod_brand_norm and prod_brand_norm in feed_title_norm:
                overlap += 3

            if overlap > best_score:
                best_score = overlap
                best_match = row

        if best_match and best_score >= 4:
            img = (best_match.get(mapping["image_url"]) or "").strip()
            price = (best_match.get(mapping["price"]) or "").strip()
            orig = (best_match.get(mapping.get("original_price") or "") or "").strip()
            link = (best_match.get(mapping["deeplink"]) or "").strip()

            if img:
                prod["image_url"] = img
            if price:
                try:
                    price_num = float(re.sub(r"[^\d.]", "", price))
                    prod["shopee_price"] = f"RM {price_num:.2f}"
                    prod["price_num"] = f"{price_num:.2f}"
                except Exception:
                    pass
            if orig:
                try:
                    orig_num = float(re.sub(r"[^\d.]", "", orig))
                    prod["original_price"] = f"RM {orig_num:.2f}"
                except Exception:
                    pass
            if link:
                prod["affiliate_url"] = link

            print(f"✅ Matched [{prod['id']}]: score={best_score}")
            print(f"   Image: {prod['image_url'][:80]}...")
            print(f"   Price: {prod['shopee_price']}")
            updated_count += 1
        else:
            print(f"⚠️ No strong match for [{prod['id']}] (best_score={best_score})")

    # Save updated file
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)

    print(f"\nDone: {updated_count}/{len(existing)} products updated.")
    print("Zero images saved to VM disk — using external CDN URLs directly.")


if __name__ == "__main__":
    main()
