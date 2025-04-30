import os
import csv
import re
from email import policy
from email.parser import BytesParser

eml_folder = "./data/raw/Mercari"

def extract_mercari_transactions(eml_folder):
    rows = []
    def extract_transaction_details(body):
        lines = body.splitlines()
        transactions = []
        start = False
        for line in lines:
            if not start:
                if "利用履歴" in line:
                    start = True
                continue
            m = re.match(r"(.+?)\s*:\s*([\d,]+)\s*円", line)
            if m:
                entity = m.group(1).strip()
                amount = m.group(2).replace(",", "")
                transactions.append((entity, amount))
        return transactions

    def extract_month(filename):
        m = re.search(r'(\d{2}):(\d{4})', filename)
        if m:
            return f"{m.group(2)}{m.group(1)}"
        m2 = re.search(r'(\d{4}[/-]?\d{2})', filename)
        if m2:
            return m2.group(1).replace("-", "").replace("/", "")
        return "Unknown"

    for filename in os.listdir(eml_folder):
        if filename.lower().endswith(".eml"):
            with open(os.path.join(eml_folder, filename), "rb") as f:
                msg = BytesParser(policy=policy.default).parse(f)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body += part.get_content()
                else:
                    body = msg.get_content()
                transactions = extract_transaction_details(body)
                month = extract_month(filename)
                for entity, amount in transactions:
                    rows.append([month, entity, amount, "Mercari"])
    return rows

rows = extract_mercari_transactions(eml_folder)