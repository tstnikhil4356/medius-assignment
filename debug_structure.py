import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
except:
    driver = webdriver.Chrome(options=chrome_options)

driver.get(os.getenv('FORM_URL'))
time.sleep(5)

print("="*70)
print("DEBUGGING FORM STRUCTURE")
print("="*70)

print("\n1. TEXT INPUTS:")
text_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
for i, inp in enumerate(text_inputs):
    aria_label = inp.get_attribute('aria-label') or 'No label'
    print(f"   [{i}] {aria_label}")

print("\n2. TEXTAREAS:")
textareas = driver.find_elements(By.TAG_NAME, 'textarea')
for i, ta in enumerate(textareas):
    aria_label = ta.get_attribute('aria-label') or 'No label'
    print(f"   [{i}] {aria_label}")

print("\n3. ALL INPUTS (any type):")
all_inputs = driver.find_elements(By.TAG_NAME, 'input')
for i, inp in enumerate(all_inputs):
    input_type = inp.get_attribute('type')
    aria_label = inp.get_attribute('aria-label') or 'No label'
    print(f"   [{i}] type={input_type}, label={aria_label}")

print("="*70)
input("\nPress ENTER to close...")
driver.quit()