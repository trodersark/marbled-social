"""Marbled LA holiday 2026 emails. python3 build.py OUTDIR IMGBASE
IMGBASE: prefix for image files, e.g. "../img/" for local preview or a CDN URL."""
import os, sys, json

OUT = sys.argv[1]
IMG = sys.argv[2]
STORE = "https://order.marbled.la/holiday"

G, DG, INK, MUTE, LINE, SAGE = "#4A7C59", "#2C4A36", "#161616", "#6B6F68", "#DAD8D1", "#9FB7A5"
COND = "'Barlow Condensed','Arial Narrow',Arial,sans-serif"
BODY = "Barlow,'Helvetica Neue',Arial,sans-serif"

# key: (id, short name, price, line, image key)
P = {
 "ham_dinner": ("cmumtcu5s0000cy260xj7j6lq", "The Ham Dinner", 345, "Save $19", "hamdinner"),
 "rib_dinner": ("cmumtcubc0001cy26gu8p5i0h", "The Prime Rib Dinner", 620, "Save $34", "ribdinner"),
 "full_table": ("cmumtcuf20002cy269vnimd8g", "The Full Table", 925, "Save $47", "fulltable"),
 "primerib": ("cmrtuys7j000satbrmf7wle9b", "Roasted Prime Rib", 240, "Horseradish cream, red wine bordelaise. Serves 8 to 10.", "primerib"),
 "ham": ("cmrtuyttz000vatbrgszs95e8", "Honey Glazed Ham", 120, "Caramelized edges, warm spices. Serves 8 to 10.", "ham"),
 "shortribs": ("cmulwb3aj000011xdt93ngcu1", "Short Ribs", 198, "Braised in red wine with shallots and carrots. Serves 8 to 10.", "shortribs"),
 "salmon": ("cmrtuyrox000ratbrbj8eheid", "Roasted Salmon", 180, "Lemon herb beurre blanc. Serves 10 to 12.", "salmon"),
 "cauli": ("cmrtuxjux000dd5c1s23xzmmi", "Cauliflower Steak", 84, "Vegan. Seared with garlic and thyme. Serves 8 to 10.", "cauli"),
 "skirt": ("cmrtuy3qm0015d5c1qi0ga197", "Skirt Steak", 180, "Char grilled, red chimichurri. Serves 10 to 12.", "skirt"),
 "tritip": ("cmrtuyt8l000uatbrmls0njmk", "Tri-Tip", 144, "Blackened, tomato and garlic confit. Serves 8 to 10.", "tritip"),
 "latkes": ("cmulwb3jc000211xd3v88hgg5", "Potato Latkes", 82, "Apple compote, chive sour cream. Serves 10 to 12.", "latkes"),
 "carrots": ("cmrtuynd6000katbrj8kr8db7", "Cumin Carrots", 66, "Vegan. Caramelized onion, dill. Serves 10 to 12.", "carrots"),
 "citrus": ("cmulwb3ft000111xd6acntmtp", "Winter Citrus Salad", 84, "Blood orange, pomegranate, pistachio. Serves 10 to 12.", "citrus"),
 "mash": ("cmrtuyqqa000patbrcafu8c4u", "Mashed Potatoes", 66, "Whipped with confit garlic. Serves 10 to 12.", "mash"),
 "brussels": ("cmrtuyrcn000qatbr8x5pjeb5", "Brussels Sprouts", 78, "Sherry molasses glaze. Serves 10 to 12.", "brussels"),
 "mac": ("cmrtuy3b10014d5c1gcj77aak", "Jalape&ntilde;o Mac", 78, "Cheddar, bacon, breadcrumb crust. Serves 10 to 12.", "mac"),
 "spinach": ("cmrtuymad000jatbroe5w78k1", "Creamed Spinach", 66, "A little nutmeg, a lot of cream. Serves 10 to 12.", "spinach"),
 "gravy": ("cmrtuyk5h000fatbrl1px28gf", "Gravy", 35, "32 oz, fresh herbs.", "gravy"),
 "marketveg": ("cmrtuy1o40013d5c1rm3wbq41", "Market Vegetables", 66, "Vegan. Roasted with herbs. Serves 10 to 12.", "marketveg"),
 "farmsalad": ("cmrtuyi5q000batbrw75lzcma", "Farmer's Market Salad", 66, "Vegan. Lemon vinaigrette. Serves 10 to 12.", "farmsalad"),
 "gingerbread": ("cmulwb3qf000411xdqsch7u9h", "Gingerbread Bars", 54, "Molasses, warm spice, cream cheese frosting. Serves 10.", "gingerbread"),
 "peppermint": ("cmulwb3ty000511xdp4orc92b", "Peppermint Brownies", 54, "Dark chocolate, crushed candy cane. Serves 10.", "peppermint"),
 "pecan": ("cmrtuxsok000pd5c1mgsqtvuv", "Pecan Pie", 55, "Handmade, 9 inch, butter crust.", "pecan"),
 "apple": ("cmrtuyfhw0007atbr8rkv0uim", "Apple Pie", 55, "Handmade, 9 inch, spiced apples.", "apple"),
 "cheesecake": ("cmrtuycx40004atbreudp76qq", "Cheesecake", 55, "Berry compote, 9 inch. Serves 10.", "cheesecake"),
 "cookies": ("cmrtuydth0005atbrlo0dgd1f", "Sea Salt Cookies", 44, "Chocolate chip, one dozen.", "cookies"),
 "brownies20": ("cmrtuy7if0025d5c1skqzteoz", "Brownies for 20", 70, "Fudgy, chewy, gone fast.", "brownies20"),
 "charcuterie": ("cmrtuyj64000datbrfe1xyzmp", "Charcuterie Platter", 204, "Cheeses, cured meats, crostini. Serves 12 to 15.", "charcuterie"),
 "crudite": ("cmrtuy8t8002dd5c1n8b92pjs", "Crudit&eacute; Platter", 140, "Market vegetables, assorted dips. Serves 18 to 20.", "crudite"),
 "chafing": ("cmrtuxice000ad5c1x6vrkqe9", "Chafing Dishes", 38, "Per set, with fuel and water pans.", "chafing"),
 "plates": ("cmrtuxhho0008d5c19q08v1nn", "Plates + Cutlery", 27, "Heavy duty plates and cutlery for 12.", "plates"),
}

