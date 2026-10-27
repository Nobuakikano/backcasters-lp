import html, json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
KIT=os.path.dirname(HERE)
from genko import DAYS, LABEL, build
items=[]
for i,d in enumerate(DAYS,1):
    b=build(i,d); v=d["video"]
    items.append(dict(n=i,date=d["date"],label=LABEL[d["t"]],title=d["title"],
      video=f"① {v[0]}\n② {v[1]}\n③ {v[2]}\n（最後に「続きはプロフィールから」）",**b))
import os
def zipa(i,d):
    z=[f for f in os.listdir(d) if f.endswith(".zip")]
    return f'<a class="dl pc" href="c/{i:02d}/{z[0]}" download>パソコンに保存（5枚をZIPで）</a>' if z else ""
def vid(i):
    d=os.path.join(KIT,"c",f"{i:02d}")
    if not os.path.isdir(d): return ""
    v=[f for f in os.listdir(d) if f.endswith("_short.mp4")]
    if not v: return ""
    u=f"c/{i:02d}/{v[0]}"
    return f'''<div class="blk"><div class="vrow"><video src="{u}#t=0.5" muted playsinline preload="metadata" controls></video>
<p>画像5枚をつないだ18秒の縦動画（音楽つき）。YouTubeのショートにそのまま使えます。</p></div>
<button type="button" class="dl sv" data-file="{u}">動画を送る（スマホ）</button><p class="msg"></p>
<a class="dl pc" href="{u}" download>パソコンに保存（動画）</a></div>'''
def imgs(i):
    d=os.path.join(KIT,"c",f"{i:02d}")
    if not os.path.isdir(d): return ""
    fs=sorted(f for f in os.listdir(d) if f.endswith(".jpg"))
    th="".join(f'<a href="c/{i:02d}/{f}" target="_blank"><img src="c/{i:02d}/{f}" alt="{k+1}枚目" loading="lazy"></a>' for k,f in enumerate(fs))
    data=",".join(f'"c/{i:02d}/{f}"' for f in fs)
    return f'''<h3>画像（{len(fs)}枚・Instagram用）</h3><div class="blk"><div class="thumbs">{th}</div>
<button type="button" class="dl sp" data-files='[{data}]'>{len(fs)}枚まとめて保存する（スマホ）</button><p class="msg"></p>
{zipa(i,d)}
<p class="hint">スマホでうまくいかないときは、画像を押して開き、長押しで「写真に追加」。パソコンはZIPを開くと5枚が入っています。</p></div>'''
def box(k,label,val,i):
    rows=min(14,max(3,val.count("\n")+2))
    return f'<div class="blk"><div class="bh"><span>{label}</span><button type="button" data-t="{k}{i}">コピー</button></div><textarea id="{k}{i}" readonly rows="{rows}">{html.escape(val)}</textarea></div>'
