import time
import schedule # https://schedule.readthedocs.io/en/stable/installation.html

from selenium import webdriver # https://www.selenium.dev/documentation/webdriver/getting_started/install_library/
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from email.message import EmailMessage
import smtplib
import sys

sys.path.insert(1, "../secrets")
import aachen_appts

import random

from twilio.rest import Client # https://www.twilio.com/docs/voice/quickstart/python

def check_for_appt():
    try:

        # Get current time
        time_now = time.localtime()
        # print(time_now)
        check_start_hour = int(time.strftime("%H", time_now)) + 2 # Correct server that is 2 hours behind
        if check_start_hour >= 24: check_start_hour = check_start_hour - 24
        check_start_hour = str(check_start_hour)
        check_start_minute = time.strftime("%M", time_now)
        print("Starting check - " + check_start_hour + ":" + check_start_minute)

        # Decide which team to check
        teams = [1, 2, 3]
        team = random.choice(teams)

        # Initialize Selenium browser
        options = webdriver.ChromeOptions() # https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
        # options.add_argument("--headless=new")
        # options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(options=options) # https://googlechromelabs.github.io/chrome-for-testing/

        # Start page, direct link of https://termine.staedteregion-aachen.de/auslaenderamt/ + Aufenthaltsangelegenheiten (first option)
        browser.get("https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1")
        # print("Page opened")
        browser.implicitly_wait(3)
        ActionChains(browser).scroll_by_amount(0, 300).perform() # Scrolls to put button into view
        # print("Scrolled down")
        browser.implicitly_wait(2)

        # Click "+" in the right category (Erteilung/Verlängerung Aufenthalt - Nachname: A - Z (Team 3))
        accordion = browser.find_element(By.ID, "header_concerns_accordion-456").click()
        # print("Clicked accordion")
        browser.implicitly_wait(2)
        ActionChains(browser).scroll_by_amount(0, 300).perform() # Scrolls to put button into view
        # print("Scrolled down")
        browser.implicitly_wait(2)

        # Click "+" twice because it's an appointment for my wife and I
        if team == 1: # Team 1
            print("Team 1")
            button_plus = browser.find_element(By.ID, "button-plus-293").click()
            # print("Clicked plus button")
            browser.implicitly_wait(2)
            button_plus = browser.find_element(By.ID, "button-plus-293").click()
            # print("Clicked plus button twice")
            browser.implicitly_wait(2)
            
        elif team == 2: # Team 2
            print("Team 2")
            button_plus = browser.find_element(By.ID, "button-plus-296").click()
            # print("Clicked plus button")
            browser.implicitly_wait(2)
            button_plus = browser.find_element(By.ID, "button-plus-296").click()
            # print("Clicked plus button twice")
            browser.implicitly_wait(2)

        elif team == 3: # Team 3
            print("Team 3")
            button_plus = browser.find_element(By.ID, "button-plus-297").click()
            # print("Clicked plus button")
            browser.implicitly_wait(2)
            button_plus = browser.find_element(By.ID, "button-plus-297").click()
            # print("Clicked plus button twice")
            browser.implicitly_wait(2)
        
        # Move to the next page
        button_next = browser.find_element(By.ID, "WeiterButton")
        ActionChains(browser).scroll_by_amount(0, 1000).perform() # Scrolls all the way down
        # print("Scrolled down")
        browser.implicitly_wait(2)
        button_next.click()
        # print("Clicked next button")
        time.sleep(2)
        button_ok_overlay = browser.find_element(By.ID, "OKButton").click()
        # print("Clicked OK button")
        browser.implicitly_wait(3)

        # # Save HTML before selecting the office to see if "Kein freier Termin" is already there
        # source_before_office = browser.page_source
        # html_before_office = open("before_office.html", "w")
        # html_before_office.write(source_before_office)
        # html_before_office.close()
        # print("Saved HTML before office selection\n")

        # # Search the HTML to test the .find() method without "Kein freier Termin" there
        # source_before_office = browser.page_source
        # search_before = source_before_office.find("Kein freier Termin")
        # print(search_before)

        # Select the office
        ActionChains(browser).scroll_by_amount(0, 1000).perform() # Scrolls all the way down
        # print("Scrolled down")
        browser.implicitly_wait(2)
        office_buttons = browser.find_elements(By.NAME, "select_location")
        # Find the right button to press
        for button in office_buttons:
            # print(button.accessible_name)
            # print(button.aria_role)
            # print(button.parent)
            # print(button.tag_name)
            # print(button.id)

            if button.aria_role == "button":
                button.click()
                # print("Clicked office button")

        # # Save HTML after selecting the office to compare with before
        # source_after_office = browser.page_source
        # html_after_office = open("after_office.html", "w")
        # html_after_office.write(source_after_office)
        # html_after_office.close()
        # print("Saved HTML after office selection\n")

        # Check if "Kein freier Termin" is in the page
        time.sleep(2)
        source = browser.page_source
        search = source.find("Kein freier Termin")
        # print(search)
        if search != -1: # Found string somewhere, no appointments available
            print("No appointments available :-(\n")

            # # Take screenshot
            # check_start_second = time.strftime("%S", time_now)
            # browser.execute_script("document.body.style.zoom='70%'")
            # browser.save_screenshot("screenshots/" + check_start_hour + check_start_minute + check_start_second + ".png")
            # print("Screenshot saved")

        else: # Appointment(s) available
            print("Appointment(s) available!")

            # Take screenshot
            check_start_second = time.strftime("%S", time_now)
            image_path = "screenshots/" + check_start_hour + check_start_minute + check_start_second + ".png"
            browser.execute_script("document.body.style.zoom='70%'")
            browser.save_screenshot(image_path)
            print("Screenshot saved")

            # Create mail
            email = EmailMessage()
            email["From"] = "GuiBot <" + aachen_appts.GMAIL_SENDER + ">"
            email["To"] = [aachen_appts.EMAIL_GUI, aachen_appts.EMAIL_GEORGIA]
            email["Subject"] = "Urgent - EU Blue Card appointment"
            email.set_content("Appointments available! Double check the attached screenshot.<br><br>"
                "Go to https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1, "
                "select Aufenthalt (2nd category), Team " + str(team) + ", and 2 appointments (plus button).", subtype="html")
            with open(image_path, "rb") as image_file:
                email.add_attachment(image_file.read(), maintype="image", subtype="png", filename="screenshot.png")

            # Start the connection
            smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtpserver.ehlo()
            smtpserver.login(aachen_appts.GMAIL_SENDER, aachen_appts.GMAIL_APP_PASSWORD)

            # Send email
            smtpserver.send_message(email)

            # Close the connection
            smtpserver.quit()
            print("Email sent")

            # Call with Twilio
            account_sid = aachen_appts.TWILIO_ACCOUNT_SID
            auth_token = aachen_appts.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            call = client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                to=aachen_appts.PHONE_GUI,
                from_=aachen_appts.TWILIO_PHONE_NUMBER)
            print("Call placed: " + call.sid + "\n")

        # Close the browser
        browser.close()
    
    # Ctrl+C interruption error
    except KeyboardInterrupt:
        print("\n\nAlright, done for now")
        exit()

    # All other errors
    except:
        # Create email
        email = EmailMessage()
        email["From"] = "GuiBot <" + aachen_appts.GMAIL_SENDER + ">"
        email["To"] = [aachen_appts.EMAIL_GUI]
        email["Subject"] = "Script error"
        email.set_content("Check up on the instance, the script is having problems.", subtype="html")

        # Start the connection
        smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtpserver.ehlo()
        smtpserver.login(aachen_appts.GMAIL_SENDER, aachen_appts.GMAIL_APP_PASSWORD)

        # Send email
        smtpserver.send_message(email)

        # Close the connection
        smtpserver.quit()

        print("\nError warning email sent\n")
        print(type(error).__name__, "–", error)
        exit()

# check_for_appt()

# Timed run
print("Program started\n")
check_for_appt()

# schedule.every(2).minutes.do(check_for_appt)
schedule.every(20).seconds.do(check_for_appt)
while True:
    schedule.run_pending()
    time.sleep(1)