def esc_id(k): return P[k][0]

class Email:
    def __init__(self, code, campaign, corp=False):
        self.code, self.campaign, self.corp = code, campaign, corp
        self.parts = []
    def url(self, slot, add=None):
        u = f"{STORE}?utm_source=mailchimp&utm_medium=email&utm_campaign={self.campaign}&utm_content={self.code}-{slot}"
        if add:
            ids = ",".join(esc_id(k) for k in (add if isinstance(add, (list, tuple)) else [add]))
            u += f"&add={ids}"
        return u

    # ---- blocks ----
    def bar(self, text, prefix=""):
        pre = f'<span class="hide-m">{prefix} &nbsp;&middot;&nbsp; </span>' if prefix else ""
        self.parts.append(f'''<tr><td bgcolor="{G}" align="center" style="background:{G};padding:11px 20px;" mc:edit="deadline">
  <a class="bar" href="{self.url('deadline-bar')}" target="_blank" style="font-family:{COND};font-size:14px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FFFFFF;text-decoration:none;">{pre}{text} &rarr;</a>
</td></tr>
<tr><td bgcolor="#FFFFFF" style="padding:18px 32px;background:#FFFFFF;border-bottom:1px solid {LINE};" class="pad">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
    <td align="left" valign="middle"><a href="{self.url('logo')}" target="_blank" style="text-decoration:none;"><img src="{IMG}logo.png" width="140" alt="Marbled LA" style="display:block;width:140px;height:auto;border:0;"></a></td>
    <td align="right" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="{INK}" style="background:{INK};">
      <a href="{self.url('header')}" target="_blank" style="display:block;padding:11px 18px;font-family:{COND};font-size:14px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#FFFFFF;text-decoration:none;">Order now</a></td></tr></table></td>
  </tr></table>
</td></tr>''')

    def button(self, label, href, bg=G, big=True):
        pad = "21px 38px" if big else "16px 24px"
        fs = 22 if big else 18
        return f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" class="btn" style="margin:0 auto;"><tr>
