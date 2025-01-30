from selenium import webdriver
import tkinter as tk
from time import sleep
from common import start_driver
from PIL import Image, ImageTk, ImageDraw
from selenium.webdriver.common.by import By
import pygetwindow as gw
import threading


def downloadFleetData(driver):
    driver.execute_script("window.open('http://tata.fleetmanager.guentner.local/", '_blank')  
    sleep(1)

    #username = driver.find_element(By.NAME, '_username')
    #password = driver.find_element(By.NAME, '_password')
    #username.send_keys("office@coolbridge.com")
    #password.send_keys("zero2HERO")

    reports_menu = driver.find_element(By.XPATH, "//span[text()='Reports']/parent::a")
    reports_menu.click()
    sleep(2)

    reports_sub_menu = driver.find_element(By.XPATH, "//span[text()='Reports']/parent::a")
    reports_sub_menu.click()
    sleep(2)
    
if __name__ == "__main__":
    driver = start_driver()
    try:
        downloadFleetData(driver)

    finally:
        driver.quit()
