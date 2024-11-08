from twilio.rest import Client

import sys
sys.path.insert(1, "../secrets")
import aachen_appts

account_sid = aachen_appts.TWILIO_ACCOUNT_SID
# print(account_sid)
auth_token = aachen_appts.TWILIO_AUTH_TOKEN
# print(auth_token)

client = Client(account_sid, auth_token)

call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to=aachen_appts.PHONE_GUI,
    from_=aachen_appts.TWILIO_PHONE_NUMBER)

print(call.sid)