<td align="center" bgcolor="{bg}" style="background:{bg};">
<a href="{href}" target="_blank" style="display:block;padding:{pad};font-family:{COND};font-size:{fs}px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:#FFFFFF;text-decoration:none;text-align:center;">{label}</a>
</td></tr></table>'''

    def intro(self, eyebrow, h1, body, cta, cta_add=None, size=72):
        self.parts.append(f'''<tr><td bgcolor="#FFFFFF" style="padding:48px 44px 36px;background:#FFFFFF;" class="pad" mc:edit="intro"><p style="margin:0;font-family:{COND};font-size:15px;font-weight:700;letter-spacing:4px;text-transform:uppercase;color:{G};text-align:center;">{eyebrow}</p><div style="height:10px;line-height:10px;font-size:1px;">&nbsp;</div><h1 style="margin:0;font-family:{COND};font-size:{size}px;line-height:1;font-weight:800;text-transform:uppercase;letter-spacing:.5px;color:{INK};text-align:center;" class="h1">{h1}</h1><p style="margin:20px 0 0;font-family:{BODY};font-size:18px;line-height:1.55;color:{INK};text-align:center;">{body}</p><div style="height:24px;line-height:24px;font-size:1px;">&nbsp;</div>{self.button(cta + '&nbsp;&rarr;' if not cta.startswith('+') else cta, self.url('hero-cta', cta_add))}</td></tr>''')

    def hero(self, img, alt, add=None):
        self.parts.append(f'''<tr><td style="padding:0;"><a href="{self.url('hero-img', add)}" target="_blank" style="text-decoration:none;"><img src="{IMG}{img}-hero.jpg" width="600" height="360" alt="{alt}" style="display:block;width:100%;max-width:600px;height:auto;border:0;outline:none;" class="fluid"></a></td></tr>''')

    def heading(self, eyebrow, h2, body=None, bg="#FFFFFF", top=40):
        b = f'<p style="margin:12px 0 0;font-family:{BODY};font-size:17px;line-height:1.55;color:{INK};text-align:center;">{body}</p>' if body else ""
        self.parts.append(f'''<tr><td bgcolor="{bg}" style="padding:{top}px 44px 6px;background:{bg};" class="pad"><p style="margin:0;font-family:{COND};font-size:14px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{G};text-align:center;">{eyebrow}</p><h2 style="margin:8px 0 0;font-family:{COND};font-size:40px;line-height:1;font-weight:800;text-transform:uppercase;color:{INK};text-align:center;" class="h1">{h2}</h2>{b}</td></tr>''')

    def packages(self, keys, note):
        rows = ""
        for i, k in enumerate(keys):
            pid, name, price, save, _ = P[k]
            bg = G if i == 1 else INK
            rows += f'''<tr><td style="padding:14px 0;border-bottom:1px solid {LINE};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td valign="middle" style="font-family:{COND};font-size:24px;font-weight:800;text-transform:uppercase;color:{INK};">{name}<br><span style="font-size:15px;color:{G};letter-spacing:1px;">${price} &middot; {save.upper()}</span></td>
<td valign="middle" align="right" width="150" style="width:150px;"><a href="{self.url('add-' + k, k)}" target="_blank" style="display:inline-block;background:{bg};color:#FFFFFF;font-family:{COND};font-size:15px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;padding:13px 16px;white-space:nowrap;">Add to cart</a></td></tr></table></td></tr>'''
        self.parts.append(f'''<tr><td bgcolor="#FFFFFF" style="padding:22px 44px 38px;background:#FFFFFF;" class="pad" mc:edit="packages"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table><p style="margin:14px 0 0;font-family:{BODY};font-size:15px;line-height:1.55;color:{MUTE};text-align:center;">{note}</p></td></tr>''')

    def tiles(self, keys, bg="#F6F5F1", txt_h=112):
        """2-up product tiles. Equal column widths and fixed text height so buttons line up."""
        cells = []
        for k in keys:
            pid, name, price, line, img = P[k]
            cells.append(f'''<td width="260" valign="top" style="width:260px;padding-bottom:24px;" class="stack tile"><a href="{self.url('img-' + k, k)}" target="_blank" style="text-decoration:none;"><img src="{IMG}{img}-tile.jpg" width="260" height="186" alt="{name}" style="display:block;width:100%;max-width:260px;height:auto;border:0;outline:none;" class="fluid"></a><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td height="{txt_h}" valign="top" class="tile-txt" style="height:{txt_h}px;vertical-align:top;">
