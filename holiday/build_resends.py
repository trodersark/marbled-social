"""Create the "did not open" resend for every TG26 / HOL26 campaign, as DRAFTS.

    python3 holiday/build_resends.py          # shows what it would create
    python3 holiday/build_resends.py --go     # creates the drafts (never schedules)

Each resend copies its original's template, preview text and tracking, takes the
resend subject where the plan gives one, and targets "did not open <original>".
That audience only resolves once the original has gone out, so these must not be
scheduled before then; holiday/schedule_campaigns.py refuses until it has.
"""
import base64, json, os, re, sys, urllib.error, urllib.request

key = open(os.path.expanduser("~/.mailchimp_key")).read().strip()
DC = key.rsplit("-", 1)[-1]
HDR = {"Authorization": "Basic " + base64.b64encode(f"x:{key}".encode()).decode(), "Content-Type": "application/json"}
LIST = "2ff9d77158"

def api(method, path, body=None):
    req = urllib.request.Request(f"https://{DC}.api.mailchimp.com/3.0{path}", method=method, headers=HDR,
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            t = r.read(); return json.loads(t) if t else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"Mailchimp said {e.code} on {method} {path}: {e.read()[:300]}")

# When each resend goes, and its subject/preview when the plan changes them
# (HANDOFF.md for Thanksgiving, holiday/PLAN.md for Holiday). Default: next day, same time, same subject.
RESENDS = {
    "TG26 Corp 01": ("Wed 10/14 9am", None, None), "TG26 Home 01": ("Wed 10/14 10am", None, None),
    "TG26 Corp 02": ("Wed 10/21 9am", None, None), "TG26 Home 02": ("Wed 10/21 10am", None, None),
    "TG26 Corp 03": ("Wed 10/28 9am", None, None), "TG26 Home 04": ("Wed 10/28 10am", None, None),
    "TG26 Corp 04": ("Fri 10/30 9am", None, None),
    "TG26 Corp 05": ("Wed 11/4 9am", None, None), "TG26 Home 06": ("Wed 11/4 10am", None, None),
    "TG26 Home 03": ("Mon 11/9 9am", None, None), "TG26 Corp 06": ("Tue 11/10 9am", None, None),
    "TG26 Corp 07": ("Fri 11/13 9am", None, None), "TG26 Home 05": ("Fri 11/13 10am", None, None),
    "TG26 Home 07": ("Mon 11/16 9am", None, None), "TG26 Corp 08": ("Tue 11/17 9am", None, None),
    "TG26 Corp 09": ("Thu 11/19 9am", None, None), "TG26 Home 09": ("Thu 11/19 10am", None, None),
    "TG26 Corp 10": ("Mon 11/23 7am", "Office orders close at noon today", None),
    "TG26 Home 10": ("Mon 11/23 7am", "Closes at noon today", None),
    "TG26 Home 11": ("Tue 11/24 2pm", None, None),
    "HOL26 Corp 01": ("Tue 12/1 9am", None, None), "HOL26 Home 01": ("Thu 12/3 10am", None, None),
    "HOL26 Home 02": ("Wed 12/2 7am", "Last day to order for the first night", "Hanukkah starts Friday. Order today."),
    "HOL26 Corp 02": ("Fri 12/4 9am", None, None), "HOL26 Home 03": ("Mon 12/7 9am", None, None),
    "HOL26 Corp 03": ("Wed 12/9 9am", None, None), "HOL26 Corp 04": ("Fri 12/11 9am", None, None),
    "HOL26 Home 04": ("Fri 12/11 10am", None, None), "HOL26 Home 05": ("Mon 12/14 9am", None, None),
    "HOL26 Corp 05": ("Wed 12/16 9am", None, None), "HOL26 Corp 06": ("Fri 12/18 9am", None, None),
    "HOL26 Home 06": ("Fri 12/18 10am", None, None),
    "HOL26 Home 07": ("Mon 12/21 7am", "Hot Christmas delivery closes at noon today", "Last call for hot Christmas delivery."),
    "HOL26 Home 08": ("Tue 12/22 2pm", "Last day to order for Christmas Eve", "Cold orders close tomorrow, Wed, Dec 23."),
    "HOL26 Home 09": ("Mon 12/28 9am", None, None),
}

go = "--go" in sys.argv
camps = api("GET", "/campaigns?count=500&fields=campaigns.id,campaigns.status,campaigns.settings,campaigns.tracking")["campaigns"]
titles = {c["settings"]["title"] for c in camps}
made = 0
for c in sorted(camps, key=lambda c: c["settings"]["title"]):
    t = c["settings"]["title"]
    m = re.match(r"((?:TG26|HOL26) (?:Home|Corp) \d\d) - ", t)
    if not m or " RESEND " in t:
        continue
    base = m[1]
    when, subj, prev = RESENDS[base]
    title = f"{base} RESEND - {when}"
    if title in titles:
        print(f"  exists {title}"); continue
    s = c["settings"]
    subject = subj or s["subject_line"]; preview = prev or s.get("preview_text", "")
    if not go:
        print(f"  would  {title}  | {subject}"); continue
    api("POST", "/campaigns", {
        "type": "regular",
        "recipients": {"list_id": LIST, "segment_opts": {"match": "all", "conditions": [
            {"condition_type": "Aim", "field": "aim", "op": "noopen", "value": c["id"]}]}},
        "settings": {"title": title, "subject_line": subject, "preview_text": preview, "from_name": s["from_name"],
                     "reply_to": s["reply_to"], "template_id": s["template_id"], "auto_footer": False},
        "tracking": {k: c["tracking"][k] for k in ("opens", "html_clicks", "text_clicks", "google_analytics")},
    })
    made += 1
    print(f"  draft  {title}  | {subject}")
print(f"\n{made} resend drafts created." if go else "\nNothing created. Add --go.")
