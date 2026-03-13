import requests
from bs4 import BeautifulSoup
from datetime import datetime

NAME    = "Unnat Jain"
CONTACT = "9810163148"
URL     = "https://drmariabooking.com/"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Referer": URL,
})

print(f"🕐 Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🌐 Fetching page...")

res  = session.get(URL, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

if "Booking full" in res.text:
    print("❌ Booking is full for today!")
else:
    form   = soup.find("form")
    action = form.get("action", URL) if form else URL
    if not action.startswith("http"):
        action = URL.rstrip("/") + "/" + action.lstrip("/")

    data = {}
    if form:
        for inp in form.find_all("input"):
            if inp.get("name"):
                data[inp["name"]] = inp.get("value", "")

    data["name"]    = NAME
    data["contact"] = CONTACT

    print(f"📤 Submitting to: {action}")
    print(f"📋 Data: {data}")

    res2 = session.post(action, data=data, timeout=10)
    body = BeautifulSoup(res2.text, "html.parser").get_text(strip=True)

    print(f"📥 Status: {res2.status_code}")
    print(f"📋 Response: {body[:400]}")

    if any(w in body.lower() for w in ["success", "booked", "confirmed", "token", "slot"]):
        print("✅ BOOKING SUCCESSFUL!")
    else:
        print("⚠️ Check response above for result.")