<p style="margin:12px 0 0;font-family:{COND};font-size:23px;font-weight:800;text-transform:uppercase;color:{INK};line-height:1;">{name} <span style="color:{G};">${price}</span></p>
<p style="margin:6px 0 0;font-family:{BODY};font-size:15px;line-height:1.45;color:{MUTE};">{line}</p></td></tr></table><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:10px;"><tr>
<td align="center" bgcolor="{INK}" style="background:{INK};"><a href="{self.url('add-' + k, k)}" target="_blank" style="display:block;padding:12px 10px;font-family:{COND};font-size:15px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:#FFFFFF;text-decoration:none;">+ Add to cart</a></td></tr></table></td>''')
        rows = ""
        for i in range(0, len(cells), 2):
            pair = cells[i:i + 2]
            if len(pair) == 1:
                pair.append('<td width="260" class="hide-m" style="width:260px;">&nbsp;</td>')
            rows += f'<tr>{pair[0]}<td width="40" class="hide-m" style="width:40px;">&nbsp;</td>{pair[1]}</tr>'
        self.parts.append(f'''<tr><td bgcolor="{bg}" style="padding:30px 40px 12px;background:{bg};" class="pad" mc:edit="grid"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="table-layout:fixed;">{rows}</table></td></tr>''')

    def bundle(self, eyebrow, title, keys, note, bg="#F6F5F1"):
        total = sum(P[k][2] for k in keys)
        names = " + ".join(P[k][1] for k in keys)
        self.parts.append(f'''<tr><td bgcolor="{bg}" style="padding:4px 40px 40px;background:{bg};" class="pad"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:2px solid {INK};background:#FFFFFF;"><tr><td class="bpad" style="padding:26px 26px 28px;" bgcolor="#FFFFFF"><p style="margin:0;font-family:{COND};font-size:14px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{G};text-align:center;">{eyebrow}</p><p class="bt" style="margin:8px 0 0;font-family:{COND};font-size:32px;line-height:1;font-weight:800;text-transform:uppercase;color:{INK};text-align:center;">{title} <span style="color:{G};">${total}</span></p><p style="margin:10px 0 18px;font-family:{BODY};font-size:15px;line-height:1.5;color:{MUTE};text-align:center;">{names}. {note}</p>{self.button('+ Add all to cart', self.url('add-bundle', keys), G, big=False)}</td></tr></table></td></tr>''')

    def strip(self, keys):
        cells = "".join(f'''<td width="25%" style="width:25%;"><a href="{self.url('img-' + k, k)}" target="_blank" style="text-decoration:none;"><img src="{IMG}{P[k][4]}-sq.jpg" width="150" height="150" alt="{P[k][1]}" style="display:block;width:100%;max-width:150px;height:auto;border:0;outline:none;" class="fluid"></a></td>''' for k in keys)
        self.parts.append(f'<tr><td style="padding:0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{cells}</tr></table></td></tr>')

    def contents(self, title, items):
        half = (len(items) + 1) // 2
        col = lambda xs: "".join(f'<p style="margin:0 0 9px;font-family:{BODY};font-size:16px;line-height:1.4;color:{INK};"><span style="color:{G};font-weight:600;">+</span>&nbsp; {x}</p>' for x in xs)
        self.parts.append(f'''<tr><td bgcolor="#F6F5F1" style="padding:34px 44px 26px;background:#F6F5F1;" class="pad"><p style="margin:0 0 16px;font-family:{COND};font-size:14px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{G};">{title}</p><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td width="50%" valign="top" class="stack" style="width:50%;">{col(items[:half])}</td><td width="50%" valign="top" class="stack" style="width:50%;">{col(items[half:])}</td></tr></table></td></tr>''')

    def timeline(self, steps):
        rows = ""
        for i, (when, title, text, hot) in enumerate(steps):
            last = i == len(steps) - 1
            dot = G if hot else INK
            wc = "#FFFFFF" if hot else SAGE
            line = "" if last else f'<div style="width:2px;height:58px;background:#3A3A36;margin:4px 0 0 7px;"></div>'
            pb = "0" if last else "24px"
            rows += f'''<tr><td width="118" valign="top" style="width:118px;padding:0 14px {pb} 0;font-family:{COND};font-size:15px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{wc};">{when}</td>
<td width="18" valign="top" style="width:18px;"><div style="width:14px;height:14px;border-radius:7px;background:{dot};border:2px solid {G};"></div>{line}</td>
<td valign="top" style="padding:0 0 {pb} 14px;"><p style="margin:0;font-family:{COND};font-size:24px;font-weight:800;text-transform:uppercase;color:#FFFFFF;line-height:1;">{title}</p>
<p style="margin:6px 0 0;font-family:{BODY};font-size:15px;line-height:1.5;color:#BDBDB6;">{text}</p></td></tr>'''
        self.parts.append(f'<tr><td bgcolor="{INK}" style="padding:38px 40px 42px;background:{INK};" class="pad" mc:edit="timeline"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table></td></tr>')

    def closing(self, eyebrow, h1, cta, small):
        self.parts.append(f'''<tr><td bgcolor="{DG}" style="padding:46px 40px 48px;background:{DG};" class="pad" mc:edit="closing"><p style="margin:0 0 10px;font-family:{COND};font-size:14px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{SAGE};text-align:center;">{eyebrow}</p><h1 style="margin:0;font-family:{COND};font-size:44px;line-height:1;font-weight:800;text-transform:uppercase;letter-spacing:.5px;color:#FFFFFF;text-align:center;" class="h1">{h1}</h1><div style="height:26px;line-height:26px;font-size:1px;">&nbsp;</div>{self.button(cta + '&nbsp;&rarr;', self.url('closing'))}<p style="margin:18px 0 0;font-family:{BODY};font-size:14px;line-height:1.6;color:#BDBDB6;text-align:center;">{small}</p></td></tr>''')

    def html(self):
        who = "your team signed up" if self.corp else "you signed up"
        footer = f'''<tr><td bgcolor="{INK}" style="padding:30px 32px 34px;background:{INK};" class="pad" mc:edit="footer">
  <p style="margin:0;font-family:{COND};font-size:20px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#FFFFFF;">Marbled LA</p>
  <p style="margin:8px 0 0;font-family:{BODY};font-size:14px;line-height:1.6;color:#BDBDB6;">Questions about your order? Reply to this email or call <a href="tel:+13239633475" style="color:#FFFFFF;text-decoration:none;">323.963.3475</a>.<br>
  <a href="mailto:info@marbled.la" style="color:#BDBDB6;text-decoration:none;">info@marbled.la</a> &nbsp;&middot;&nbsp; <a href="https://www.marbled.la" style="color:#BDBDB6;text-decoration:none;">marbled.la</a></p>
  <p style="margin:18px 0 0;font-family:{BODY};font-size:12px;line-height:1.6;color:#8A8A84;">You're getting this because {who} with Marbled LA or ordered from us. <a href="*|UPDATE_PROFILE|*" style="color:#8A8A84;">Update preferences</a> &middot; <a href="*|UNSUB|*" style="color:#8A8A84;">Unsubscribe</a><br>*|LIST:ADDRESSLINE|*</p>
</td></tr>'''
        body = "\n".join(self.parts) + footer
        # Mailchimp needs every mc:edit name unique; a repeated name (two product
        # grids in one email) makes both blocks show the same content.
        seen = {}
        def uniq(m):
            seen[m.group(1)] = seen.get(m.group(1), 0) + 1
            n = seen[m.group(1)]
            return f'mc:edit="{m.group(1)}{n if n > 1 else ""}"'
        body = __import__("re").sub(r'mc:edit="([^"]+)"', uniq, body)
        return HEAD + body + TAIL

