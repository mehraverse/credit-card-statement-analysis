import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extract_pdf_data import extract_rakuten_transactions
from extract_eml_data import extract_mercari_transactions
from categorize_transactions import categorize_rows
import csv

def main():
    rakuten_rows = extract_rakuten_transactions("./data/raw/Rakuten")
    mercari_rows = extract_mercari_transactions("./data/raw/Mercari")
    all_rows = rakuten_rows + mercari_rows
    all_rows.sort(key=lambda x: (x[0], x[1]))  # Sort by Month, then Merchant

    categorized_rows = categorize_rows(all_rows)

    with open("./data/processed/all_transactions.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Month", "Merchant", "Amount", "Company", "Category"])
        writer.writerows(categorized_rows)

if __name__ == "__main__":
    main()
    