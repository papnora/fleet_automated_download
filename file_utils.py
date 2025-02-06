import os
import time
import shutil

def wait_for_download(download_path, timeout=60):
    """Megvárja, hogy egy .xls vagy .xlsx fájl letöltődjön."""
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = os.listdir(download_path)
        if any(file.endswith((".xls", ".xlsx")) for file in files):
            print("✅ Fájl letöltve!")
            return True
        time.sleep(2)
    print("⏳ Időtúllépés: A fájl nem töltődött le időben.")
    return False

def move_latest_file(source, target):
    """A legutoljára letöltött fájlt áthelyezi a célmappába."""
    files = [os.path.join(source, f) for f in os.listdir(source) if f.endswith((".xls", ".xlsx"))]
    if files:
        latest_file = max(files, key=os.path.getctime)
        shutil.move(latest_file, os.path.join(target, os.path.basename(latest_file)))
        print(f"Fájl áthelyezve: {latest_file} → {target}")
