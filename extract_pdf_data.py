import pdfplumber
import csv
import os
import re

pdf_folder = "Rakuten"
output_csv = "rakuten_transactions.csv"

rows = []

def extract_month(filename):
    # Try to extract YYYYMM or YYYY-MM or similar from filename
    match = re.search(r'(\d{4}[/-]?\d{2})', filename)
    if match:
        return match.group(1).replace("-", "").replace("/", "")
    return "Unknown"

for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        month = extract_month(filename)
        with pdfplumber.open(os.path.join(pdf_folder, filename)) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Skip header rows by checking for column names
                        if "利用店名" in row and "支払方法" in row:
                            continue
                        # Extract columns: 利用店名 (col2), 支払方法 (col5)
                        try:
                            entity = row[1]
                            amount = row[4]
                            if entity and amount:
                                amount = amount.replace(",", "")  # Remove commas
                                rows.append([month, entity, amount])
                        except IndexError:
                            continue

# Sort rows by Month, then Merchant
rows.sort(key=lambda x: (x[0], x[1]))

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Month", "Merchant", "Amount"])
    writer.writerows(rows)