tabs="".join(f'<button type="button" class="tab" data-d="{it["n"]}"><small>{html.escape(it["date"])}</small><b>{it["label"]}</b></button>' for it in items)
secs=""
for it in items:
    i=it["n"]
    secs+=f'''<section class="day" id="d{i}" hidden>
<h2><em>{it["label"]}</em>{html.escape(it["title"])}</h2>
{imgs(i)}<h3>動画の文字（3場面・約18秒）</h3>{box("v","動画",it["video"],i)}
<h3>X</h3>{box("xb","本文",it["x_body"],i)}{box("xr","返信（リンク）",it["x_reply"],i)}
<h3>Instagram</h3>{box("ig","キャプション",it["ig"],i)}
<h3>YouTube（ショート）</h3>{vid(i)}{box("yt","タイトル",it["yt_title"],i)}{box("yd","説明",it["yt_desc"],i)}
</section>'''
dates=json.dumps([it["date"][:it["date"].index("（")] for it in items])
page=f'''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow"><title>毎日の原稿｜ひとりでやらない実家じまい</title>
<style>
:root{{--bg:#f4f1ea;--card:#fff;--ink:#1f2622;--muted:#5d6861;--green:#2b3a2f;--gold:#b98a4a;--stamp:#b5452f;--line:#e2ded3;--ok:#2f7d4f}}
@media (prefers-color-scheme: dark){{:root{{--bg:#141a16;--card:#1e2620;--ink:#e9ece7;--muted:#a3ada6;--green:#e6c99a;--gold:#e6c99a;--stamp:#e08a74;--line:#2e3831;--ok:#7fd0a0;color-scheme:dark}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif;line-height:1.7;padding:16px 16px 48px}}
main{{max-width:560px;margin:0 auto}}
h1{{font-size:19px;margin:0 0 4px}} .sub{{color:var(--muted);font-size:13px;margin:0 0 12px}}
.tabs{{display:flex;gap:6px;overflow-x:auto;padding-bottom:8px;position:sticky;top:0;background:var(--bg);z-index:2;padding-top:6px}}
.tab{{flex:none;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:10px;padding:6px 10px;font:inherit;cursor:pointer;text-align:center;line-height:1.3}}
.tab small{{display:block;font-size:11px;color:var(--muted)}} .tab b{{font-size:15px}}
.tab[aria-current=true]{{background:var(--green);color:var(--bg);border-color:var(--green)}} .tab[aria-current=true] small{{color:inherit}}
.tab.today::after{{content:"今日";display:block;font-size:10px;color:var(--stamp);font-weight:700}} .tab[aria-current=true].today::after{{color:inherit}}
.day h2{{font-size:17px;line-height:1.5;margin:12px 0 4px}}
.day h2 em{{font-style:normal;display:inline-block;border:2px solid var(--stamp);color:var(--stamp);border-radius:6px;padding:0 6px;margin-right:8px;font-size:14px}}
h3{{font-size:14px;margin:18px 0 6px;color:var(--muted)}}
.blk{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px;margin-bottom:8px}}
.bh{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;font-size:13px;font-weight:700}}
.bh button{{border:0;border-radius:8px;background:var(--green);color:var(--bg);font:inherit;font-weight:700;padding:6px 16px;cursor:pointer}}
.bh button.done{{background:var(--ok)}}
.thumbs{{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-bottom:10px}}.thumbs img{{width:100%;border-radius:6px;display:block;border:1px solid var(--line)}}
.dl{{display:block;text-align:center;text-decoration:none;box-sizing:border-box;width:100%;border:0;border-radius:10px;background:var(--green);color:var(--bg);font:inherit;font-weight:700;font-size:16px;padding:13px;cursor:pointer}}.dl.done{{background:var(--ok)}}.dl.pc{{margin-top:8px;background:transparent;color:var(--green);border:2px solid var(--green)}}
.msg{{font-size:13px;color:var(--ok);margin:6px 0 0;min-height:1em}}.hint{{font-size:12px;color:var(--muted);margin:4px 0 0}}
.vrow{{display:grid;grid-template-columns:120px 1fr;gap:12px;align-items:center;margin-bottom:10px}}.vrow video{{width:120px;border-radius:8px;background:#000}}.vrow p{{margin:0;font-size:13px;color:var(--muted)}}
textarea{{width:100%;border:1px solid var(--line);border-radius:8px;padding:8px;font:inherit;font-size:13px;background:var(--bg);color:var(--ink);resize:vertical}}
</style></head><body><main>
<h1>毎日の原稿</h1>
<p class="sub">介護→相続→遺品→実家→お墓 の順に1日1テーマ。数字はすべてサイトの記事と同じ出典です。</p>
<nav class="tabs">{tabs}</nav>
{secs}
</main><script>
const dates={dates};
const now=new Date(new Date().toLocaleString("en-US",{{timeZone:"Asia/Tokyo"}}));
const key=(now.getMonth()+1)+"/"+now.getDate();
let start=dates.indexOf(key)+1; if(start<1) start=1;
const tabs=[...document.querySelectorAll(".tab")];
if(dates.indexOf(key)>=0) tabs[start-1].classList.add("today");
function show(n){{document.querySelectorAll(".day").forEach(s=>s.hidden=s.id!=="d"+n);tabs.forEach(t=>t.setAttribute("aria-current",t.dataset.d==n));}}
tabs.forEach(t=>t.addEventListener("click",()=>show(t.dataset.d)));
show(start);
document.querySelectorAll(".bh button").forEach(b=>b.addEventListener("click",async()=>{{
  const a=document.getElementById(b.dataset.t);
  try{{await navigator.clipboard.writeText(a.value)}}catch(e){{a.removeAttribute("readonly");a.select();document.execCommand("copy");a.setAttribute("readonly","")}}
  b.textContent="コピーしました";b.classList.add("done");setTimeout(()=>{{b.textContent="コピー";b.classList.remove("done")}},2000);
}}));
document.querySelectorAll(".dl.sp").forEach(b=>b.addEventListener("click",async()=>{{
  const m=b.nextElementSibling;m.textContent="準備中…";
  try{{
    const urls=JSON.parse(b.dataset.files);
    const files=await Promise.all(urls.map(async u=>{{const r=await fetch(u);const bl=await r.blob();return new File([bl],u.split("/").pop(),{{type:"image/jpeg"}})}}));
    if(navigator.canShare&&navigator.canShare({{files}})){{await navigator.share({{files}});m.textContent="「画像を保存」を選ぶと写真に入ります";b.classList.add("done")}}
    else{{for(const f of files){{const a=document.createElement("a");a.href=URL.createObjectURL(f);a.download=f.name;document.body.appendChild(a);a.click();a.remove();await new Promise(r=>setTimeout(r,400))}}m.textContent="ダウンロードしました";b.classList.add("done")}}
  }}catch(e){{m.textContent=(e&&e.name==="AbortError")?"":"うまくいきませんでした。画像を押して長押しで保存してください"}}
}}));
document.querySelectorAll(".dl.sv").forEach(b=>b.addEventListener("click",async()=>{{
  const m=b.nextElementSibling;m.textContent="準備中…";
  try{{const r=await fetch(b.dataset.file);const bl=await r.blob();const f=new File([bl],b.dataset.file.split("/").pop(),{{type:"video/mp4"}});
    if(navigator.canShare&&navigator.canShare({{files:[f]}})){{await navigator.share({{files:[f]}});m.textContent="「ビデオを保存」またはYouTubeを選んでください";b.classList.add("done")}}
    else{{location.href=b.dataset.file}}
  }}catch(e){{m.textContent=(e&&e.name==="AbortError")?"":"うまくいきませんでした。もう一度押してください"}}
}}));
</script></body></html>'''
open(os.path.join(KIT,"index.html"),"w").write(page)
print(len(page))
