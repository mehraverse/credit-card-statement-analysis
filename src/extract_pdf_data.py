import pdfplumber
import csv
import os
import re

pdf_folder = "./data/raw/Rakuten"

def extract_rakuten_transactions(pdf_folder):
    rows = []
    def extract_month(filename):
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
                            if "利用店名" in row and "当月請求額" in row:
                                continue
                            try:
                                entity = row[1]
                                amount = row[7]
                                if entity and amount:
                                    amount = amount.replace(",", "")
                                    rows.append([month, entity, amount, "Rakuten"])
                            except IndexError:
                                continue
    return rows

rows = extract_rakuten_transactions(pdf_folder)
