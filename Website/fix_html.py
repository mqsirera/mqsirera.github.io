#!/usr/bin/env python3
"""Move Quarto's after-body script out of #quarto-content so CSS cannot paint it."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent / "_site"
PAT = re.compile(
    r'\s*<script id="quarto-html-after-body"[^>]*>.*?</script>',
    re.S,
)

def fix(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    match = PAT.search(text)
    if not match:
        return
    snippet = match.group(0).strip()
    text = PAT.sub("\n", text, count=1)
    if "</body>" in text:
        text = text.replace("</body>", snippet + "\n</body>", 1)
    path.write_text(text, encoding="utf-8")
    print(f"moved after-body script in {path.name}")

def main() -> None:
    if not ROOT.exists():
        return
    for html_path in ROOT.rglob("*.html"):
        fix(html_path)

if __name__ == "__main__":
    main()
