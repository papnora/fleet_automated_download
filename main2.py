import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def close_existing_chrome():
    """Bezárja az összes futó Chrome böngészőt Windows rendszeren."""
    os.system("taskkill /IM chrome.exe /F")
    print("Minden Chrome böngészőt bezártam.")

def setup_browser():
    """Elindít egy Chrome böngészőt az alapértelmezett beállításokkal."""
    options = webdriver.ChromeOptions()
    user_name = os.environ.get("USERNAME") or os.getlogin()
    chrome_profile_path = f"C:\\Users\\{user_name}\\AppData\\Local\\Google\\Chrome\\User Data"
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("profile-directory=Default")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
