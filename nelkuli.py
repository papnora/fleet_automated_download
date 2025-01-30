import sys
sys.path.append("c:/Projects/Glabs signin")

import tkinter as tk
from time import sleep
from common import start_driver
from PIL import Image, ImageTk, ImageDraw
from selenium.webdriver.common.by import By
import pygetwindow as gw
import threading

# Globális változók
is_chrome_open = False

def run_logis(driver):
    driver.get("http://10.4.11.9/OAS/Logis/Account/Login?ReturnUrl=%2FOAS%2FLogis%2F")
    sleep(1)

    username = driver.find_element(By.NAME, 'UserName')
    password = driver.find_element(By.NAME, 'Password')
    username.send_keys("display")
    password.send_keys("display11")

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    sleep(1)
    
    # Oldal nagyítása JavaScript segítségével
    driver.execute_script("""
        document.body.style.transform = 'scale(1.5)';
        document.body.style.transformOrigin = '0 0';
    """)
    sleep(1)


def run_glabs(driver):
    driver.execute_script("window.open('https://guntner.glabs.me/hu/login', '_blank');")  
    sleep(1)
    
    driver.switch_to.window(driver.window_handles[1])
    sleep(1)

    driver.maximize_window()

    username = driver.find_element(By.NAME, '_username')
    password = driver.find_element(By.NAME, '_password')
    username.send_keys("office@coolbridge.com")
    password.send_keys("zero2HERO")

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    sleep(2)

    sidebar_settings = driver.find_element(By.XPATH, "//span[text()='Settings']")
    sidebar_settings.click()
    sleep(2)

    devices_connections = driver.find_element(By.XPATH, "//span[text()='Devices and connections']")
    devices_connections.click()
    sleep(2)

    displays_option = driver.find_element(By.XPATH, "//span[text()='Displays']")
    displays_option.click()
    sleep(2)
    

    disconnect_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Disconnect')]")
    disconnect_button.click()

    driver.refresh()
    sleep(2)

    pair_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Pairing display')]")
    pair_button.click()
    sleep(6)

    pin_digits = driver.find_elements(By.CSS_SELECTOR, 'div.pin-digit')
    pin_code = [digit.text for digit in pin_digits[:6]]

    driver.get("https://guntner.glabs.me/display")
    sleep(5)
    pin_input = driver.find_element(By.CLASS_NAME, 'pin-input')
    pin_input.clear()
    pin_input.send_keys(''.join(pin_code))

    activate_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Activate')]")
    activate_button.click()
    sleep(5)

    driver.fullscreen_window()


def is_other_chrome_open():
    """Ellenőrzi, hogy van-e másik, megadott tartalmú Chrome ablak megnyitva."""
    chrome_windows = [win for win in gw.getWindowsWithTitle('') if 'Chrome' in win.title]
    for win in chrome_windows:
        if any(keyword in win.title for keyword in ['Workout Program', 'Holidays', 'Nameday', 'Coolbridge']):
            return True
    return False

def minimize_chrome(driver):
    """Bezárja a GLABS display oldalt, majd tálcára helyezi a Selenium által megnyitott Chrome ablakot."""
    # Bezárjuk a display tabot, ha megtaláljuk
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if "GLABs.me - Global Logistics Appointment Booking System" in driver.title:
            print(f"GLABS Display oldal bezárása ({driver.title})...")
            driver.close()
            break  # Kilépünk, miután bezártuk a megfelelő tabot

    # Ezután tálcára helyezzük a Chrome ablakot
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        window_title = driver.execute_script("return document.title;")
        print(f"Tálcára helyezés: {window_title}")
        # Pygetwindow-rel minimalizáljuk
        chrome_windows = [win for win in gw.getWindowsWithTitle(window_title) if 'Chrome' in win.title]
        for win in chrome_windows:
            win.minimize()
            print(f"{win.title} tálcára helyezve.")


def restore_chrome(driver):
    """Visszaállítja kizárólag a Selenium által megnyitott Chrome ablakot, és újranyitja a GLABS display oldalt."""
    # Visszaállítjuk a Selenium ablakokat
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        window_title = driver.execute_script("return document.title;")
        chrome_windows = [win for win in gw.getWindowsWithTitle(window_title) if 'Chrome' in win.title]
        for win in chrome_windows:
            win.restore()
            print(f"{win.title} teljes méretre visszaállítva.")

    # Ellenőrizzük, hogy nincs-e már nyitva a GLABS display oldal
    if not any("GLABs.me - Global Logistics Appointment Booking System" in driver.title for handle in driver.window_handles):
        print("GLABS Display oldal újranyitása...")
        # Új tabot nyit a GLABS display oldallal
        driver.execute_script("window.open('https://guntner.glabs.me/display', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])  # Az újonnan megnyitott tabra vált
        driver.fullscreen_window()
        print("GLABS Display oldal fullscreen módra váltva.")


def monitor_chrome():
    """Figyeli, hogy van-e másik Chrome böngésző megnyitva, és ennek megfelelően kezeli az ablakokat."""
    global is_chrome_open
    previous_state = is_chrome_open  # Tároljuk az előző állapotot

    while True:
        current_state = is_other_chrome_open()  # Ellenőrizzük az aktuális állapotot
        if current_state != previous_state:  # Csak akkor hajtsuk végre, ha változott az állapot
            if current_state:
                print("Másik Chrome ablak érzékelve. Chrome minimalizálása...")
                is_chrome_open = True
                minimize_chrome(driver)
            else:
                print("Nincs másik Chrome ablak. Chrome visszaállítása...")
                is_chrome_open = False
                restore_chrome(driver)

        previous_state = current_state  # Frissítjük az előző állapotot
        sleep(2)  # 2 másodpercenként ellenőrizzük az állapotot


def switch_tabs(driver):
    """Tabok közötti váltást végez, ha nincs másik Chrome ablak megnyitva, és a böngésző nincs tálcára helyezve."""
    global is_chrome_open
    while True:
        # Ellenőrizzük, hogy a böngésző nincs-e tálcára helyezve
        if is_chrome_open:
            print("Másik Chrome böngésző megnyitva, vagy a böngésző tálcán van. Tab váltás szünetel.")
            sleep(10)  # 10 másodpercenként ellenőrizzük újra
            continue

        print("Nincs másik Chrome böngésző. Tab váltása...")

        try:
            for i in range(len(driver.window_handles)):
                driver.switch_to.window(driver.window_handles[i])
                driver.fullscreen_window()
                sleep(60)  # 1 percenként vált tabot
        except IndexError as e:
            print(f"Tab váltás közben hiba történt: {e}. Ellenőrzés újrakezdése...")
            sleep(5)  # Rövid szünet, mielőtt újra próbálkozunk


if __name__ == "__main__":
    driver = start_driver()
    try:
        # Chrome ellenőrzés külön szálon
        monitoring_thread = threading.Thread(target=monitor_chrome, daemon=True)
        monitoring_thread.start()

        run_logis(driver)
        run_glabs(driver)
        switch_tabs(driver)

        # GUI -EXE
        root = tk.Tk()
        root.title("Glabs automation running")
        label = tk.Label(root, text="Az automatikus Glabs és Logis bejelentkezési program fut. A megállításhoz zárd be ezt az ablakot.")
        label.pack(padx=20, pady=20)

        root.protocol("WM_DELETE_WINDOW", root.quit)  # Windows close
        root.mainloop()
    finally:
        driver.quit()
