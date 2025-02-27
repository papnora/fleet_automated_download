
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_RETRIES = 3 

def ensure_search_panel_open(driver, panel_id, panel_name):
    """Biztosítja, hogy egy adott keresési panel lenyitott állapotban legyen."""
    attempt = 0
    
    while attempt < MAX_RETRIES:
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

            return

        except Exception as e:
            print(f"❌ Hiba történt a {panel_name} keresési panel lenyitásánál: {e}")
            attempt += 1
            time.sleep(3)  # Kicsi várakozás újrapróbálás előtt

    print(f"❌ Nem sikerült lenyitni a {panel_name} keresési panelt {MAX_RETRIES} próbálkozás után.")


def ensure_panel_open(driver, panel_name, panel_xpath, button_xpath):
    """Általános függvény bármilyen panel lenyitásához a weboldalon."""
    attempt = 0
    while attempt < MAX_RETRIES:
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
                print(f"A {panel_name} panel LE VAN NYITVA.")
            
            return
        
        except Exception as e:
            print(f"❌ Hiba történt a {panel_name} panel lenyitásánál (próbálkozás {attempt + 1}/{MAX_RETRIES}): {e}")
            attempt += 1
            time.sleep(3)  # Kicsi várakozás újrapróbálás előtt

    print(f"❌ Nem sikerült lenyitni a {panel_name} panelt {MAX_RETRIES} próbálkozás után.")

#Asset report
def ensure_service_product_panel_open(driver):
    ensure_panel_open(driver, 
                      "Service product details", 
                      "//div[h3[contains(text(), 'Service products details')]]", 
                      "//div[h3[contains(text(), 'Service products details')]]//button[@id='ServiceProductsDetailsList_Collapse']/i")

def ensure_vehicle_service_panel_open(driver):
    ensure_panel_open(driver, 
                      "Vehicle in service", 
                      "//div[h3[contains(text(), 'Vehicle in service')]]", 
                      "//div[h3[contains(text(), 'Vehicle in service')]]//button[@id='VehicleService_Collapse']/i")

#Forklift report
def ensure_vehicle_electrical_consumption_panel_open(driver):
    ensure_panel_open(driver, 
                      "Vehicle electrical consumption", 
                      "//div[h3[contains(text(), 'Vehicle electrical consumption')]]", 
                      "//div[h3[contains(text(), 'Vehicle electrical consumption')]]//button[@id='VehicleElectricalConsumption_Collapse']/i")
    
#Vehicle usage per engine report
def ensure_vehicle_usage_perengine_panel_open(driver):
    ensure_panel_open(driver, 
                      "Vehicle usage per engine sessions", 
                      "//div[h3[contains(text(), 'Vehicle usage per engine sessions')]]", 
                      "//div[h3[contains(text(), 'Vehicle usage per engine sessions')]]//button[@id='VehicleUsuageTable_Collapse']/i")

#Fuel supplier - 3 stck
def ensure_fuel_supplier_panel_open(driver):
    ensure_panel_open(driver, 
                      "Fuel supplier summary", 
                      "//div[h3[contains(text(), 'Fuel supplier summary')]]", 
                      "//div[h3[contains(text(), 'Fuel supplier summary')]]//button[@id='CostPerSupplier_Collapse']/i")
    
