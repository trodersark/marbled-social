import sys, os
P = sys.argv[1]
POSTS = [
 ("h01","fulltable","Holiday 2026 · Serves 10","Holiday dinner,<br>done for you.","Dinners for 10 from $345. Hot delivery Dec 22 to 24."),
 ("h02","latkes","Hanukkah · First night Fri, Dec 4","Eight nights.<br>One less dinner.","Latkes and short ribs. Order by Wed, Dec 2."),
 ("h03","ribdinner","The Prime Rib Dinner · Serves 10","Prime rib,<br>done properly.","Horseradish cream, bordelaise, sides and pies. $620."),
 ("h04","shortribs","Build your own table","Pick an entree.<br>Fill the table.","Short ribs, ham, salmon or cauliflower steak, plus the sides."),
 ("h05","gingerbread","Holiday desserts","The dessert<br>table.","Gingerbread bars, peppermint brownies and pies."),
 ("h06","ribdinner","How Christmas works","Four days<br>to order hot.","Hot delivery Dec 22 to 24. Order by noon Mon, Dec 21."),
 ("h07","primerib","Hot cutoff","Hot orders<br>close Monday.","Noon Mon, Dec 21. Then it's cold pickup Christmas Eve."),
 ("h08","ham","Christmas Eve pickup","Still time.<br>Pick it up cold.","Order by Wed, Dec 23. Pick up Christmas Eve until 5pm."),
 ("h09","charcuterie","New Year's Eve","Ring it in<br>at home.","Charcuterie, steak and short ribs. Order by Tue, Dec 29."),
]
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;background:#2C4A36}
.post{width:1080px;display:flex;flex-direction:column;background:#2C4A36;color:#fff;overflow:hidden}
.photo{width:1080px;background-size:cover;background-position:center}
.band{padding:58px 72px 0;display:flex;flex-direction:column;flex:1}
.eb{font:700 26px/1 'Barlow Condensed',sans-serif;letter-spacing:6px;text-transform:uppercase;color:#A9C2AF}
h1{font:800 112px/0.92 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:1px;margin:20px 0 22px}
.sub{font:500 33px/1.3 Barlow,sans-serif;color:#E4EBE5;max-width:900px;text-wrap:balance}
.foot{display:flex;align-items:center;justify-content:space-between;border-top:2px solid rgba(255,255,255,.18);padding:26px 0 46px;margin-top:auto}
.foot img{height:84px;width:auto;margin-left:-10px}
.foot span{font:700 26px/1 'Barlow Condensed',sans-serif;letter-spacing:3px;text-transform:uppercase;color:#A9C2AF}
.story h1{font-size:146px;margin:26px 0 28px}
.story .eb{font-size:30px}
.story .sub{font-size:40px}
.story .band{padding-top:76px}
.story .foot{margin-top:48px}
.story .sticker{flex:1;min-height:300px}
"""
def doc(p, story):
    code, img, eb, h1, sub = p
    ph = 960 if story else 790
    h = 1920 if story else 1350
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@500&display=swap" rel="stylesheet">
<style>{CSS} .post{{height:{h}px}}</style></head><body>
<div class="post {'story' if story else ''}"><div class="photo" style="height:{ph}px;background-image:url('src/{img}.jpg')"></div>
<div class="band"><p class="eb">{eb}</p><h1>{h1}</h1><p class="sub">{sub}</p>
<div class="foot"><img src="src/logo-white.png" alt=""><span>order.marbled.la/holiday</span></div>
{'<div class="sticker"></div>' if story else ''}</div></div></body></html>"""
for p in POSTS:
    for story in (False, True):
        open(f"{P}/{p[0]}-{'story' if story else 'feed'}.html","w").write(doc(p, story))
print("ok")
