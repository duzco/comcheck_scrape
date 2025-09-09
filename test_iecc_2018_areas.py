#!/usr/bin/env python3
"""
Test IECC 2018 and open Select Area Category dropdown
Goal: Select IECC 2018 code and access area categories
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_iecc_2018_area_categories():
    """
    Select IECC 2018 and attempt to open area category dropdown
    """
    driver = None
    try:
        print("=== TESTING IECC 2018 AREA CATEGORIES ===")
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
            print("✓ Loading indicator disappeared")
        except:
            print("✓ No loading indicator found")
        
        print("Step 6: Selecting IECC 2018 from code dropdown...")
        code_dropdown = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "code"))
        )
        
        # Use Select class to properly select the option
        select = Select(code_dropdown)
        select.select_by_value("CEZ_IECC2018")  # From our extracted codes
        print("✓ Selected IECC 2018")
        
        print("Step 6.5: Waiting for page to update after code selection...")
        # Wait for page to reload/update after code selection
        time.sleep(2)
        
        # Check if there's a loading indicator after code change
        try:
            # Wait for any new loading indicator to appear and then disappear
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "loadingIndicator"))
            )
            print("✓ Detected loading after code selection, waiting for completion...")
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.ID, "loadingIndicator"))
            )
            print("✓ Page finished updating after code selection")
        except:
            print("✓ No additional loading detected, page should be ready")
        
        # Additional wait to ensure page is fully rendered
        time.sleep(3)
        print("✓ Page update wait completed")
        
        print("Step 7: Looking for INT. LIGHTING tab...")
        # The INT. LIGHTING tab should already be visible or active
        try:
            lighting_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'INT. LIGHTING') or contains(@title, 'Interior Lighting')]"))
            )
            lighting_tab.click()
            print("✓ Clicked INT. LIGHTING tab")
            time.sleep(2)
        except:
            print("✓ INT. LIGHTING tab already active or not found")
        
        print("Step 8: Debugging - looking for all available tabs...")
        # First, let's see what tabs are actually available
        try:
            all_links = driver.find_elements(By.TAG_NAME, "a")
            tab_links = [link for link in all_links if link.text and any(keyword in link.text.lower() for keyword in ['lighting', 'method', 'area', 'envelope', 'building'])]
            print(f"Found {len(tab_links)} potential tab links:")
            for i, link in enumerate(tab_links):
                print(f"  Tab {i+1}: '{link.text}' (href: {link.get_attribute('href')})")
        except:
            print("Could not enumerate tab links")
        
        print("Step 8.5: Looking for 'Interior Lighting Method and Areas' sub-tab...")
        try:
            # Try multiple variations of the tab text
            tab_variations = [
                "//a[contains(text(), 'Interior Lighting Method and Areas')]",
                "//a[contains(text(), 'Method and Areas')]", 
                "//a[contains(text(), 'Lighting Method')]",
                "//a[contains(text(), 'Building Envelope and Interior Lighting Areas')]",
                "//a[text()='Interior Lighting Method and Areas']"
            ]
            
            method_areas_tab = None
            for variation in tab_variations:
                try:
                    method_areas_tab = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, variation))
                    )
                    print(f"✓ Found tab using: {variation}")
                    break
                except:
                    continue
            
            if method_areas_tab:
                method_areas_tab.click()
                print("✓ Clicked 'Interior Lighting Method and Areas' tab")
                time.sleep(2)
            else:
                print("⚠️ Could not find the specific sub-tab")
        except Exception as e:
            print(f"⚠️ Error with sub-tab navigation: {e}")
        
        print("Step 9: Looking for 'Add Area Category' button by ID...")
        try:
            # First try the specific ID we found in dev tools
            add_area_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "addAreaCategory"))
            )
            print("✓ Found 'Add Area Category' button by ID")
            add_area_button.click()
            print("✓ Clicked 'Add Area Category' button")
            time.sleep(3)  # Wait for modal to open
        except Exception as e:
            print(f"❌ Could not find button by ID 'addAreaCategory': {e}")
            # Fallback to other methods
            try:
                # Try by class combination
                add_area_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.checkButton.addButton"))
                )
                print("✓ Found button by CSS class")
                add_area_button.click()
                print("✓ Clicked 'Add Area Category' button via CSS class")
                time.sleep(3)
            except Exception as e2:
                print(f"❌ Could not find button by class either: {e2}")
                # Debug: show all anchor tags with these classes
                try:
                    all_buttons = driver.find_elements(By.CSS_SELECTOR, "a[class*='addButton'], a[id*='add'], a[class*='checkButton']")
                    print(f"Found {len(all_buttons)} potential add buttons:")
                    for i, btn in enumerate(all_buttons):
                        btn_id = btn.get_attribute('id')
                        btn_class = btn.get_attribute('class')
                        btn_text = btn.text
                        print(f"  Button {i+1}: ID='{btn_id}', Class='{btn_class}', Text='{btn_text}'")
                except:
                    print("Could not debug button elements")
        
        print("Step 10: Looking for area category modal or dropdown...")
        # After clicking "Add Area Category", a modal should open with area category options
        try:
            # Try different possible selectors for the area category dropdown
            selectors_to_try = [
                "select[title*='Area Category']",
                "select[name*='area']",
                "select[id*='area']",
                "select[class*='area']",
                "//select[contains(text(), 'Select Area Category')]",
                "//select//option[contains(text(), 'Select Area Category')]/.."
            ]
            
            area_dropdown = None
            for selector in selectors_to_try:
                try:
                    if selector.startswith("//"):
                        # XPath selector
                        area_dropdown = driver.find_element(By.XPATH, selector)
                    else:
                        # CSS selector
                        area_dropdown = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✓ Found area dropdown using selector: {selector}")
                    break
                except:
                    continue
            
            if not area_dropdown:
                # If specific selectors don't work, find all select elements and inspect them
                print("Searching for all select elements on page...")
                all_selects = driver.find_elements(By.TAG_NAME, "select")
                print(f"Found {len(all_selects)} select elements")
                
                for i, select_elem in enumerate(all_selects):
                    try:
                        # Get the first option text to identify the dropdown
                        options = select_elem.find_elements(By.TAG_NAME, "option")
                        if options:
                            first_option_text = options[0].text.strip()
                            print(f"  Select {i+1}: First option = '{first_option_text}'")
                            
                            # Look for area category related text
                            if any(keyword in first_option_text.lower() for keyword in ['select area', 'area category', 'category']):
                                area_dropdown = select_elem
                                print(f"✓ Found area category dropdown (Select {i+1})")
                                break
                    except:
                        print(f"  Select {i+1}: Could not read options")
            
            if area_dropdown:
                print("Step 9: Attempting to open area category dropdown...")
                area_dropdown.click()
                time.sleep(2)
                
                print("Step 11: Reading area category options...")
                options = area_dropdown.find_elements(By.TAG_NAME, "option")
                print(f"Found {len(options)} area category options:")
                print("=" * 50)
                
                for i, option in enumerate(options[:10], 1):  # Show first 10
                    text = option.text.strip()
                    value = option.get_attribute('value')
                    if text:  # Skip empty options
                        print(f"{i:2d}. {text:<35} (value: {value})")
                
                if len(options) > 10:
                    print(f"... and {len(options) - 10} more options")
                
                print("=" * 50)
                
            else:
                print("❌ Could not find area category dropdown")
                print("Current page source snippet:")
                # Print a portion of page source for debugging
                print(driver.page_source[:2000])
                
        except Exception as e:
            print(f"❌ Error finding area category dropdown: {e}")
        
        print("\n=== TEST COMPLETED ===")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        if driver:
            print(f"Current URL: {driver.current_url}")
            print(f"Page title: {driver.title}")
        
    finally:
        if driver:
            print("\nBrowser remaining open for inspection...")
            input("Press Enter to close browser...")
            driver.quit()

if __name__ == "__main__":
    test_iecc_2018_area_categories()
