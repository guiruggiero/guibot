import time
import schedule # https://schedule.readthedocs.io/en/stable/installation.html

from selenium import webdriver # https://www.selenium.dev/documentation/webdriver/getting_started/install_library/
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from email.message import EmailMessage
import smtplib
import sys

sys.path.insert(1, "../../secrets")
import guibot

def check_for_appt():
    try:

        # Get current time
        check_start_time = time.strftime("%H:%M", time.localtime())
        print("Starting check - " + check_start_time)

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
        browser.get("https://termine.staedteregion-aachen.de/select2?md=2")
        # print("Page opened")
        browser.implicitly_wait(3)

        # Click "+" in the right category (Umschreibung ausländische Fahrerlaubnis oder Dienstfahrerlaubnis)
        ActionChains(browser).scroll_by_amount(0, 1000).perform() # Scrolls all the way down
        accordion = browser.find_element(By.ID, "header_concerns_accordion-7254").click()
        # print("Clicked accordion")
        browser.implicitly_wait(2)
        button_plus = browser.find_element(By.ID, "button-plus-818").click() # Umschreibung einer ausländischen Fahrerlaubnis
        # print("Clicked plus button")
        browser.implicitly_wait(2)

        # Exception tests
        # raise KeyboardInterrupt
        # raise Exception

        # Move to the next page
        button_next = browser.find_element(By.ID, "WeiterButton")
        ActionChains(browser).scroll_by_amount(0, 1000).perform() # Scrolls all the way down
        # print("Scrolled down")
        browser.implicitly_wait(2)
        button_next.click()
        # print("Clicked next button")
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
        office_buttons = browser.find_elements(By.NAME, "select_location")
        ActionChains(browser).scroll_by_amount(0, 1000).perform() # Scrolls all the way down
        # Find the right button to press
        for button in office_buttons:
            # print(button.accessible_name)
            # print(button.aria_role)
            # print(button.parent)
            # print(button.tag_name)
            # print(button.id)
            # print("\n")

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

        else: # Appointment(s) available
            print("Appointment(s) available!")

            # # Take screenshot
            # # check_start_second = time.strftime("%S", time.localtime())
            # time_now = time.strftime("%H%M%S", time.localtime())
            # image_path = "screenshots/" + time_now + ".png"
            # # browser.execute_script("document.body.style.zoom='70%'")
            # browser.save_screenshot(image_path)
            # print("Screenshot saved")

            # Create mail
            email = EmailMessage()
            email["From"] = "GuiBot <" + guibot.GMAIL_SENDER + ">"
            email["To"] = [guibot.EMAIL2]
            email["Subject"] = "Urgent - Driver's license appointment(s) available"
            email.set_content("Appointments available!<br><br>Go to https://termine.staedteregion-aachen.de/select2?md=2, "
                "select 'Umschreibung ausländische Fahrerlaubnis oder Dienstfahrerlaubnis', Umschreibung einer ausländischen "
                "Fahrerlaubnis (first option), and 1 appointment (plus button).", subtype="html")
            # with open(image_path, "rb") as image_file:
            #     email.add_attachment(image_file.read(), maintype="image", subtype="png", filename="screenshot.png")

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
        # Create email
        email = EmailMessage()
        email["From"] = "GuiBot <" + guibot.GMAIL_SENDER + ">"
        email["To"] = [guibot.EMAIL1]
        email["Subject"] = "Script error"
        email.set_content("The script is having problems, go check it.", subtype="html")

        # Start the connection
        smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtpserver.ehlo()
        smtpserver.login(guibot.GMAIL_SENDER, guibot.GMAIL_APP_PASSWORD)

        # Send email
        smtpserver.send_message(email)

        # Close the connection
        smtpserver.quit()
        print("\nError warning email sent\n")
        exit()

# check_for_appt()

# Timed run
print("Program started\n")
check_for_appt()

# schedule.every(2).minutes.do(check_for_appt)
schedule.every(30).seconds.do(check_for_appt)
while True:
    schedule.run_pending()
    time.sleep(1)