# Instagram画像（5枚）を日ごとに作る。数字はすべてサイトの記事と同じ。
# 決まりごと：表紙にスタンプは入れない／表紙は見出しと大きな数字だけ／最後は「詳しくは」＋ボタン
import re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = "<style>" + open(os.path.join(HERE, "base.css")).read() + "</style>"
CSS = CSS.replace("</style>", """
.c1 .bigtext{font-family:"Noto Serif CJK JP";font-weight:700;color:var(--stamp);font-size:120px;line-height:1.3;margin-top:40px}
.c1 .bigtext small{font-size:64px}
.f .row.k span{color:var(--ink);font-weight:700;font-size:40px}
.f .row:last-child{border-bottom:0}
.f .row p{font-size:38px;line-height:1.5}
.f .row p small{display:block;font-size:30px;color:var(--muted);margin-top:4px}
.f .row.txt{display:block}
.f .row.txt b{font-size:40px}
.cs .call{margin-top:64px;font-size:50px;line-height:1.6;padding:56px 56px}
.cs .body{margin-top:48px;font-size:40px;line-height:1.75}
.cs .body b{color:var(--stamp)}
</style>""")
BRAND = '<p class="brand"><b>ひとりでやらない実家じまい</b></p>'

def cover(lead, big):
    return f'<section class="s c1"><p class="lead">{lead}</p>{big}<div class="band"></div>{BRAND}<p class="pg">1/5 →</p></section>'
def rows(h, items, total=None, warn=None, src=None):
    r = ""
    for it in items:
        if len(it) == 2: r += f'<div class="row"><span>{it[0]}</span><b>{it[1]}</b></div>'
        else: r += f'<div class="row txt"><p>{it[0]}</p></div>'
    if total: r += f'<div class="tot"><span>{total[0]}</span><b>{total[1]}</b></div>'
    return (f'<p class="h">{h}</p><div class="f">{r}</div>' + (f'<p class="warn">{warn}</p>' if warn else "")
            + (f'<p class="src">{src}</p>' if src else ""))
def bars(h, items, call=None, src=None):
    b = "".join(f'<div class="bar{" hl" if hl else ""}"><div class="lb"><span>{l}</span><b>{v}</b></div><div class="tr"><i style="width:{p}%"></i></div></div>' for l, v, p, hl in items)
    return f'<p class="h">{h}</p><div class="bars">{b}</div>' + (f'<div class="call">{call}</div>' if call else "") + (f'<p class="src">{src}</p>' if src else "")
def ask(h, items, lock=None):
    q = "".join(f'<div class="q"><span class="n">{i}</span><p>{t}' + (f'<small>{s}</small>' if s else "") + '</p></div>' for i, (t, s) in enumerate(items, 1))
    if lock: q += f'<div class="q lock"><span class="n">{len(items)+1}</span><p>{lock}</p></div>'
    return f'<p class="h">{h}</p><div class="ask">{q}</div>'
def callslide(h, call, body=None, src=None):
    return ("CS", f'<p class="h">{h}</p><div class="call">{call}</div>' + (f'<p class="body">{body}</p>' if body else "") + (f'<p class="src">{src}</p>' if src else ""))
def cta(msg):
    return f'<section class="s c5"><p class="msg">{msg}</p><p class="sub">詳しくは</p><p class="btn">プロフィールのリンクから</p><p class="brand"><b>ひとりでやらない実家じまい</b>　@hitori_jikka</p><p class="pg">5/5</p></section>'

def big(num, unit="", pre=""):
    return f'<p class="big">' + (f'<small class="pre">{pre}</small>' if pre else "") + f'{num}' + (f'<small>{unit}</small>' if unit else "") + '</p>'
def bigtext(t):
    return f'<p class="bigtext">{t}</p>'

D = {}
D[2] = [cover("相続税がかかった人は", big("10.4", "%")),
  rows("かかるかどうかは、<br>基礎控除と比べる", [("子1人", "3,600万円"), ("子2人", "4,200万円"), ("配偶者＋子2人", "4,800万円"), ("配偶者＋子3人", "5,400万円")],
       warn="基礎控除＝3,000万円＋600万円×法定相続人の数。親の財産の合計がこれ以下なら、相続税はかかりません。",
       src="出典：国税庁「令和6年分 相続税の申告事績の概要」（2024年に亡くなった方の10.4％）"),
  callslide("ただし「0円」でも、<br>申告が必要なことがある", "自宅の土地を減額する特例は、<br><em>申告書を出して初めて</em>使えます。",
       "期限は、相続を知った日の翌日から<b>10か月以内</b>。「うちは0円だから」と放っておくと、特例を使えずに税金がかかることがあります。"),
  ask("では、誰に相談するか", [("明らかに基礎控除より少ない", "名義変更は、手続きの代行や司法書士へ"), ("超えるか微妙・特例で0円になる", "相続税に慣れた税理士へ")], "税理士に必ず聞くひと言は、記事に"),
  cta("うちは関係ない、<br>と思う前に<br>3分だけ。")]
