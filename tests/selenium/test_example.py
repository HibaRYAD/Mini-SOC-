from selenium import webdriver
from selenium.webdriver.common.by import By

def test_dashboard_loads():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    try:
        driver.get("https://wazuh.lab")
        assert "Wazuh" in driver.title
    finally:
        driver.quit()
