
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ensure_search_panel_open(driver, panel_id, panel_name):
    """Biztosítja, hogy egy adott keresési panel lenyitott állapotban legyen."""
    try:
        collapse_search_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"#{panel_id} i"))
        )
        print(f"✅ Megtaláltam a(z) {panel_name} panelt!")

        icon_class = collapse_search_btn.get_attribute("class")

        if "fa-plus" in icon_class:
            print(f"🔒 A {panel_name} keresési panel NINCS LENYITVA.")
            collapse_search_btn.click()
            print(f"✅ A {panel_name} keresési panelt LENYITOTTAM.")
        elif "fa-minus" in icon_class:
            print(f"✅ A {panel_name} keresési panel LE VAN NYITVA.")

    except Exception as e:
        print(f"❌ Hiba történt a {panel_name} keresési panel lenyitásánál: {e}")


def ensure_panel_open(driver, panel_name, panel_xpath, button_xpath):
    """Általános függvény bármilyen panel lenyitásához a weboldalon."""
    try:
        wait = WebDriverWait(driver, 10)
        collapse_button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
        icon_class = collapse_button.get_attribute("class")

        if "fa-plus" in icon_class:
            print(f"A {panel_name} panel NINCS LENYITVA.")
            collapse_button.click()
            time.sleep(3)
            print(f"A {panel_name} panelt LENYITOTTAM.")
        elif "fa-minus" in icon_class:
            print(f"A {panel_name} panel LE VAN LENYITVA.")
    except Exception as e:
        print(f"Hiba történt a {panel_name} panel ellenőrzésekor: {e}")


def ensure_service_product_panel_open(driver):
    ensure_panel_open(driver, 
                      "Service product details", 
                      "//div[h3[contains(text(), 'Service products details')]]", 
                      "//div[h3[contains(text(), 'Service products details')]]//button[@id='ServiceProductsDetailsList_Collapse']/i")
