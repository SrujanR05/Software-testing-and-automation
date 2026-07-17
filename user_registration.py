import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_user_registration_test(driver):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    register_page_path = os.path.join(base_dir, "AutomationProject", "src", "test", "resources", "mocksite", "register.html")
    register_url = "file:///" + register_page_path.replace("\\", "/")
    
    # 1. Open registration page
    print(f"Navigating to: {register_url}")
    driver.get(register_url)
    
    wait = WebDriverWait(driver, 10)
    
    # 2. Generate unique email automatically
    timestamp = int(time.time() * 1000)
    unique_email = f"user_{timestamp}@testdomain.com"
    print(f"Generated unique email: {unique_email}")
    
    # 3. Enter valid details
    first_name_field = wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
    first_name_field.send_keys("Automated")
    
    last_name_field = driver.find_element(By.ID, "last-name")
    last_name_field.send_keys("Tester")
    
    email_field = driver.find_element(By.ID, "reg-email")
    email_field.send_keys(unique_email)
    
    password_field = driver.find_element(By.ID, "reg-password")
    password_field.send_keys("P@ssword123")
    
    confirm_password_field = driver.find_element(By.ID, "confirm-password")
    confirm_password_field.send_keys("P@ssword123")
    
    # 4. Submit registration
    register_btn = driver.find_element(By.ID, "register-btn")
    register_btn.click()
    
    # 5. Verify registration is successful (should redirect to dashboard)
    # Use WebDriverWait to wait for the URL to change to contain 'dashboard.html'
    wait.until(EC.url_contains("dashboard.html"))
    current_url = driver.current_url
    print(f"Redirected URL: {current_url}")
    assert "dashboard.html" in current_url, f"Expected redirect to dashboard.html but got {current_url}"
    
    # Verify welcome message on dashboard
    welcome_msg_element = wait.until(EC.visibility_of_element_located((By.ID, "welcome-msg")))
    welcome_text = welcome_msg_element.text
    print(f"Dashboard Welcome text: {welcome_text}")
    assert "Welcome to your dashboard" in welcome_text, f"Unexpected welcome message: {welcome_text}"

def test_user_registration():
    """Pytest entrypoint"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_user_registration_test(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Executing User Registration Test...")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_user_registration_test(driver)
        print("Test SUCCESS!")
    except Exception as e:
        print(f"Test FAILED: {e}")
        raise e
    finally:
        driver.quit()
