from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

# chrome os
# os.chmod("/home/guilhermeruggiero/chromedriver", 755)
# driver = webdriver.Chrome(executable_path="/home/guilhermeruggiero/chromedriver")

# windows
os.chmod(r"C:\Users\gui\Downloads\chromedriver.exe", 755)
driver = webdriver.Chrome(executable_path=r"C:\Users\gui\Downloads\chromedriver.exe")

driver.get("http://www.python.org")
time.sleep(5)
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
# elem.submit()
time.sleep(5)
assert "No results found." not in driver.page_source
driver.close()