D[3] = [cover("実家の片付けで払う額は", bigtext("作業費<br>− 買取額")),
  rows("費用を決めるのは、<br>間取りではない", [("物の量<small>作業する人数、階段か、トラックが止められるか</small>",), ("売れる物があるか<small>着物・切手・古銭・ブランド品・貴金属など</small>",)],
       warn="同じ3LDKでも、払う額はまったく違います。料金表の金額だけで業者を比べても、あまり意味がありません。"),
  rows("国民生活センターに<br>寄せられた相談の例", [("見積もりのときに、契約をせかされた",), ("解約を申し出たら、高額なキャンセル料を請求された",), ("作業当日に追加料金を請求され、<b>見積額の2倍</b>を払った",)],
       src="出典：国民生活センター 報道発表資料（2018年7月19日）。遺品整理サービスの相談は年73〜114件（2013〜2017年度）"),
  ask("業者に頼む前に、<br>確かめること", [("見積もりは2〜3社から", "家を見てもらう。電話の概算で決めない"), ("追加料金の条件とキャンセル料", None)], "残り3つは、記事にまとめました"),
  cta("残すものは、<br>家族で選ぶ。")]
D[4] = [cover("親の名義のままの家、<br>名義変更の期限は", bigtext("2027年<br>3月31日")),
  rows("相続登記は<br>「義務」になった", [("始まり", "2024年4月1日"), ("期限", "知った日から3年"), ("放っておくと", "10万円以下の過料")],
       warn="2024年4月より前に相続した家も対象です。この場合の期限は2027年3月31日です。", src="出典：法務省「相続登記の申請義務化に関するQ&A」"),
  callslide("売るにも、貸すにも、<br>まず名義から", "売る・貸す・置いておく。<br>どの道を選んでも、<br><em>出発点は名義変更</em>です。",
       "親の代、祖父母の代の名義のまま放ってある家がないか、一度確かめてみてください。"),
  ask("名義の次に、<br>知っておきたいこと", [("一度貸すと、売るときの控除が使えなくなる", "最大3,000万円の特別控除"), ("空き家を放っておくと、固定資産税の軽減が外れることがある", None)], "売る・貸す・置いておくの比べ方は、記事に"),
  cta("思い出の家<br>だからこそ、<br>決め方は数字で。")]
D[5] = [cover("墓じまいの総額、<br>行き先だけで差が", big("88", "万円", "約")),
  rows("お墓を片付ける費用<br>（仮の例）", [("墓石の撤去（2㎡）", "20.0万円"), ("閉眼供養のお布施", "5.0万円"), ("離檀料", "10.0万円"), ("役所の手続き", "0.3万円")], total=("合計", "35.3万円"),
       warn="すべて仮の数字です。撤去費は1㎡あたり10万円程度の目安で計算。"),
  bars("移す先で、<br>総額はこれだけ違う", [("樹木葬へ移す", "103.1万円", 54, False), ("一般墓を建て直す", "191.0万円", 100, True)],
       call="片付ける費用は、どちらも35.3万円。<br>差の<em>約88万円</em>は、すべて行き先の違い。",
       src="行き先の価格：鎌倉新書「第16回 お墓の消費者全国実態調査（2025年）」の平均購入価格"),
  ask("見積もりで<br>見落としやすい費用", [("遺骨の数による追加", "1人分（1柱）ごとに料金がかかる契約がある"), ("離檀料", "法律で決まった料金ではない。お寺には早めに相談")], "3つ目は、記事にまとめました"),
  cta("守る人が<br>いなくなる前に、<br>行き先を決めておく。")]
D[6] = [cover("親の判断能力が落ちると、", bigtext("預金も実家も<br>動かせなくなる<br><small>ことがある</small>")),
  callslide("介護の費用を、<br>親のお金でまかなうなら", "本人の意思が確認できないと、<br><em>預金の引き出し</em>や<em>実家の売却</em>が<br>難しくなることがあります。",
       "介護の支払原資を、親の年金・貯蓄や実家の売却と考えている家ほど、早めの準備が必要です。"),
  rows("元気なうちに<br>取れる手段", [("家族信託<small>親の財産の管理を、家族に託す契約</small>",), ("任意後見<small>判断能力が落ちたときに備えて、支える人を元気なうちに決めておく契約</small>",)],
       warn="どれが合うかは、家族の状況で変わります。"),
  callslide("だから、<br>元気なうちに一度", "親と一緒に、<br><em>専門家に相談</em>しておくと<br>安心です。"),
  cta("お金の話は<br>切り出しにくい。<br>だから、<br>元気なうちに。")]
