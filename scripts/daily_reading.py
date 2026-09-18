import os, glob, re, html
from pypdf import PdfReader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source_pdfs"
DIST = ROOT / "dist"
TEMPLATE = (ROOT / "templates/reading.html").read_text(encoding="utf-8")

DIST.mkdir(exist_ok=True)
processed = {p.stem for p in DIST.glob("*/index.html")}
processed |= {p.stem for p in DIST.glob("*.html")}

pdfs = sorted(SOURCE.glob("*.pdf"))
target = None
for p in pdfs:
    safe = re.sub(r"[^a-z0-9]+", "-", p.stem.lower()).strip("-") or "reading"
    if safe not in processed:
        target = (p, safe)
        break

if not target:
    print("没有待处理的 PDF")
    raise SystemExit

pdf, slug = target
print("处理:", pdf.name)

reader = PdfReader(str(pdf))
text = ""
for i in range(min(5, len(reader.pages))):
    t = reader.pages[i].extract_text() or ""
    text += t + "\n\n"

paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
body = "\n".join("<p>" + html.escape(p) + "</p>" for p in paras)
title = pdf.stem
content = f"<h1>{html.escape(title)}</h1>\n{body}"

page = TEMPLATE.replace("{{document_title}}", html.escape(title))
page = page.replace("{{description}}", html.escape(title))
page = page.replace("{{content}}", content)

out = DIST / slug / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page, encoding="utf-8")
print("生成:", out)
