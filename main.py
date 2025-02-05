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


def wait_for_download(download_path, timeout=60):
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = os.listdir(download_path)
        if any(file.endswith(".xls") or file.endswith(".xlsx") for file in files):
            print("Fájl letöltve!")
            return True
        time.sleep(2)
    print("Időtúllépés: A fájl nem töltődött le időben.")
    return False

def move_latest_file(source, target):
    files = [os.path.join(source, f) for f in os.listdir(source) if f.endswith((".xls", ".xlsx"))]
    if files:
        latest_file = max(files, key=os.path.getctime)  # Legutóbb letöltött fájl
        shutil.move(latest_file, os.path.join(target, os.path.basename(latest_file)))
        print(f"Fájl áthelyezve: {latest_file} → {target}")

def downloadFleetData():
    user_name = os.environ.get("USERNAME") or os.getlogin()
    print(user_name)

    target_folder = r"\\hucbrfs\Coolbridge\COMMON\ERP\BUSINESS_INTELLIGENCE\source_raw\fleet_management"
    download_path = "C:\\Users\\npap\\Downloads"

    chrome_profile_path = f"C:\\Users\\{user_name}\\AppData\\Local\\Google\\Chrome\\User Data"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Újabb headless mód
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("profile-directory=Default")  # Ha más profilnév, cseréld ki!
    options.add_argument("--allow-running-insecure-content")  # Allow insecure content
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://tata.fleetmanager.guentner.local/")  # site's domain
    options.add_experimental_option("prefs", {
   # "download.default_directory": download_path.replace("\\", "/"),
  #  "download.prompt_for_download": False,
   # "download.directory_upgrade": True,
    "safebrowsing.enabled": True,  # Kapcsold be a biztonságos böngészést
   # "safebrowsing.disable_download_protection": True  # letoltesvedelem
    })


    # WebDriver elindítása
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get("http://tata.fleetmanager.guentner.local/")
    wait = WebDriverWait(driver, 5)
    time.sleep(5)
    
    try:
        lang_switch = wait.until(EC.element_to_be_clickable((By.ID, "enCulture")))
        lang_switch.click()
    except Exception as e:
         print("Hiba történt:", e)


    time.sleep(5)
    driver.refresh()
    time.sleep(2)

    # Reports 
    try:
        reports_menu = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Reports']/ancestor::a")))
        reports_menu.click()
    except:
        print("Selenium nem tud kattintani, próbálkozás JavaScript-tel...")
        reports_menu = driver.find_element(By.XPATH, "//span[text()='Reports']/ancestor::a")
        driver.execute_script("arguments[0].click();", reports_menu)

    time.sleep(2)

    reports_sub_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[text()='Reports'])[2]/parent::a")))
    reports_sub_menu.click()

    time.sleep(2)

    fuel_supplier_summary = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='divFuelSupplierSummary']")))
    fuel_supplier_summary.click()

    time.sleep(3)

    collapse_button = wait.until(EC.element_to_be_clickable((By.ID, "ReportsIndexSearch_Collapse")))

    collapse_Reports = driver.find_element(By.CSS_SELECTOR, "#ReportsIndexSearch_Collapse i")

    icon_Reports = collapse_Reports.get_attribute("class")

    if "fa-plus" in icon_Reports:
        print("A keresési panel NINCS LENYITVA.")
        collapse_Reports.click() 
        print("A Fuel supplier panelt LENYITOTTAM.")
    elif "fa-minus" in icon_Reports:
        print("A keresési panel LE VAN LENYITVA.")
       

    time.sleep(4)

    #Jelenlegi dátum
    today = datetime.today()
    day_today = today.strftime("%d")  # (DD)
    month_today = today.strftime("%m")  # (MM)
    year_today = today.strftime("%Y")  # (YYYY)

    print(f"Current date: {day_today}.{month_today}.{year_today}")

    # 3 hónappal ezelőtti dátum kiszámítása
    three_months_ago = datetime.today() - timedelta(days=90)
    day_3M = three_months_ago.strftime("%d")  # (DD)
    month_3M = three_months_ago.strftime("%m")  # (MM)
    year_3M = three_months_ago.strftime("%Y")  # (YYYY)

    print(f"Date of 3 months ago: {day_3M}.{month_3M}.{year_3M}")

    # Start Date 
    start_date_input = wait.until(EC.element_to_be_clickable((By.ID, "startDateWrapp")))
    start_date_input.click()  
    time.sleep(2)

   # Shift+Tab 2X FOR BACKSTEP
    actions = ActionChains(driver)
    actions.key_down(Keys.SHIFT)  
    actions.send_keys(Keys.TAB)  
    actions.send_keys(Keys.TAB)  
    actions.key_up(Keys.SHIFT)  
    actions.perform()
    time.sleep(2)
    

    start_date_input.send_keys(Keys.BACKSPACE * 2)  
    start_date_input.send_keys(day_3M)  
    start_date_input.send_keys(Keys.TAB) 
    time.sleep(2)

    start_date_input.send_keys(Keys.BACKSPACE * 2)  
    start_date_input.send_keys(month_3M)  
    start_date_input.send_keys(Keys.TAB)  
    time.sleep(2)

    start_date_input.send_keys(Keys.BACKSPACE * 4)  
    start_date_input.send_keys(year_3M)  
    start_date_input.send_keys(Keys.ENTER) 
    time.sleep(2)


    #End Date mező - endDateWrapp
    end_date_input = wait.until(EC.element_to_be_clickable((By.ID, "endDateWrapp")))
    end_date_input.click()  
    time.sleep(2)

    actions = ActionChains(driver)
    actions.key_down(Keys.SHIFT)  
    actions.send_keys(Keys.TAB)  
    actions.send_keys(Keys.TAB)  
    actions.key_up(Keys.SHIFT)  
    actions.perform()
    time.sleep(2)

    end_date_input.send_keys(Keys.BACKSPACE * 2) 
    end_date_input.send_keys(day_today)  
    end_date_input.send_keys(Keys.TAB) 
    time.sleep(2)

    end_date_input.send_keys(Keys.BACKSPACE * 2)  
    end_date_input.send_keys(month_today)  
    end_date_input.send_keys(Keys.TAB)  
    time.sleep(2)

    end_date_input.send_keys(Keys.BACKSPACE * 4)  
    end_date_input.send_keys(year_today)  
    end_date_input.send_keys(Keys.ENTER)  
    time.sleep(3)
    
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='box-footer']//button[contains(text(), 'Search')]")))
    search_button.click()
    time.sleep(2)

    # Tables & Rows - Guentner internal Gas supplier
    table_Suppliers = driver.find_element(By.ID, "CostPerSupplierTable_wrapper")
    rows = table_Suppliers.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        if "Guentner internal Gas supplier" in row.text:
            button = row.find_element(By.TAG_NAME, "button")
            button.click()
            break  
    time.sleep(5)


    box_headers = driver.find_elements(By.CLASS_NAME, "box-header")

    for box in box_headers:
        if "Guentner internal Gas supplier" in box.text:
            export_button = box.find_element(By.XPATH, ".//button[contains(text(), 'Export Excel')]")
            export_button.click()
            break  

    time.sleep(15)

    wait_for_download(download_path)
    move_latest_file(download_path, target_folder)

    #többi letöltése

    #collapse_fuelSupplier = driver.find_element(By.CSS_SELECTOR, "#CostPerSupplier_Collapse i")
    collapse_fuelSupplier = driver.find_element(By.XPATH, "//div[h3[contains(text(), 'Fuel supplier summary')]]//button[@id='CostPerSupplier_Collapse']/i")


    icon_fuelSupplier = collapse_fuelSupplier.get_attribute("class")

    if "fa-plus" in icon_fuelSupplier:
        print("A Fuel supplier panel NINCS LENYITVA.")
        collapse_fuelSupplier.click() 
        print("A Fuel supplier panelt LENYITOTTAM.")
    elif "fa-minus" in icon_fuelSupplier:
        print("A Fuel supplier panel LE VAN LENYITVA.")


