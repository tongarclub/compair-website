#!/usr/bin/env python3
"""
Script to add 'รูปสินค้า' column to a Shopee affiliate CSV file
by extracting image URLs from the product.html file.

Usage:
    python3 add_product_images.py

Input:
    - product.html  : HTML file from Shopee Affiliate (same directory)
    - *.csv         : CSV file without 'รูปสินค้า' column (same directory)

Output:
    - Updates the CSV file in-place, adding the 'รูปสินค้า' column
      with image URLs matched by product ID.
"""

import csv
import re
import sys
import os
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(SCRIPT_DIR, "product.html")
IMAGE_COLUMN = "รูปสินค้า"
ID_COLUMN = "รหัสสินค้า"


def extract_product_images(html_path: str) -> dict[str, str]:
    """Parse HTML and return {product_id: image_url} mapping."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Each product block: href contains the product ID, followed by img src
    # Pattern: /offer/product_offer/{ID}  ...  <img src="{image_url}"
    pattern = re.compile(
        r'/offer/product_offer/(\d+)[^"]*"'   # product ID in href
        r'.*?'                                  # anything in between
        r'<img src="(https?://[^"]+\.(?:webp|jpg|jpeg|png))"',
        re.DOTALL,
    )

    mapping: dict[str, str] = {}
    for match in pattern.finditer(content):
        product_id = match.group(1)
        image_url = match.group(2)
        if product_id not in mapping:
            mapping[product_id] = image_url

    return mapping


def find_csv_file(directory: str) -> str:
    """Find the CSV file in the given directory (skip if already has image column)."""
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    if not csv_files:
        print("ERROR: No CSV file found in", directory)
        sys.exit(1)

    # Prefer files that do NOT have the image column yet
    for path in csv_files:
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if IMAGE_COLUMN not in (reader.fieldnames or []):
                return path

    # If all already have the column, just return the first one
    print("WARNING: All CSV files already have the image column. Updating the first one.")
    return csv_files[0]


def add_images_to_csv(csv_path: str, image_map: dict[str, str]) -> None:
    """Read CSV, add/update 'รูปสินค้า' column, write back."""
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if IMAGE_COLUMN not in fieldnames:
        fieldnames.append(IMAGE_COLUMN)
        print(f"Added new column '{IMAGE_COLUMN}' to {os.path.basename(csv_path)}")
    else:
        print(f"Column '{IMAGE_COLUMN}' already exists — will overwrite with matched values.")

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

    print(f"\nResults:")
    print(f"  Total rows   : {len(rows)}")
    print(f"  Matched      : {matched}")
    print(f"  Not matched  : {len(missing)}")
    if missing:
        print(f"  Missing IDs  : {', '.join(missing)}")
    print(f"\nOutput saved to: {csv_path}")


def main():
    if not os.path.exists(HTML_FILE):
        print(f"ERROR: HTML file not found: {HTML_FILE}")
        sys.exit(1)

    print(f"Parsing image URLs from: {HTML_FILE}")
    image_map = extract_product_images(HTML_FILE)
    print(f"Found {len(image_map)} product image(s) in HTML.\n")

    csv_path = find_csv_file(SCRIPT_DIR)
    print(f"Processing CSV: {os.path.basename(csv_path)}")

    add_images_to_csv(csv_path, image_map)


if __name__ == "__main__":
    main()
