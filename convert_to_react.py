import os
import re

files_to_convert = [
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

for file, comp_name in files_to_convert:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the template string
    match = re.search(r'template\s*=\s*\"\"\"(.*?)\"\"\"', content, re.DOTALL)
    if not match:
        print(f"Template not found in {file}")
        continue
    
    template = match.group(1)
    
    # We only want the content inside <main>...</main>, excluding <header> and <footer>
    # because the React app already has a global Layout with Header and Footer.
    
    main_match = re.search(r'<main.*?>(.*?)</main>', template, re.DOTALL | re.IGNORECASE)
    if not main_match:
        print(f"Main not found in {file}")
        continue
        
    main_content = main_match.group(1)
    
    # Remove header
    main_content = re.sub(r'<!-- Header -->.*?</header>', '', main_content, flags=re.DOTALL | re.IGNORECASE)
    # Remove footer
    main_content = re.sub(r'<!-- Footer -->.*?</footer>', '', main_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Convert {key} to {t('comp_name.key')}
    # but first handle {{ and }}
    main_content = main_content.replace('{{', '{').replace('}}', '}')
    
    # Replace {key} with {t('page.key')}
    # using a regex
    def replacer(m):
        key = m.group(1)
        # ignore some variables if they are javascript
        if key in ['lang']:
            return '{lang}'
        return f"{{t('{comp_name.lower()}.{key}')}}"
        
    main_content = re.sub(r'\{([a-zA-Z0-9_]+)\}', replacer, main_content)
    
    # Convert class= to className=
    main_content = main_content.replace('class=', 'className=')
    
    # Convert self-closing tags
    main_content = re.sub(r'<img(.*?)(?<!/)>', r'<img\1 />', main_content)
    main_content = re.sub(r'<br(.*?)(?<!/)>', r'<br\1 />', main_content)
    main_content = re.sub(r'<hr(.*?)(?<!/)>', r'<hr\1 />', main_content)
    
    # Convert inline styles if any (e.g. style="display: none;")
    main_content = main_content.replace('style="display: none;"', 'style={{display: "none"}}')
    
    # Also extract the <script type="application/ld+json"> for Helmet
    head_match = re.search(r'<head>(.*?)</head>', template, re.DOTALL | re.IGNORECASE)
    schemas = []
    if head_match:
        head_content = head_match.group(1)
        schema_matches = re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head_content, re.DOTALL)
        for sm in schema_matches:
            schema_str = sm.group(1).strip()
            # Restore {}
            schema_str = schema_str.replace('{{', '{').replace('}}', '}')
            # Replace {key} with ${t('page.key')}
            def schema_replacer(m):
                key = m.group(1)
                if key == 'lang': return '${lang}'
                return f"${{t('{comp_name.lower()}.{key}')}}"
            schema_str = re.sub(r'\{([a-zA-Z0-9_]+)\}', schema_replacer, schema_str)
            schemas.append(schema_str)

    schema_tags = ""
    for s in schemas:
        schema_tags += f"\n        <script type=\"application/ld+json\">{{`{s}`}}</script>"

    react_comp = f"""import {{ useTranslation }} from 'react-i18next';
import {{ Helmet }} from 'react-helmet-async';
import {{ useParams }} from 'react-router-dom';

export default function {comp_name}() {{
  const {{ t }} = useTranslation();
  const {{ lang }} = useParams();

  return (
    <>
      <Helmet>
        <title>{{t('{comp_name.lower()}.title')}}</title>
        <meta name="description" content={{t('{comp_name.lower()}.desc')}} />
        <meta name="keywords" content={{t('{comp_name.lower()}.keywords')}} />{schema_tags}
      </Helmet>

      <div className="flex-1">
        {main_content.strip()}
      </div>
    </>
  );
}}
"""
    
    out_path = f"frontend/website/src/pages/{comp_name}.tsx"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(react_comp)
    print(f"Generated React component {comp_name}.tsx")

