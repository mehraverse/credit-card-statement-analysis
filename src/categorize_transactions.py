from config.category_keywords import CATEGORY_KEYWORDS
import unicodedata

def normalize_merchant(merchant):
    # Convert to half-width, remove spaces (including full-width)
    merchant = unicodedata.normalize('NFKC', merchant)
    merchant = merchant.replace(" ", "").replace("　", "")
    return merchant

def categorize_transaction(merchant):
    merchant_norm = normalize_merchant(merchant)
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            keyword_norm = normalize_merchant(keyword)
            if keyword_norm in merchant_norm:
                return category
    return "Uncategorized"

def categorize_rows(rows):
    # rows: list of [Month, Merchant, Amount, Company]
    categorized = []
    for row in rows:
        month, merchant, amount, company = row
        category = categorize_transaction(merchant)
        categorized.append([month, merchant, amount, company, category])
    return categorized