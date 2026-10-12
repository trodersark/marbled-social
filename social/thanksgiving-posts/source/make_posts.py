import sys, os
P = sys.argv[1]
POSTS = [
 ("tg01","classic","Thanksgiving 2026 · Serves 10","Thanksgiving,<br>minus the dishes.","Three tables for ten, from $345. Orders close noon Mon, Nov 23."),
 ("tg02","fulltable","The Thanksgiving menu","The menu,<br>annotated.","Every dish, a one-line opinion and an add button."),
 ("tg04","stuffing","Build your own table","The sides<br>do the work.","Stuffing, mash, yams, mac and brussels. Half pans serve 10 to 12."),
 ("tg08","harvest","Office Thanksgiving","Thanksgiving<br>for the office.","Delivered hot and on time. Order by noon Mon, Nov 23."),
 ("tg06","turkey","Two ways to do Thanksgiving","Hot<br>or cold?","Hot and ready Thursday, or chilled a day early with a reheating guide."),
 ("tg03","gravy","Thanksgiving 2026","24, 10, 1, 0.","Hours of brine. People per table. Delivery window. Pans to scrub."),
 ("tg05","mash","The Thanksgiving countdown","Two weeks<br>until the table.","Lock it in now. Orders close noon Mon, Nov 23."),
 ("tg07","pumpkin","Handmade, 9 inch","Leave room<br>for pie.","Pumpkin, pecan, apple and mixed berry. $55 each."),
 ("tg09","turkeyhalf","The turkey question","Carve it. Or<br>keep it whole.","Brined 24 hours. Full turkey $240, carved for $25 more."),
 ("tg10","yams","Last call","The oven&rsquo;s<br>almost full.","Hot Thanksgiving orders close at noon Monday, Nov 23."),
 ("tg11","brussels","Still time","Missed it?<br>Pick it up cold.","Cold, with reheating instructions. Pick up Wed, Nov 25 or Thanksgiving morning."),
]
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;background:var(--band)}
.post{width:1080px;display:flex;flex-direction:column;background:var(--band);color:#fff;overflow:hidden}
.photo{width:1080px;background-size:cover;background-position:center}
.band{padding:58px 72px 0;display:flex;flex-direction:column;flex:1}
.eb{font:700 26px/1 'Barlow Condensed',sans-serif;letter-spacing:6px;text-transform:uppercase;color:var(--label)}
h1{font:800 112px/0.92 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:1px;margin:20px 0 22px}
.sub{font:500 33px/1.3 Barlow,sans-serif;color:#E4EBE5;max-width:900px;text-wrap:balance}
.foot{display:flex;align-items:center;justify-content:space-between;border-top:3px solid var(--rule);padding:26px 0 46px;margin-top:auto}
.foot img{height:84px;width:auto;margin-left:-10px}
.foot span{font:700 26px/1 'Barlow Condensed',sans-serif;letter-spacing:3px;text-transform:uppercase;color:var(--label)}
.story h1{font-size:146px;margin:26px 0 28px}
.story .eb{font-size:30px}
.story .sub{font-size:40px}
.story .band{padding-top:76px}
.story .foot{margin-top:48px}
.story .sticker{flex:1;min-height:300px}
"""
# Thanksgiving keeps the brand greens (the holiday posts use their own palette).
PAL = {"holiday": ("#2C4A36", "#A9C2AF", "rgba(255,255,255,.22)")}

def doc(p, story):
    code, img, eb, h1, sub = p
    band, label, rule = PAL.get(code, PAL["holiday"])
    ph = 960 if story else 790
    h = 1920 if story else 1350
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@500&display=swap" rel="stylesheet">
<style>:root{{--band:{band};--label:{label};--rule:{rule}}}{CSS} .post{{height:{h}px}}</style></head><body>
<div class="post {'story' if story else ''}"><div class="photo" style="height:{ph}px;background-image:url('src/{img}.jpg')"></div>
<div class="band"><p class="eb">{eb}</p><h1>{h1}</h1><p class="sub">{sub}</p>
<div class="foot"><img src="src/logo-white.png" alt=""><span>order.marbled.la/thanksgiving</span></div>
{'<div class="sticker"></div>' if story else ''}</div></div></body></html>"""
for p in POSTS:
    for story in (False, True):
        open(f"{P}/{p[0]}-{'story' if story else 'feed'}.html","w").write(doc(p, story))
print("ok")