# Tables & Rows -  Shell
    table_Suppliers = driver.find_element(By.ID, "CostPerSupplierTable_wrapper")
    rows = table_Suppliers.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        if "MOL" in row.text:
            button = row.find_element(By.TAG_NAME, "button")
            button.click()
            break  
    time.sleep(5)


    box_headers = driver.find_elements(By.CLASS_NAME, "box-header")

    for box in box_headers:
        if "MOL" in box.text:
            export_button = box.find_element(By.XPATH, ".//button[contains(text(), 'Export Excel')]")
            export_button.click()
            break  

    time.sleep(15)

    wait_for_download(download_path)
    move_latest_file(download_path, target_folder)


    if "fa-plus" in icon_fuelSupplier:
        print("A Fuel supplier panel NINCS LENYITVA.")
        icon_fuelSupplier.click() 
        print("A Fuel supplier panelt LENYITOTTAM.")
    elif "fa-minus" in icon_fuelSupplier:
        print("A Fuel supplier panel LE VAN LENYITVA.")


# Tables & Rows -  Shell
    table_Suppliers = driver.find_element(By.ID, "CostPerSupplierTable_wrapper")
    rows = table_Suppliers.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        if "Shell Hungary Kft." in row.text:
            button = row.find_element(By.TAG_NAME, "button")
            button.click()
            break  
    time.sleep(5)


    box_headers = driver.find_elements(By.CLASS_NAME, "box-header")

    for box in box_headers:
        if "Shell Hungary Kft." in box.text:
            export_button = box.find_element(By.XPATH, ".//button[contains(text(), 'Export Excel')]")
            export_button.click()
            break  

    time.sleep(15)

    wait_for_download(download_path)
    move_latest_file(download_path, target_folder)




    #

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
