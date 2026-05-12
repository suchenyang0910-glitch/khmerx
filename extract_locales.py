import os
import ast
import json
import re

pages = [
    ("generate_feepages.py", "Fees"),
    ("generate_faq.py", "FAQ"),
    ("generate_contact.py", "Contact"),
    ("generate_risk.py", "Risk"),
    ("generate_privacy.py", "Privacy"),
    ("generate_terms.py", "Terms"),
    ("generate_about.py", "About"),
    ("generate_app.py", "AppDownload"),
    ("generate_blog.py", "Blog"),
    ("generate_article.py", "Article")
]

# 1. Update locales
locales = {"zh": {}, "en": {}, "km": {}}

# First, let's just manually run through the files and extract the dictionaries.
def extract_dicts_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Very basic regex to find content_zh = {...}
    zh_match = re.search(r'content_zh\s*=\s*(\{.*?\})', content, re.DOTALL)
    en_match = re.search(r'content_en\s*=\s*(\{.*?\})', content, re.DOTALL)
    km_match = re.search(r'content_km\s*=\s*(\{.*?\})', content, re.DOTALL)
    
    def parse_dict(match):
        if not match: return {}
        try:
            # Safely evaluate the dictionary
            s = match.group(1)
            # Some python code might have expressions, but ours are static dicts
            return ast.literal_eval(s)
        except Exception as e:
            print(f"Error parsing dict in {filepath}: {e}")
            return {}

    return parse_dict(zh_match), parse_dict(en_match), parse_dict(km_match)

# For each page, extract the dictionaries
for file, comp_name in pages:
    zh_d, en_d, km_d = extract_dicts_from_file(file)
    page_key = comp_name.lower()
    
    locales["zh"][page_key] = zh_d
    locales["en"][page_key] = en_d
    locales["km"][page_key] = km_d

# Load existing locales
for lang in ["zh", "en", "km"]:
    filepath = f"frontend/website/src/locales/{lang}.json"
    data = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    
    # Update with new parsed dicts
    for page_key, d in locales[lang].items():
        if page_key not in data:
            data[page_key] = {}
        data[page_key].update(d)
        
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Locales extracted and updated successfully!")
