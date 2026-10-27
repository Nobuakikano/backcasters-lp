"""日ごとの画像5枚・ZIP・18秒の縦動画を作り、原稿ページを作り直す。
使い方: python3 make_day.py 11 12   （番号は genko.py の DAYS の順番＝slides.py の D のキー）
"""
import os, sys, subprocess, zipfile, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
KIT = os.path.dirname(HERE)
from slides import D, page
from PIL import Image
from playwright.sync_api import sync_playwright

def check(pg):
    return pg.evaluate("""[...document.querySelectorAll('section')].map(s=>{const t=s.getBoundingClientRect().top;let m=0;
      s.querySelectorAll('.f,.warn,.call,.ask,.bars,.body,.big,.bigtext,.lead,.msg,.btn').forEach(e=>m=Math.max(m,e.getBoundingClientRect().bottom-t));
      const src=s.querySelector('.src');const lim=src?src.getBoundingClientRect().top-t:1350-110;
      const cover=s.classList.contains('c1');const lim2=cover?910:lim;
      const wide=[...s.querySelectorAll('.big,.bigtext,.lead,.h')].some(e=>e.getBoundingClientRect().right-s.getBoundingClientRect().left>1080-60);
      return {bottom:Math.round(m),limit:Math.round(lim2),overflow:m>lim2||wide}})""")

def video(out, N):
    ins = []
    for i in range(1, 6): ins += ["-loop", "1", "-t", "4", "-i", f"{out}/jikka_{N}_{i}.jpg"]
    pad = ",".join([])
    fc = "".join(f"[{i}]scale=1080:1350,pad=1080:1920:0:285:color=0xf6f2e9,setsar=1,fps=30[v{i}];" for i in range(5))
    fc += "[v0][v1]xfade=transition=fade:duration=0.4:offset=3.6[a1];[a1][v2]xfade=transition=fade:duration=0.4:offset=7.2[a2];"
    fc += "[a2][v3]xfade=transition=fade:duration=0.4:offset=10.8[a3];[a3][v4]xfade=transition=fade:duration=0.4:offset=14.4,format=yuv420p[v];"
    fc += "[5]afade=t=out:st=16.8:d=1.2[a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-i", os.path.join(HERE, "bgm.m4a"), "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-t", "18", "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{out}/jikka_{N}_short.mp4"], check=True)

def main(days):
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for n in days:
            N = f"{n:03d}"; out = os.path.join(KIT, "c", f"{n:02d}"); os.makedirs(out, exist_ok=True)
            html = page(D[n]).replace("url(house.jpg)", f"url(file://{HERE}/house.jpg)")
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f: f.write(html); tmp = f.name
            pg.goto("file://" + tmp); pg.wait_for_timeout(500)
            r = check(pg); print(n, r)
            if any(x["overflow"] for x in r): bad.append(n)
            for i in range(1, 6):
                pg.locator(f"#s{i}").screenshot(path=f"{out}/_{i}.png")
                Image.open(f"{out}/_{i}.png").convert("RGB").save(f"{out}/jikka_{N}_{i}.jpg", quality=92); os.remove(f"{out}/_{i}.png")
            with zipfile.ZipFile(f"{out}/jikka_{N}_images.zip", "w") as z:
                for i in range(1, 6): z.write(f"{out}/jikka_{N}_{i}.jpg", f"jikka_{N}_{i}.jpg")
            video(out, N)
            sh = Image.new("RGB", (5 * 368, 450), "white")
            for i in range(1, 6): sh.paste(Image.open(f"{out}/jikka_{N}_{i}.jpg").resize((360, 450)), ((i - 1) * 368, 0))
            sh.save(os.path.join(tempfile.gettempdir(), f"sheet_{N}.jpg")); print("一覧:", os.path.join(tempfile.gettempdir(), f"sheet_{N}.jpg"))
        b.close()
    subprocess.run([sys.executable, os.path.join(HERE, "build_page.py")], check=True)
    if bad: print("★はみ出しの疑い:", bad)

if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]])
