from selenium import webdriver
import time

browser = webdriver.Chrome()

browser.get("http://www.google.com")
time.sleep(5)
browser.close()