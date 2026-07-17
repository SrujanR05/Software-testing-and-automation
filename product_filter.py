import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_product_filter_test(driver):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    products_page_path = os.path.join(base_dir, "AutomationProject", "src", "test", "resources", "mocksite", "products.html")
    products_url = "file:///" + products_page_path.replace("\\", "/")
    
    # 1. Open products catalog page
    print(f"Navigating to: {products_url}")
    driver.get(products_url)
    
    wait = WebDriverWait(driver, 10)
    
    # Wait for the products to load/display initially
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product-card")))
    
    # --- Category Filter Test ---
    print("Testing Category Filter: Electronics")
    # 2. Filter by Category: check Electronics
    cat_electronics = driver.find_element(By.ID, "cat-electronics")
    if not cat_electronics.is_selected():
        cat_electronics.click()
        
    # Click filter button
    filter_btn = driver.find_element(By.ID, "filter-btn")
    filter_btn.click()
    
    # Verify displayed products satisfy Category filter
    # Let's wait a moment or verify cards
    product_cards = driver.find_elements(By.CLASS_NAME, "product-card")
    print(f"Found {len(product_cards)} products matching category 'Electronics'")
    
    assert len(product_cards) > 0, "No products displayed for category 'Electronics'."
    
    for card in product_cards:
        category_elem = card.find_element(By.CLASS_NAME, "product-category")
        category_text = category_elem.text
        title_elem = card.find_element(By.CLASS_NAME, "product-title")
        print(f" - Product: '{title_elem.text}' | Category: '{category_text}'")
        assert category_text == "ELECTRONICS", f"Expected category 'ELECTRONICS' but found '{category_text}' for product '{title_elem.text}'"

    # --- Price Range Filter Test ---
    print("\nTesting Price Range Filter: $40 to $200 (within Electronics category)")
    # 3. Filter by Price Range: Min=40, Max=200
    min_price_input = driver.find_element(By.ID, "min-price")
    max_price_input = driver.find_element(By.ID, "max-price")
    
    # In Chrome/Selenium, clearing number fields can sometimes require backspacing or script execution
    driver.execute_script("arguments[0].value = '';", min_price_input)
    min_price_input.send_keys("40")
    
    driver.execute_script("arguments[0].value = '';", max_price_input)
    max_price_input.send_keys("200")
    
    # Click filter button to apply
    filter_btn.click()
    
    # Verify displayed products satisfy selected filters
    product_cards_filtered = driver.find_elements(By.CLASS_NAME, "product-card")
    print(f"Found {len(product_cards_filtered)} products within price range $40 - $200 in 'Electronics'")
    
    assert len(product_cards_filtered) > 0, "No products found in price range $40-$200 for Electronics."
    
    for card in product_cards_filtered:
        category_elem = card.find_element(By.CLASS_NAME, "product-category")
        price_elem = card.find_element(By.CLASS_NAME, "product-price")
        title_elem = card.find_element(By.CLASS_NAME, "product-title")
        
        category_text = category_elem.text
        price_text = price_elem.text
        # Remove '$' from price
        price_value = float(price_text.replace("$", ""))
        
        print(f" - Product: '{title_elem.text}' | Category: '{category_text}' | Price: '{price_text}'")
        
        # Assert category is still Electronics
        assert category_text == "ELECTRONICS", f"Product '{title_elem.text}' category is '{category_text}', expected 'ELECTRONICS'"
        # Assert price is within [40, 200]
        assert 40 <= price_value <= 200, f"Product '{title_elem.text}' price {price_value} is not within range $40 - $200"

def test_product_filter():
    """Pytest entrypoint"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_product_filter_test(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Executing Product Filter Test...")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_product_filter_test(driver)
        print("Test SUCCESS!")
    except Exception as e:
        print(f"Test FAILED: {e}")
        raise e
    finally:
        driver.quit()
