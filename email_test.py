from email.message import EmailMessage

import sys
sys.path.insert(1, "../secrets")
import gmail

# print(gmail.SENDER)
# print(gmail.GMAIL_APP_PASSWORD)
# print(gmail.GUI)

import smtplib

# Start the connection
smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtpserver.ehlo()
smtpserver.login(gmail.SENDER, gmail.GMAIL_APP_PASSWORD)

# Test with simple email
# sent_from = gmail.SENDER
# sent_to = gmail.GUI
# email_text = "Testing"
# smtpserver.sendmail(sent_from, sent_to, email_text)

# Create mail
email = EmailMessage()
email["From"] = gmail.SENDER
# email["To"] = gmail.GUI
recipients = [gmail.GUI, gmail.GEORGIA]
email["To"] = recipients
email["Subject"] = "Test"
email.set_content("Testing", subtype="html")

# Send email
smtpserver.send_message(email)

# Close the connection
smtpserver.close()