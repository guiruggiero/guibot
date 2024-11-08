import time
import schedule # https://schedule.readthedocs.io/en/stable/installation.html

from selenium import webdriver # https://www.selenium.dev/documentation/webdriver/getting_started/install_library/
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService

from email.message import EmailMessage
import smtplib
import sys

sys.path.insert(1, "../../secrets")
import guibot

def check_for_stock():
    try:
        time_now = time.localtime()
        # print(time_now)
        check_start_hour = int(time.strftime("%H", time_now)) + 2
        if check_start_hour >= 24: check_start_hour = check_start_hour - 24
        check_start_hour = str(check_start_hour)
        check_start_minute = time.strftime("%M", time_now)
        print("Starting check - " + check_start_hour + ":" + check_start_minute)       

        # Initialize Selenium browser
        options = webdriver.ChromeOptions() # https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
        options.add_argument("--headless=new")
        # options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(options=options) # https://googlechromelabs.github.io/chrome-for-testing/

        # Fetch page source
        url = "https://shop.olympics.com/en/paris-2024/paris-2024-olympics-pin-badge/t-4588774218+p-125766430724+z-8-4134459471"
        browser.get(url)
        time.sleep(2)
        source = browser.page_source
        # print(source)
        # html = open("source.html", "w")
        # html.write(source)
        # html.close()
        # print("Saved HTML source\n")

        # Check if "Out of Stock" is in the page
        search = source.find("Out of Stock")
        # print(search)
        if search != -1: # Found string somewhere, still out of stock
            print("Still out of stock :-(\n")

        else: # In stock
            print("Pin in stock!")

            # Create mail
            email = EmailMessage()
            email["From"] = "GuiBot <" + guibot.GMAIL_SENDER + ">"
            email["To"] = [guibot.EMAIL1]
            email["Subject"] = "Urgent - 2024 Olympics pin back in stock"
            email.set_content("The pin is in stock!<br><br>Go to https://shop.olympics.com/en/paris-2024/"
                "paris-2024-olympics-pin-badge/t-4588774218+p-125766430724+z-8-4134459471 and get one.", subtype="html")

            # Start the connection
            smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtpserver.ehlo()
            smtpserver.login(guibot.GMAIL_SENDER, guibot.GMAIL_APP_PASSWORD)

            # Send email
            smtpserver.send_message(email)

            # Close the connection
            smtpserver.quit()
            print("Email sent")

        # Close the browser
        browser.close()
    
    # Ctrl+C interruption error
    except KeyboardInterrupt:
        print("\n\nAlright, done for now")
        exit()

    # All other errors
    except:
        # print("Error!")

        # Create email
        email = EmailMessage()
        email["From"] = "GuiBot <" + guibot.GMAIL_SENDER + ">"
        email["To"] = [guibot.EMAIL1]
        email["Subject"] = "Script error"
        email.set_content("Check up on the instance, the script is having problems.", subtype="html")

        # Start the connection
        smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtpserver.ehlo()
        smtpserver.login(guibot.GMAIL_SENDER, guibot.GMAIL_APP_PASSWORD)

        # Send email
        smtpserver.send_message(email)

        # Close the connection
        smtpserver.quit()
        print("\nError warning email sent\n")
        print(type(error).__name__, "–", error)

        # exit()

# check_for_stock()

# Timed run
print("Program started\n")
check_for_stock()

schedule.every(5).minutes.do(check_for_stock)
while True:
    schedule.run_pending()
    time.sleep(1)