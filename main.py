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

from chrome_utils import close_existing_chrome, setup_browser, interact_with_page
from file_utils import download, wait_for_download, move_latest_file
from panel_utils import ensure_vehicle_usage_perengine_panel_open, ensure_search_panel_open, ensure_service_product_panel_open, ensure_vehicle_service_panel_open, ensure_vehicle_electrical_consumption_panel_open, ensure_fuel_supplier_panel_open
from date_utils import fill_date_field, fill_fix_date_field, fill_week_date_field

def Fleet():

    close_existing_chrome()
    driver, user_name, download_path = setup_browser()
    wait = WebDriverWait(driver, 10)

    #Vehicle usage per engine session  ############################################################
    # nteract_with_page(driver)
    vehicle_usage = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@id='divVehicleUsuage'][.//h5/strong[contains(text(), 'Vehicle usage per engine sessions')]]")))
    driver.execute_script("arguments[0].scrollIntoView();", vehicle_usage)
    time.sleep(1)
    
    vehicle_usage.click()
    print("")
    print("Kiválasztva: Vehicle usage per engine sessions")
    time.sleep(3)
    ensure_search_panel_open(driver, "ReportsIndexSearch_Collapse", "Reports")
    fill_week_date_field(driver, wait)
    ensure_vehicle_usage_perengine_panel_open(driver)
    print("VU OPEN OK")
    time.sleep(4)
    downloaded = download(driver, wait, user_name, "exportExcel")
    time.sleep(5)

    #Asset report - Vehicle service ################################################################
    interact_with_page(driver)
    manual_vehicle_service = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'list-group-item')][.//h5/strong[text()='Manual vehicle service']]")))
    driver.execute_script("arguments[0].scrollIntoView();", manual_vehicle_service)
    time.sleep(1)
    
    manual_vehicle_service.click()
    print("Kiválasztva: A Manual Vehicle Service")
    time.sleep(3)
    ensure_search_panel_open(driver, "ReportsIndexSearch_Collapse", "Reports")
    fill_fix_date_field(driver, wait) 
    
    ensure_vehicle_service_panel_open(driver)
    print("VSP OPEN OK")
    time.sleep(5)
    downloaded = download(driver, wait, user_name, "exportExcel")
    time.sleep(4)

    #Service Product Details ############################################################################
    interact_with_page(driver)
    service_product_details = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@id='divServiceCategoryProductCost'][.//h5/strong[contains(text(), 'Service products details')]]")))
    driver.execute_script("arguments[0].scrollIntoView();", service_product_details) 
    time.sleep(1)  
    service_product_details.click()
    print("")
    print("Kiválasztva: Service product panel details")

    time.sleep(3)

    ensure_search_panel_open(driver, "ReportsIndexSearch_Collapse", "Reports")
    fill_date_field(driver, wait)
    ensure_service_product_panel_open(driver)

    time.sleep(5)

    # Exportálás és letöltés
    downloaded = download(driver, wait, user_name, "exportExcelServiceProductsDetails")

    time.sleep(4)

    #Forklift report - vehicle electrical consumption ####################################################
    interact_with_page(driver)
    vehicle_electrical_consumption = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@id='divVehicleElectricalConsumption'][.//h5/strong[contains(text(), 'Vehicle electrical consumption')]]")))
    driver.execute_script("arguments[0].scrollIntoView();", vehicle_electrical_consumption)
    time.sleep(1)
    
    vehicle_electrical_consumption.click()
    print("")
    print("Kiválasztva: Vehicle electrical consuption")
    time.sleep(3)
    ensure_search_panel_open(driver, "ReportsIndexSearch_Collapse", "Reports")
    fill_date_field(driver, wait)
    ensure_vehicle_electrical_consumption_panel_open(driver)
    print("VECSP OPEN OK")
    time.sleep(4)
    downloaded = download(driver, wait, user_name, "exportExcel")
    time.sleep(5)

    #Fuel supplier #######################################################################################
    interact_with_page(driver)
    fuel_supplier = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@id='divFuelSupplierSummary'][.//h5/strong[contains(text(), 'Fuel supplier summary')]]")))
    driver.execute_script("arguments[0].scrollIntoView();", fuel_supplier)
    time.sleep(1)
    
    fuel_supplier.click()
    print("")
    print("Kiválasztva: Fuel supplier summary")
    time.sleep(3)
    ensure_search_panel_open(driver, "ReportsIndexSearch_Collapse", "Reports")
    fill_date_field(driver, wait)
    ensure_fuel_supplier_panel_open(driver)
    time.sleep(5)

    # Tables & Rows
    target_folder = r"\\hucbrfs\Coolbridge\COMMON\ERP\BUSINESS_INTELLIGENCE\source_raw\fleet_management"
    download_path = f"C:\\Users\\{user_name}\\Downloads"
    companies = ["Guentner internal Gas supplier","MOL", "Shell Hungary Kft." ]

    for company in companies:
        ensure_fuel_supplier_panel_open(driver)  
    
        table_Suppliers = driver.find_element(By.ID, "CostPerSupplierTable")
        rows = table_Suppliers.find_elements(By.TAG_NAME, "tr")
        
        found = False 
        downloaded = True 
        
        for row in rows:
            if company in row.text:  
                found = True  

                try:
                    button = row.find_element(By.XPATH, ".//button[contains(text(), 'Details')]")
                    button.click()
                    print(f"Rákattintottam a {company} Details gombjára.")
                    time.sleep(5)  
                    
                    box_headers = driver.find_elements(By.CLASS_NAME, "box-header") 

                    for box in box_headers:
                        if company in box.text:  
                            try:
                                export_button = box.find_element(By.XPATH, ".//button[contains(text(), 'Export Excel')]")
                                export_button.click()
                                print(f"Rákattintottam a {company} Export Excel gombjára.")
                                time.sleep(10)  

                                latest_file = wait_for_download(download_path)
                                if latest_file:
                                    move_latest_file(latest_file, target_folder)
                            
                                ensure_fuel_supplier_panel_open(driver)

                            except Exception as e:
                                print(f"Hiba történt az Export Excel gombnál ({company}): {e}")
                                downloaded = False  
                            break 
                    break  
                except Exception as e:
                    print(f"Hiba történt a {company} sorban: {e}")
                    downloaded = False
                    ensure_fuel_supplier_panel_open(driver)
        if not found:  
            print(f"Nem találtam meg a {company}-t a táblázatban.")
            ensure_fuel_supplier_panel_open(driver)

    time.sleep(4)

    # Exportálás és letöltés
    downloaded = download(driver, wait, user_name, "exportExcel")

    time.sleep(4)

    if downloaded:
        print("🔥Assets reports adatai sikeresen letöltve! 🔥")
    
    time.sleep(15)

    return driver

if __name__ == "__main__":
    driver = None
    try:
        driver = Fleet()
      
    except Exception as e:
        print(f"Hiba történt: {e}")
        input("Nyomj Entert a kilépéshez...")
    finally:
        if driver:
            driver.quit()
