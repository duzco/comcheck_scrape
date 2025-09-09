import time
import yaml
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_comcheck_web(driver):
    """
    Clicks the 'Start COMcheck-Web' button on the initial landing page.
    """
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "startButton"))
    )
    start_button.click()
    print("Clicked the 'Start COMcheck-Web' button.")

def click_code_dropdown(driver):
    """
    Finds and clicks the 'Code:' dropdown to open it.
    """
    code_dropdown_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "code"))
    )
    code_dropdown_element.click()
    print("Successfully clicked the 'Code:' dropdown.")

def navigate_to_lighting_section(driver):
    """
    Navigates to the Interior Lighting section of the project.
    """
    # This function will contain the Selenium logic to:
    # 1. Find and click the "INT. LIGHTING" main tab.
    # 2. The "Interior Lighting Method and Areas" sub-tab is usually
    #    selected by default, but we can add a click here if needed.
    pass

def add_area_category(driver):
    """
    Clicks the 'Add Area Category' button to prepare for adding a new space.
    """
    # This function will contain the Selenium logic to:
    # 1. Find and click the "Add Area Category" button.
    pass

def scrape_space_types_from_modal(driver):
    """
    Scrapes all space categories and subcategories from the 'Create Area Category' modal.

    This function will be called once the modal is open. It will programmatically
    click each category radio button to reveal its subcategory dropdown, then read
    and store all the options.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        dict: A dictionary where keys are the main categories and values are lists
              of subcategory strings.
    """
    # This function will:
    # 1. Find all the radio button elements for the main categories.
    # 2. Iterate through each radio button:
    #    a. Get the text label of the category (e.g., "Common Space Types").
    #    b. Click the radio button.
    #    c. Find the corresponding <select> dropdown element.
    #    d. Get all the <option> text from that dropdown.
    #    e. Store this in a dictionary.
    # 3. Return the completed dictionary.
    pass


def add_all_space_types(driver, space_types):
    """
    Iterates through all space types and adds them to the project.

    Args:
        driver: The Selenium WebDriver instance.
        space_types (dict): The dictionary of space types from the YAML file.
    """
    # This function will implement the main automation loop:
    #
    # 1. The modal should already be open from the `add_area_category` call.
    #
    # 2. Loop through each category (e.g., "Common Space Types") and its
    #    list of subcategories from the `space_types` data.
    #
    # 3. For each subcategory:
    #    a. Find and click the radio button for the main category.
    #    b. Find the dropdown menu associated with that category.
    #    c. Select the subcategory name from the dropdown.
    #    d. Find and click the "Create Area Category" button.
    #    e. Wait for the modal to close.
    #    f. Call `add_area_category(driver)` again to reopen the modal
    #       for the next iteration (unless it's the last item).
    #
    pass


def main():
    """
    Main function to orchestrate the CXL generation process.
    """
    driver = None
    try:
        print("Initializing WebDriver...")
        service = ChromeService()
        driver = webdriver.Chrome(service=service)
        
        # 2. Navigate to the COMcheck-Web URL.
        url = "https://energycode.pnl.gov/COMcheckWeb/"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Store the original window handle
        original_window = driver.current_window_handle
        
        # --- Click the Start button on the landing page ---
        start_comcheck_web(driver)

        # --- Switch to the new window ---
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        # --- DIAGNOSTIC STEP ---
        print("SUCCESS: Switched to the new application window.")
        
        # We will stop here for this test. The goal is to see the print statement.

    except Exception as e:
        print(f"\nAN ERROR OCCURRED: {e}")
        if driver:
            print("\nDumping page source for debugging:")
            # We print the source of whichever window the driver is currently focused on
            print(driver.page_source)
    
    finally:
        print("\nScript finished. The browser will remain open.")
        input("Press Enter in this terminal to close the browser...")


if __name__ == '__main__':
    main()