D[7] = [cover("自宅の土地の評価額が", big("80", "%減")),
  rows("使える条件<br>（主なもの）", [("亡くなった方が住んでいた家の土地",), ("配偶者や、同居していた家族などが相続する",), ("330㎡までの部分",)], src="小規模宅地等の特例（租税特別措置法第69条の4）。要件は細かく決まっています"),
  bars("仮の例で比べると", [("特例を使わない", "5,300万円", 100, True), ("基礎控除（母＋子2人）", "4,800万円", 91, False), ("特例を使う", "2,900万円", 55, False)],
       call="3,000万円の土地が600万円に。<br>合計が<em>基礎控除を下回ります</em>。", src="すべて仮の数字（土地3,000万円・建物300万円・預貯金2,000万円）"),
  callslide("ただし、<br>申告しないと使えない", "税金が0円になる場合でも、<br>相続を知った日の翌日から<br><em>10か月以内に申告</em>が必要です。",
       "要件を満たすかの判断が、税額を大きく左右します。相続税に慣れた税理士への相談がおすすめです。"),
  cta("0円でも、<br>申告が必要な<br>ことがある。")]
D[8] = [cover("相続放棄の期限は、原則", big("3", "か月")),
  callslide("片付ける前に、<br>知っておきたいこと", "遺品を処分したり<br>売ったりすると、<br>相続を受け入れたとみなされ、<br><em>放棄できなくなる</em><br>ことがあります。",
       "親に借金があるかもしれない場合、相続人は「相続放棄」を選べます。期限は原則、相続を知ってから3か月以内です。", src="民法第915条（相続の承認・放棄の期間）、第921条（法定単純承認）"),
  rows("片付けの前に、<br>確かめること", [("親に借金の心当たりはないか",), ("相続を知ってから、どのくらいたったか",)], warn="少しでも心当たりがあるなら、片付けを始める前に、司法書士や弁護士などの専門家に相談してください。"),
  ask("業者に頼む前にも、<br>確かめること", [("大切な物は、先に取り出す", "写真・手紙・通帳・権利証など。処分した物は戻りません"), ("見積もりは2〜3社から", "家の中を見てもらう")], "残り3つは、記事にまとめました"),
  cta("片付ける前に、<br>一度だけ<br>立ち止まって。")]
D[9] = [cover("空き家を放っておくと<br>外れることがある", big("6", "分の1")),
  rows("家が建つ土地の<br>固定資産税の軽減", [("対象", "200㎡以下の部分"), ("計算のもとが", "6分の1に")],
       warn="2023年12月の改正空家法で、管理が行き届いていない空き家として自治体から「勧告」を受けると、この軽減から外れることになりました。",
       src="出典：仙台市 改正空家法の案内（改正法の施行日・勧告と住宅用地特例）"),
  callslide("「6倍になる」とは<br>限らない", "税額が何倍になるかは、<br>土地の評価や<br><em>自治体の計算</em>で変わります。", "正確な額は、お住まいの自治体で<br>確認してください。"),
  ask("置いておくのにも、<br>お金がかかる", [("固定資産税", None), ("草刈り・換気・見回りの費用", None), ("実家までの交通費", None)]),
  cta("置いておくにも、<br>お金と手間が<br>かかる。")]
D[10] = [cover("墓じまいの見積もりは", bigtext("1人分？<br>全員分？")),
  callslide("遺骨の数で、<br>費用が変わる", "代々のお墓には、<br>何人分もの遺骨が<br>入っていることがあります。",
       "新しい納骨先によっては、遺骨<b>1人分（1柱）ごとに追加料金</b>がかかる契約があります。見積もりが「1人分」か「全員分」か、確かめてください。"),
  bars("墓じまいをする人は、<br>10年でほぼ倍に", [("2014年度", "約8万4千件", 48, False), ("2024年度", "約17万6千件", 100, True)],
       call="理由で多いのは<br>「お墓が遠い」<em>52.0%</em><br>「継ぐ人がいない」<em>44.1%</em>",
       src="出典：総務省 東北管区行政評価局（2026年1月）※改葬件数は厚生労働省「衛生行政報告例」"),
  ask("見積もりで<br>見落としやすい費用", [("遺骨の数による追加", None), ("離檀料", "法律で決まった料金ではない"), ("合祀は、あとから取り出せない", "親族に「手を合わせる場所を残したい」人はいないか")]),
  cta("ご先祖さまの<br>行き先は、<br>家族みんなで。")]

def page(slides):
    out = []
    for i, s in enumerate(slides, 1):
        if isinstance(s, tuple):
            s = f'<section class="s cs">{s[1]}{BRAND}<p class="pg">{i}/5</p></section>'
        elif not s.startswith("<section"):
            s = f'<section class="s">{s}{BRAND}<p class="pg">{i}/5</p></section>'
        out.append(s.replace('<section class="', f'<section id="s{i}" class="', 1))
    return f'<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">{CSS}</head><body>{"".join(out)}</body></html>'

