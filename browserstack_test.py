import threading
from selenium import webdriver
from selenium.webdriver.common.by import By

BROWSERSTACK_USERNAME = "YOUR_USERNAME"
BROWSERSTACK_ACCESS_KEY = "YOUR_ACCESS_KEY"

devices = [
    {"os": "Windows", "os_version": "10", "browser": "Chrome", "browser_version": "latest"},
    {"os": "OS X", "os_version": "Ventura", "browser": "Safari", "browser_version": "latest"},
    {"device": "Samsung Galaxy S22", "real_mobile": "true", "os_version": "12.0"},
    {"device": "iPhone 14", "real_mobile": "true", "os_version": "16"},
    {"os": "Windows", "os_version": "11", "browser": "Firefox", "browser_version": "latest"},
]

def run_test(cap):
    url = "https://elpais.com/opinion/"
    desired_cap = {
        "browserstack.user": BROWSERSTACK_USERNAME,
        "browserstack.key": BROWSERSTACK_ACCESS_KEY,
        "name": "El Pais Opinion Test",
        **cap
    }
    driver = webdriver.Remote(
        command_executor="http://hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=desired_cap
    )
    try:
        driver.get(url)
        heading = driver.title
        print(f"{heading} | {cap.get('device', cap.get('browser'))}")
    finally:
        driver.quit()

threads = []
for cap in devices:
    thread = threading.Thread(target=run_test, args=(cap,))
    threads.append(thread)
    thread.start()

for t in threads:
    t.join()
