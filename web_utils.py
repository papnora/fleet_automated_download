import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_element(driver, xpath, timeout=10):
    """Kattint egy elemre a megadott XPATH alapján."""
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    time.sleep(2)
