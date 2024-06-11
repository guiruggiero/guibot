# Install Selenium https://pypi.org/project/selenium/
# Install Chrome driver https://chromedriver.chromium.org/downloads

from time import sleep
from selenium import webdriver

browser = webdriver.Chrome()

browser.get("http://www.google.com")
print("Page opened\n")
sleep(3)

browser.close()