# 🤖 Olympics Pin Checker

Automated script to check for availability of the 2024 Olympics pin on the official Olympics online store and send email notifications when it's in stock.

Built by [Gui Ruggiero](https://guiruggiero.com/).

## ✨ Features

- Automated checking at configurable intervals
- Email notifications when the pin is back in stock
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

Keep checking intervals reasonable to avoid overloading the website.

## 🖥️ Deployment

While this script can be run locally, it was designed to run on a remote instance. The recommended setup uses an `e2-micro` Compute Engine instance on Google Cloud Platform (GCP), which is free. There is no need for a GUI, as script does not manipulate the website directly - instead, it just fetches the page source and analyzes it.

---

### ⚠️ Disclaimer

This script is provided "as is" without any warranties. Use at your own risk. The author is not responsible for any consequences of using this software, including but not limited to potential website blocking or other issues. Please use responsibly and ensure you comply with all relevant terms of service and regulations.

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. You are free to use, modify, and distribute this software for any purpose, provided you include the original copyright notice and the full license text in any copies or substantial portions of the software. Attribution is required.