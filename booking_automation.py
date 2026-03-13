"""
Dr. Maria's Rohini Clinic - Slot Booking Bot
Waits until 6:00 AM tomorrow, then auto-books.

Install: pip install selenium webdriver-manager
Run:     python booking_automation.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

NAME    = "Unnat Jain"
CONTACT = "9810163148"

# ── Helper: click any element by trying multiple selectors ────────────────────
def smart_click(driver, selectors, label):
    for by, value in selectors:
        try:
            el = driver.find_element(by, value)
            driver.execute_script("arguments[0].scrollIntoView(true);", el)
            driver.execute_script("arguments[0].click();", el)
            print(f"✅ Clicked '{label}'")
            return True
        except Exception:
            continue
    print(f"❌ Could not click '{label}'. Visible elements on page:")
    for el in driver.find_elements(By.XPATH, "//*[string-length(normalize-space(text())) > 0]"):
        print(f"   <{el.tag_name}> : {el.text.strip()[:60]}")
    return False

# ── Helper: fill input by trying multiple selectors ───────────────────────────
def smart_fill(driver, selectors, value, label):
    for by, selector in selectors:
        try:
            el = driver.find_element(by, selector)
            driver.execute_script("arguments[0].scrollIntoView(true);", el)
            el.clear()
            el.send_keys(value)
            print(f"✅ Filled '{label}' with: {value}")
            return True
        except Exception:
            continue
    print(f"❌ Could not fill '{label}'. Input elements on page:")
    for el in driver.find_elements(By.TAG_NAME, "input"):
        print(f"   placeholder='{el.get_attribute('placeholder')}'  name='{el.get_attribute('name')}'  id='{el.get_attribute('id')}'")
    return False

# ── Wait until tomorrow 6:00 AM ───────────────────────────────────────────────
def wait_until_6am():
    now = datetime.now()
    target = (now + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)

    print(f"🕐 Current time  : {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Booking target: {target.strftime('%Y-%m-%d %H:%M:%S')} (6:00 AM tomorrow)")
    print("⏳ Waiting...\n")

    while True:
        now = datetime.now()
        remaining = (target - now).total_seconds()

        if remaining <= 0:
            print("🟢 It's 6:00 AM! Starting booking now...")
            break
        elif remaining > 3600:
            hours = int(remaining // 3600)
            mins  = int((remaining % 3600) // 60)
            print(f"   ⏳ {hours}h {mins}m remaining...", end="\r")
            time.sleep(60)
        elif remaining > 60:
            mins = int(remaining // 60)
            secs = int(remaining % 60)
            print(f"   ⏳ {mins}m {secs}s remaining...", end="\r")
            time.sleep(10)
        elif remaining > 5:
            print(f"   🔥 {int(remaining)} seconds remaining...", end="\r")
            time.sleep(1)
        else:
            # Final 5-second countdown
            print(f"   🚀 {int(remaining)}...", end="\r")
            time.sleep(0.5)

# ── Main ──────────────────────────────────────────────────────────────────────
#wait_until_6am()

print("🚀 Opening browser...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 1. Open website
driver.get("https://drmariabooking.com/")
time.sleep(2)

# 2. Click "Booking Slot" tab
smart_click(driver, [
    (By.XPATH, "//*[normalize-space(text())='Booking Slot']"),
    (By.XPATH, "//*[contains(text(),'Booking Slot')]"),
    (By.XPATH, "//button[contains(text(),'Booking')]"),
    (By.XPATH, "//a[contains(text(),'Booking')]"),
    (By.XPATH, "//div[contains(text(),'Booking')]"),
    (By.XPATH, "//li[contains(text(),'Booking')]"),
    (By.XPATH, "//span[contains(text(),'Booking')]"),
    (By.PARTIAL_LINK_TEXT, "Booking"),
], "Booking Slot tab")
time.sleep(1.5)

# 3. Check if slots are full
body_text = driver.find_element(By.TAG_NAME, "body").text
if "Booking full" in body_text:
    print("❌ Booking is full for today!")
    input("\nPress ENTER to close browser...")
    driver.quit()
    exit()

# 4. Fill Name
smart_fill(driver, [
    (By.XPATH, "//input[@placeholder='Your Name']"),
    (By.XPATH, "//input[contains(@placeholder,'Name')]"),
    (By.XPATH, "//input[contains(@placeholder,'name')]"),
    (By.NAME,  "name"),
    (By.ID,    "name"),
    (By.XPATH, "(//input[@type='text'])[1]"),
], NAME, "Name field")

# 5. Fill Contact
smart_fill(driver, [
    (By.XPATH, "//input[@placeholder='Your Contact']"),
    (By.XPATH, "//input[contains(@placeholder,'Contact')]"),
    (By.XPATH, "//input[contains(@placeholder,'contact')]"),
    (By.XPATH, "//input[contains(@placeholder,'Mobile')]"),
    (By.XPATH, "//input[contains(@placeholder,'Phone')]"),
    (By.NAME,  "contact"),
    (By.ID,    "contact"),
    (By.XPATH, "//input[@type='tel']"),
    (By.XPATH, "//input[@type='number']"),
    (By.XPATH, "(//input[@type='text'])[2]"),
], CONTACT, "Contact field")

# 6. Click "Book Now"
smart_click(driver, [
    (By.XPATH, "//button[normalize-space(text())='Book Now']"),
    (By.XPATH, "//button[contains(text(),'Book Now')]"),
    (By.XPATH, "//button[contains(text(),'Book')]"),
    (By.XPATH, "//*[contains(text(),'Book Now')]"),
    (By.XPATH, "//input[@value='Book Now']"),
    (By.XPATH, "//a[contains(text(),'Book')]"),
    (By.XPATH, "//div[contains(text(),'Book Now')]"),
], "Book Now button")
time.sleep(2)

# 7. Show result
print("\n📋 Booking Result:")
print(driver.find_element(By.TAG_NAME, "body").text[:400])
print(f"\n🕐 Booked at: {datetime.now().strftime('%H:%M:%S')}")

input("\nPress ENTER to close browser...")
driver.quit()
