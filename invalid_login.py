import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_invalid_login_test(driver):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    login_page_path = os.path.join(base_dir, "AutomationProject", "src", "test", "resources", "mocksite", "login.html")
    login_url = "file:///" + login_page_path.replace("\\", "/")
    
    # 1. Open login page
    print(f"Navigating to: {login_url}")
    driver.get(login_url)
    
    wait = WebDriverWait(driver, 10)
    
    # 2. Enter invalid credentials
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    username_field.send_keys("wrong_user@example.com")
    
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("WrongPassword123")
    
    # 3. Click Login
    login_btn = driver.find_element(By.ID, "login-btn")
    login_btn.click()
    
    # 4. Verify error message appears and validate exact text
    try:
        error_msg_element = wait.until(EC.visibility_of_element_located((By.ID, "error-msg")))
        error_text = error_msg_element.text
        print(f"Captured error message: {error_text}")
        
        # Verify exact error message text
        assert error_text == "Invalid username or password.", \
            f"Expected error 'Invalid username or password.' but got '{error_text}'"
            
    except AssertionError as ae:
        # Capture screenshot on assertion failure
        screenshots_dir = os.path.join(base_dir, "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshots_dir, "login_failure.png")
        driver.save_screenshot(screenshot_path)
        print(f"Assertion failed. Screenshot captured at: {screenshot_path}")
        raise ae
    except Exception as e:
        # Capture screenshot on unexpected error
        screenshots_dir = os.path.join(base_dir, "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshots_dir, "login_error.png")
        driver.save_screenshot(screenshot_path)
        print(f"Unexpected exception occurred. Screenshot captured at: {screenshot_path}")
        raise e

def test_invalid_login():
    """Pytest entrypoint"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_invalid_login_test(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Executing Invalid Login Test...")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_invalid_login_test(driver)
        print("Test SUCCESS!")
    except Exception as e:
        print(f"Test FAILED: {e}")
        raise e
    finally:
        driver.quit()
