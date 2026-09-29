"""template.html（デザインと固定ページ）＋ 下の用語データ → book.html（本文20語入りの完全版）

- 用語データにない番号は、template.html にある見本ページ（04・12・13）をそのまま使う。
- 実行：python make_book.py
"""
import html
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
CH1, CH2, CH3 = "第1章 箱のしくみ", "第2章 画面の部品", "第3章 ページの考え方"

TERMS = {
    1: dict(
        yomi="element", name="要素", chapter=CH1,
        hitokoto="ページを組み立てる<em>部品1個分</em>。タグで囲んだひとかたまり。",
        fig='''<div class="el-fig">
      <div class="mini-page">
        <div class="el-box"><span class="badge">1</span><b style="font-size:10.5pt">季節のタルト</b></div>
        <div class="el-box"><span class="badge">2</span>旬の果物をたっぷりのせました。</div>
        <div class="el-box img"><span class="badge">3</span><i></i></div>
        <div class="el-box"><span class="badge">4</span><span class="btn-mini">予約する</span></div>
      </div>
      <div class="el-code">
        <p><span class="badge">1</span>&lt;h1&gt;季節のタルト&lt;/h1&gt;</p>
        <p><span class="badge">2</span>&lt;p&gt;旬の果物を…&lt;/p&gt;</p>
        <p><span class="badge">3</span>&lt;img src="tart.jpg"&gt;</p>
        <p><span class="badge">4</span>&lt;button&gt;予約する&lt;/button&gt;</p>
      </div>
    </div>''',
        cap="画面の部品1つが、HTMLの要素1つ。番号どうしが対応している。",
        ng="「<u>上のほうの文字</u>を大きくして」",
        ngr="→ 見出し・ロゴ・メニューのどれが変わるかわからない。",
        ok="「ページ最上部の<b>見出し要素（h1）</b>だけ、文字サイズを32pxにして」",
        lang="CSS", code="h1 {\n  font-size: 32px;\n}",
        rel="02 タグとclass ／ 03 ボックスモデル",
    ),
    2: dict(
        yomi="tag / クラス", name="タグとclass", chapter=CH1,
        hitokoto="タグは部品の種類、classは<em>AIに場所を伝える名札</em>。",
        fig='''<div class="cls-row">
      <div class="fig-col"><div class="c-card"><span class="nametags"><span class="nametag">card</span></span><i></i><b>チーズケーキ</b></div><span class="sel">div.card</span></div>
      <div class="fig-col"><div class="c-card"><span class="nametags"><span class="nametag">card</span></span><i></i><b>季節のタルト</b></div><span class="sel">div.card</span></div>
      <div class="fig-col"><div class="c-card pickup"><span class="nametags"><span class="nametag">card</span><span class="nametag hl">card--pickup</span></span><i></i><b>おすすめ</b></div><span class="sel">div.card.card--pickup</span></div>
    </div>
    <div class="key">
      <span class="nametag" style="background:var(--ink-2)">div</span><span>タグ：部品の種類（ここでは「箱」）</span>
      <span class="nametag">card</span><span>class：名札。同じ名札の部品は同じ見た目になる</span>
    </div>''',
        cap="名札（class）で指定すれば、並び順が変わっても狙った部品だけが変わる。",
        ng="「<u>2つ目のカード</u>だけ色を変えて」",
        ngr="→ 並び順が変わると、別のカードの色が変わってしまう。",
        ok="「classが<b>card--pickup</b>のカードだけ、背景を薄い黄色（#fff6d6）にして」",
        lang="CSS", code=".card--pickup {\n  background: #fff6d6;\n}",
        rel="01 要素",
    ),
    3: dict(
        yomi="box model", name="ボックスモデル", chapter=CH1,
        hitokoto="どの要素も<em>中身・padding・border・margin</em>の4層の箱。",
        fig='''<div class="fig-row">
      <div class="bm m"><span class="bm-label">margin</span>
        <div class="bm b"><span class="bm-label">border</span>
          <div class="bm p"><span class="bm-label">padding</span>
            <div class="bm c">中身（content）</div>
          </div>
        </div>
      </div>
    </div>''',
        cap="内側から 中身 → padding → border → margin の順に重なる。色は第1章で共通。",
        ng="「<u>もうちょっと余白を空けて</u>」",
        ngr="→ 内側か外側か、どの要素の余白かが伝わらない。",
        ok="「カードの内側の<b>padding</b>は20pxのまま、カード同士の<b>margin</b>を24pxにして」",
        lang="CSS", code=".card {\n  padding: 20px; margin-bottom: 24px;\n}",
        rel="04 padding ／ 05 margin ／ 06 border",
    ),
    5: dict(
        yomi="マージン", name="margin", chapter=CH1,
        hitokoto="箱の<em>外側</em>、となりの箱との距離。",
        fig='''<div class="fig-row" style="gap:10mm; align-items:flex-start">
      <div class="fig-col">
        <p class="fig-label">カードの間が margin</p>
        <div class="m-demo"><div class="m-card">カード A</div><div class="m-gap">margin 24px</div><div class="m-card">カード B</div></div>
      </div>
      <div class="fig-col">
        <p class="fig-label">上下の margin は重なる</p>
        <div class="m-demo"><div class="m-card">下に 20px</div><div class="m-overlap"><i class="b"></i><i class="a"></i><span class="la">20px</span><span class="lb">30px</span></div><div class="m-card">上に 30px</div></div>
        <p class="fig-note">間は 50px ではなく 30px</p>
      </div>
    </div>''',
        cap="margin は透明な外側の余白。上下に並ぶと足し算されず、大きいほうだけが効く。",
        ng="「<u>カードの間をもっと空けて</u>」",
        ngr="→ padding が増え、カードの中がスカスカになることがある。",
        ok="「カード同士の間隔を<b>margin</b>で24pxにして。カードの内側の余白は変えないで」",
        lang="CSS", code=".card + .card {\n  margin-top: 24px;\n}",
        rel="03 ボックスモデル ／ 04 padding",
    ),
    6: dict(
        yomi="ボーダー", name="border", chapter=CH1,
        hitokoto="padding と margin の境目に引く<em>枠線</em>。",
        fig='''<div class="bd-row">
      <div class="fig-col"><div class="bd s"></div><span class="sel">1px solid</span></div>
      <div class="fig-col"><div class="bd d"></div><span class="sel">1px dashed</span></div>
      <div class="fig-col"><div class="bd t"></div><span class="sel">4px solid</span></div>
      <div class="fig-col"><div class="bd r"></div><span class="sel">radius 8px</span></div>
    </div>
    <div class="bd-anat">
      <span>border:</span>
      <span>1px<small>太さ</small></span>
      <span>solid<small>線の種類</small></span>
      <span>#d0d5dc;<small>色</small></span>
    </div>''',
        cap="border は「太さ・線の種類・色」の3点セット。角の丸みは border-radius で別に指定する。",
        ng="「カードを<u>枠で囲って丸くして</u>」",
        ngr="→ 太さ・色・丸みが毎回ばらばらになる。",
        ok="「カードに1pxのグレー（#d0d5dc）の<b>border</b>を付けて、角を<b>border-radius</b>で8px丸くして」",
        lang="CSS", code=".card {\n  border: 1px solid #d0d5dc; border-radius: 8px;\n}",
        rel="03 ボックスモデル",
    ),
    7: dict(
        yomi="block / inline", name="ブロックとインライン", chapter=CH1,
        hitokoto="<em>縦に積む箱</em>と、<em>文字のように横へ流れる箱</em>。",
        fig='''<div class="bi">
      <div>
        <p class="bi-title">ブロック：横幅いっぱいに広がり、縦に積まれる</p>
        <div class="blk"><span>季節のタルト</span><code>&lt;h2&gt;</code></div>
        <div class="blk"><span>旬の果物をたっぷりのせました。</span><code>&lt;p&gt;</code></div>
        <div class="blk"><span>カード</span><code>&lt;div&gt;</code></div>
      </div>
      <div>
        <p class="bi-title">インライン：文字と同じように横へ流れる</p>
        <div class="inl-box">営業は<span class="inl">10時〜18時</span>です。ご予約は<span class="inl">こちら</span>から、<span class="inl">前日まで</span>にどうぞ。</div>
        <p class="fig-note" style="text-align:left; margin-top:1.2mm">赤い点線がインライン要素（span・a・strong など）</p>
      </div>
    </div>''',
        cap="インラインの箱には幅や高さが効かない。ボタンの形にしたいときは inline-block にする。",
        ng="「このリンクを<u>ボタンっぽく大きく</u>して」",
        ngr="→ 文字が大きくなるだけで、ボタンの形にならない。",
        ok="「ナビのリンク（aタグ）を<b>inline-block</b>にして、幅120px・高さ40pxのボタン型にして」",
        lang="CSS", code="nav a { display: inline-block;\n  width: 120px; height: 40px; }",
        rel="01 要素 ／ 09 グローバルナビ",
    ),
    8: dict(
        yomi="header / footer", name="ヘッダー・フッター", chapter=CH2,
        hitokoto="どのページにも共通で出る<em>上端と下端の帯</em>。",
        fig='''<div class="fig-row">
      <div class="pg-set">
        <div class="fig-col"><div class="pg-thumb"><div class="pg-h">KOMOREBI<span class="dots"><i></i><i></i><i></i></span></div><div class="pg-body"><i class="img"></i><i></i><i style="width:80%"></i><i></i><i style="width:60%"></i></div><div class="pg-f"></div><span class="hl-band top"></span><span class="hl-band bottom"></span></div><span class="fig-note">トップ</span></div>
        <div class="fig-col"><div class="pg-thumb"><div class="pg-h">KOMOREBI<span class="dots"><i></i><i></i><i></i></span></div><div class="pg-body"><i style="width:50%"></i><i></i><i></i><i style="width:70%"></i><i></i><i style="width:85%"></i></div><div class="pg-f"></div><span class="hl-band top"></span><span class="hl-band bottom"></span></div><span class="fig-note">メニュー</span></div>
        <span class="badge" style="top: 1.8mm">1</span>
        <span class="badge" style="top: 51.5mm">2</span>
      </div>
    </div>
    <div class="key">
      <span class="badge" style="background:var(--warn)">1</span><span>ヘッダー：ロゴとメニューが入る上端の帯</span>
      <span class="badge" style="background:var(--warn)">2</span><span>フッター：会社情報などが入る下端の帯</span>
    </div>''',
        cap="ページが変わっても、ヘッダーとフッターは同じものが出る。",
        ng="「<u>一番上のところ</u>をスクロールしてもついてくるようにして」",
        ngr="→ 見出しやバナーが固定されることがある。",
        ok="「<b>ヘッダー</b>をスクロールしても画面上部に固定して。高さは64pxで、本文が隠れないようにして」",
        lang="CSS", code="header {\n  position: sticky; top: 0; height: 64px;\n}",
        rel="09 グローバルナビ ／ 18 ファーストビュー",
    ),
    9: dict(
        yomi="global navigation", name="グローバルナビ", chapter=CH2,
        hitokoto="サイトの<em>どのページにも出る</em>主要メニュー。",
        fig='''<div class="fig-row">
      <div class="fig-col"><div class="gn-thumb"><div class="gn-h"><span class="gn-logo">KOMOREBI</span><span class="gn-nav"><span class="on">ホーム</span><span>メニュー</span><span>店舗</span></span></div><div class="gn-body"><i class="img"></i><i></i><i style="width:70%"></i></div></div><span class="fig-note">ホーム</span></div>
      <div class="fig-col"><div class="gn-thumb"><div class="gn-h"><span class="gn-logo">KOMOREBI</span><span class="gn-nav"><span>ホーム</span><span class="on">メニュー</span><span>店舗</span></span></div><div class="gn-body"><i style="width:60%"></i><i></i><i></i><i style="width:80%"></i><i></i></div></div><span class="fig-note">メニュー</span></div>
      <div class="fig-col"><div class="gn-thumb"><div class="gn-h"><span class="gn-logo">KOMOREBI</span><span class="gn-nav"><span>ホーム</span><span>メニュー</span><span class="on">店舗</span></span></div><div class="gn-body"><i class="img"></i><i style="width:85%"></i><i></i></div></div><span class="fig-note">店舗</span></div>
    </div>''',
        cap="点線の中がグローバルナビ。どのページでも同じ位置にあり、今いるページの項目だけ色と下線で示す。",
        ng="「<u>メニューのリンク</u>を増やして」",
        ngr="→ ページ内の目次やフッターのリンクが増えることがある。",
        ok="「ヘッダーの<b>グローバルナビ</b>の最後に「アクセス」を追加して。今いるページの項目は下線で示して」",
        lang="HTML", code='<nav class="global-nav">\n  <a href="/menu" aria-current="page">メニュー</a> …\n  <a href="/access">アクセス</a></nav>',
        rel="08 ヘッダー・フッター ／ 10 ハンバーガーメニュー",
    ),
    10: dict(
        yomi="hamburger menu", name="ハンバーガーメニュー", chapter=CH2,
        hitokoto="メニューを開くための<em>三本線のボタン</em>。",
        fig='''<div class="fig-row" style="gap:6mm">
      <div class="fig-col"><div class="phone"><div class="phone-bar">KOMOREBI<span class="burger ring"><i></i><i></i><i></i></span></div><div class="phone-body"><i class="img"></i><i></i><i style="width:80%"></i><i></i><i style="width:60%"></i></div></div><span class="fig-note">閉じているとき</span></div>
      <div class="go">→<small>タップ</small></div>
      <div class="fig-col"><div class="phone"><div class="phone-bar">KOMOREBI<span class="x-icon">×</span></div><div class="phone-body"><i class="img"></i><i></i><i style="width:80%"></i></div><div class="dim-overlay"></div><div class="drawer-panel"><span>ホーム</span><span>メニュー</span><span>店舗</span><span>予約</span></div></div><span class="fig-note">開いたとき</span></div>
    </div>''',
        cap="赤で囲んだ三本線がハンバーガー（ボタン）。開いて出てくるメニュー本体はドロワー。",
        ng="「スマホでは<u>メニューを三本線にして</u>」",
        ngr="→ ボタンだけ作られ、押しても何も開かないことがある。",
        ok="「幅768px以下ではナビを<b>ハンバーガーメニュー</b>にまとめて。押したら右からドロワーを開き、アイコンは×に変えて」",
        lang="CSS", code="@media (max-width: 768px) {\n  .global-nav { display: none; }\n  .hamburger { display: block; } }",
        rel="11 ドロワー ／ 19 レスポンシブ",
    ),
    11: dict(
        yomi="drawer", name="ドロワー", chapter=CH2,
        hitokoto="画面の端から<em>引き出しのように</em>出てくるパネル。",
        fig='''<div class="fig-row" style="gap:9mm">
      <div class="fig-col"><div class="phone"><div class="phone-bar">KOMOREBI<span class="x-icon">×</span></div><div class="phone-body"><i class="img"></i><i></i></div><div class="dim-overlay"></div><span class="slide-in" style="top:55%">←</span><div class="drawer-panel"><span>ホーム</span><span>メニュー</span><span>店舗</span><span>予約</span></div></div><span class="fig-note">右から出る（幅80%）</span></div>
      <div class="fig-col" style="gap:3mm">
        <div class="fig-col"><div class="mini-thumb"><div class="dim-overlay"></div><div class="dd"></div></div><span class="fig-note"><b>ドロワー</b>：端から出る</span></div>
        <div class="fig-col"><div class="mini-thumb"><div class="dim-overlay"></div><div class="mm"></div></div><span class="fig-note"><b>モーダル</b>：中央に出る</span></div>
      </div>
    </div>''',
        cap="出てくる位置で呼び名が変わる。後ろを暗くする幕（オーバーレイ）はどちらにも付く。",
        ng="「メニューを<u>横からシュッと出して</u>」",
        ngr="→ 出てくる向き・幅・速さがばらばらになる。",
        ok="「メニューを右からの<b>ドロワー</b>にして。幅は画面の80%、0.3秒で開き、後ろは半透明の黒で暗くして」",
        lang="CSS", code=".drawer { width: 80%; transform: translateX(100%);\n  transition: transform 0.3s; }\n.drawer.is-open { transform: translateX(0); }",
        rel="10 ハンバーガーメニュー ／ 13 モーダル",
    ),
    14: dict(
        yomi="accordion", name="アコーディオン", chapter=CH2,
        hitokoto="見出しを押すと<em>中身が開閉する</em>折りたたみ。",
        fig='''<div class="acc-demo">
      <div class="acc-q"><span class="badge">1</span>テイクアウトできますか？<span class="pm">＋</span></div>
      <div class="acc-q"><span class="badge">2</span>予約は何日前からできますか？<span class="pm">－</span></div>
      <div class="acc-a">2か月前の同じ日から、Webで予約できます。</div>
      <div class="acc-q"><span class="badge">1</span>駐車場はありますか？<span class="pm">＋</span></div>
    </div>
    <div class="key">
      <span class="badge">1</span><span>閉じた状態：質問だけが見える（＋）</span>
      <span class="badge">2</span><span>開いた状態：答えが下に出る（－）</span>
    </div>''',
        cap="よくある質問（FAQ）の定番。答えは同じ場所で、質問のすぐ下に開く。",
        ng="「よくある質問を<u>クリックで出るように</u>して」",
        ngr="→ 答えがモーダルや別ページで出ることがある。",
        ok="「よくある質問を<b>アコーディオン</b>にして。質問を押すと答えが下に開き、最初は全部閉じた状態にして」",
        lang="HTML", code="<details>\n  <summary>テイクアウトできますか？</summary>\n  はい、全メニューできます。</details>",
        rel="15 タブ",
    ),
    15: dict(
        yomi="tab", name="タブ", chapter=CH2,
        hitokoto="同じ場所で<em>中身を切り替える</em>見出しボタン。",
        fig='''<div class="fig-row">
      <div class="tab-demo"><div class="tab-bar"><span class="on">フード</span><span>ドリンク</span><span>スイーツ</span></div><div class="tab-panel"><div><i></i>サンドイッチ</div><div><i></i>キッシュ</div><div><i></i>スープセット</div></div></div>
      <div class="go">→<small>ドリンクを押す</small></div>
      <div class="tab-demo"><div class="tab-bar"><span>フード</span><span class="on">ドリンク</span><span>スイーツ</span></div><div class="tab-panel"><div><i></i>カフェラテ</div><div><i></i>紅茶</div><div><i></i>レモネード</div></div></div>
    </div>''',
        cap="ページは移動せず、下の中身だけが切り替わる。ここがナビとの違い。",
        ng="「メニューを<u>フードとドリンクで分けて</u>」",
        ngr="→ 別ページに分かれたり、見出しで縦に並んだりする。",
        ok="「メニュー一覧を<b>タブ</b>で<span class='nobr'>「フード／ドリンク／スイーツ」</span>に切り替えて。ページは移動させず、最初はフードを表示して」",
        lang="HTML", code='<div role="tablist">\n  <button role="tab" aria-selected="true">フード</button>\n  <button role="tab">ドリンク</button> …</div>',
        rel="14 アコーディオン ／ 09 グローバルナビ",
    ),
    16: dict(
        yomi="carousel", name="カルーセル", chapter=CH2,
        hitokoto="画像などが<em>横に切り替わっていく</em>表示枠。",
        fig='''<div class="car">
      <div class="slide">秋のタルト</div>
      <div class="slide main"><span class="badge">1</span>新メニュー</div>
      <div class="slide">予約受付中</div>
    </div>
    <div class="car-dots"><span class="badge" style="margin-right:1.5mm">2</span><i></i><i class="on"></i><i></i></div>
    <div class="key">
      <span class="badge">1</span><span>見える枠：1枚ずつ表示し、5秒ごとに次へ</span>
      <span class="badge">2</span><span>ドット：今が何枚目かを示し、押すと切り替わる</span>
    </div>''',
        cap="横に並んだ画像のうち、枠の中の1枚だけが見えている。",
        ng="「トップの画像を<u>スライダーにして</u>」",
        ngr="→ 音量つまみのような「スライダー」部品が作られることがある。",
        ok="「トップの画像3枚を<b>カルーセル</b>にして。5秒ごとに自動で次へ進め、下のドットでも選べるようにして」",
        lang="JavaScript", code="new Swiper('.hero', {\n  loop: true, autoplay: { delay: 5000 },\n  pagination: { el: '.swiper-pagination' } });",
        rel="18 ファーストビュー",
    ),
    17: dict(
        yomi="toast", name="トースト", chapter=CH2,
        hitokoto="操作の結果を<em>短く知らせて自動で消える</em>通知。",
        fig='''<div class="fig-row" style="gap:3mm">
      <div class="fig-col"><div class="phone sm"><div class="phone-bar">KOMOREBI</div><div class="phone-body"><i></i><i style="width:70%"></i><i></i><span class="btn-mini ring">保存</span></div></div><span class="fig-note">① 保存を押す</span></div>
      <div class="go">→</div>
      <div class="fig-col"><div class="phone sm"><div class="phone-bar">KOMOREBI</div><div class="phone-body"><i></i><i style="width:70%"></i><i></i><span class="btn-mini">保存</span></div><span class="toast-pill">保存しました</span></div><span class="fig-note">② 下に出る</span></div>
      <div class="go">→</div>
      <div class="fig-col"><div class="phone sm"><div class="phone-bar">KOMOREBI</div><div class="phone-body"><i></i><i style="width:70%"></i><i></i><span class="btn-mini">保存</span></div><span class="toast-gone">消えた</span></div><span class="fig-note">③ 3秒で消える</span></div>
    </div>''',
        cap="出ている間も画面は操作できる。閉じるまで操作を止めるモーダルとの違い。",
        ng="「保存したら<u>メッセージを出して</u>」",
        ngr="→ 閉じるまで操作できない確認ダイアログが出ることがある。",
        ok="「保存したら、画面の下中央に「保存しました」の<b>トースト</b>を出して。3秒で自動で消して」",
        lang="JavaScript", code="toast.textContent = '保存しました';\ntoast.classList.add('show');\nsetTimeout(() => toast.classList.remove('show'), 3000);",
        rel="13 モーダル",
    ),
    18: dict(
        yomi="first view", name="ファーストビュー", chapter=CH3,
        hitokoto="ページを開いて<em>スクロールせずに見える</em>範囲。",
        fig='''<div class="fv-set">
      <div class="fig-col"><div class="fv pc"><div class="fv-head"></div><div class="fv-hero"><b>CAFE KOMOREBI</b><small>木もれびの席で、ゆっくり</small><span class="btn-mini">予約する</span></div><div class="fv-rest"><i></i><i style="width:80%"></i><i></i><i style="width:60%"></i></div><span class="fv-frame"></span></div><span class="fig-note">PC</span></div>
      <div class="fig-col"><div class="fv sp"><div class="fv-head"></div><div class="fv-hero"><b>CAFE<br>KOMOREBI</b><small>木もれびの席で、<br>ゆっくり</small><span class="btn-mini">予約する</span></div><div class="fv-rest"><i></i><i style="width:70%"></i></div><span class="fv-frame"></span></div><span class="fig-note">スマホ</span></div>
    </div>''',
        cap="太枠の中がファーストビュー。画面の大きさで範囲が変わる。",
        ng="「<u>最初の画面をもっとインパクトある感じ</u>に」",
        ngr="→ 何をどこまで変えるか伝わらず、全体が作り直される。",
        ok="「<b>ファーストビュー</b>を画面の高さいっぱいにして、店名・キャッチコピー・予約ボタンだけを中央に置いて」",
        lang="CSS", code=".hero {\n  min-height: 100svh; display: grid; place-items: center;\n}",
        rel="19 レスポンシブ ／ 20 CTA",
    ),
    19: dict(
        yomi="responsive / breakpoint", name="レスポンシブとブレイクポイント", chapter=CH3, long=True,
        hitokoto="画面の幅に合わせて<em>レイアウトを組み替える</em>しくみ。",
        fig='''<div class="rs-set">
      <div class="fig-col"><div class="rs-pc"><div class="rs-card"><i></i><b></b></div><div class="rs-card"><i></i><b></b></div><div class="rs-card"><i></i><b></b></div></div><span class="fig-note">PC：3列</span></div>
      <div class="fig-col"><div class="rs-sp"><div class="rs-card"><i></i><b></b></div><div class="rs-card"><i></i><b></b></div><div class="rs-card"><i></i><b></b></div></div><span class="fig-note">スマホ：1列</span></div>
    </div>
    <div class="ruler"><span class="bar"></span><span class="tick"></span><span class="tick-label">ブレイクポイント 768px</span><span class="end l">画面の幅 狭い：1列</span><span class="end r">広い：3列</span></div>''',
        cap="画面の幅が境目（ブレイクポイント）をまたぐと、レイアウトが切り替わる。",
        ng="「<u>スマホでも見やすく</u>して」",
        ngr="→ 文字の縮小や一部の非表示など、何が変わるかわからない。",
        ok="「カードを、幅768px以上では3列、それより狭いときは1列にして。<b>ブレイクポイント</b>は768pxの1つだけ」",
        lang="CSS", code=".cards { display: grid; gap: 16px; }\n@media (min-width: 768px) {\n  .cards { grid-template-columns: repeat(3, 1fr); } }",
        rel="10 ハンバーガーメニュー ／ 18 ファーストビュー",
    ),
    20: dict(
        yomi="シーティーエー（Call To Action）", name="CTA", chapter=CH3,
        hitokoto="見た人に<em>とってほしい行動</em>へ誘うボタンやリンク。",
        fig='''<div class="fig-row" style="gap:7mm; align-items:flex-start">
      <div class="fig-col"><span class="verdict ok">○ 目立つのは1つ</span><div class="cta-thumb"><i class="img"></i><i></i><i style="width:70%"></i><span class="b-primary">予約する</span><div class="btns"><span class="b-ghost">メニュー</span><span class="b-ghost">アクセス</span></div></div></div>
      <div class="fig-col"><span class="verdict ng">× 全部が目立つ</span><div class="cta-thumb"><i class="img"></i><i></i><i style="width:70%"></i><div class="btns"><span class="b-loud">予約する</span><span class="b-loud">メニュー</span><span class="b-loud">アクセス</span><span class="b-loud">お知らせ</span><span class="b-loud">SNS</span></div></div></div>
    </div>''',
        cap="CTAは1ページに1つ。ほかのボタンを控えめにすると、押してほしいボタンが際立つ。",
        ng="「<u>ボタンを目立たせて</u>」",
        ngr="→ 全部のボタンが派手になり、どれも目立たなくなる。",
        ok="「このページの<b>CTA</b>は「予約する」ボタン1つだけ。メイン色で一番大きくし、ほかはグレーの枠線だけにして」",
        lang="CSS", code=".btn-primary { background: #0e7c86; font-size: 18px; }\n.btn { background: none; border: 1px solid #c3c8cf; }",
        rel="18 ファーストビュー ／ 02 タグとclass",
    ),
}

