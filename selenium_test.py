from selenium import webdriver
import time

# Install selenium https://pypi.org/project/selenium/
# Install chrome driver https://chromedriver.chromium.org/downloads

browser = webdriver.Chrome()

browser.get("http://www.google.com")
time.sleep(5)

browser.close()