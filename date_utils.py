import time
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def get_today():
    today = datetime.today()
    day_today = today.strftime("%d")  
    month_today = today.strftime("%m")  
    year_today = today.strftime("%Y") 
    
    print("")
    print(f"Aktuális dátum: {day_today}.{month_today}.{year_today}")

    return day_today, month_today, year_today

def get_three_months_ago():
    three_months_ago = datetime.today() - timedelta(days=90)
    day_3M = three_months_ago.strftime("%d")  
    month_3M = three_months_ago.strftime("%m") 
    year_3M = three_months_ago.strftime("%Y")  

    print(f"Három hónappal ezelőtti dátum: {day_3M}.{month_3M}.{year_3M}")
    print("")
    return day_3M, month_3M, year_3M

def get_fixed_date():
    print(f"Fix dátum: 01.08.2022")
    print("")
    return "01", "08", "2022"

def get_weekago():
    last_week = datetime.today() - timedelta(weeks=1)
    day_last_week = last_week.strftime("%d") 
    month_last_week = last_week.strftime("%m")  
    year_last_week = last_week.strftime("%Y") 
    start_time = "00:01"

    print(f"Egy héttel ezelőtti dátum: {day_last_week}.{month_last_week}.{year_last_week}.{start_time}")
    print("")

    return day_last_week, month_last_week, year_last_week, start_time

def fill_week_date_field(driver, wait):
    day_today, month_today, year_today = get_today()
    day_last_week, month_last_week, year_last_week, start_time = get_weekago()
    hour_today = datetime.now().strftime("%H")
    minute_today = datetime.now().strftime("%M")

    # Start Date Kitöltése
    start_date_input = wait.until(EC.element_to_be_clickable((By.ID, "startDateWrapp")))
    start_date_input.click()
    time.sleep(1)
    
    start_date_input.send_keys(Keys.CONTROL + "a")  
    start_date_input.send_keys(Keys.BACKSPACE)  
    time.sleep(0.5)

    start_date_input.send_keys(f"{day_last_week}.{month_last_week}.{year_last_week} {start_time}")
    start_date_input.send_keys(Keys.ENTER)
    time.sleep(1)

    # End Date Kitöltése
    end_date_input = wait.until(EC.element_to_be_clickable((By.ID, "endDateWrapp")))
    end_date_input.click()
    time.sleep(1)

    end_date_input.send_keys(Keys.CONTROL + "a") 
    end_date_input.send_keys(Keys.BACKSPACE)  
    time.sleep(0.5)

    end_date_input.send_keys(f"{day_today}.{month_today}.{year_today} {hour_today}:{minute_today}")
    end_date_input.send_keys(Keys.ENTER)
    time.sleep(1)


    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='box-footer']//button[contains(text(), 'Search')]")))
    search_button.click()
   
    time.sleep(2)

def fill_fix_date_field(driver, wait):
    day_today, month_today, year_today = get_today()
    day_fix, month_fix, year_fix = get_fixed_date()

    start_date_input = wait.until(EC.element_to_be_clickable((By.ID, "startDateWrapp")))
    start_date_input.click()
    time.sleep(2)

    start_date_input.send_keys(Keys.CONTROL + "a")
    start_date_input.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
    
    start_date_input.send_keys(f"{day_fix}.{month_fix}.{year_fix}")
    start_date_input.send_keys(Keys.ENTER)
    time.sleep(1)

    end_date_input = wait.until(EC.element_to_be_clickable((By.ID, "endDateWrapp")))
    end_date_input.click()
    time.sleep(1)

    end_date_input.send_keys(Keys.CONTROL + "a")
    end_date_input.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
    
    end_date_input.send_keys(f"{day_today}.{month_today}.{year_today}")
    end_date_input.send_keys(Keys.ENTER)
    time.sleep(1)

    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='box-footer']//button[contains(text(), 'Search')]")))
    search_button.click()
    time.sleep(2)

def fill_date_field(driver, wait):
    day_today, month_today, year_today = get_today()
    day_3M, month_3M, year_3M = get_three_months_ago()

    start_date_input = wait.until(EC.element_to_be_clickable((By.ID, "startDateWrapp")))
    start_date_input.click()
    time.sleep(2)

    actions = ActionChains(driver)
    actions.key_down(Keys.SHIFT)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.key_up(Keys.SHIFT)
    actions.perform()
    time.sleep(2)

    start_date_input.send_keys(Keys.BACKSPACE * 2)
    start_date_input.send_keys(day_3M)
    start_date_input.send_keys(Keys.TAB)
    time.sleep(2)

    start_date_input.send_keys(Keys.BACKSPACE * 2)
    start_date_input.send_keys(month_3M)
    start_date_input.send_keys(Keys.TAB)
    time.sleep(2)

    start_date_input.send_keys(Keys.BACKSPACE * 4)
    start_date_input.send_keys(year_3M)
    start_date_input.send_keys(Keys.ENTER)
    time.sleep(2)

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

    # Keresés gomb megnyomása
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='box-footer']//button[contains(text(), 'Search')]")))
    search_button.click()
   
    time.sleep(2)

def search_data(driver, wait):
    search_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='box-footer']//button[contains(text(), 'Search')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
    search_button.click()
