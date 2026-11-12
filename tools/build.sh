#!/usr/bin/env bash
# Rebuilds data.json, icons/ and index.html from the latest game data.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="${1:-/tmp/cka}"
if [ ! -d "$SRC/.git" ]; then
  git clone --depth 1 --filter=blob:none --no-checkout https://github.com/ClashKingInc/ClashKingAssets.git "$SRC"
fi
git -C "$SRC" checkout HEAD -- assets/static_data
mkdir -p icons
python3 tools/data.py "$SRC"
python3 - <<'PY'
from PIL import Image; import glob
for f in glob.glob('icons/*.webp'):
    im = Image.open(f); im.thumbnail((112, 112)); im.save(f, 'WEBP', quality=82, method=6)
t = open('tools/template.html').read()
open('index.html', 'w').write(t.replace('/*__DATA__*/{}', open('data.json').read()))
PY
echo "Built index.html"