HEAD = """<!doctype html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<title>*|MC:SUBJECT|*</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;700;800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { margin:0; padding:0; width:100% !important; -webkit-text-size-adjust:100%; }
  img { -ms-interpolation-mode:bicubic; }
  a { color:#4A7C59; }
  @media (max-width:620px) {
    .wrap { width:100% !important; }
    .pad { padding-left:22px !important; padding-right:22px !important; }
    td.stack, table.stack > tbody > tr > td, table.stack > tr > td { display:block !important; width:100% !important; box-sizing:border-box; }
    .h1 { font-size:40px !important; }
    .fluid { width:100% !important; max-width:100% !important; height:auto !important; }
    .stack img.fluid { width:100% !important; }
    .hide-m { display:none !important; }
    .btn { width:100% !important; }
    .tile { padding-bottom:26px !important; }
    .tile-txt { height:auto !important; }
    .bt { font-size:26px !important; }
    .bpad { padding:22px 16px 22px !important; }
    .bar { font-size:11px !important; letter-spacing:1px !important; }
    .btn a { padding-left:14px !important; padding-right:14px !important; font-size:18px !important; }
  }
</style>
<!--[if mso]><style>* { font-family: Arial, sans-serif !important; }</style><![endif]-->
</head>
<body style="margin:0;padding:0;background:#FFFFFF;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all;">*|MC_PREVIEW_TEXT|*&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" style="background:#FFFFFF;">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" class="wrap" style="width:600px;max-width:600px;">
"""
TAIL = """
</table>
</td></tr>
</table>
</body>
</html>
"""

XMAS_BAR = ("Christmas hot orders close noon Mon, Dec 21", "")
XMAS_SMALL = "Hot delivery Dec 22 to 24 &nbsp;&middot;&nbsp; Cold pickup Christmas Eve &nbsp;&middot;&nbsp; Every dish labeled with allergens"
PKGS = ["ham_dinner", "rib_dinner", "full_table"]
HC, CC = "holiday-2026", "holiday-2026-corp"
emails = []

def mk(code, corp=False):
    e = Email(code, CC if corp else HC, corp); emails.append(e); return e

# ---------------- HOME ----------------
e = mk("h01-menu-open")
e.bar(*XMAS_BAR)
e.intro("Holiday 2026 &middot; serves 10", "Holiday dinner,<br>handled.",
        "Prime rib, honey glazed ham, sides, salads and pies, cooked in our kitchen and ready for yours. Hot delivery Dec 22 to 24, or pick it up cold with a reheating guide.",
        "See the holiday menu")
