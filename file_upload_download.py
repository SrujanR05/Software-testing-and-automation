import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_file_operations_test(driver, download_dir):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    upload_page_path = os.path.join(base_dir, "AutomationProject", "src", "test", "resources", "mocksite", "upload.html")
    upload_url = "file:///" + upload_page_path.replace("\\", "/")
    
    # Create temporary files for uploading
    valid_file_path = os.path.join(base_dir, "sample_valid.txt")
    invalid_file_path = os.path.join(base_dir, "sample_invalid.exe")
    
    with open(valid_file_path, "w") as f:
        f.write("This is a valid test file for upload verification.")
        
    with open(invalid_file_path, "w") as f:
        f.write("Mock binary content simulating executable file.")
        
    try:
        # 1. Open upload page
        print(f"Navigating to: {upload_url}")
        driver.get(upload_url)
        
        wait = WebDriverWait(driver, 10)
        
        # --- Part A: Valid File Upload ---
        print("\nPart A - Valid File Upload Test...")
        # Since input is hidden under label, we can locate `#file-upload-input` directly
        file_input = wait.until(EC.presence_of_element_located((By.ID, "file-upload-input")))
        file_input.send_keys(valid_file_path)
        
        upload_btn = driver.find_element(By.ID, "upload-submit-btn")
        upload_btn.click()
        
        # Verify success message
        status_msg = wait.until(EC.visibility_of_element_located((By.ID, "upload-status-msg")))
        success_text = status_msg.text
        print(f"Upload Result message: {success_text}")
        assert "File uploaded successfully" in success_text, f"Expected success message but got: '{success_text}'"
        assert "sample_valid.txt" in success_text, f"Expected file name in success message but got: '{success_text}'"
        
        # --- Part B: Invalid File Upload ---
        print("\nPart B - Invalid File Upload Test...")
        # Re-fetch input to avoid stale element reference
        file_input = driver.find_element(By.ID, "file-upload-input")
        file_input.send_keys(invalid_file_path)
        
        upload_btn.click()
        
        # Verify error message
        wait.until(lambda d: "Unsupported file type" in d.find_element(By.ID, "upload-status-msg").text)
        error_text = status_msg.text
        print(f"Invalid Upload Result message: {error_text}")
        assert "Error: Unsupported file type" in error_text, f"Expected validation error message but got: '{error_text}'"
        
        # --- Part C: File Download ---
        print("\nPart C - File Download Test...")
        # Clean previous downloads if any
        target_download_file = os.path.join(download_dir, "testdownload.txt")
        if os.path.exists(target_download_file):
            os.remove(target_download_file)
            
        download_link = driver.find_element(By.ID, "file-download-link")
        download_link.click()
        print("Clicked download link, waiting for file completion...")
        
        # Wait for file download to complete
        # Poll directory for up to 10 seconds
        downloaded = False
        for _ in range(20):
            if os.path.exists(target_download_file):
                # Verify file size > 0 and file is not still downloading (.crdownload)
                file_size = os.path.getsize(target_download_file)
                if file_size > 0:
                    downloaded = True
                    break
            time.sleep(0.5)
            
        assert downloaded, "Download failed: File was not created in the download directory within the timeout."
        
        # Verify filename and size > 0
        actual_filename = os.path.basename(target_download_file)
        actual_size = os.path.getsize(target_download_file)
        
        print(f"Downloaded File Name: {actual_filename}")
        print(f"Downloaded File Size: {actual_size} bytes")
        
        assert actual_filename == "testdownload.txt", f"Expected filename 'testdownload.txt' but got '{actual_filename}'"
        assert actual_size > 0, f"Expected downloaded file size to be greater than zero but got {actual_size}"
        
    finally:
        # Cleanup temporary files
        if os.path.exists(valid_file_path):
            os.remove(valid_file_path)
        if os.path.exists(invalid_file_path):
            os.remove(invalid_file_path)
        if os.path.exists(target_download_file):
            os.remove(target_download_file)

def test_file_upload_download():
    """Pytest entrypoint"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(base_dir, "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Configure default download preferences
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_file_operations_test(driver, download_dir)
    finally:
        driver.quit()
        # Clean up download folder
        try:
            os.rmdir(download_dir)
        except OSError:
            pass

if __name__ == "__main__":
    print("Executing File Upload and Download Test...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(base_dir, "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_file_operations_test(driver, download_dir)
        print("Test SUCCESS!")
    except Exception as e:
        print(f"Test FAILED: {e}")
        raise e
    finally:
        driver.quit()
        try:
            os.rmdir(download_dir)
        except OSError:
            pass
