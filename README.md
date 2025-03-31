# NUEIP Auto Clock In/Out Script

---

## Overview

This script automates the process of logging into NUEIP and performing clock in/out actions using Selenium. It is intended **only for employees whose company uses NUEIP** for clocking in and out. Optional email notifications can be sent using Gmail or other SMTP servers.

---

## Requirements

- Python 3.7+
- Google Chrome (installed)
- ChromeDriver

---

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/Auto_Clock_In_Out.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Auto_Clock_In_Out
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Edit the `nueip_clock.py` file at the top to update the configuration:

- **NUEIP Login Details**: Update `COMPANY_CODE`, `EMPLOYEE_ID`, and `PASSWORD`.
- **Email Notification Settings**: Set `enable_email_notification` to `True` if you want to receive email notifications, and configure `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, and `EMAIL_TO`.
- **Gmail Token**: If using Gmail for notifications, generate an app token as shown in [this video](https://www.youtube.com/watch?v=GsXyF5Zb5UY).
- **Holidays and Workdays**: Modify the `HOLIDAYS`, `SPECIAL_WORKDAYS`, and `LEAVE_DAYS` lists as needed.

---

## Usage

To run the script manually:

- Clock in:
  ```bash
  python nueip_clock.py clock_in
  ```
- Clock out:
  ```bash
  python nueip_clock.py clock_out
  ```

---

## Automating with Crontab

You can schedule automatic clock in/out using crontab on macOS/Linux:

1. Open the crontab editor:
   ```bash
   crontab -e
   ```
   - For vi/vim, press `i` to enter insert mode.
2. Add the following lines (adjust paths and times as needed):
   ```cron
   # Clock in every weekday at 08:50 AM
   50 8 * * 1-5 /path/to/python3 /path/to/nueip_clock.py clock_in >> /tmp/clock_in.log 2>&1

   # Clock out every weekday at 18:05 PM
   05 18 * * 1-5 /path/to/python3 /path/to/nueip_clock.py clock_out >> /tmp/clock_out.log 2>&1
   ```
3. Save and exit the editor (in vim, press `Esc` then type `:wq` and hit Enter).
4. Check logs:
   ```bash
   cat /tmp/clock_in.log
   cat /tmp/clock_out.log
   ```
5. List current crontab entries:
   ```bash
   crontab -l
   ```

---

## Keeping Your Mac Awake (Optional)

To ensure scheduled tasks run without interruption (e.g., if your Mac goes to sleep), you can use the `caffeinate` command.

- **Run in the background:**
  ```bash
  caffeinate -dimsu &
  ```
  - To stop: `killall caffeinate`
- **Run interactively:**
  - Run `caffeinate` without `&` to keep the terminal busy; press `Ctrl + C` to exit when no longer needed.

---

## Disclaimer and Regional Settings

- **Region**: This script’s settings (holidays, time zones, etc.) are tailored for Taiwan on macOS. If you are in a different region or using another operating system, you may need to modify the code and commands accordingly.
- **Usage**: This tool is designed solely for companies using NUEIP for clock in/out. Use it at your own risk.
