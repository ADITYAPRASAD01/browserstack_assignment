import os
import threading
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# List of desired capabilities for 5 different browsers/devices
capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10",
        "name": "Chrome_Win10"
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Monterey",
        "name": "Firefox_macOS"
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "osVersion": "12.0",
        "browserName": "Chrome",
        "realMobile": "true",
        "name": "Galaxy_Chrome_Mobile"
    },
    {
        "deviceName": "iPhone 14",
        "osVersion": "16",
        "browserName": "Safari",
        "realMobile": "true",
        "name": "iPhone_Safari"
    },
    {
        "browserName": "Edge",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "11",
        "name": "Edge_Win11"
    }
]

# Test function to run in parallel
def run_test(cap):
    options = webdriver.ChromeOptions()
    for key, value in cap.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor=URL,
        options=options
    )

    try:
        driver.get("https://www.google.com")
        print(f"✅ Visited Google on: {cap.get('name', 'Unnamed Test')}")
    finally:
        driver.quit()

# Launch tests in parallel
threads = []

for cap in capabilities:
    t = threading.Thread(target=run_test, args=(cap,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
