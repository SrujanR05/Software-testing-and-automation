import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def calculate_expected_totals(items_prices_qtys):
    subtotal = sum(price * qty for price, qty in items_prices_qtys)
    tax = subtotal * 0.1
    grand_total = subtotal + tax
    return subtotal, grand_total

def run_shopping_cart_test(driver):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    products_page_path = os.path.join(base_dir, "AutomationProject", "src", "test", "resources", "mocksite", "products.html")
    cart_page_path = os.path.join(base_dir, "AutomationProject", "src", "test", "resources", "mocksite", "cart.html")
    
    products_url = "file:///" + products_page_path.replace("\\", "/")
    cart_url = "file:///" + cart_page_path.replace("\\", "/")
    
    # 1. Open products catalog page
    print(f"Navigating to: {products_url}")
    driver.get(products_url)
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product-card")))
    
    # Locate all Add to Cart buttons
    add_buttons = driver.find_elements(By.CLASS_NAME, "add-to-cart-btn")
    
    # Add first product (Quantum Laptop: $1200)
    add_buttons[0].click()
    print("Added first product to cart")
    
    # Wait for the confirmation toast to disappear or just click the next item
    # Add second product (Noise Cancelling Headphones: $250)
    add_buttons[1].click()
    print("Added second product to cart")
    
    # 2. Navigate to Cart page
    print(f"Navigating to: {cart_url}")
    driver.get(cart_url)
    
    # Wait for cart items to render
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart-item")))
    cart_items = driver.find_elements(By.CLASS_NAME, "cart-item")
    
    # 3. Verify products appear in cart
    print(f"Number of items in cart: {len(cart_items)}")
    assert len(cart_items) == 2, f"Expected 2 items in cart, but found {len(cart_items)}"
    
    # Check individual product subtotal matches initial add ($1200 + $250)
    subtotal_elem = driver.find_element(By.ID, "cart-subtotal")
    grandtotal_elem = driver.find_element(By.ID, "cart-grandtotal")
    
    subtotal_val = float(subtotal_elem.text.replace("$", ""))
    grandtotal_val = float(grandtotal_elem.text.replace("$", ""))
    
    print(f"Initial Subtotal: {subtotal_val} | Initial Grand Total: {grandtotal_val}")
    
    expected_sub, expected_grand = calculate_expected_totals([(1200.0, 1), (250.0, 1)])
    assert subtotal_val == expected_sub, f"Expected subtotal {expected_sub} but got {subtotal_val}"
    assert grandtotal_val == expected_grand, f"Expected grand total {expected_grand} but got {grandtotal_val}"
    
    # 4. Increase quantity of first item
    first_item = cart_items[0]
    first_item_title = first_item.find_element(By.CLASS_NAME, "cart-item-title").text
    inc_btn = first_item.find_element(By.CLASS_NAME, "qty-inc-btn")
    print(f"Increasing quantity of '{first_item_title}'")
    inc_btn.click()
    
    # Verify quantity updates correctly
    qty_span = first_item.find_element(By.CLASS_NAME, "item-qty")
    wait.until(lambda d: qty_span.text == "2")
    assert qty_span.text == "2", f"Expected quantity to be 2, but got '{qty_span.text}'"
    
    # Verify totals updated after quantity increase
    subtotal_val = float(driver.find_element(By.ID, "cart-subtotal").text.replace("$", ""))
    grandtotal_val = float(driver.find_element(By.ID, "cart-grandtotal").text.replace("$", ""))
    print(f"After Qty Increase - Subtotal: {subtotal_val} | Grand Total: {grandtotal_val}")
    
    expected_sub, expected_grand = calculate_expected_totals([(1200.0, 2), (250.0, 1)])
    assert subtotal_val == expected_sub, f"Expected subtotal {expected_sub} after increase but got {subtotal_val}"
    assert grandtotal_val == expected_grand, f"Expected grand total {expected_grand} after increase but got {grandtotal_val}"
    
    # 5. Decrease quantity of first item back to 1
    dec_btn = first_item.find_element(By.CLASS_NAME, "qty-dec-btn")
    print(f"Decreasing quantity of '{first_item_title}'")
    dec_btn.click()
    wait.until(lambda d: qty_span.text == "1")
    assert qty_span.text == "1", f"Expected quantity to be 1, but got '{qty_span.text}'"
    
    # 6. Remove one product (second product)
    # Re-evaluate the cart items list from DOM to avoid stale references
    cart_items = driver.find_elements(By.CLASS_NAME, "cart-item")
    second_item = cart_items[1]
    second_item_title = second_item.find_element(By.CLASS_NAME, "cart-item-title").text
    remove_btn = second_item.find_element(By.CLASS_NAME, "remove-item-btn")
    print(f"Removing product: '{second_item_title}'")
    remove_btn.click()
    
    # Verify only one product remains
    wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "cart-item")) == 1)
    cart_items_after_remove = driver.find_elements(By.CLASS_NAME, "cart-item")
    assert len(cart_items_after_remove) == 1, "Expected only 1 item to remain in cart."
    
    # 7. Verify subtotal and grand total are updated correctly after deletion
    subtotal_val = float(driver.find_element(By.ID, "cart-subtotal").text.replace("$", ""))
    grandtotal_val = float(driver.find_element(By.ID, "cart-grandtotal").text.replace("$", ""))
    print(f"After Removal - Subtotal: {subtotal_val} | Grand Total: {grandtotal_val}")
    
    expected_sub, expected_grand = calculate_expected_totals([(1200.0, 1)])
    assert subtotal_val == expected_sub, f"Expected subtotal {expected_sub} after deletion but got {subtotal_val}"
    assert grandtotal_val == expected_grand, f"Expected grand total {expected_grand} after deletion but got {grandtotal_val}"
    
    # 8. Verify total changes after another quantity modification
    remaining_item = cart_items_after_remove[0]
    inc_btn = remaining_item.find_element(By.CLASS_NAME, "qty-inc-btn")
    print("Modifying remaining item quantity to 3")
    inc_btn.click()
    inc_btn.click()
    
    qty_span = remaining_item.find_element(By.CLASS_NAME, "item-qty")
    wait.until(lambda d: qty_span.text == "3")
    
    subtotal_val = float(driver.find_element(By.ID, "cart-subtotal").text.replace("$", ""))
    grandtotal_val = float(driver.find_element(By.ID, "cart-grandtotal").text.replace("$", ""))
    print(f"After Qty to 3 - Subtotal: {subtotal_val} | Grand Total: {grandtotal_val}")
    
    expected_sub, expected_grand = calculate_expected_totals([(1200.0, 3)])
    assert subtotal_val == expected_sub, f"Expected subtotal {expected_sub} for 3 items but got {subtotal_val}"
    assert grandtotal_val == expected_grand, f"Expected grand total {expected_grand} for 3 items but got {grandtotal_val}"

def test_shopping_cart():
    """Pytest entrypoint"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_shopping_cart_test(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Executing Shopping Cart Test...")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        run_shopping_cart_test(driver)
        print("Test SUCCESS!")
    except Exception as e:
        print(f"Test FAILED: {e}")
        raise e
    finally:
        driver.quit()
