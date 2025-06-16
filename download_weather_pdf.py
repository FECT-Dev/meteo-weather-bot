import os
import time
import tempfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a unique temp folder for user-data-dir (avoid Chrome conflicts)
temp_user_data_dir = tempfile.mkdtemp()

# Create today's dated folder for downloads
today = datetime.now().strftime('%Y-%m-%d')
download_path = os.path.join(os.getcwd(), "downloads", today)
os.makedirs(download_path, exist_ok=True)

# Configure Chrome options
chrome_options = Options()
chrome_options.binary_location = os.path.abspath("./chrome-linux64/chrome")
chrome_options.add_argument("--headless=new")  # Recommended for Chrome 109+
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir}")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "plugins.always_open_pdf_externally": True
})

# Start the WebDriver
driver = webdriver.Chrome(
    service=Service(executable_path=os.path.abspath("./chromedriver-linux64/chromedriver")),
    options=chrome_options
)

# Open the website
driver.get("https://meteo.gov.lk/")
wait = WebDriverWait(driver, 20)

# Wait and click "Weather Data"
weather_data = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Weather Data")))
weather_data.click()

# Wait and click "Weather Report for the 24hour Period"
report_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Weather Report for the 24hour Period")))
report_link.click()

# Wait for the PDF to download
time.sleep(10)

driver.quit()
print(f"✅ Downloaded to: {download_path}")
