import os
import time
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def download(driver, wait, user_name, button_id):
    target_folder = r"\\hucbrfs\Coolbridge\COMMON\ERP\BUSINESS_INTELLIGENCE\source_raw\fleet_management"
    download_path = f"C:\\Users\\{user_name}\\Downloads"
    all_downloaded = True

    time.sleep(5)

    try:
        export_button = wait.until(
            EC.presence_of_element_located((By.ID, button_id))
        )
        wait.until(EC.element_to_be_clickable((By.ID, button_id)))

        print("🔍 Megtalált elem HTML kódja:")
        print(export_button.get_attribute("outerHTML"))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", export_button)
        time.sleep(1)

        driver.execute_script("arguments[0].click();", export_button)
        print(f"✅ Rákattintottam a(z) {button_id} gombjára.")

        time.sleep(15)

        if wait_for_download(download_path):
            move_latest_file(download_path, target_folder)
        else:
            all_downloaded = False
    
    except Exception as e:
        print(f"⚠️ Hiba történt: {e}")
        all_downloaded = False
    
    return all_downloaded
