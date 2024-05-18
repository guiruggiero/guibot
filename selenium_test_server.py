# Install Selenium https://pypi.org/project/selenium/
# Install Chrome driver https://chromedriver.chromium.org/downloads

from time import sleep
from selenium import webdriver

driver_location = "/usr/bin/chromedriver"
# driver_location = "/usr/lib/chromium-browser/chromedriver"
service = webdriver.ChromeService(executable_path=driver_location)

bin_location = "/usr/bin/chromedriver" # TODO: fix "no chrome binary" error
options = webdriver.ChromeOptions()
options.binary_location = bin_location

browser = webdriver.Chrome(service=service, options=options)

browser.get("http://www.google.com")
print("Page opened\n")
sleep(3)

browser.close()