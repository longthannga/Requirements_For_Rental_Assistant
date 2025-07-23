from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scraper(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        driver.set_page_load_timeout(45)  # Increase timeout to 45 seconds
        driver.get(url)
        
        # Wait for page to fully render
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Scroll to trigger lazy-loaded content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for content to load
        
        return driver.page_source
    except Exception as e:
        print(f"Error loading {url}: {str(e)}")
        return "<html><body>Error loading page</body></html>"
    finally:
        driver.quit()

    

def clean_body_content(body_content):
    try:
        soup = BeautifulSoup(body_content, "html.parser")
        
        # Remove unnecessary elements
        for element in soup(["script", "style", "noscript", "header", "footer", 
                            "nav", "aside", "form", "iframe", "svg"]):
            element.decompose()
            
        # Get clean text
        text = soup.get_text(separator="\n")
        cleaned = "\n".join(
            line.strip() for line in text.splitlines() if line.strip()
        )
        return cleaned
    except Exception as e:
        print(f"Error cleaning content: {str(e)}")
        return "Content extraction failed"


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


