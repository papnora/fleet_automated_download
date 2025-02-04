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


# 🔹 Letöltés figyelése
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
   # user_name = os.environ.get("USERNAME") or os.getlogin()
    #print(user_name)

    target_folder = r"\\hucbrfs\Coolbridge\COMMON\ERP\BUSINESS_INTELLIGENCE\source_raw\fleet_management"
    download_path = "C:\\Users\\npap\\Downloads"

    #chrome_profile_path = f"C:\\Users\\{user_name}\\AppData\\Local\\Google\\Chrome\\User Data"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Újabb headless mód
    #options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("profile-directory=Default")  # Ha más profilnév, cseréld ki!
    options.add_argument("--allow-running-insecure-content")  # Allow insecure content
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://tata.fleetmanager.guentner.local/")  # site's domain
    options.add_experimental_option("prefs", {
    "download.default_directory": download_path.replace("\\", "/"),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,  # Kapcsold be a biztonságos böngészést
    "safebrowsing.disable_download_protection": True  # Tiltsd le a letöltésvédelmet
    })


    # WebDriver elindítása
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    time.sleep(5)
    driver.refresh()
    time.sleep(2)
    driver.get("http://tata.fleetmanager.guentner.local/")
    time.sleep(2)
    print("Aktuális oldal címe:", driver.title)


    #------------


    #------------


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

    collapse_icon = driver.find_element(By.CSS_SELECTOR, "#ReportsIndexSearch_Collapse i")
    #collapse_button.click()
   # Lekérdezzük a class attribútumát
    icon_class = collapse_icon.get_attribute("class")

    # Ellenőrizzük, hogy fa-plus vagy fa-minus van benne
    if "fa-plus" in icon_class:
        print("A keresési panel NINCS LENYITVA.")
        collapse_icon.click()  # Ha nincs lenyitva, kattintunk rá
    elif "fa-minus" in icon_class:
        print("A keresési panel LE VAN LENYITVA.")
       

    time.sleep(4)

    #Jelenlegi dátum
    today = datetime.today()
    day_today = today.strftime("%d")  # Nap (DD)
    month_today = today.strftime("%m")  # Hónap (MM)
    year_today = today.strftime("%Y")  # Év (YYYY)

    print(f"Current date: {day_today}.{month_today}.{year_today}")

    # 3 hónappal ezelőtti dátum kiszámítása
    three_months_ago = datetime.today() - timedelta(days=90)
    day_3M = three_months_ago.strftime("%d")  # Nap (DD)
    month_3M = three_months_ago.strftime("%m")  # Hónap (MM)
    year_3M = three_months_ago.strftime("%Y")  # Év (YYYY)

    print(f"Date of 3 months ago: {day_3M}.{month_3M}.{year_3M}")

    # Start Date mező (látható input mező)
    start_date_input = wait.until(EC.element_to_be_clickable((By.ID, "startDateWrapp")))
    start_date_input.click()  # Kattintás a mezőbe
    time.sleep(2)

   # Shift+Tab két alkalommal történő használata, hogy visszalépj
    actions = ActionChains(driver)
    actions.key_down(Keys.SHIFT)  # Nyomd le a Shift billentyűt
    actions.send_keys(Keys.TAB)  # Először Shift+Tab
    actions.send_keys(Keys.TAB)  # Másodszor Shift+Tab
    actions.key_up(Keys.SHIFT)  # Engedd fel a Shift billentyűt
    actions.perform()
    time.sleep(2)
    

    # Nap beírása
    start_date_input.send_keys(Keys.BACKSPACE * 2)  # Töröljük az előző értéket
    start_date_input.send_keys(day_3M)  
    start_date_input.send_keys(Keys.TAB)  # Tabulátor a hónaphoz
    time.sleep(2)

    # Hónap beírása
    start_date_input.send_keys(Keys.BACKSPACE * 2)  
    start_date_input.send_keys(month_3M)  
    start_date_input.send_keys(Keys.TAB)  # Tabulátor az évhez
    time.sleep(2)

    # Év beírása
    start_date_input.send_keys(Keys.BACKSPACE * 4)  
    start_date_input.send_keys(year_3M)  
    start_date_input.send_keys(Keys.ENTER)  # Enter a változások mentéséhez
    time.sleep(2)


    #End Date mező - endDateWrapp
    end_date_input = wait.until(EC.element_to_be_clickable((By.ID, "endDateWrapp")))
    end_date_input.click()  # Kattintás a mezőbe
    time.sleep(2)

   # Shift+Tab két alkalommal történő használata, hogy visszalépj
    actions = ActionChains(driver)
    actions.key_down(Keys.SHIFT)  # Nyomd le a Shift billentyűt
    actions.send_keys(Keys.TAB)  # Először Shift+Tab
    actions.send_keys(Keys.TAB)  # Másodszor Shift+Tab
    actions.key_up(Keys.SHIFT)  # Engedd fel a Shift billentyűt
    actions.perform()
    time.sleep(2)


    # Nap beírása
    end_date_input.send_keys(Keys.BACKSPACE * 2)  # Töröljük az előző értéket
    end_date_input.send_keys(day_today)  
    end_date_input.send_keys(Keys.TAB)  # Tabulátor a hónaphoz
    time.sleep(2)

    # Hónap beírása
    end_date_input.send_keys(Keys.BACKSPACE * 2)  
    end_date_input.send_keys(month_today)  
    end_date_input.send_keys(Keys.TAB)  # Tabulátor az évhez
    time.sleep(2)

    # Év beírása
    end_date_input.send_keys(Keys.BACKSPACE * 4)  
    end_date_input.send_keys(year_today)  
    end_date_input.send_keys(Keys.ENTER)  # Enter a változások mentéséhez
    time.sleep(3)
    
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='box-footer']//button[contains(text(), 'Search')]")))
    search_button.click()
    time.sleep(2)

    # Táblázat, sorok
    table_Suppliers = driver.find_element(By.ID, "CostPerSupplierTable_wrapper")
    rows = table_Suppliers.find_elements(By.TAG_NAME, "tr")

    # Végigmegyünk a sorokon és megkeressük a megfelelőt
    for row in rows:
        if "Guentner internal Gas supplier" in row.text:
            # Ha megtaláltuk a megfelelő sort, keressük meg benne a Details gombot
            button = row.find_element(By.TAG_NAME, "button")
            button.click()
            break  # Ha megtaláltuk és rákattintottunk, kilépünk a ciklusból
    time.sleep(5)

    #table_SpecificSupplier = driver.find_element(By.ID, "divCostPerSupplier")
    #--
    # Megkeressük az összes box-header div-et
    box_headers = driver.find_elements(By.CLASS_NAME, "box-header")

    # Végigmegyünk rajtuk, hogy megtaláljuk a megfelelőt
    for box in box_headers:
        if "Guentner internal Gas supplier" in box.text:
            # Megkeressük benne az "Export Excel" gombot
            export_button = box.find_element(By.XPATH, ".//button[contains(text(), 'Export Excel')]")
            export_button.click()
            break  # Ha megtaláltuk és kattintottunk, kilépünk a ciklusból

    time.sleep(15)

    wait_for_download(download_path)
    move_latest_file(download_path, target_folder)

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
