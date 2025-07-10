# 🌐 BrowserStack Customer Engineer Technical Assignment

This project demonstrates technical skills across **web scraping**, **language translation**, **natural language processing**, and **parallel cross-browser testing** using **BrowserStack**. It simulates real-world problem-solving relevant to the **Customer Engineering** role.

---

## ✅ Problem Statement

Extract the latest articles from *El País* (a Spanish news website), translate content to English, analyze word usage, and validate cross-browser compatibility with BrowserStack.

---

## 🧠 Solution Overview

1. **Scraper (`scraper.py`)**
   - Uses **Selenium** to scrape 5 opinion articles from [https://elpais.com/opinion/](https://elpais.com/opinion/)
   - Extracts title, content, and article image
   - Translates Spanish titles to English using **Google Translate API**
   - Performs basic **word frequency analysis**
   - Saves article images locally

2. **Automated Testing (`browserstack_test.py`)**
   - Uses **BrowserStack Automate** to open Google across 5 platforms:
     - Chrome on Windows 10
     - Edge on Windows 11
     - Firefox on macOS
     - Safari on iPhone 15
     - Chrome on Galaxy S23
   - Validates visual compatibility and parallel execution using `threading`

---

## 🧪 Test Output Snapshot

```bash
✅ Visited Google on: Chrome_Win10
✅ Visited Google on: Firefox_macOS
✅ Visited Google on: Galaxy_Chrome_Mobile
✅ Visited Google on: iPhone_Safari
✅ Visited Google on: Edge_Win11
