import os
import time
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


def setup_browser():
    """Elindítja és beállítja a Chrome böngészőt, majd megnyitja a szükséges menüket."""
    user_name = os.environ.get("USERNAME") or os.getlogin()
    print("A Fleet KPI adatok letöltése folyamatban van, kérlek várj.")
    print(f"USERNAME: {user_name}")

    chrome_profile_path = f"C:\\Users\\{user_name}\\AppData\\Local\\Google\\Chrome\\User Data"
    
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Újabb headless mód
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("profile-directory=Default")
    options.add_argument("--allow-running-insecure-content")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://tata.fleetmanager.guentner.local/")
    options.add_experimental_option("prefs", {"safebrowsing.enabled": True})
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://tata.fleetmanager.guentner.local/")
    wait = WebDriverWait(driver, 5)
    time.sleep(5)
    
    try:
        lang_switch = wait.until(EC.element_to_be_clickable((By.ID, "enCulture")))
        lang_switch.click()
        print("Nyelvváltás OK")
    except Exception as e:
        print("Hiba történt a nyelvváltáskor:", e)
    
    time.sleep(5)
    
    # Reports menü megnyitása
    try:
        reports_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Reports']/ancestor::a")))
        reports_menu.click()
    except:
        print("Selenium nem tud kattintani, próbálkozás JavaScript-tel...")
        reports_menu = driver.find_element(By.XPATH, "//span[text()='Reports']/ancestor::a")
        driver.execute_script("arguments[0].click();", reports_menu)
    
    time.sleep(2)
    
    reports_sub_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[text()='Reports'])[2]/parent::a")))
    reports_sub_menu.click()
    
    time.sleep(2)
    print("ITT OKÉ")
    return driver, user_name

