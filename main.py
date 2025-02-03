
from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
def downloadFleetData():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)           
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://tata.fleetmanager.guentner.local/")
    
    wait = WebDriverWait(driver, 5)
    sleep(5)
    driver.refresh()
    sleep(2)
    # Reports 
    try:
        reports_menu = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Reports']/ancestor::a")))
        reports_menu.click()
    except:
        print("Selenium nem tud kattintani, próbálkozás JavaScript-tel...")
        reports_menu = driver.find_element(By.XPATH, "//span[text()='Reports']/ancestor::a")
        driver.execute_script("arguments[0].click();", reports_menu)
    sleep(2)
    reports_sub_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[text()='Reports'])[2]/parent::a")))
    reports_sub_menu.click()
    sleep(2)
    fuel_supplier_summary = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='divFuelSupplierSummary']")))
    fuel_supplier_summary.click()
    sleep(5)
    collapse_button = wait.until(EC.element_to_be_clickable((By.ID, "ReportsIndexSearch_Collapse")))
    collapse_button.click()
    
    sleep(7)
    # 3 hónappal ezelőtti dátum kiszámítása
    three_months_ago = datetime.today() - timedelta(days=90)
    day = three_months_ago.strftime("%d")  # Nap (DD)
    month = three_months_ago.strftime("%m")  # Hónap (MM)
    year = three_months_ago.strftime("%Y")  # Év (YYYY)
    # Start Date mező (látható input mező)
    start_date_input = wait.until(EC.element_to_be_clickable((By.ID, "startDateWrapp")))
    start_date_input.click()  # Kattintás a mezőbe
    sleep(2)
   # Shift+Tab két alkalommal történő használata, hogy visszalépj
    actions = ActionChains(driver)
    actions.key_down(Keys.SHIFT)  # Nyomd le a Shift billentyűt
    actions.send_keys(Keys.TAB)  # Először Shift+Tab
    actions.send_keys(Keys.TAB)  # Másodszor Shift+Tab
    actions.key_up(Keys.SHIFT)  # Engedd fel a Shift billentyűt
    actions.perform()
    sleep(2)
    

# Nap beírása
    start_date_input.send_keys(Keys.BACKSPACE * 2)  # Töröljük az előző értéket
    start_date_input.send_keys(day)  
    start_date_input.send_keys(Keys.TAB)  # Tabulátor a hónaphoz
    
    sleep(2)
    # Hónap beírása
    start_date_input.send_keys(Keys.BACKSPACE * 2)  
    start_date_input.send_keys(month)  
    start_date_input.send_keys(Keys.TAB)  # Tabulátor az évhez
    sleep(2)
    # Év beírása
    start_date_input.send_keys(Keys.BACKSPACE * 4)  
    start_date_input.send_keys(year)  
    start_date_input.send_keys(Keys.ENTER)  # Enter a változások mentéséhez
    sleep(2)

    
   
    sleep(2)
    return driver
if __name__ == "__main__":
    driver = None
    try:
        driver = downloadFleetData()
      
    except Exception as e:
        print(f"Hiba történt: {e}")
        input("Nyomj Entert a kilépéshez...")
    finally:
        if driver:
            driver.quit()
