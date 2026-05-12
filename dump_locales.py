import json
import os
import ast

def extract_dicts_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return {}
    
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
        page_name = file.replace('generate_', '').replace('pages', '').replace('.py', '')
        if page_name == 'landing':
            page_name = 'landings'
        dicts = extract_dicts_from_file(file)
        for lang, data in dicts.items():
            i18n_data[lang][page_name] = data

if os.path.exists('generate_landings.py'):
    with open('generate_landings.py', 'r', encoding='utf-8') as f:
        content = f.read()
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
                                        key = f"landing_{slug.replace('-', '_')}"
                                        i18n_data[lang][key] = page[lang]
                        except Exception as e:
                            pass

os.makedirs('frontend/website/src/locales', exist_ok=True)
for lang in ['zh', 'en', 'km']:
    with open(f'frontend/website/src/locales/{lang}.json', 'w', encoding='utf-8') as f:
        json.dump(i18n_data[lang], f, ensure_ascii=False, indent=2)

print("Locales dumped successfully.")
