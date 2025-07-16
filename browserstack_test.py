import os
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# Load .env file
load_dotenv()
USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Browser/device configurations
capabilities_list = [
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

# Test function
def run_test(cap):
    # Use ChromeOptions only to carry capabilities – it works cross-browser here
    options = Options()
    for key, value in cap.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor=URL,
        options=options
    )

    try:
        driver.get("https://www.google.com")
        if "Google" in driver.title:
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Google loaded successfully"}}'
            )
            print(f"✅ Passed: {cap['name']}")
        else:
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "Title mismatch"}}'
            )
            print(f"❌ Failed: {cap['name']} - Title mismatch")
    except Exception as e:
        driver.execute_script(
            f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed","reason": "{str(e)}"}}}}'
        )
        print(f"❌ Error: {cap['name']} - {e}")
    finally:
        driver.quit()

# Parallel execution
threads = []
for cap in capabilities_list:
    t = threading.Thread(target=run_test, args=(cap,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