e.hero("fulltable", "The Full Table, holiday dinner for 10", "full_table")
e.packages(PKGS, "Each feeds ten. Add or swap anything after.")
e.heading("New this year", "Fresh on the menu", top=36, bg="#F6F5F1")
e.tiles(["shortribs", "latkes", "citrus", "peppermint"])
e.closing("Christmas hot orders close noon Mon, Dec 21", "Book it before the calendar fills.", "Order holiday dinner", XMAS_SMALL)

e = mk("h02-hanukkah")
e.bar("Hanukkah orders by Wed, Dec 2", "First night Fri, Dec 4")
e.intro("Hanukkah &middot; first night Fri, Dec 4", "Eight nights.<br>One less dinner.",
        "Crisp latkes with apple compote and chive sour cream. Short ribs braised in red wine until they fall apart. You light the candles, we cook. Order with 48 hours&rsquo; notice, hot or cold.",
        "Order for Hanukkah")
e.hero("latkes", "Potato latkes with apple compote", "latkes")
e.heading("The first-night table", "Pick your dishes", top=36, bg="#F6F5F1")
e.tiles(["latkes", "shortribs", "salmon", "carrots", "citrus", "cheesecake"])
e.bundle("One tap", "First night for 10", ["latkes", "shortribs", "carrots", "citrus"], "Serves 10.")
e.closing("Order by Wed, Dec 2 for Fri, Dec 4", "Light the candles. We&rsquo;ve got dinner.", "Order for Hanukkah",
          "48 hours&rsquo; notice &nbsp;&middot;&nbsp; Hot or cold &nbsp;&middot;&nbsp; Every dish labeled with allergens")

e = mk("h03-prime-rib")
e.bar(*XMAS_BAR)
e.intro("The centerpiece", "Prime rib,<br>done properly.",
        "Slow roasted, with horseradish cream and red wine bordelaise. The Prime Rib Dinner brings everything else to the table too. Ten people, $620.",
        "+ Add the Prime Rib Dinner", "rib_dinner")
e.hero("ribdinner", "The Prime Rib Dinner for 10", "rib_dinner")
e.contents("What&rsquo;s in the Prime Rib Dinner", ["Roasted prime rib", "Mashed potatoes", "Roasted brussels sprouts", "Candied yams", "Gravy with fresh herbs", "Buttermilk biscuits", "Roasted beet salad", "Handmade apple pie"])
e.heading("Or go your own way", "Just the roast, or more", top=36, bg="#F6F5F1")
e.tiles(["primerib", "ham"])
e.closing("Christmas hot orders close noon Mon, Dec 21", "Carve it at the table.", "Order prime rib", XMAS_SMALL)

e = mk("h04-build-your-own")
e.bar(*XMAS_BAR)
e.intro("Build your own", "Pick an entree.<br>Fill the table.",
        "Not a package person? Start with one entree, then add the sides your family actually fights over. One tap each.",
        "Start with an entree")
e.heading("Step one", "The entree", top=36, bg="#F6F5F1")
e.tiles(["shortribs", "ham", "salmon", "cauli"])
e.heading("Step two", "The sides", top=8, bg="#F6F5F1")
e.tiles(["mash", "brussels", "mac", "spinach"])
e.bundle("The usual suspects", "Mash, brussels + gravy", ["mash", "brussels", "gravy"], "Feeds 10 to 12.")
e.closing("Christmas hot orders close noon Mon, Dec 21", "Your table, your rules.", "Build your table", XMAS_SMALL)

e = mk("h05-desserts")
e.bar(*XMAS_BAR)
e.intro("Holiday desserts", "Leave room<br>for dessert.",
        "Gingerbread with cream cheese frosting. Dark chocolate brownies with crushed candy cane. Handmade pies with a flaky butter crust.",
        "See desserts")
e.hero("gingerbread", "Gingerbread bars with cream cheese frosting", "gingerbread")
e.tiles(["gingerbread", "peppermint", "pecan", "cheesecake", "apple", "cookies"])
e.bundle("The holiday pair", "Gingerbread + peppermint", ["gingerbread", "peppermint"], "Serves 20.")
e.closing("Christmas hot orders close noon Mon, Dec 21", "Dessert is decided.", "Order dessert", XMAS_SMALL)

e = mk("h06-how-christmas-works")
e.bar(*XMAS_BAR)
e.intro("Christmas 2026", "Four days<br>to order hot.",
        "Here&rsquo;s how Christmas week works, so nothing sneaks up on you.",
        "Order Christmas dinner")
