# AI指示 図解帳

『AIへの指示が一発で通る Webサイト用語図解帳』の原稿（A5・HTML → PDF）。

| ファイル | 内容 |
| --- | --- |
| `template.html` | デザインと固定ページ、見本の用語ページ（04・12・13） |
| `make_book.py` | 用語データ（`TERMS`）を template.html に流し込み、`book.html` を生成 |
| `book.html` | 本文20語入りの完全版（生成物） |
| `build.sh` | Chrome ヘッドレスで PDF に書き出し、品質チェック結果を表示（Windows + Git Bash 用） |

```bash
python make_book.py   # book.html を作り直す
bash build.sh         # template.html → template-sample.pdf
bash build.sh book    # book.html → book.pdf
```
