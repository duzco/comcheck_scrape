#!/usr/bin/env python3
"""
Basic COMcheck navigation test - Step 1
Goal: Navigate to COMcheck and successfully read the first code option from dropdown
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_basic_navigation():
    """
    Test basic navigation to COMcheck and dropdown access
    """
    driver = None
    try:
        print("=== BASIC NAVIGATION TEST ===")
        print("Step 1: Initializing WebDriver...")
        
        # Setup Chrome driver
        service = ChromeService()
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        
        print("Step 2: Navigating to COMcheck-Web...")
        url = "https://energycode.pnl.gov/COMcheckWeb/"
        driver.get(url)
        
        print("Step 3: Looking for Start button...")
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "startButton"))
        )
        print(f"✓ Found start button: {start_button.text}")
        
        print("Step 4: Clicking Start button...")
        start_button.click()
        
        print("Step 5: Waiting for new window...")
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        
        # Switch to new window
        original_window = driver.current_window_handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        print("✓ Successfully switched to application window")
        
        print("Step 6: Waiting for loading indicator to disappear...")
        # Wait for loading indicator to disappear
        try:
            loading_indicator = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "loadingIndicator"))
            )
            print("✓ Found loading indicator, waiting for it to disappear...")
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.ID, "loadingIndicator"))
            )
            print("✓ Loading indicator disappeared")
        except:
            print("✓ No loading indicator found or already gone")
        
        print("Step 7: Looking for code dropdown...")
        # Wait for page to load and find the code dropdown
        code_dropdown = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "code"))
        )
        print("✓ Found code dropdown element")
        
        print("Step 8: Clicking code dropdown to open it...")
        code_dropdown.click()
        time.sleep(2)  # Give it time to populate
        
        print("Step 9: Attempting to read dropdown options...")
        # Look for option elements within the dropdown
        options = driver.find_elements(By.CSS_SELECTOR, "#code option")
        
        if options:
            print(f"✓ Found {len(options)} code options in dropdown")
            print(f"First option text: '{options[0].text}'")
            print(f"First option value: '{options[0].get_attribute('value')}'")
            
            # Print first few options for verification
            print("\nFirst 5 options:")
            for i, option in enumerate(options[:5]):
                print(f"  {i+1}. {option.text} (value: {option.get_attribute('value')})")
                
        else:
            print("❌ No options found in dropdown")
            print("Dropdown HTML:")
            print(code_dropdown.get_attribute('outerHTML'))
        
        print("\n=== TEST COMPLETED SUCCESSFULLY ===")
        
    except Exception as e:
        print(f"\n❌ ERROR OCCURRED: {e}")
        if driver:
            print("\nCurrent page title:", driver.title)
            print("Current URL:", driver.current_url)
            
            # Try to find any select elements for debugging
            selects = driver.find_elements(By.TAG_NAME, "select")
            print(f"Found {len(selects)} select elements on page")
            
    finally:
        if driver:
            print("\nBrowser will remain open for inspection...")
            input("Press Enter to close browser...")
            driver.quit()

if __name__ == "__main__":
    test_basic_navigation()
