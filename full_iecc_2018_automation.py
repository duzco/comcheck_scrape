#!/usr/bin/env python3
"""
Full IECC 2018 Area Category Automation
Goal: Populate ALL 82 area categories for IECC 2018
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def populate_all_iecc_2018_areas():
    """
    Populate ALL area categories for IECC 2018
    """
    driver = None
    try:
        print("=== FULL IECC 2018 AREA AUTOMATION ===")
        print("Goal: Add ALL 82 area categories to IECC 2018 project")
        
        # Setup
        print("Step 1: Setting up browser and navigating to IECC 2018...")
        service = ChromeService()
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        
        # Navigate to COMcheck
        url = "https://energycode.pnl.gov/COMcheckWeb/"
        driver.get(url)
        
        # Click start
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "startButton"))
        )
        start_button.click()
        
        # Switch to new window
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        original_window = driver.current_window_handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        # Wait for loading
        try:
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.ID, "loadingIndicator"))
            )
        except:
            pass
        
        # Select IECC 2018
        code_dropdown = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "code"))
        )
        select = Select(code_dropdown)
        select.select_by_value("CEZ_IECC2018")
        print("✓ Selected IECC 2018")
        
        # Wait for page update after code selection
        time.sleep(2)
        try:
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.ID, "loadingIndicator"))
            )
        except:
            pass
        time.sleep(3)
        
        # Click Interior Lighting Method and Areas tab
        int_lighting_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='bat_category_int_lighting']"))
        )
        int_lighting_tab.click()
        time.sleep(2)
        print("✓ Navigated to Interior Lighting Method and Areas")
        
        # Load catalog
        print("Step 2: Loading area categories catalog...")
        catalog_file = '/Users/home/comcheck_scrape/iecc_2018_areas_catalog.json'
        with open(catalog_file, 'r') as f:
            catalog_data = json.load(f)
        
        categories = catalog_data['categories']
        total_combinations = sum(len(subcats) for subcats in categories.values() if subcats)
        print(f"📊 Loaded {len(categories)} categories with {total_combinations} total area combinations")
        
        # Start the automation loop
        print("Step 3: Starting full automation loop...")
        success_count = 0
        error_count = 0
        
        for category_name, subcategories in categories.items():
            if not subcategories:  # Skip categories with no subcategories
                print(f"⏭️  Skipping '{category_name}' (no subcategories)")
                continue
                
            print(f"\n📂 Processing category: '{category_name}' ({len(subcategories)} subcategories)")
            
            for i, subcategory in enumerate(subcategories, 1):
                try:
                    print(f"  🔄 Adding {i}/{len(subcategories)}: '{subcategory}'")
                    
                    # Step A: Open modal
                    add_area_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "addAreaCategory"))
                    )
                    add_area_button.click()
                    time.sleep(0.5)  # Reduced from 2s to 0.5s
                    
                    # Step B: Find and click the radio button for this category
                    radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                    category_radio = None
                    
                    for radio in radio_buttons:
                        radio_id = radio.get_attribute('id')
                        if radio_id:
                            try:
                                label = driver.find_element(By.CSS_SELECTOR, f"label[for='{radio_id}']")
                                if label.text.strip() == category_name:
                                    category_radio = radio
                                    break
                            except:
                                continue
                    
                    if not category_radio:
                        print(f"    ❌ Could not find radio button for '{category_name}'")
                        error_count += 1
                        # Close modal before continuing
                        try:
                            cancel_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'cancel')]")
                            cancel_btn.click()
                            time.sleep(0.2)  # Reduced from 1s to 0.2s
                        except:
                            pass
                        continue
                    
                    # Step C: Click the radio button
                    driver.execute_script("arguments[0].click();", category_radio)
                    time.sleep(0.3)  # Reduced from 1s to 0.3s
                    
                    # Step D: Find dropdown and select subcategory
                    try:
                        parent = category_radio.find_element(By.XPATH, "./..")
                        select_elem = parent.find_element(By.TAG_NAME, "select")
                        select_obj = Select(select_elem)
                        select_obj.select_by_visible_text(subcategory)
                        time.sleep(0.2)  # Reduced from 1s to 0.2s
                    except Exception as e:
                        print(f"    ❌ Could not select subcategory '{subcategory}': {e}")
                        error_count += 1
                        # Close modal before continuing
                        try:
                            cancel_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'cancel')]")
                            cancel_btn.click()
                            time.sleep(0.2)  # Reduced from 1s to 0.2s
                        except:
                            pass
                        continue
                    
                    # Step E: Click Create Area Category button
                    try:
                        create_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@class='accept default']"))
                        )
                        create_button.click()
                        time.sleep(0.5)  # Reduced from 2s to 0.5s
                        
                        success_count += 1
                        print(f"    ✅ Successfully added '{subcategory}'")
                        
                    except Exception as e:
                        print(f"    ❌ Could not click Create button: {e}")
                        error_count += 1
                        # Try to close modal
                        try:
                            cancel_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'cancel')]")
                            cancel_btn.click()
                            time.sleep(0.2)  # Reduced from 1s to 0.2s
                        except:
                            pass
                
                except Exception as e:
                    print(f"    ❌ Error adding '{subcategory}': {e}")
                    error_count += 1
                    # Try to close any open modal
                    try:
                        cancel_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'cancel')]")
                        cancel_btn.click()
                        time.sleep(0.2)  # Reduced from 1s to 0.2s
                    except:
                        pass
        
        # Final results
        print(f"\n🏁 FULL AUTOMATION COMPLETE!")
        print(f"✅ Successfully added: {success_count}")
        print(f"❌ Errors: {error_count}")
        total_attempted = success_count + error_count
        if total_attempted > 0:
            success_rate = (success_count / total_attempted) * 100
            print(f"📊 Success rate: {success_rate:.1f}%")
        
        if success_count == total_combinations:
            print("🎉 ALL 82 AREA CATEGORIES SUCCESSFULLY ADDED!")
        else:
            print(f"⚠️  {total_combinations - success_count} categories still need to be added")
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        
    finally:
        if driver:
            print("\n🎯 AUTOMATION FINISHED!")
            print("Browser remaining open for inspection...")
            input("Press Enter to close browser...")
            driver.quit()

if __name__ == "__main__":
    populate_all_iecc_2018_areas()
