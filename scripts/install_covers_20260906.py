"""One-off: install the v8 CwC + WwC front-cover mockups as the site cover images (1024x1536), archiving the old ones."""
from PIL import Image
import shutil, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
pairs = [
    (r'C:\Users\rctha\Documents\cowork_projects\05_Book_Creating_with_Claude\production\front_cover_source\Creating_with_Claude_Front_Cover_Mockup_v8.png', 'creating-with-claude-cover.png'),
    (r'C:\Users\rctha\Documents\cowork_projects\16_With_Claude_Series\1-Writing-with-Claude\cover\Writing_with_Claude_Front_Cover_Mockup_v8.png', 'writing-with-claude-cover.png'),
]
arch = os.path.join('_archive', 'covers-2026-09-06')
os.makedirs(arch, exist_ok=True)
for src, name in pairs:
    for d in ('site', '.'):
        p = os.path.join(d, name)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(arch, ('root' if d == '.' else d) + '-' + name))
    im = Image.open(src).convert('RGB').resize((1024, 1536), Image.LANCZOS)
    im.save(os.path.join('site', name), optimize=True)
    im.save(name, optimize=True)
    print(name, os.path.getsize(os.path.join('site', name)) // 1024, 'KB')
