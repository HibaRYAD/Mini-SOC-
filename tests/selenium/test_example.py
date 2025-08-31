import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = os.environ.get("BASE_URL", "https://wazuh.lab")

def create_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opts)

def test_wazuh_dashboard_loads():
    driver = create_driver()
    try:
        driver.set_page_load_timeout(60)
        driver.get(BASE_URL)
        time.sleep(3)
        title = driver.title.lower()
        assert "wazuh" in title or "dashboard" in title, f"Unexpected title: {driver.title}"
        body_text = driver.page_source.lower()
        assert "username" in body_text or "login" in body_text
    finally:
        driver.quit()

