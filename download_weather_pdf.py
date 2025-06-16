import os
import time
import tempfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Create a unique temp folder for user-data-dir (avoid Chrome conflicts)
temp_user_data_dir = tempfile.mkdtemp()

# Create today's dated folder for downloads
today = datetime.now().strftime('%Y-%m-%d')
download_path = os.path.join(os.getcwd(), "downloads", today)
os.makedirs(download_path, exist_ok=True)

# Configure Chrome for Testing binary paths
chrome_options = Options()
chrome_options.binary_location = os.path.abspath("./chrome-linux64/chrome")
chrome_options.add_argument("--headless=new")  # "new" for Chrome 109+
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir}")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "plugins.always_open_pdf_externally": True
})

# Launch Chrome using specific ChromeDriver
driver = webdriver.Chrome(
    service=Service(executable_path=os.path.abspath("./chromedriver-linux64/chromedriver")),
    options=chrome_options
)

# Navigate and download the PDF
driver.get("https://meteo.gov.lk/")
time.sleep(3)
driver.find_element(By.LINK_TEXT, "Weather Data").click()
time.sleep(3)
driver.find_element(By.PARTIAL_LINK_TEXT, "Weather Report for the 24hour Period").click()
time.sleep(10)  # Wait for the download to finish

driver.quit()
print(f"✅ Downloaded to: {download_path}")
