import os
import glob
import re

def fix_jsx(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove HTML comments
    content = re.sub(r'<!--(.*?)-->', r'{/* \1 */}', content, flags=re.DOTALL)

    # Fix self-closing issues that might have been incorrectly created
    content = content.replace('</p />', '</p>')
    content = content.replace('</a />', '</a>')
    content = content.replace('</div />', '</div>')
    content = content.replace('</span />', '</span>')
    content = content.replace('</h1 />', '</h1>')
    content = content.replace('</h2 />', '</h2>')
    content = content.replace('</h3 />', '</h3>')
    content = content.replace('</h4 />', '</h4>')
    content = content.replace('</li />', '</li>')
    content = content.replace('</ul />', '</ul>')
    content = content.replace('</ol />', '</ol>')
    content = content.replace('</section />', '</section>')
    content = content.replace('</details />', '</details>')
    content = content.replace('</summary />', '</summary>')
    content = content.replace('</strong />', '</strong>')
    
    # Fix inline styles
    content = content.replace('style="animation-delay: 1.5s;"', "style={{ animationDelay: '1.5s' }}")
    content = content.replace('style="display: none;"', "style={{ display: 'none' }}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Use absolute path
target_dir = r"D:\projects\khmerx\frontend\website\src\pages\*.tsx"
files = glob.glob(target_dir)

for f in files:
    fix_jsx(f)

print(f"Fixed {len(files)} JSX files.")