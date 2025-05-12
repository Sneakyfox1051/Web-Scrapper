from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

# ✅ Update this path to where your chromedriver.exe is located
CHROMEDRIVER_PATH = r"D:\WOrk\AI-Web-Scraper\chromedriver.exe"


def scrape_website(website):
    print("Launching local Chrome browser...")

    # Chrome options
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")  
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Set up ChromeDriver service
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
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
