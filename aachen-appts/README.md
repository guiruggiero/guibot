# 📅 Aachen appointment checkers

Automated scripts to check for available appointments at the Aachen, Germany Foreigners Office (Ausländeramt) and Driver's License Office (Führerscheinstelle). The scripts will notify you via email (and sometimes via phone call) when appointments become available.

Built by [Gui Ruggiero](https://guiruggiero.com/?utm_source=github&utm_medium=guibot).

> **Note**: Code works as of October 2024. Updates may be needed if the Aachen websites change their structure, element IDs, or names.

## ✨ Features

- Automated checking at configurable intervals
- Email notifications when appointments are found
- Optional phone call notifications (Ausländeramt only)
- Screenshot capture of available appointments
- Error monitoring and notifications

## 🛠️ Prerequisites

- Python 3.x
- Chrome browser
- Chrome WebDriver

## 📦 Required Python packages

```bash
pip install selenium schedule twilio
```

- [selenium](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/) - web automation with [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)
- [schedule](https://schedule.readthedocs.io/en/stable/installation.html) - task scheduling
- [twilio](https://www.twilio.com/docs/voice/quickstart/python) - phone calls

## 🚀 Setup

1. Create a `secrets` folder in the parent directory
2. Create `guibot.py` in the secrets folder with the following variables:
   - `GMAIL_SENDER`: Email address for sending notifications
   - `GMAIL_APP_PASSWORD`: [Google app password](https://myaccount.google.com/apppasswords) for authentication
   - `EMAIL1`: Primary email recipient for notifications
   - `EMAIL2`: Secondary email recipient
   - `TWILIO_ACCOUNT_SID`: Twilio account SID (for phone calls)
   - `TWILIO_AUTH_TOKEN`: Twilio auth token
   - `TWILIO_PHONE_NUMBER`: Twilio phone number
   - `PHONE`: Phone number for notifications
3. Create a `screenshots` folder in the scripts directory

## 🧪 Testing

The `tests` folder in the parent directory of this repository contains individual Python files for testing various components:
- Selenium web automation
- Email sending
- Email attachments
- Twilio phone calls

## 📝 Usage

### Ausländeramt script
```bash
python3 auslaenderamt_err_server.py
```
- Checks random team (1, 2, or 3) for appointments
- Default interval: 20 seconds
- Sends email and calls when appointments found

### Führerscheinstelle script
```bash
python3 fuhrerscheinstelle_err.py
```
- Checks for foreign license conversion appointments
- Default interval: 30 seconds
- Email notifications only

### Combined script
```bash
python3 combined_run.py
```
- Runs both scripts sequentially
- Default interval: 3 minutes

## ⚙️ Customization

Adjust checking intervals by modifying:
```python
schedule.every(20).seconds.do(check_for_appt)  # Ausländeramt
schedule.every(30).seconds.do(check_for_appt)  # Führerscheinstelle
schedule.every(3).minutes.do(check_for_appts)  # Combined script
```

## 🖥️ Deployment

While these scripts can be run locally, they were designed to run on a remote instance. The recommended setup uses an `e2-small` Compute Engine instance on Google Cloud Platform (GCP) with Chrome Remote Desktop for Linux. Follow the setup guide [here](https://cloud.google.com/architecture/chrome-desktop-remote-on-compute-engine).