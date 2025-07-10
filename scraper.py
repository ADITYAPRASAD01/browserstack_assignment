import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
from urllib.parse import urljoin
from dotenv import load_dotenv

# Load API Key from .env file (optional if you use other APIs)
load_dotenv()

# Translation setup (Google Translate API - unofficial)
TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
PARAMS = {
    "client": "gtx",
    "sl": "es",
    "tl": "en",
    "dt": "t",
    "q": ""
}

# Setup Chrome driver
driver = webdriver.Chrome()

# Open El País Opinion section
driver.get("https://elpais.com/opinion/")
time.sleep(3)

# Get first 5 article links
articles = driver.find_elements(By.CSS_SELECTOR, "a[href*='/opinion/']")[:10]
links = []
for a in articles:
    href = a.get_attribute("href")
    if href and href not in links:
        links.append(href)
    if len(links) == 5:
        break

titles = []
translated_titles = []

for idx, url in enumerate(links):
    driver.get(url)
    print(f"\n🔗 Opening article {idx+1}: {url}")
    time.sleep(2)

    try:
        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except:
        print(f"❌ Skipping article {idx+1} — title not found.")
        continue

    # Try to wait for content
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-dtm-region='article_body'], article"))
        )
    except:
        print(f"⚠️ Timeout waiting for content on article {idx+1}")

    # Try multiple selectors for article body
    try:
        body = driver.find_element(By.CSS_SELECTOR, "div[data-dtm-region='article_body']").text.strip()
    except:
        try:
            body = driver.find_element(By.CSS_SELECTOR, "article").text.strip()
        except:
            print(f"❌ Skipping article {idx+1} — content not found.")
            continue

    titles.append(title)

    print(f"\n📰 Title [{idx+1}] (Spanish): {title}")
    print(f"📝 Content:\n{body[:500]}...\n")  # limit to first 500 chars

    # Translate the title
    PARAMS["q"] = title
    try:
        response = requests.get(TRANSLATE_URL, params=PARAMS)
        translated = response.json()[0][0][0]
    except:
        translated = "[Translation Failed]"

    translated_titles.append(translated)
    print(f"🌐 Translated Title: {translated}")

    # Download image if available
    try:
        img = driver.find_element(By.CSS_SELECTOR, "figure img")
        src = img.get_attribute("src")
        if src:
            img_data = requests.get(src).content
            os.makedirs("images", exist_ok=True)
            img_path = f"images/article_{idx+1}.jpg"
            with open(img_path, "wb") as f:
                f.write(img_data)
            print(f"🖼️  Image saved to {img_path}")
    except:
        print("⚠️  No image found.")

# Analyze translated headers
words = " ".join(translated_titles).lower().split()
word_counts = Counter(words)
print("\n🔍 Repeated Words in Translated Titles:")
found = False
for word, count in word_counts.items():
    if count > 2:
        print(f"'{word}' appears {count} times.")
        found = True

if not found:
    print("No word appears more than twice.")

driver.quit()