PRISM = {"CSS": "css", "HTML": "html", "JavaScript": "javascript"}


def render(no, t):
    page = no + 3
    name_cls = "term-name long" if t.get("long") else "term-name"
    return f'''<!-- ============ {page}p {no:02d} {t["name"]} ============ -->
<section class="page term" data-page="{page}" data-kind="term">
  <header class="term-head">
    <span class="term-no">{no:02d}</span>
    <div><p class="term-yomi">{t["yomi"]}</p><h2 class="{name_cls}">{t["name"]}</h2></div>
    <span class="term-chapter">{t["chapter"]}</span>
  </header>
  <p class="hitokoto">{t["hitokoto"]}</p>
  <figure class="zu">
    {t["fig"]}
    <figcaption class="zu-cap">{t["cap"]}</figcaption>
  </figure>
  <div class="pair">
    <div class="card ng">
      <h3>× NG指示</h3>
      <p class="say">{t["ng"]}</p>
      <p class="result">{t["ngr"]}</p>
    </div>
    <div class="card ok">
      <h3>○ 伝わる指示</h3>
      <p class="say">{t["ok"]}</p>
    </div>
  </div>
<pre class="code" data-lang="AIが返すコード（例）｜ {t["lang"]}"><code class="language-{PRISM[t["lang"]]}">{html.escape(t["code"], quote=False)}</code></pre>
  <footer class="page-foot"><span>関連：{t["rel"]}</span><span class="nombre">{page}</span></footer>
</section>
'''


def main():
    src = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    pat = re.compile(r'(?:<!-- =+[^\n]*-->\n)?<section class="page term" data-page="(\d+)".*?</section>\n', re.S)
    found = list(pat.finditer(src))
    samples = {int(m.group(1)) - 3: m.group(0) for m in found}
    pages = []
    for no in range(1, 21):
        if no in TERMS:
            pages.append(render(no, TERMS[no]))
        elif no in samples:
            pages.append(samples[no])
        else:
            raise SystemExit(f"用語 {no:02d} のデータがありません")
    out = src[:found[0].start()] + "\n".join(pages) + "\n" + src[found[-1].end():]
    out = out.replace("<title>AIへの指示が一発で通る Webサイト用語図解帳（見本）</title>", "<title>AIへの指示が一発で通る Webサイト用語図解帳</title>", 1)
    open(os.path.join(HERE, "book.html"), "w", encoding="utf-8", newline="\n").write(out)
    print("book.html:", len(pages), "語")


if __name__ == "__main__":
    main()
