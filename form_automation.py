import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from datetime import datetime

# ----------------------------
# LOAD ENVIRONMENT VARIABLES
# ----------------------------
load_dotenv()
print("DEBUG: GENDER =", os.getenv('GENDER'))  # Debug check

chrome_options = Options()
chrome_options.add_argument('--start-maximized')

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
except:
    driver = webdriver.Chrome(options=chrome_options)

# ----------------------------
# READ VALUES FROM .ENV
# ----------------------------
form_url = os.getenv('FORM_URL')
full_name = os.getenv('FULL_NAME')
contact_number = os.getenv('CONTACT_NUMBER')
email_id = os.getenv('EMAIL_ID')
full_address = os.getenv('FULL_ADDRESS')
pin_code = os.getenv('PIN_CODE')
date_of_birth = os.getenv('DATE_OF_BIRTH')
gender = os.getenv('GENDER')

print("=" * 70)
print(" " * 20 + "GOOGLE FORM AUTOMATION")
print("=" * 70)

# ----------------------------
# OPEN FORM
# ----------------------------
driver.get(form_url)
print("\n[1/9] Opening form...")
time.sleep(5)

text_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
textarea = driver.find_elements(By.TAG_NAME, 'textarea')[0]
date_field = driver.find_element(By.CSS_SELECTOR, 'input[type="date"]')

print(f"Found {len(text_inputs)} text fields, 1 textarea, 1 date field\n")


def fill_field(field, value, name):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
        time.sleep(0.8)
        field.click()
        time.sleep(0.3)
        field.clear()
        time.sleep(0.2)
        field.send_keys(value)
        time.sleep(0.5)
        print(f"✓ {name}: {value[:50]}")
        return True
    except Exception as e:
        print(f"✗ {name}: ERROR - {str(e)}")
        return False


# ----------------------------
# FILL TEXT FIELDS
# ----------------------------
print("[2/9] Filling Full Name...")
fill_field(text_inputs[0], full_name, "Full Name")

print("[3/9] Filling Contact Number...")
fill_field(text_inputs[1], contact_number, "Contact Number")

print("[4/9] Filling Email ID...")
fill_field(text_inputs[2], email_id, "Email ID")

print("[5/9] Filling Full Address (TEXTAREA)...")
fill_field(textarea, full_address, "Full Address")

print("[6/9] Filling Pin Code...")
fill_field(text_inputs[3], pin_code, "Pin Code")

# ----------------------------
# FILL DATE FIELD
# ----------------------------
print("[7/9] Filling Date of Birth...")
try:
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_field)
    time.sleep(0.8)

    date_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')

    date_field.click()
    time.sleep(0.5)

    driver.execute_script("arguments[0].value = '';", date_field)
    time.sleep(0.3)

    year = str(date_obj.year)
    month = str(date_obj.month).zfill(2)
    day = str(date_obj.day).zfill(2)
    formatted_date = f"{year}-{month}-{day}"

    driver.execute_script(f"arguments[0].value = '{formatted_date}';", date_field)
    time.sleep(0.5)
    date_field.send_keys(Keys.TAB)
    time.sleep(1)

    print(f"✓ Date of Birth: {day}/{month}/{year}")
except Exception as e:
    print(f"✗ Date of Birth: ERROR - {str(e)}")

# ----------------------------
# FILL GENDER FIELD (AUTO-DETECT)
# ----------------------------
print("[8/9] Selecting Gender (Auto-Detect)...")
time.sleep(1.5)

try:
    # Case 1: Radio buttons
    radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
    if radio_buttons:
        print(f"   Found {len(radio_buttons)} radio options")
        gender_found = False
        for radio in radio_buttons:
            aria_label = radio.get_attribute('aria-label') or ''
            data_value = radio.get_attribute('data-value') or ''
            if gender.lower() in aria_label.lower() or gender.lower() == data_value.lower():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
                time.sleep(0.5)
                radio.click()
                print(f"✓ Gender: {gender} selected (radio)")
                gender_found = True
                break
        if not gender_found:
            print("⚠ Gender radio option not found, trying other methods...")

    # Case 2: Dropdown
    if not radio_buttons:
        try:
            gender_dropdown = driver.find_element(By.CSS_SELECTOR, 'div[role="listbox"]')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender_dropdown)
            gender_dropdown.click()
            time.sleep(1)
            option = driver.find_element(By.XPATH, f"//div[@role='option' and text()='{gender}']")
            option.click()
            print(f"✓ Gender: {gender} selected (dropdown)")
        except Exception:
            # Case 3: Text input (fallback)
            print("⚠ No radio/dropdown found — filling as text input...")
            if len(text_inputs) > 4:
                fill_field(text_inputs[4], gender, "Gender")
            else:
                print("✗ No gender input field available")
except Exception as e:
    print(f"✗ Gender selection error: {str(e)}")

# ----------------------------
# FILL VERIFICATION CODE
# ----------------------------
print("[9/9] Filling Verification Code (GNFPYC)...")
time.sleep(1)

code_fields = []
for inp in text_inputs:
    try:
        inp_value = inp.get_attribute('value') or ''
        if inp_value == '':
            code_fields.append(inp)
    except:
        pass

if len(code_fields) > 0:
    last_empty_field = code_fields[-1]
    fill_field(last_empty_field, "GNFPYC", "Verification Code")
else:
    fill_field(text_inputs[-1], "GNFPYC", "Verification Code")

# ----------------------------
# FINAL CONFIRMATIONS
# ----------------------------
print("\n" + "=" * 70)
print(" " * 15 + "🎯 ALL FIELDS FILLED! 🎯")
print("=" * 70)

time.sleep(2)
driver.save_screenshot('form_filled_before_submit.png')
print("✓ Screenshot saved: form_filled_before_submit.png")

print("\n" + "=" * 70)
print("VERIFY in browser window:")
print("  ✓ Full Name: " + full_name)
print("  ✓ Contact: " + contact_number)
print("  ✓ Email: " + email_id)
print("  ✓ Address: " + full_address)
print("  ✓ Pin: " + pin_code)
print("  ✓ DOB: " + date_of_birth)
print("  ✓ Gender: " + gender + " (CHECK IN FORM!)")
print("  ✓ Code: GNFPYC")
input("\nPress ENTER to SUBMIT (Ctrl+C to cancel)...")
print("=" * 70)

# ----------------------------
# SUBMIT FORM
# ----------------------------
try:
    print("\nSubmitting form...")
    submit_buttons = driver.find_elements(By.CSS_SELECTOR, '[type="submit"]')
    if submit_buttons:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_buttons[0])
        time.sleep(1)
        submit_buttons[0].click()
        print("✓ Clicked Submit")
        time.sleep(6)
        driver.save_screenshot('form_confirmation.png')
        print("✓ Confirmation screenshot saved")

        print("\n" + "=" * 70)
        print(" " * 10 + "FORM SUBMITTED SUCCESSFULLY!")
        print("=" * 70)
        print("\n Files created:")
        print("   • form_filled_before_submit.png")
        print("   • form_confirmation.png")
        print("\n Next: Run 'python send_email_simple.py'")
        print("=" * 70)
    else:
        print("✗ Submit button not found")
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    driver.save_screenshot('error_screenshot.png')

print("\nClosing in 3 seconds...")
time.sleep(3)
driver.quit()
print("Done!")
