#!/usr/bin/env python3
"""
Extract all available code years from COMcheck dropdown
Goal: Get complete list of all codes for iteration
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_all_codes():
    """
    Extract all available code options from the COMcheck dropdown
    """
    driver = None
    try:
        print("=== EXTRACTING ALL CODE OPTIONS ===")
        print("Step 1: Initializing WebDriver...")
        
        service = ChromeService()
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        
        print("Step 2: Navigating to COMcheck-Web...")
        url = "https://energycode.pnl.gov/COMcheckWeb/"
        driver.get(url)
        
        print("Step 3: Clicking Start button...")
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "startButton"))
        )
        start_button.click()
        
        print("Step 4: Switching to application window...")
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        original_window = driver.current_window_handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        print("Step 5: Waiting for loading to complete...")
        try:
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.ID, "loadingIndicator"))
            )
        except:
            pass  # Loading indicator might not be present
        
        print("Step 6: Opening code dropdown...")
        code_dropdown = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "code"))
        )
        code_dropdown.click()
        time.sleep(2)
        
        print("Step 7: Extracting all code options...")
        options = driver.find_elements(By.CSS_SELECTOR, "#code option")
        
        codes_data = []
        print(f"\nFound {len(options)} total code options:")
        print("=" * 60)
        
        for i, option in enumerate(options, 1):
            text = option.text.strip()
            value = option.get_attribute('value')
            
            # Skip empty options
            if not text or not value:
                continue
                
            codes_data.append({
                "index": i,
                "text": text,
                "value": value
            })
            
            print(f"{i:2d}. {text:<40} (value: {value})")
        
        print("=" * 60)
        print(f"Total valid codes: {len(codes_data)}")
        
        # Save to JSON file for later use
        with open('/Users/home/comcheck_scrape/all_codes.json', 'w') as f:
            json.dump(codes_data, f, indent=2)
        
        print(f"\n✓ Saved all codes to: /Users/home/comcheck_scrape/all_codes.json")
        
        # Categorize codes
        iecc_codes = [code for code in codes_data if 'IECC' in code['text']]
        standard_codes = [code for code in codes_data if 'Standard' in code['text']]
        local_codes = [code for code in codes_data if 'Standard' not in code['text'] and 'IECC' not in code['text']]
        
        print(f"\nCode Categories:")
        print(f"  IECC Codes: {len(iecc_codes)}")
        print(f"  90.1 Standards: {len(standard_codes)}")
        print(f"  Local Codes: {len(local_codes)}")
        
        return codes_data
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None
        
    finally:
        if driver:
            print("\nBrowser remaining open for inspection...")
            input("Press Enter to close browser...")
            driver.quit()

if __name__ == "__main__":
    codes = extract_all_codes()
    if codes:
        print(f"\n✅ Successfully extracted {len(codes)} code options!")
