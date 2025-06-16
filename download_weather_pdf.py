import os
import time
import tempfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Create a unique temp folder for user-data-dir (avoid conflict)
temp_user_data_dir = tempfile.mkdtemp()

# Create dated download folder
today = datetime.now().strftime('%Y-%m-%d')
download_path = os.path.join(os.getcwd(), "downloads", today)
os.makedirs(download_path, exist_ok=True)

# Setup headless Chromium with full compatibility
chrome_options = Options()
chrome_options.binary_location = "/snap/bin/chromium"
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument(f'--user-data-dir={temp_user_data_dir}')  # ✅ unique temp profile
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "plugins.always_open_pdf_externally": True
})

# Launch browser
driver = webdriver.Chrome(service=Service(), options=chrome_options)

# Go to the website and download the PDF
driver.get("https://meteo.gov.lk/")
time.sleep(3)
driver.find_element(By.LINK_TEXT, "Weather Data").click()
time.sleep(3)
driver.find_element(By.PARTIAL_LINK_TEXT, "Weather Report for the 24hour Period").click()
time.sleep(10)

driver.quit()
print(f"✅ Downloaded to: {download_path}")
