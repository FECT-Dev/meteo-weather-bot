import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Create a folder with today's date
today = datetime.now().strftime('%Y-%m-%d')
download_path = os.path.join(os.getcwd(), "downloads", today)
os.makedirs(download_path, exist_ok=True)

# Configure Chrome options for headless operation and correct binary path
chrome_options = Options()
chrome_options.binary_location = "/snap/bin/chromium"  # ✅ Path to Chromium installed on GitHub runner
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "plugins.always_open_pdf_externally": True
})

# Launch Chrome WebDriver
driver = webdriver.Chrome(service=Service(), options=chrome_options)

# Navigate to the website and download the PDF
driver.get("https://meteo.gov.lk/")
time.sleep(3)
driver.find_element(By.LINK_TEXT, "Weather Data").click()
time.sleep(3)
driver.find_element(By.PARTIAL_LINK_TEXT, "Weather Report for the 24hour Period").click()
time.sleep(10)  # Wait for download to complete

driver.quit()
print(f"✅ Downloaded to: {download_path}")