e.timeline([
    ("Now", "Pick your dinner", "A package for ten, or build your own from the menu.", False),
    ("Mon, Dec 21", "Hot orders close", "At noon. That&rsquo;s the last call for hot delivery.", True),
    ("Dec 22 to 24", "Hot delivery", "Delivered hot and ready to serve.", False),
    ("Wed, Dec 23", "Last day for cold orders", "Missed the hot cutoff? Order cold by Wednesday.", False),
    ("Christmas Eve", "Cold pickup", "Pick it up until 5pm, with a reheating guide.", False),
    ("Christmas Day", "We&rsquo;re closed online", "Need something special? Call us at 323.963.3475.", False),
])
e.packages(PKGS, "Each feeds ten. Add or swap anything after.")
e.closing("Hot orders close noon Mon, Dec 21", "Get on the list.", "Order Christmas dinner", XMAS_SMALL)

e = mk("h07-last-call")
e.bar("Hot orders close noon Mon, Dec 21", "Last call")
e.intro("Last call", "The oven&rsquo;s<br>almost full.",
        "Hot Christmas orders close <strong>Monday, December 21 at noon</strong>. After that it&rsquo;s cold only: order by Wednesday, Dec 23 and pick it up Christmas Eve, with reheating instructions.",
        "Get on the list", size=78)
e.strip(["primerib", "ham", "mash", "pecan"])
e.packages(PKGS, "Each feeds ten. Hot delivery Dec 22 to 24.")
e.closing("Hot orders close noon Mon, Dec 21", "Last chance for hot.", "Order before it closes", XMAS_SMALL)

e = mk("h08-cold-pickup")
e.bar("Order cold by Wed, Dec 23", "Christmas Eve pickup")
e.intro("Cold pickup &middot; Christmas Eve", "Still time.<br>Pick it up cold.",
        "Hot orders are closed, but the whole holiday menu is still available cold, with reheating instructions written for your order. Order by Wednesday, Dec 23 and pick it up on Christmas Eve, until 5pm.",
        "Order for pickup")
e.strip(["ham", "primerib", "brussels", "apple"])
e.timeline([
    ("Wed, Dec 23", "Last day to order", "Any package or dish, same menu.", True),
    ("Christmas Eve", "Pick it up cold", "Any time until 5pm.", False),
    ("Christmas Day", "Reheat and serve", "Follow the guide. Take the credit.", False),
])
e.packages(PKGS, "Each feeds ten. Cold, with reheating instructions.")
e.closing("Order by Wed, Dec 23 &middot; Pickup Christmas Eve", "Christmas, still handled.", "Order for pickup",
          "Cold pickup Christmas Eve &nbsp;&middot;&nbsp; Reheating guide included &nbsp;&middot;&nbsp; Every dish labeled with allergens")

e = mk("h09-new-years-eve")
e.bar("New Year&rsquo;s Eve orders by Tue, Dec 29", "48 hours&rsquo; notice")
e.intro("New Year&rsquo;s Eve", "Ring it in<br>at home.",
        "Skip the reservation. Charcuterie to start, steak or short ribs for dinner, something sweet at midnight. Order with 48 hours&rsquo; notice, hot or cold.",
        "Order for New Year&rsquo;s Eve")
e.hero("charcuterie", "Cheese and charcuterie platter", "charcuterie")
e.tiles(["charcuterie", "skirt", "shortribs", "salmon", "crudite", "cookies"])
e.bundle("One tap", "Party for 10", ["charcuterie", "skirt", "marketveg", "cookies"], "Serves 10 to 12.")
e.closing("Order by Tue, Dec 29", "Here&rsquo;s to fewer dishes in 2027.", "Order for New Year&rsquo;s Eve",
          "48 hours&rsquo; notice &nbsp;&middot;&nbsp; Hot or cold &nbsp;&middot;&nbsp; Every dish labeled with allergens")

# ---------------- CORPORATE ----------------
CBAR = ("Book with 48 hours&rsquo; notice", "Office holiday parties")
CSMALL = "Delivered hot, on time, ready to serve &nbsp;&middot;&nbsp; 48 hours&rsquo; notice &nbsp;&middot;&nbsp; Every dish labeled with allergens"
CLOSE_EB = "Christmas week orders close noon Mon, Dec 21"

e = mk("c01-office-party", True)
e.bar(*CBAR)
e.intro("Office holiday party", "The office party,<br>handled.",
        "Prime rib, ham, sides, salads and dessert, delivered hot and on time, labeled for every diet. You book it. We bring it. Your team eats well.",
        "Plan the party")
