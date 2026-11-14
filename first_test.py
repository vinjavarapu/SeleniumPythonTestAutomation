import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_google_search_interaction():
    driver = webdriver.Chrome()
    
    try:
        driver.get("https://www.google.com")
        driver.maximize_window()
        
        # 1. Locate the Google Search input field
        search_box = driver.find_element(By.NAME, "q")
        
        # 2. Type text into the field
        search_box.send_keys("Selenium")
        time.sleep(1) 
        
        # 3. Press Enter
        search_box.send_keys(Keys.RETURN)
        
        # 4. Wait for results page to load
        time.sleep(3)
        
        # 5. Bulletproof Assertion: Check the URL instead of the title!
        assert "selenium" in driver.current_url.lower()
        print("\nSearch interaction test passed perfectly!")
        
    finally:
        driver.quit()
