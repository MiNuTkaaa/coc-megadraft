"""Rebuild index.html from tools/template.html and data.json (no network needed).

Run from the repo root:  python tools/inject.py
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
template = (root / "tools" / "template.html").read_text(encoding="utf-8")
data = (root / "data.json").read_text(encoding="utf-8")
(root / "index.html").write_text(template.replace("/*__DATA__*/{}", data), encoding="utf-8")
print("Built index.html")
