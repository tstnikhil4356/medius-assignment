import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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

form_url = os.getenv('FORM_URL')
full_name = os.getenv('FULL_NAME')
contact_number = os.getenv('CONTACT_NUMBER')
email_id = os.getenv('EMAIL_ID')
full_address = os.getenv('FULL_ADDRESS')
pin_code = os.getenv('PIN_CODE')
date_of_birth = os.getenv('DATE_OF_BIRTH')
gender = os.getenv('GENDER')

print("=" * 60)
print("Opening Google Form...")
print("=" * 60)

driver.get(form_url)
time.sleep(5)

print("\nFinding all input fields...")
inputs = driver.find_elements(By.TAG_NAME, 'input')
print(f"Found {len(inputs)} input fields")

data_to_fill = [
    full_name,
    contact_number,
    email_id,
    full_address,
    pin_code,
    "GNFPYC"
]

print("\nFilling text fields...")
text_field_index = 0

for inp in inputs:
    input_type = inp.get_attribute('type')
    if input_type == 'text' and text_field_index < len(data_to_fill):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", inp)
            time.sleep(0.5)
            inp.click()
            time.sleep(0.3)
            inp.clear()
            inp.send_keys(data_to_fill[text_field_index])
            print(f"  Field {text_field_index + 1}: {data_to_fill[text_field_index][:30]}...")
            text_field_index += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  Error on field {text_field_index}: {e}")

print("\nFilling date field...")
try:
    date_input = driver.find_element(By.CSS_SELECTOR, 'input[type="date"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", date_input)
    time.sleep(0.5)

    from datetime import datetime

    date_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')
    date_formatted = date_obj.strftime('%m%d%Y')

    date_input.click()
    time.sleep(0.3)
    date_input.send_keys(date_formatted)
    print(f"  Date filled: {date_obj.strftime('%m/%d/%Y')}")
    time.sleep(0.5)
except Exception as e:
    print(f"  Error filling date: {e}")

print("\nSelecting gender...")
try:
    radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
    for radio in radio_buttons:
        data_value = radio.get_attribute('data-value') or ''
        if gender.lower() in data_value.lower():
            driver.execute_script("arguments[0].scrollIntoView(true);", radio)
            time.sleep(0.5)
            radio.click()
            print(f"  Gender selected: {gender}")
            time.sleep(0.5)
            break
except Exception as e:
    print(f"  Error selecting gender: {e}")

print("\n" + "=" * 60)
print("Form filling complete!")
print("=" * 60)

input("\nCheck the form. Press ENTER to take screenshot and close...")

print("Taking screenshot...")
driver.save_screenshot('form_filled_manual.png')
print("Saved: form_filled_manual.png")

print("\nTo submit:")
print("1. Manually click Submit button")
print("2. Wait for confirmation page")
print("3. Take screenshot: driver.save_screenshot('form_confirmation.png')")

input("\nPress ENTER after you manually submit to take confirmation screenshot...")

try:
    driver.save_screenshot('form_confirmation.png')
    print("Saved: form_confirmation.png")
except:
    print("Could not save confirmation screenshot")

time.sleep(2)
driver.quit()
print("\nDone!")