import os
import time
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_download(download_path, timeout=60):
      while True:
        end_time = time.time() + timeout
        latest_file = None

        while time.time() < end_time:
            files = [f for f in os.listdir(download_path) if f.endswith((".xls", ".xlsx"))]
            if files:
                latest_file = max([os.path.join(download_path, f) for f in files], key=os.path.getctime)
                print(f"\n✅ Fájl letöltve: {os.path.basename(latest_file)}")
                return latest_file  # Visszaadja a letöltött fájl teljes elérési útját
            time.sleep(2)
        print("\n⏳ Időtúllépés: A fájl nem töltődött le időben.")

        # Ha az első próbálkozás sikertelen, újrapróbálkozás 10 perces timeouttal
        if timeout == 600:  # 10 perc már volt, ne próbálkozzunk újra
            return False

        print("🔄 Újrapróbálkozás 10 perces időkorláttal...")
        timeout = 600  # 10 perc
        return None

def move_latest_file(source, target):
    if source and os.path.exists(source):
        shutil.move(source, os.path.join(target, os.path.basename(source)))
        print(f"📂 Fájl áthelyezve: {source} → {target}\n")
    else:
        print(f"⚠️ A forrásfájl nem található ({source}), nem lehet áthelyezni.")



def download(driver, wait, user_name, button_id):
    target_folder = r"\\hucbrfs\Coolbridge\COMMON\ERP\BUSINESS_INTELLIGENCE\source_raw\fleet_management"
    download_path = f"C:\\Users\\{user_name}\\Downloads"
    downloaded = True

    time.sleep(5)

    try:
        export_button = wait.until(
            EC.presence_of_element_located((By.ID, button_id))
        )
        wait.until(EC.element_to_be_clickable((By.ID, button_id)))

        #print("🔍 Megtalált elem HTML kódja:")
        #print(export_button.get_attribute("outerHTML"))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", export_button)
        time.sleep(1)

        driver.execute_script("arguments[0].click();", export_button)
        print(f"👆 Rákattintottam a(z) {button_id} gombjára.")

        time.sleep(15)

        latest_file = wait_for_download(download_path)
        if latest_file:
            move_latest_file(latest_file, target_folder)
        else:
            downloaded = False
    
    except Exception as e:
        print(f"⚠️ Hiba történt: {e}")
        downloaded = False
    
    return downloaded
