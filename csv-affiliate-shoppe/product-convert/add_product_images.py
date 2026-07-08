#!/usr/bin/env python3
"""
Script to add 'รูปสินค้า' column to Shopee affiliate CSV files
by extracting image URLs from .txt files (saved HTML from Shopee Affiliate Portal).

Usage:
    python3 add_product_images.py

Input:
    - txt/*.txt  : HTML content saved from Shopee Affiliate Portal (1 or more files)
    - csv/*.csv  : CSV files exported from Shopee Affiliate (1 or more files)

Output:
    - Updates each CSV file in csv/ in-place, adding the 'รูปสินค้า' column
      with image URLs matched by product ID.

Directory structure:
    product-convert/
    ├── add_product_images.py
    ├── txt/                    ← วาง .txt files ที่ copy มาจากหน้า Shopee Affiliate
    │   ├── product_offer_list.txt
    │   └── product_offer_list (1).txt
    └── csv/                    ← วาง .csv files ที่ export จาก Shopee Affiliate
        ├── 5080.csv
        └── 5090.csv
"""

import csv
import re
import sys
import os
import glob

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
TXT_DIR      = os.path.join(SCRIPT_DIR, "txt")
CSV_DIR      = os.path.join(SCRIPT_DIR, "csv")
IMAGE_COLUMN = "รูปสินค้า"
ID_COLUMN    = "รหัสสินค้า"


def extract_product_images(txt_path: str) -> dict[str, str]:
    """Parse HTML/text content and return {product_id: image_url} mapping."""
    with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    pattern = re.compile(
        r'/offer/product_offer/(\d+)[^"]*"'
        r'.*?'
        r'<img src="(https?://[^"]+\.(?:webp|jpg|jpeg|png))"',
        re.DOTALL,
    )

    mapping: dict[str, str] = {}
    for match in pattern.finditer(content):
        product_id = match.group(1)
        image_url  = match.group(2)
        if product_id not in mapping:
            mapping[product_id] = image_url

    return mapping


def build_image_map_from_txt_dir(txt_dir: str) -> dict[str, str]:
    """อ่านทุก .txt ใน txt_dir แล้ว merge image map รวมกัน"""
    txt_files = sorted(glob.glob(os.path.join(txt_dir, "*.txt")))
    if not txt_files:
        print(f"ERROR: No .txt files found in {txt_dir}")
        sys.exit(1)

    combined: dict[str, str] = {}
    for path in txt_files:
        mapping = extract_product_images(path)
        new_ids = len([k for k in mapping if k not in combined])
        combined.update(mapping)
        print(f"  [{os.path.basename(path)}] → {len(mapping)} images ({new_ids} new)")

    return combined


def add_images_to_csv(csv_path: str, image_map: dict[str, str]) -> None:
    """Read CSV, add/update 'รูปสินค้า' column, write back in-place."""
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader    = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows      = list(reader)

    if IMAGE_COLUMN not in fieldnames:
        fieldnames.append(IMAGE_COLUMN)
        print(f"  Added column '{IMAGE_COLUMN}'")
    else:
        print(f"  Column '{IMAGE_COLUMN}' already exists — overwriting matched values")

    matched = 0
    missing = []

    for row in rows:
        product_id = str(row.get(ID_COLUMN, "")).strip()
        if product_id in image_map:
            row[IMAGE_COLUMN] = image_map[product_id]
            matched += 1
        else:
            if not row.get(IMAGE_COLUMN):
                row[IMAGE_COLUMN] = ""
            missing.append(product_id)

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Total: {len(rows)}  Matched: {matched}  Not matched: {len(missing)}")
    if missing:
        print(f"  Missing IDs: {', '.join(missing)}")


def main():
    # ── 1. build image map จากทุก .txt ใน txt/ ────────────────────────────────
    print(f"📂 อ่าน .txt จาก: {TXT_DIR}")
    image_map = build_image_map_from_txt_dir(TXT_DIR)
    print(f"✅ รวม {len(image_map)} image URLs จากทุกไฟล์\n")

    # ── 2. process ทุก .csv ใน csv/ ───────────────────────────────────────────
    csv_files = sorted(glob.glob(os.path.join(CSV_DIR, "*.csv")))
    if not csv_files:
        print(f"ERROR: No .csv files found in {CSV_DIR}")
        sys.exit(1)

    print(f"📂 พบ {len(csv_files)} CSV file(s) ใน: {CSV_DIR}")
    for csv_path in csv_files:
        print(f"\n🔄 {os.path.basename(csv_path)}")
        add_images_to_csv(csv_path, image_map)

    print(f"\n✅ เสร็จสิ้น — อัปเดต {len(csv_files)} ไฟล์แล้ว")


if __name__ == "__main__":
    main()
