"""
==============================================================
Day 10 Lab: Build Your First Automated ETL Pipeline
==============================================================
Student ID: AI20K-2004
Name: Dat Nguyen Tien

Nhiem vu:
   1. Extract:   Doc du lieu tu file JSON
   2. Validate:  Kiem tra & loai bo du lieu khong hop le
   3. Transform: Chuan hoa category + tinh gia giam 10%
   4. Load:      Luu ket qua ra file CSV
==============================================================
"""

import json
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'

# ANSI color codes
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def _banner(msg, color="\033[96m"):
    width = 54
    line = "-" * width
    print(f"\n{color}{line}")
    print(f"  {msg}")
    print(f"{line}\033[0m")


def extract(file_path):
    """
    Task 1: Doc du lieu JSON tu file.

    Returns:
        list: Danh sach cac records (dictionaries)
    """
    _banner(f"EXTRACT  <-  {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  {GREEN}[OK] Extracted {len(data)} raw records.{RESET}")
        return data
    except FileNotFoundError:
        print(f"  {RED}[ERR] Source file not found: {file_path}{RESET}")
        return []
    except json.JSONDecodeError as e:
        print(f"  {RED}[ERR] JSON parse error: {e}{RESET}")
        return []


def validate(data):
    """
    Task 2: Kiem tra chat luong du lieu.

    Quy tac:
       - Price phai > 0 (loai bo gia am hoac bang 0)
       - Category khong duoc rong

    Returns:
        list: Danh sach cac records hop le
    """
    _banner("VALIDATE  --  Data Quality Gate")
    valid_records = []
    error_count   = 0

    for record in data:
        price    = record.get('price', 0)
        category = record.get('category', '')

        # Rule 1: price must be a positive number
        try:
            price_val = float(price)
        except (TypeError, ValueError):
            price_val = 0

        if price_val <= 0:
            print(
                f"  {RED}[DROP] id={record.get('id','?')} "
                f"'{record.get('product','?')}' -> price={price} invalid (must be > 0){RESET}"
            )
            error_count += 1
            continue

        # Rule 2: category must not be blank
        if not str(category).strip():
            print(
                f"  {RED}[DROP] id={record.get('id','?')} "
                f"'{record.get('product','?')}' -> category is empty{RESET}"
            )
            error_count += 1
            continue

        valid_records.append(record)
        print(f"  {GREEN}[KEEP] id={record.get('id','?')} '{record.get('product','?')}'{RESET}")

    print(
        f"\n  Validation summary: "
        f"{GREEN}{len(valid_records)} records kept{RESET}  |  "
        f"{RED}{error_count} records dropped{RESET}"
    )
    return valid_records


def transform(data):
    """
    Task 3: Ap dung business logic.

    Yeu cau:
       - discounted_price = price * 0.9
       - category -> Title Case
       - them cot processed_at

    Returns:
        pd.DataFrame
    """
    _banner("TRANSFORM  --  Enrich & Normalise")
    df = pd.DataFrame(data)

    # 10% discount
    df['discounted_price'] = (df['price'] * 0.9).round(2)

    # Title Case category
    df['category'] = df['category'].astype(str).str.strip().str.title()

    # Observability timestamp
    df['processed_at'] = datetime.datetime.now().isoformat()

    print(f"  {GREEN}[OK] discounted_price = price x 0.90{RESET}")
    print(f"  {GREEN}[OK] category normalised to Title Case{RESET}")
    print(f"  {GREEN}[OK] processed_at = {df['processed_at'].iloc[0]}{RESET}")
    print(f"\n  Preview:")
    print(df[['id', 'product', 'price', 'discounted_price', 'category']].to_string(index=False))
    return df


def load(df, output_path):
    """
    Task 4: Luu DataFrame ra file CSV.
    """
    _banner(f"LOAD  ->  {output_path}")
    df.to_csv(output_path, index=False)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  {GREEN}[OK] File written: {output_path}  ({size_kb:.1f} KB){RESET}")
    print(f"  {GREEN}[OK] Columns: {list(df.columns)}{RESET}")
    print(f"Data saved to {output_path}")


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    pipeline_start = datetime.datetime.now()

    print("=" * 50)
    print("ETL Pipeline Started...")
    print("=" * 50)

    # 1. Extract
    raw_data = extract(SOURCE_FILE)

    if raw_data:
        # 2. Validate
        clean_data = validate(raw_data)

        # 3. Transform
        final_df = transform(clean_data)

        # 4. Load
        if final_df is not None and not final_df.empty:
            load(final_df, OUTPUT_FILE)

            elapsed = (datetime.datetime.now() - pipeline_start).total_seconds()
            print(f"\nPipeline completed! {len(final_df)} records saved.")
            print(f"Duration: {elapsed:.3f}s")
        else:
            print("\nTransform returned None. Check your transform() function.")
    else:
        print("\nPipeline aborted: No data extracted.")
