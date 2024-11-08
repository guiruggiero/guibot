from twilio.rest import Client

import sys
sys.path.insert(1, "../../secrets")
import guibot

account_sid = guibot.TWILIO_ACCOUNT_SID
# print(account_sid)
auth_token = guibot.TWILIO_AUTH_TOKEN
# print(auth_token)

client = Client(account_sid, auth_token)

call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to=guibot.PHONE,
    from_=guibot.TWILIO_PHONE_NUMBER)

print(call.sid)