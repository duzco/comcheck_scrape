#!/usr/bin/env python3
"""
Test adding a single area category - Complete cycle proof of concept
Goal: Select radio button → open dropdown → pick option → submit
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def discover_all_area_categories(driver):
    """
    Discover and catalog all area categories and subcategories
    """
    print("=== DISCOVERING ALL AREA CATEGORIES ===")
    
    categories_catalog = {}
    
    try:
        # Find all radio buttons in the modal
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        print(f"Found {len(radio_buttons)} radio buttons")
        
        for i, radio in enumerate(radio_buttons):
            try:
                # Get the label text for this radio button
                radio_id = radio.get_attribute('id')
                if not radio_id:
                    continue
                    
                # Find the label associated with this radio
                try:
                    label = driver.find_element(By.CSS_SELECTOR, f"label[for='{radio_id}']")
                    category_name = label.text.strip()
                except:
                    # Fallback: look for text near the radio
                    category_name = f"Category_{i+1}"
                
                if not category_name:
                    continue
                    
                print(f"\nDiscovering category: '{category_name}'")
                
                # Click the radio button to unlock its dropdown
                driver.execute_script("arguments[0].click();", radio)
                time.sleep(1)
                
                # Look for the associated dropdown/select element
                subcategories = []
                try:
                    # Try to find select element near this radio
                    parent = radio.find_element(By.XPATH, "./..")
                    select_elem = parent.find_element(By.TAG_NAME, "select")
                    
                    # Get all options from the dropdown
                    select_obj = Select(select_elem)
                    options = select_obj.options
                    
                    for option in options[1:]:  # Skip first "Select..." option
                        option_text = option.text.strip()
                        if option_text:
                            subcategories.append(option_text)
                    
                    print(f"  Found {len(subcategories)} subcategories")
                    categories_catalog[category_name] = subcategories
                    
                except Exception as e:
                    print(f"  ⚠️ Could not find dropdown for '{category_name}': {e}")
                    # Still add the category, even if no subcategories found
                    categories_catalog[category_name] = []
                
            except Exception as e:
                print(f"  ❌ Error processing radio button {i+1}: {e}")
                continue
        
        # Save the catalog
        catalog_file = '/Users/home/comcheck_scrape/iecc_2018_areas_catalog.json'
        with open(catalog_file, 'w') as f:
            json.dump({
                "code": "IECC 2018", 
                "categories": categories_catalog,
                "total_categories": len(categories_catalog),
                "total_subcategories": sum(len(subcats) for subcats in categories_catalog.values())
            }, f, indent=2)
        
        print(f"\n✅ DISCOVERY COMPLETE!")
        print(f"📁 Saved catalog to: {catalog_file}")
        print(f"📊 Found {len(categories_catalog)} main categories")
        print(f"📊 Found {sum(len(subcats) for subcats in categories_catalog.values())} total subcategories")
        
        return categories_catalog
        
    except Exception as e:
        print(f"❌ Error during discovery: {e}")
        return {}

def populate_all_area_categories(driver, catalog_file='/Users/home/comcheck_scrape/iecc_2018_areas_catalog.json'):
    """
    Populate all area categories from the catalog
    """
    print("=== POPULATING ALL AREA CATEGORIES ===")
    
    # Load the catalog
    try:
        with open(catalog_file, 'r') as f:
            catalog_data = json.load(f)
        categories = catalog_data['categories']
        total_combinations = sum(len(subcats) for subcats in categories.values() if subcats)
        print(f"📊 Loaded catalog with {len(categories)} categories and {total_combinations} total combinations")
    except Exception as e:
        print(f"❌ Could not load catalog: {e}")
        return
    
    success_count = 0
    error_count = 0
    
    # Iterate through each category and its subcategories
    for category_name, subcategories in categories.items():
        if not subcategories:  # Skip categories with no subcategories
            print(f"⏭️  Skipping '{category_name}' (no subcategories)")
            continue
            
        print(f"\n📂 Processing category: '{category_name}' ({len(subcategories)} subcategories)")
        
        for i, subcategory in enumerate(subcategories, 1):
            try:
                print(f"  🔄 Adding {i}/{len(subcategories)}: '{subcategory}'")
                
                # Step 1: Click Add Area Category button to open modal
                add_area_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "addAreaCategory"))
                )
                add_area_button.click()
                time.sleep(2)
                
                # Step 2: Find and click the radio button for this category
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
                    continue
                
                # Click the radio button
                driver.execute_script("arguments[0].click();", category_radio)
                time.sleep(1)
                
                # Step 3: Find the dropdown and select the subcategory
                try:
                    parent = category_radio.find_element(By.XPATH, "./..")
                    select_elem = parent.find_element(By.TAG_NAME, "select")
                    select_obj = Select(select_elem)
                    select_obj.select_by_visible_text(subcategory)
                    time.sleep(1)
                except Exception as e:
                    print(f"    ❌ Could not select subcategory '{subcategory}': {e}")
                    error_count += 1
                    continue
                
                # Step 4: Click "Create Area Category" button
                try:
                    create_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create Area Category')] | //*[@value='Create Area Category']"))
                    )
                    create_button.click()
                    time.sleep(2)  # Wait for modal to close and area to be added
                    
                    success_count += 1
                    print(f"    ✅ Successfully added '{subcategory}'")
                    
                except Exception as e:
                    print(f"    ❌ Could not click Create button: {e}")
                    error_count += 1
                
            except Exception as e:
                print(f"    ❌ Error adding '{subcategory}': {e}")
                error_count += 1
    
    print(f"\n🏁 POPULATION COMPLETE!")
    print(f"✅ Successfully added: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Success rate: {success_count/(success_count + error_count)*100:.1f}%" if (success_count + error_count) > 0 else "No items processed")

def test_single_area_addition():
    """
    Test adding one area category to establish the complete flow
    """
    driver = None
    try:
        print("=== TESTING SINGLE AREA CATEGORY ADDITION ===")
        print("Step 1: Setting up and navigating to IECC 2018...")
        
        service = ChromeService()
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        
        # Navigate and setup (reusing our proven flow)
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
        print("✓ Page updated after code selection")
        
        print("Step 2: Clicking Interior Lighting Method and Areas tab...")
        # Click the Interior Lighting Method and Areas tab (it's a label/tab, not a radio button)
        try:
            # Try clicking the label for the radio button (which acts as the tab)
            int_lighting_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='bat_category_int_lighting']"))
            )
            int_lighting_tab.click()
            print("✓ Clicked Interior Lighting Method and Areas tab via label")
        except:
            # Fallback: click the radio input directly
            int_lighting_radio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "bat_category_int_lighting"))
            )
            int_lighting_radio.click()
            print("✓ Clicked Interior Lighting Method and Areas tab via radio input")
        time.sleep(2)
        
        print("Step 3: Opening Add Area Category modal...")
        # Click Add Area Category button using the exact ID from the screenshot
        try:
            add_area_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "addAreaCategory"))
            )
            add_area_button.click()
            print("✓ Clicked Add Area Category button by ID")
        except:
            # Fallback to CSS selector
            try:
                add_area_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.checkButton.addButton"))
                )
                add_area_button.click()
                print("✓ Clicked Add Area Category button by CSS class")
            except Exception as e:
                print(f"❌ Could not find Add Area Category button: {e}")
                # Debug: show available buttons
                buttons = driver.find_elements(By.TAG_NAME, "a")
                print(f"Found {len(buttons)} anchor elements, looking for Add buttons:")
                for i, btn in enumerate(buttons[:10]):
                    btn_id = btn.get_attribute('id')
                    btn_text = btn.text.strip()
                    btn_class = btn.get_attribute('class')
                    if 'add' in btn_id.lower() if btn_id else False or 'add' in btn_text.lower() if btn_text else False:
                        print(f"  Button {i+1}: ID='{btn_id}', Text='{btn_text}', Class='{btn_class}'")
                raise
        
        time.sleep(3)
        print("✓ Modal opened")
        
        print("Step 4: Using the open modal for single area test...")
        # The modal is already open from Step 3, no need to close and reopen it
        
        # Find and click the "Convention Center" radio button (using discovery script approach)
        print("Step 5: Looking for Convention Center radio button...")
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        convention_radio = None
        
        print(f"Found {len(radio_buttons)} radio buttons in modal")
        
        for i, radio in enumerate(radio_buttons):
            try:
                radio_id = radio.get_attribute('id')
                if not radio_id:
                    continue
                    
                # Find the label associated with this radio (same as discovery script)
                try:
                    label = driver.find_element(By.CSS_SELECTOR, f"label[for='{radio_id}']")
                    category_name = label.text.strip()
                    print(f"  Radio {i+1}: '{category_name}' (ID: {radio_id})")
                    
                    if "Convention Center" in category_name:
                        convention_radio = radio
                        print(f"✓ Found Convention Center radio: '{category_name}'")
                        break
                except:
                    # Fallback: look for text near the radio
                    category_name = f"Category_{i+1}"
                    print(f"  Radio {i+1}: '{category_name}' (no label found)")
                    
            except Exception as e:
                print(f"  ❌ Error processing radio button {i+1}: {e}")
                continue
        
        if not convention_radio:
            print("❌ Could not find Convention Center radio button")
            return
        
        # Click the Convention Center radio button
        print("Step 6: Clicking Convention Center radio button...")
        driver.execute_script("arguments[0].click();", convention_radio)
        time.sleep(2)
        print("✓ Clicked Convention Center radio button")
        
        # Find the dropdown and select subcategory (using discovery script approach)
        print("Step 7: Looking for dropdown and selecting subcategory...")
        subcategories = []
        try:
            # Try to find select element near this radio (same as discovery script)
            parent = convention_radio.find_element(By.XPATH, "./..")
            select_elem = parent.find_element(By.TAG_NAME, "select")
            
            # Get all options from the dropdown (same as discovery script)
            select_obj = Select(select_elem)
            options = select_obj.options
            
            print(f"Found {len(options)} options in dropdown:")
            for i, option in enumerate(options):
                option_text = option.text.strip()
                option_value = option.get_attribute('value')
                print(f"  {i+1}. '{option_text}' (value: {option_value})")
                if option_text and not option_text.startswith("Select"):  # Skip placeholder
                    subcategories.append(option_text)
            
            print(f"Valid subcategories: {subcategories}")
            
            # Select the first valid subcategory
            if subcategories:
                target_subcategory = subcategories[0]
                select_obj.select_by_visible_text(target_subcategory)
                print(f"✓ Selected: '{target_subcategory}'")
                time.sleep(1)
            else:
                print("❌ No valid subcategories found")
                return
                
        except Exception as e:
            print(f"❌ Could not find dropdown for Convention Center: {e}")
            return
        
        # Click "Create Area Category" button
        print("Step 8: Clicking Create Area Category button...")
        try:
            # Try multiple selectors for the create button (including class-based selectors)
            button_selectors = [
                "//button[contains(text(), 'Create Area Category')]",
                "//input[@value='Create Area Category']", 
                "//button[@class='accept default']",
                "//input[@class='accept default']",
                "//button[contains(@class, 'accept')]",
                "//input[contains(@class, 'accept')]",
                "//button[contains(text(), '» Create Area Category')]",
                "//input[contains(@value, '» Create Area Category')]"
            ]
            
            create_button = None
            for selector in button_selectors:
                try:
                    create_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✓ Found create button using: {selector}")
                    break
                except:
                    continue
            
            if not create_button:
                # Debug: show all buttons in the modal
                print("Debugging: Looking for all buttons in modal...")
                all_buttons = driver.find_elements(By.XPATH, "//button | //input[@type='button'] | //input[@type='submit']")
                print(f"Found {len(all_buttons)} buttons:")
                for i, btn in enumerate(all_buttons):
                    btn_text = btn.text or btn.get_attribute('value') or btn.get_attribute('title')
                    btn_id = btn.get_attribute('id')
                    btn_class = btn.get_attribute('class')
                    print(f"  Button {i+1}: '{btn_text}' (ID: {btn_id}, Class: {btn_class})")
                raise Exception("Could not find Create Area Category button")
            
            create_button.click()
            time.sleep(3)
            print("✓ Clicked Create Area Category button")
            print("✓ SINGLE AREA CATEGORY TEST COMPLETED!")
            
        except Exception as e:
            print(f"❌ Could not click Create button: {e}")
            
        print("\n🎉 SINGLE AREA TEST COMPLETE!")
        print("Check if the area was added to the project table.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        
    finally:
        if driver:
            print("\nBrowser remaining open for inspection...")
            input("Press Enter to close browser...")
            driver.quit()

if __name__ == "__main__":
    test_single_area_addition()
