"""Create the 15 holiday emails as Mailchimp templates ("Code your own").

    MAILCHIMP_API_KEY=xxxxxxxx-us8 python3 holiday/import_templates.py        # shows what it would do
    MAILCHIMP_API_KEY=xxxxxxxx-us8 python3 holiday/import_templates.py --go   # creates them

The key never leaves your computer: it is read from the environment and sent only
to Mailchimp. A template that already exists by name is skipped, so running it
twice does not make duplicates. Prints each template's id (edit at
/templates/design?tid=<id>). Uses only the Python standard library.
"""
import base64, json, os, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "templates", "holiday")

# Same naming as the Thanksgiving set (TG26 Home 01 ...), in send order.
NAMES = {
    "h01-menu-open": "HOL26 Home 01 Menu open",
    "h02-hanukkah": "HOL26 Home 02 Hanukkah",
    "h03-prime-rib": "HOL26 Home 03 Prime rib",
    "h04-build-your-own": "HOL26 Home 04 Build your own",
    "h05-desserts": "HOL26 Home 05 Desserts",
    "h06-how-christmas-works": "HOL26 Home 06 How Christmas works",
    "h07-last-call": "HOL26 Home 07 Last call for hot",
    "h08-cold-pickup": "HOL26 Home 08 Cold pickup",
    "h09-new-years-eve": "HOL26 Home 09 New Years Eve",
    "c01-office-party": "HOL26 Corp 01 Office party",
    "c02-party-menu": "HOL26 Corp 02 Party menu",
    "c03-easy-setup": "HOL26 Corp 03 Easy setup",
    "c04-team-dessert": "HOL26 Corp 04 Team dessert",
    "c05-before-the-break": "HOL26 Corp 05 Before the break",
    "c06-hosting-at-home": "HOL26 Corp 06 Hosting at home",
}


def api(method, path, key, body=None):
    dc = key.rsplit("-", 1)[-1]
    req = urllib.request.Request(
        f"https://{dc}.api.mailchimp.com/3.0{path}",
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={
            "Authorization": "Basic " + base64.b64encode(f"anystring:{key}".encode()).decode(),
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:400]
        sys.exit(f"Mailchimp said {e.code} on {method} {path}: {detail}")


def main():
    go = "--go" in sys.argv
    key = os.environ.get("MAILCHIMP_API_KEY", "").strip()
    files = {n: os.path.join(SRC, f"{n}.html") for n in NAMES}
    missing = [f for f in files.values() if not os.path.exists(f)]
    if missing:
        sys.exit(f"Missing files: {missing}")
    if not key or "-" not in key:
        print("Set MAILCHIMP_API_KEY (Mailchimp: Profile > Extras > API keys; it ends in -us8). Would create:")
        for n, name in NAMES.items():
            print(f"  {name:36} <- templates/holiday/{n}.html ({os.path.getsize(files[n]) // 1024} KB)")
        return

    existing = {t["name"]: t["id"] for t in api("GET", "/templates?type=user&count=1000&fields=templates.id,templates.name", key).get("templates", [])}
    for n, name in NAMES.items():
        if name in existing:
            print(f"  skip   {name:36} already exists (tid {existing[name]})")
            continue
        if not go:
            print(f"  would create {name}")
            continue
        html = open(files[n], encoding="utf-8").read()
        t = api("POST", "/templates", key, {"name": name, "html": html})
        print(f"  created {name:36} tid {t['id']}")
    if not go:
        print("\nNothing created. Run again with --go to create them.")


if __name__ == "__main__":
    main()
