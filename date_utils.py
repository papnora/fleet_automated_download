import time
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def get_today():
    """Visszaadja a mai dátumot DD.MM.YYYY formátumban."""
    today = datetime.today()
    day_today = today.strftime("%d")  # (DD)
    month_today = today.strftime("%m")  # (MM)
    year_today = today.strftime("%Y")  # (YYYY)

    print(f"Aktuális dátum: {day_today}.{month_today}.{year_today}")

    return day_today, month_today, year_today

def get_three_months_ago():
    """Visszaadja a három hónappal ezelőtti dátumot DD.MM.YYYY formátumban."""
    three_months_ago = datetime.today() - timedelta(days=90)
    day_3M = three_months_ago.strftime("%d")  # (DD)
    month_3M = three_months_ago.strftime("%m")  # (MM)
    year_3M = three_months_ago.strftime("%Y")  # (YYYY)

    print(f"Három hónappal ezelőtti dátum: {day_3M}.{month_3M}.{year_3M}")
    return day_3M, month_3M, year_3M

def get_fixed_date():
    """Visszaad egy fix dátumot (01.08.2022)."""
    return "01.08.2022"

def fill_date_field(driver, wait):
    """
    Kitölti a kezdő- és végdátum mezőket a három hónappal ezelőtti, illetve a mai dátummal.
    """
    day_today, month_today, year_today = get_today()
    day_3M, month_3M, year_3M = get_three_months_ago()

    # Kezdő dátum mező kitöltése (három hónappal ezelőtti dátum)
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

    # Végdátum mező kitöltése (mai dátum)
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
    """Megkeresi és rákattint a keresés gombra."""
    search_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='box-footer']//button[contains(text(), 'Search')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
    search_button.click()
