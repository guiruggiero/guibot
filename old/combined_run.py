import time
import schedule # https://schedule.readthedocs.io/en/stable/installation.html

from fuhrerscheinstelle_err import check_for_appt as check_for_appt_fuherscheinstelle
from auslaenderamt_err import check_for_appt as check_for_appt_auslaenderamt

def check_for_appts():
    check_for_appt_fuherscheinstelle()
    check_for_appt_auslaenderamt()

# check_for_appts()

# Timed run
print("Program started\n")
check_for_appts()
schedule.every(3).minutes.do(check_for_appts)
while True:
    schedule.run_pending()
    time.sleep(1)