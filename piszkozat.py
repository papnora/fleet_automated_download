import os
import time
import shutil
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from chrome_utils import close_existing_chrome, setup_browser
from file_utils import download
from panel_utils import ensure_search_panel_open, ensure_service_product_panel_open
from date_utils import fill_date_field

def Fleet():

    close_existing_chrome()

    driver, user_name =setup_browser()
 
    print("ITT NEM OK")

    print(f"Driver értéke: {driver}")

    wait = WebDriverWait(driver, 10)
    service_product_details = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@id='divServiceCategoryProductCost'][.//h5/strong[contains(text(), 'Service products details')]]")))
    driver.execute_script("arguments[0].scrollIntoView();", service_product_details) 
    time.sleep(1)  
    service_product_details.click()
    print("RÁKATTINTOTT A SPD")

    time.sleep(3)

    ensure_search_panel_open(driver, "ReportsIndexSearch_Collapse", "Reports")

    fill_date_field(driver, wait)
    

    ensure_service_product_panel_open(driver)
    print("SP OPEN OK")

    time.sleep(5)

    # Exportálás és letöltés
    all_downloaded = download(driver, wait, user_name, "exportExcelServiceProductsDetails")

    time.sleep(4)
        
    if all_downloaded:
        print("🔥Assets reports adatai sikeresen letöltve! 🔥")
    

    time.sleep(15)

    return driver

if __name__ == "__main__":
    driver = None
    try:
        driver = Fleet()#driver
      
    except Exception as e:
        print(f"Hiba történt: {e}")
        input("Nyomj Entert a kilépéshez...")
    finally:
        if driver:
            driver.quit()
