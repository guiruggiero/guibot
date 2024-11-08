import time

from selenium import webdriver # https://www.selenium.dev/documentation/webdriver/getting_started/install_library/
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from email.message import EmailMessage
import smtplib
import sys
sys.path.insert(1, "../../secrets")
import gmail

time_now = time.localtime()
check_start_hour = int(time.strftime("%H", time_now)) + 2
if check_start_hour >= 24: check_start_hour = check_start_hour - 24
check_start_hour = str(check_start_hour)
check_start_minute = time.strftime("%M", time_now)
check_start_second = time.strftime("%S", time_now)

# Initialize Selenium browser
options = webdriver.ChromeOptions() # https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
# options.add_argument("--headless=new")
# options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=options) # https://googlechromelabs.github.io/chrome-for-testing/

# Start page
browser.get("https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1")

# Take screenshot
image_path = "screenshots/" + check_start_hour + check_start_minute + check_start_second + ".png"
browser.execute_script("document.body.style.zoom='70%'")
browser.save_screenshot(image_path)

# Create mail
email = EmailMessage()
email["From"] = "Gui's bot <" + gmail.SENDER + ">"
email["To"] = [gmail.GUI]
email["Subject"] = "Urgent - EU Blue Card appointment"
email.set_content("There might be appointments available! Double check the attached screenshot.", subtype="html")
with open(image_path, "rb") as image_file:
    email.add_attachment(image_file.read(), maintype="image", subtype="png", filename="screenshot.png")

# Start the connection
smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtpserver.ehlo()
smtpserver.login(gmail.SENDER, gmail.GMAIL_APP_PASSWORD)

# Send email
smtpserver.send_message(email)

# Close the connection
smtpserver.quit()