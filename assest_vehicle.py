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

def close_existing_chrome():
    """Bezárja az összes futó Chrome böngészőt Windows rendszeren."""
    try:
        os.system("taskkill /IM chrome.exe /F")  
        print("Minden Chrome böngészőt bezártam.")
    except Exception as e:
        print(f"Hiba történt a Chrome bezárásakor: {e}")

def wait_for_download(download_path, timeout=60):
    end_time = time.time() + timeout

    while time.time() < end_time:
        files = os.listdir(download_path)
        if any(file.endswith(".xls") or file.endswith(".xlsx") for file in files):
            print("✅ Fájl letöltve!")
            return True
        time.sleep(2)
    
    print("⏳ Időtúllépés: A fájl nem töltődött le időben.")
    return False

def move_latest_file(source, target):
    files = [os.path.join(source, f) for f in os.listdir(source) if f.endswith((".xls", ".xlsx"))]
    if files:
        latest_file = max(files, key=os.path.getctime)  
        shutil.move(latest_file, os.path.join(target, os.path.basename(latest_file)))
        print(f"Fájl áthelyezve: {latest_file} → {target}")

def ensure_service_product_panel_open(driver):
    """Ellenőrzi és szükség esetén lenyitja a Service paroduct details panelt."""
    print("ide bejön")
    try:
        wait = WebDriverWait(driver, 10)
        collapse_serviceProductDetails = wait.until(EC.presence_of_element_located((By.XPATH, "//div[h3[contains(text(), 'Vehicle in service')]]//button[@id='VehicleService_Collapse']/i")))
        icon_serviceProductDetails = collapse_serviceProductDetails.get_attribute("class")

        if "fa-plus" in icon_serviceProductDetails:
            print("A Vehicle in Service panel NINCS LENYITVA.")
            collapse_serviceProductDetails.click()
            time.sleep(3)  
            print("A Vehicle in Service panelt LENYITOTTAM.")
        elif "fa-minus" in icon_serviceProductDetails:
            print("A Vehicle in Service panel LE VAN LENYITVA.")
    except Exception as e:
        print(f"Hiba történt a Vehicle in Service panel ellenőrzésekor: {e}")

def downloadFleetData():
    close_existing_chrome()
    user_name = os.environ.get("USERNAME") or os.getlogin()
    print("A Fleet KPI adatok letöltése folyamatban van, kérlek várj.")
    print(f"USERNAME: {user_name}")

    target_folder = r"\\hucbrfs\Coolbridge\COMMON\ERP\BUSINESS_INTELLIGENCE\source_raw\fleet_management"
    download_path = f"C:\\Users\\{user_name}\\Downloads"

    chrome_profile_path = f"C:\\Users\\{user_name}\\AppData\\Local\\Google\\Chrome\\User Data"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Újabb headless mód
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("profile-directory=Default")  
    options.add_argument("--allow-running-insecure-content")  
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://tata.fleetmanager.guentner.local/")  
    options.add_experimental_option("prefs", {
   # "download.default_directory": download_path.replace("\\", "/"),
  #  "download.prompt_for_download": False,
   # "download.directory_upgrade": True,
    "safebrowsing.enabled": True,  
   # "safebrowsing.disable_download_protection": True  # letoltesvedelem
    })

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

    manual_vehicle_service = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'list-group-item') and contains(@onclick, 'ManualVehicleService')][.//h5/strong[text()='Manual vehicle service']]"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", manual_vehicle_service) 
    time.sleep(1)  
    manual_vehicle_service.click()
   
#eddig ok
    time.sleep(3)

    collapse_Reports = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#ReportsIndexSearch_Collapse i")))
    print("megtaláltam a collapse-t")

    icon_Reports = collapse_Reports.get_attribute("class")

    if "fa-plus" in icon_Reports:
        print("A keresési panel NINCS LENYITVA.")
        collapse_Reports.click() 
        print("A keresési panelt LENYITOTTAM.")
    elif "fa-minus" in icon_Reports:
        print("A keresési panel LE VAN LENYITVA.")

    time.sleep(4)

    #Date: current
    today = datetime.today()
    day_today = today.strftime("%d")  # (DD)
    month_today = today.strftime("%m")  # (MM)
    year_today = today.strftime("%Y")  # (YYYY)

    print(f"Aktuális dátum: {day_today}.{month_today}.{year_today}")

    # Date 01.08.2022 
    custom_date = "01.08.2022"
    day_custom = custom_date.split('.')[0]  # (DD)
    month_custom = custom_date.split('.')[1]  # (MM)
    year_custom = custom_date.split('.')[2]  #(YYYY)

    print(f"A kiválasztott dátum: {day_custom}.{month_custom}.{year_custom}")

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
    start_date_input.send_keys(day_custom)  
    start_date_input.send_keys(Keys.TAB) 
    time.sleep(2)

    start_date_input.send_keys(Keys.BACKSPACE * 2)  
    start_date_input.send_keys(month_custom)  
    start_date_input.send_keys(Keys.TAB)  
    time.sleep(2)

    start_date_input.send_keys(Keys.BACKSPACE * 4)  
    start_date_input.send_keys(year_custom)  
    start_date_input.send_keys(Keys.ENTER) 
    time.sleep(2)


    #End Date - endDateWrapp
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
    
    search_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='box-footer']//button[contains(text(), 'Search')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
    time.sleep(1)  
    search_button.click()
    time.sleep(2)

    ensure_service_product_panel_open(driver)  

    all_downloaded = True 

    time.sleep(5)

    try:
        # Stale element error prevention
        export_VehicleServiceBTN = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "exportExcel"))
        )
        wait.until(EC.element_to_be_clickable((By.ID, "exportExcel")))

        print("🔍 Megtalált elem HTML kódja:")
        print(export_VehicleServiceBTN.get_attribute("outerHTML"))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", export_VehicleServiceBTN)
        time.sleep(1)  

        # JavaScript if above is error
        driver.execute_script("arguments[0].click();", export_VehicleServiceBTN)
        print("✅ Rákattintottam a Service PD Export Excel gombjára.")

        time.sleep(15)  
        
        if wait_for_download(download_path):
            move_latest_file(download_path, target_folder)
        else:
            all_downloaded = False  

        ensure_service_product_panel_open(driver)

    except Exception as e:
        print(f"❌ Hiba történt az Export Excel gombnál: {e}")
    all_downloaded = False

    time.sleep(4)
        
    if all_downloaded:
        print("🔥Assets reports adatai sikeresen letöltve! 🔥")
    

    time.sleep(15)

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
