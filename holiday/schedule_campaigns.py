"""Schedule the TG26 / HOL26 Mailchimp drafts at the time in each title.

Resends (" RESEND " in the title) are only scheduled once their original has
been sent and the did-not-open audience has resolved; until then they WAIT.

    python3 holiday/schedule_campaigns.py                      # shows what it would schedule
    python3 holiday/schedule_campaigns.py --go                 # schedules every TG26/HOL26 draft
    python3 holiday/schedule_campaigns.py --go --only "TG26 Corp 01" --only "TG26 Home 01"

Titles look like "TG26 Home 02 - Tue 10/20 10am" (Pacific). Only drafts are
touched; anything already scheduled or sent is left alone. The key is read from
~/.mailchimp_key and never printed.
"""
import base64, json, os, re, sys, urllib.error, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

LA, UTC = ZoneInfo("America/Los_Angeles"), ZoneInfo("UTC")
key = open(os.path.expanduser("~/.mailchimp_key")).read().strip()
DC = key.rsplit("-", 1)[-1]
HDR = {"Authorization": "Basic " + base64.b64encode(f"x:{key}".encode()).decode(), "Content-Type": "application/json"}

def api(method, path, body=None):
    req = urllib.request.Request(f"https://{DC}.api.mailchimp.com/3.0{path}", method=method, headers=HDR,
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            t = r.read(); return json.loads(t) if t else {}
    except urllib.error.HTTPError as e:
        return {"error": e.code, "detail": e.read()[:300].decode(errors="replace")}

go = "--go" in sys.argv
only = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--only" and i + 1 < len(sys.argv)]
camps = api("GET", "/campaigns?count=500&fields=campaigns.id,campaigns.status,campaigns.settings.title")["campaigns"]
rows = []
for c in camps:
    title = c["settings"]["title"]
    if not re.match(r"(TG26|HOL26) ", title) or (only and not any(title.startswith(o + " ") for o in only)):
        continue
    m = re.search(r" - \w{3} (\d+)/(\d+) (\d+)(am|pm)$", title)
    if not m:
        print(f"  ?? no time in title: {title}"); continue
    hr = int(m[3]) % 12 + (12 if m[4] == "pm" else 0)
    year = 2026 if int(m[1]) >= 10 else 2027
    rows.append((datetime(year, int(m[1]), int(m[2]), hr, tzinfo=LA), title, c))

def resend_ready(c):
    """A RESEND goes only to people who did not open an email that has ALREADY
    gone out. Before the original is sent, Mailchimp can't resolve "did not
    open" and counts the whole list (5,756 on 2026-10-12), so scheduling it then
    would mail everyone. Refuse unless the original is sent and the resend's
    audience is smaller than the original's."""
    full = api("GET", f"/campaigns/{c['id']}?fields=recipients")["recipients"]
    conds = (full.get("segment_opts") or {}).get("conditions") or []
    aim = [x for x in conds if x.get("field") == "aim" and x.get("op") == "noopen"]
    if len(conds) != 1 or not aim:
        return False, "audience is not a single 'did not open' filter"
    orig = api("GET", f"/campaigns/{aim[0]['value']}?fields=status,emails_sent,settings.title")
    if orig.get("status") != "sent":
        return False, f"original not sent yet ({orig.get('status')})"
    if not full.get("recipient_count") or full["recipient_count"] >= (orig.get("emails_sent") or 0):
        return False, f"audience {full.get('recipient_count')} is not smaller than the {orig.get('emails_sent')} who got the original"
    return True, f"{full['recipient_count']} non-openers of {orig['emails_sent']}"

now = datetime.now(LA)
for when, title, c in sorted(rows, key=lambda r: r[0]):
    label = when.strftime("%a %m/%d %-I:%M %p PT")
    if c["status"] != "save":
        print(f"  skip   {title}  ({c['status']})"); continue
    if when <= now:
        print(f"  PAST   {title}  ({label} has passed; not scheduled)"); continue
    if " RESEND " in title:
        ok, why = resend_ready(c)
        if not ok:
            print(f"  WAIT   {title}  ({why})"); continue
        label += f", {why}"
    if not go:
        print(f"  would  {title}  -> {label}"); continue
    r = api("POST", f"/campaigns/{c['id']}/actions/schedule", {"schedule_time": when.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S+00:00")})
    print(f"  {'ERROR ' + str(r) if r.get('error') else 'scheduled'}  {title}  -> {label}")
if not go:
    print("\nNothing scheduled. Add --go to schedule.")
