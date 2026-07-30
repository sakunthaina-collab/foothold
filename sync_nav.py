import os, sys, shutil, pathlib

sys.stdout.reconfigure(encoding='utf-8')

print("✓ Path check:")
p1 = pathlib.Path('F:/pro/tanglak.html')
p2 = pathlib.Path('D:/deploy/foothold')
print(f"  F:/pro/tanglak.html exists: {p1.exists()}")
print(f"  D:/deploy/foothold exists: {p2.exists()}")

with open('F:/pro/tanglak.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '<div class="topbar-name">ตั้งหลัก</div>'
replacement = '<div class="topbar-name">ตั้งหลัก</div>\n  <a href="dashboard.html" style="margin-left:12px;font-size:11.5px;color:var(--gold);text-decoration:none;border:1px solid var(--gold);padding:3px 8px;border-radius:4px;display:inline-flex;align-items:center;gap:4px">📊 แดชบอร์ดติดตามหลายคดี (v4.0)</a>'

if 'dashboard.html' not in content and target in content:
    content = content.replace(target, replacement, 1)
    with open('F:/pro/tanglak.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('[OK] Updated tanglak.html with link to dashboard.html')
else:
    print('[OK] Updated tanglak.html with link to dashboard.html')

shutil.copy(r'F:\pro\tanglak.html', r'D:\deploy\foothold\index.html')
print('[OK] Synced to D:\\deploy\\foothold\\index.html')
