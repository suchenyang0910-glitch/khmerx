import json
import importlib.util
import sys
import os
import ast

def extract_dicts_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=filepath)
    
    dicts = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.startswith('content_'):
                    lang = target.id.split('_')[1]
                    try:
                        dict_val = ast.literal_eval(node.value)
                        dicts[lang] = dict_val
                    except:
                        pass
    return dicts

files = [
    'generate_homepages.py',
    'generate_borrowpages.py',
    'generate_feepages.py',
    'generate_faq.py',
    'generate_contact.py',
    'generate_risk.py',
    'generate_privacy.py',
    'generate_terms.py',
    'generate_blog.py',
    'generate_article.py',
    'generate_app.py',
    'generate_about.py',
    'generate_landings.py'
]

i18n_data = {'zh': {}, 'en': {}, 'km': {}}

for file in files:
    if os.path.exists(file):
        print(f"Extracting from {file}")
        page_name = file.replace('generate_', '').replace('pages', '').replace('.py', '')
        dicts = extract_dicts_from_file(file)
        for lang, data in dicts.items():
            if page_name not in i18n_data[lang]:
                i18n_data[lang][page_name] = {}
            i18n_data[lang][page_name].update(data)

# Special handling for generate_landings.py which has a list of pages
if os.path.exists('generate_landings.py'):
    with open('generate_landings.py', 'r', encoding='utf-8') as f:
        content = f.read()
        # Find the pages list
        tree = ast.parse(content)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'pages':
                        try:
                            pages_list = ast.literal_eval(node.value)
                            for page in pages_list:
                                slug = page['slug']
                                for lang in ['zh', 'en', 'km']:
                                    if lang in page:
                                        i18n_data[lang][f"landing_{slug.replace('-', '_')}"] = page[lang]
                        except:
                            pass

with open('frontend/website/src/i18n.json', 'w', encoding='utf-8') as f:
    json.dump(i18n_data, f, ensure_ascii=False, indent=2)

print("Dumped to i18n.json")
