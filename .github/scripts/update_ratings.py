import re, json, urllib.request

HANDLE = "eushaahmed08"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode()

def codeforces():
    d = json.loads(get(f"https://codeforces.com/api/user.info?handles={HANDLE}"))
    return d["result"][0].get("maxRating")

def atcoder():
    h = json.loads(get(f"https://atcoder.jp/users/{HANDLE}/history/json"))
    return max((x["NewRating"] for x in h), default=None)

def codechef():
    html = get(f"https://www.codechef.com/users/{HANDLE}")
    m = re.search(r"Highest Rating\s*(\d+)", html)
    return int(m.group(1)) if m else None

PLATFORMS = [
    ("Codeforces", f"https://codeforces.com/profile/{HANDLE}", codeforces),
    ("CodeChef",   f"https://www.codechef.com/users/{HANDLE}", codechef),
    ("AtCoder",    f"https://atcoder.jp/users/{HANDLE}", atcoder),
]

readme = open("README.md", encoding="utf-8").read()
m = re.search(r"(<!--CP_START-->\n)(.*?)(\n<!--CP_END-->)", readme, re.S)
old_block = m.group(2)

rows = ["| Platform | Handle | Peak Rating |", "|---|---|---|"]
for name, url, fn in PLATFORMS:
    old = re.search(rf"\| {name} \|.*\| (\d+) \|", old_block)
    old = int(old.group(1)) if old else None
    try:
        new = fn()
    except Exception as e:
        print(f"{name}: fetch failed ({e}), keeping old value")
        new = None
    # peak can only go up; keep old if fetch failed
    val = max(v for v in (old, new) if v is not None)
    rows.append(f"| {name} | [{HANDLE}]({url}) | {val} |")

new_block = "\n".join(rows)
if new_block != old_block:
    readme = readme[:m.start(2)] + new_block + readme[m.end(2):]
    open("README.md", "w", encoding="utf-8").write(readme)
    print("README updated")
else:
    print("No change")
