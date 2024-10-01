from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_product(driver, product_name):
    try:
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/nav/div[3]/div/div[2]/div[1]/div/div/div[2]/div/input'))
        )
        print(f"Search field found")# for product: {product_name}.")
        search_field.clear()  # Clear previous text
        search_field.send_keys(product_name)
        print(f"Search field value set to: {product_name}")
        time.sleep(2)  # Wait to observe the text input

        # Click the search button
        search_button_xpath = '/html/body/div[1]/header/nav/div[3]/div/div[2]/div[1]/div/div/div[2]/div/button'
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, search_button_xpath))
        )
        #print("Search button HTML:")
        #print(driver.execute_script("return arguments[0].outerHTML;", search_button))
        
        search_button.click()
        print("Clicked search button.\n")
        time.sleep(3)  # Wait time to observe click action

        # Allow more time for the search results to load
        time.sleep(3)  # Adjust the sleep time as needed

        # Find the search results using XPath
        results_xpath = '/html/body/main/div[2]/div/div[1]/ul//li//article//h3[@class="item-heading"]'
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, results_xpath))
        )
        if results:
            print(f"Found {len(results)} items for '{product_name}'.\n")
            for result in results:
                print(result.text)  # Print out the name of each item
            return True, len(results)
        else:
            print(f"No results found for '{product_name}'.")
            return False, 0
    except Exception as e:
        print(f"No results found for '{product_name}'.")
        return True, 0

def main():
    # Set Chrome options to start maximized
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Initialize the Chrome driver with options
    driver = webdriver.Chrome(options=options)

    # Open the H&M website
    driver.get("https://www2.hm.com/en_in/index.html")

    # Accept cookies
    try:
        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        )
        accept_cookies_button.click()
        print("Accepted cookies.")
    except Exception as e:
        print(f"Cookies acceptance button not found. Exception: {e}")

    # Read product names from file
    with open('products.txt', 'r') as file:
        products = [line.strip() for line in file]

    # Initialize report variables
    total_tests = 0
    defects_raised = 0
    tests_passed = 0
    tests_failed = 0

    for product in products:
        total_tests += 1
        success, num_items = search_product(driver, product)
        if success:
            tests_passed += 1
        else:
            tests_failed += 1
            defects_raised += 1  # Assuming each failure is considered a defect

        time.sleep(2)  # Wait before starting the next search

        # Navigate back to the main page
        driver.get("https://www2.hm.com/en_in/index.html")
        time.sleep(2)  # Allow time for the page to load

    # Close the browser
    driver.quit()

    # Print test report
    print("\nTest Report")
    print("-----------")
    print(f"Total test cases executed: {total_tests}")
    print(f"Total defects raised: {defects_raised}")
    print(f"Total test cases passed: {tests_passed}")
    print(f"Total test cases failed: {tests_failed}")

if __name__ == "__main__":
    main()
