import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_contact_form_test(driver):
    # Resolve the absolute path of contact.html dynamically
    base_dir = os.path.dirname(os.path.abspath(__file__))
    contact_page_path = os.path.join(base_dir, "AutomationProject", "src", "test", "resources", "mocksite", "contact.html")
    contact_url = "file:///" + contact_page_path.replace("\\", "/")
    
    # 1. Open the website / contact page
    print(f"Navigating to: {contact_url}")
    driver.get(contact_url)
    
    # 2. Fill all mandatory fields with WebDriverWait for stability
    wait = WebDriverWait(driver, 10)
    
    name_field = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    name_field.send_keys("Jane Doe")
    
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys("jane.doe@example.com")
    
    subject_field = driver.find_element(By.ID, "subject")
    subject_field.send_keys("Automation Testing Inquiry")
    
    message_field = driver.find_element(By.ID, "message")
    message_field.send_keys("Hello, this is a test message to verify the Contact Form submission scenario.")
    
    # 3. Submit the form
    submit_btn = driver.find_element(By.ID, "submit-btn")
    submit_btn.click()
    
    # 4. Verify the success message is displayed
    success_msg_element = wait.until(EC.visibility_of_element_located((By.ID, "success-msg")))
    success_text = success_msg_element.text
    print(f"Submission message: {success_text}")
    
    assert "Thank you! Your message has been submitted successfully." in success_text, \
        f"Unexpected success message text: '{success_text}'"
    
    # 5. Take screenshot after successful submission
    screenshots_dir = os.path.join(base_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshots_dir, "contact_success.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved successfully at: {screenshot_path}")

def test_contact_form():
    """Pytest entrypoint"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless for stability in CI environments
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_contact_form_test(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    # Allow executing the script directly via python contact_form_submission.py
    print("Executing Contact Form Submission Test...")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    # For interactive execution, we run with visible browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_contact_form_test(driver)
        print("Test SUCCESS!")
    except Exception as e:
        print(f"Test FAILED: {e}")
        raise e
    finally:
        driver.quit()
