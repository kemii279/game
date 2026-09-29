#!/usr/bin/env bash
# HTML → PDF 書き出し＋品質チェック結果の表示
#   bash build.sh          … template.html → template-sample.pdf
#   bash build.sh book     … make_book.py を実行し book.html → book.pdf
cd "$(dirname "$0")"
if [ "$1" = "book" ]; then python make_book.py || exit 1; SRC=book.html; OUT=book.pdf
else SRC=template.html; OUT=template-sample.pdf; fi
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
F="file:///$(cygpath -m "$PWD")/$SRC"
DEST="$(cygpath -w "$PWD/$OUT")"
rm -f "$OUT"
for try in 1 2 3; do   # まれに書き出しに失敗するので、最大3回試す
  "$CH" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=10000 --print-to-pdf="$DEST" "$F" 2>/dev/null
  [ -s "$OUT" ] && break
done
[ -s "$OUT" ] || { echo "PDFの書き出しに失敗しました"; exit 1; }
"$CH" --headless=new --disable-gpu --virtual-time-budget=10000 --dump-dom "$F" 2>/dev/null | grep -o '<div class="qa-panel[^>]*>.*</div>'
