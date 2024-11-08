# 🥇 Olympics Store checker

Automated script to check for availability of items on the official Olympics online store and send email notifications when it's in stock.

Built by [Gui Ruggiero](https://guiruggiero.com/?utm_source=github&utm_medium=guibot).

> **Note**: Code works as of November 2024. Updates may be needed if the Olympics Store website changes how out of stock items are displayed.

## ✨ Features

- Automated checking at configurable intervals
- Email notifications when the item is back in stock
- Error monitoring and notifications

## 🛠️ Prerequisites

- Python 3.x
- Chrome browser
- Chrome WebDriver

## 📦 Required Python packages

```bash
pip install selenium schedule
```

- [selenium](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/) - web automation with [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)
- [schedule](https://schedule.readthedocs.io/en/stable/installation.html) - task scheduling

## 🚀 Setup

1. Create a `secrets` folder in the parent directory
2. Create `guibot.py` in the secrets folder with the following variables:
   - `GMAIL_SENDER`: Email address for sending notifications
   - `GMAIL_APP_PASSWORD`: [Google app password](https://myaccount.google.com/apppasswords) for authentication
   - `EMAIL1`: Primary email recipient for notifications

## 🧪 Testing

The `tests` folder in the parent directory of this repository contains individual Python files for testing various components:
- Selenium web automation
- Email sending
- Email attachments

## 📝 Usage

```bash
python3 olympics_pin.py
```

## ⚙️ Customization

You can adjust the checking interval by modifying the following line in the script:

```python
schedule.every(5).minutes.do(check_for_stock)
```

You can also check other items by changing the URL of the product in the Olympics Store:

```python
url = "https://shop.olympics.com/en/paris-2024/paris-2024-olympics-pin-badge/t-4588774218+p-125766430724+z-8-4134459471"
```

## 🖥️ Deployment

While this script can be run locally, it was designed to run on a remote instance. The recommended setup uses an `e2-micro` Compute Engine instance on Google Cloud Platform (GCP), which is free. There is no need for a GUI, as script does not manipulate the website directly - instead, it just fetches the page source and analyzes it.