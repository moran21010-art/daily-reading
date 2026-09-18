import re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "dist"
OUT = ROOT / "_site"
BASE = "/daily-reading-site/"

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

for p in SRC.rglob("*"):
    if not p.is_file():
        continue
    rel = p.relative_to(SRC)
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if p.suffix.lower() == ".html":
        text = p.read_text(encoding="utf-8")
        text = re.sub(r'((?:href|src|action)=["\'])/(?!/)', lambda m: m.group(1) + BASE, text)
        dest.write_text(text, encoding="utf-8")
    else:
        shutil.copyfile(p, dest)

# 生成首页列表
links = ""
for d in sorted(OUT.iterdir()):
    if d.is_dir() and (d / "index.html").exists():
        links += f'<li><a href="{BASE}{d.name}/">{d.name}</a></li>\n'
index = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>阅读</title></head>
<body><h1>阅读列表</h1><ul>
{links}
</ul></body></html>"""
(OUT / "index.html").write_text(index, encoding="utf-8")

(OUT / ".nojekyll").write_text("")
print("导出完成:", OUT)
