from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import platform
import shutil

# Detect if we're running in a cloud environment like Render
IS_RENDER = "RENDER" in os.environ or platform.system() == "Linux"

# Set the ChromeDriver path and Chrome binary location
if IS_RENDER:
    CHROMEDRIVER_PATH = shutil.which("chromedriver")

    # Try both likely names
    chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]
    CHROME_BINARY_PATH = next((p for p in chrome_paths if os.path.exists(p)), None)

    if not CHROME_BINARY_PATH:
        raise FileNotFoundError("Could not find Chrome binary on server.")
else:
    CHROMEDRIVER_PATH = r"D:\WOrk\AI-Web-Scraper\chromedriver.exe"
    CHROME_BINARY_PATH = None  # Local Chrome assumed

def scrape_website(website):
    print("Launching Chrome browser...")

    options = Options()
    if CHROME_BINARY_PATH:
        options.binary_location = CHROME_BINARY_PATH

    # Common flags for both environments
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(website)
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
