import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_email_validation_test(driver):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    register_page_path = os.path.join(base_dir, "AutomationProject", "src", "test", "resources", "mocksite", "register.html")
    register_url = "file:///" + register_page_path.replace("\\", "/")
    
    # 1. Open registration page
    print(f"Navigating to: {register_url}")
    driver.get(register_url)
    
    wait = WebDriverWait(driver, 10)
    email_field = wait.until(EC.visibility_of_element_located((By.ID, "reg-email")))
    error_label = driver.find_element(By.ID, "email-error-msg")
    
    # List of invalid email formats to check
    invalid_emails = [
        "abc",
        "abc@",
        "@gmail.com",
        "abc@gmail",
        "abc.com"
    ]
    
    # 2. Verify invalid email formats show error messages
    for invalid in invalid_emails:
        email_field.clear()
        email_field.send_keys(invalid)
        
        # Click outside or type something to trigger the input validator event
        # In our script, the input event listener is triggered instantly as we type,
        # but we can explicitly wait for the label to be visible.
        try:
            wait.until(EC.visibility_of_element_located((By.ID, "email-error-msg")))
            error_text = error_label.text
            print(f"Tested '{invalid}' - Validation message displayed: '{error_text}'")
            assert "Invalid email format" in error_text, f"Expected validation message for email '{invalid}' but got '{error_text}'"
        except Exception as e:
            # Take screenshot for debugging if validation fails
            driver.save_screenshot(os.path.join(base_dir, f"error_invalid_email_{invalid.replace('@', '_')}.png"))
            raise e

    # 3. Verify valid email is accepted and error label disappears
    valid_email = "tester@example.com"
    email_field.clear()
    email_field.send_keys(valid_email)
    
    # Verify the error message goes away
    # We wait for the label style to be display: none or verify text is empty/hidden
    wait.until(EC.invisibility_of_element_located((By.ID, "email-error-msg")))
    is_displayed = error_label.is_displayed()
    print(f"Tested valid email '{valid_email}' - Error message visible: {is_displayed}")
    assert not is_displayed, "Error label should be hidden for valid email format."

def test_email_validation():
    """Pytest entrypoint"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_email_validation_test(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Executing Email Validation Test...")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_email_validation_test(driver)
        print("Test SUCCESS!")
    except Exception as e:
        print(f"Test FAILED: {e}")
        raise e
    finally:
        driver.quit()
