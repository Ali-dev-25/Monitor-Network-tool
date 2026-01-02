# Browser Activity Monitor

## Description
A Python-based monitoring tool designed for parental control or self-monitoring.
The script tracks active browser windows on Windows OS and detects visits to specific
websites such as social media platforms. When a match is found, a real-time alert
is sent to a Telegram admin.

---

## Features
- Real-time monitoring of active browser windows
- Keyword-based detection for selected websites
- Instant Telegram alerts with window title information
- Anti-spam logic to prevent duplicate notifications
- Secure handling of sensitive data using environment variables

---

## Tech Stack
- Python 3.x
- pygetwindow and pywin32 for window management
- pywinauto for UI automation and URL reading
- requests for Telegram Bot API communication

---

## Setup and Usage

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/Browser-Activity-Monitor.git
cd Browser-Activity-Monitor

pip install -r requirements.txt

# Platform Support
# Windows OS only

## Authors
Ali Al-Hatami
Khalid Al-Qozi

