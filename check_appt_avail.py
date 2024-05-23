# TODO
# test with some other appointment to see if it works

import time
import schedule

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from email.message import EmailMessage
import smtplib
import sys
sys.path.insert(1, "../secrets")
import gmail

def check_for_appt():
    check_start_time = time.strftime("%H:%M", time.localtime())
    print("Starting check - " + check_start_time)
    
    # Initialize Selenium browser
    options = webdriver.ChromeOptions() # https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md
    # options.add_argument("--headless=new")
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=options)

    # Start page, direct link of https://termine.staedteregion-aachen.de/auslaenderamt/ + Aufenthaltsangelegenheiten (first option)
    browser.get("https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1")
    # print("Page opened\n")
    time.sleep(3)

    # Click "+" in the right category (Erteilung/Verlängerung Aufenthalt - Nachname: A - Z (Team 3))
    accordion = browser.find_element(By.ID, "header_concerns_accordion-340").click()
    # print("Clicked accordion\n")
    time.sleep(2)
    button_plus = browser.find_element(By.ID, "button-plus-268").click()
    # print("Clicked plus button\n")
    time.sleep(1)

    # Move to the next page
    button_next = browser.find_element(By.ID, "WeiterButton")
    ActionChains(browser).scroll_by_amount(0, 1000).perform() # Scrolls all the way down
    # print("Scrolled down\n")
    time.sleep(2)
    button_next.click()
    # print("Clicked next button\n")
    time.sleep(2)
    button_ok_overlay = browser.find_element(By.ID, "OKButton").click()
    # print("Clicked OK button\n")
    time.sleep(3)

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
    office_buttons = browser.find_elements(By.NAME, "select_location")
    # Find the right button to press
    for button in office_buttons:
        # print(i.accessible_name)
        # print(button.aria_role)
        # print(i.parent)
        # print(i.tag_name)
        # print(i.id)

        if button.aria_role == "button":
            button.click()
            # print("Clicked office button\n")
            time.sleep(3)

    # # Save HTML after selecting the office to compare with before
    # source_after_office = browser.page_source
    # html_after_office = open("after_office.html", "w")
    # html_after_office.write(source_after_office)
    # html_after_office.close()
    # print("Saved HTML after office selection\n")

    # Instantiate email
    email = EmailMessage()

    # Check if "Kein freier Termin" is in the page
    source = browser.page_source
    search = source.find("Kein freier Termin")
    # print(search)
    if search != -1: # No appointments available
        # print("No appointments available :-(\n")
        email["Subject"] = "EU Blue Card appointment check - " + check_start_time
        recipients = [gmail.GUI]
        email.set_content("Unfortunately, there are no appointments available.", subtype="html")
    else: # Appointment(s) available
        # print("Appointment(s) available!\n")
        email["Subject"] = "Urgent - EU Blue Card appointment(s) available - "
        recipients = [gmail.GUI, gmail.GEORGIA]
        email.set_content("It looks like there are appointments available!<br><br>"
            "Go to https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1 and grab one ASAP.", subtype="html")

    # Close the browser
    browser.close()
    print("Check done")

    # Start the connection
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(gmail.SENDER, gmail.GMAIL_APP_PASSWORD)

    # Create mail
    email["From"] = "Gui's bot <" + gmail.SENDER + ">"
    email["To"] = recipients

    # Send email
    smtpserver.send_message(email)

    # Close the connection
    smtpserver.quit()
    print("Email sent\n")

# check_for_appt()

# Timed run
# schedule.every(25).seconds.do(check_for_appt)
schedule.every(30).minutes.do(check_for_appt)
while True:
    schedule.run_pending()
    time.sleep(1)