e.hero("fulltable", "The Full Table, holiday spread for 10", "full_table")
e.packages(PKGS, "Each feeds ten. Order two or three for a bigger team.")
e.heading("Start with these", "While everyone arrives", top=36, bg="#F6F5F1")
e.tiles(["charcuterie", "crudite"])
e.closing(CLOSE_EB, "Book it before the calendar fills.", "Plan the party", CSMALL)

e = mk("c02-party-menu", True)
e.bar(*CBAR)
e.intro("The party menu", "Feed the<br>whole team.",
        "Mix and match so everyone has something: steak for the meat eaters, salmon, and a vegan cauliflower steak nobody treats as an afterthought.",
        "Build the menu")
e.hero("skirt", "Char grilled skirt steak with chimichurri", "skirt")
e.tiles(["skirt", "salmon", "tritip", "cauli", "mac", "marketveg"])
e.bundle("One tap", "Team lunch for 10", ["skirt", "marketveg", "farmsalad"], "Serves 10 to 12.")
e.closing(CLOSE_EB, "Lunch, handled.", "Order for the office", CSMALL)

e = mk("c03-easy-setup", True)
e.bar(*CBAR)
e.intro("Easy setup", "Set up in<br>ten minutes.",
        "Everything arrives labeled and ready to go. Add chafing dishes to keep it hot through the toast, plus plates and cutlery, so nobody raids the break room.",
        "Plan the spread")
e.hero("charcuterie", "Cheese and charcuterie platter", "charcuterie")
e.tiles(["charcuterie", "crudite", "chafing", "plates"])
e.bundle("Setup kit", "Chafing dishes + plates", ["chafing", "plates"], "Hot food, plates and cutlery for 12.")
e.closing(CLOSE_EB, "Everything but the playlist.", "Order for the office", CSMALL)

e = mk("c04-team-dessert", True)
e.bar(*CBAR)
e.intro("Holiday desserts", "Dessert for<br>the team.",
        "Peppermint brownies with crushed candy cane. Gingerbread bars with cream cheese frosting. Cookies and brownies by the tray. Easy to share, hard to stop.",
        "Order dessert")
e.hero("peppermint", "Peppermint brownie bars", "peppermint")
e.tiles(["peppermint", "gingerbread", "cookies", "brownies20"])
e.bundle("Sweets for 40", "The dessert table", ["gingerbread", "peppermint", "brownies20"], "Serves about 40.")
e.closing(CLOSE_EB, "Sweeten the last meeting.", "Order dessert", CSMALL)

e = mk("c05-before-the-break", True)
e.bar("Christmas week orders close noon Mon, Dec 21")
e.intro("Before the break", "One more<br>team lunch.",
        "Send everyone off right. Book the last-day lunch with 48 hours&rsquo; notice. For Christmas week, orders close at noon Monday, Dec 21.",
        "Book the lunch")
e.timeline([
    ("Now", "Pick the spread", "A package for ten, or build it from the menu.", False),
    ("48 hrs ahead", "Order", "Any day in December with 48 hours&rsquo; notice.", False),
    ("Mon, Dec 21", "Christmas week cutoff", "At noon, for delivery Dec 22 to 24.", True),
    ("Lunch day", "We deliver", "Hot, on time, ready to serve.", False),
])
e.packages(PKGS, "Each feeds ten. Order two or three for a bigger team.")
e.closing(CLOSE_EB, "Last lunch of the year.", "Book the lunch", CSMALL)

e = mk("c06-hosting-at-home", True)
e.bar(*XMAS_BAR)
e.intro("For your own table", "Hosting at<br>home too?",
        "You fed the team. Now let us cook for your family. Hot delivery Dec 22 to 24, or order cold by Dec 23 and pick it up Christmas Eve.",
        "Order Christmas dinner")
e.hero("ribdinner", "The Prime Rib Dinner for 10", "rib_dinner")
e.packages(PKGS, "Each feeds ten. Add or swap anything after.")
e.closing("Hot orders close noon Mon, Dec 21", "Your turn to eat well.", "Order Christmas dinner", XMAS_SMALL)

os.makedirs(OUT, exist_ok=True)
for e in emails:
    d = os.path.join(OUT, e.code); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(e.html())
# image manifest: which crops each email needs
need = {}
import re
for e in emails:
    for m in re.findall(r'src="' + re.escape(IMG) + r'([a-z0-9]+)-(hero|tile|sq)\.jpg"', e.html()):
        need.setdefault(m[0], set()).add(m[1])
json.dump({k: sorted(v) for k, v in sorted(need.items())}, open(os.path.join(OUT, "_images.json"), "w"), indent=0)
print(len(emails), "emails;", sum(len(v) for v in need.values()), "image crops")
