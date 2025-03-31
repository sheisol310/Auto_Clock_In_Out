## NUEIP Auto Clock In/Out Script - Setup Instructions

### Step 1: Verify Requirements
Ensure your system meets these prerequisites:
- **Python 3.7 or higher** is installed.
- **Google Chrome** is installed.
- **ChromeDriver** is installed and matches your Chrome version.

---

### Step 2: Install the Script
1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/yourusername/Auto_Clock_In_Out.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd Auto_Clock_In_Out
   ```
3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

---

### Step 3: Configure the Script
Open `nueip_clock.py` in a text editor and update the following sections:

#### 3.1 Update NUEIP Login Details
- Set `COMPANY_CODE`, `EMPLOYEE_ID`, and `PASSWORD` to your NUEIP credentials.

#### 3.2 Adjust Holidays and Workdays (Optional)
- Modify `HOLIDAYS`, `SPECIAL_WORKDAYS`, and `LEAVE_DAYS` lists as needed.

---

### Step 4: Set Up Headless Mode
- **What is Headless Mode?** Runs Chrome in the background without opening a visible browser window.
- **Why Use It?** Prevents the browser from popping up during scheduled tasks, making automation seamless.
- **How to Enable:**
   1. In `nueip_clock.py`, set `enable_email_notification = True` if you want the app to run in the background.
   2. In `nueip_clock.py`, set `enable_email_notification = False` if you want to see the app running. 
- **Test It:** Run the script manually with headless mode to ensure it works without issues.

---

### Step 5: Set Up Email Notifications
- **Why Use It?** Receive confirmations or alerts about clock in/out actions, ensuring the automation is working as expected.
- **How to Set Up:**
  1. In `nueip_clock.py`, set `enable_email_notification = True`.
  2. Update the following:
     - `SMTP_SERVER`: Your email provider’s SMTP server (e.g., `smtp.gmail.com` for Gmail).
     - `SMTP_PORT`: Typically `587` for TLS.
     - `SMTP_USER`: Your email address.
     - `SMTP_PASS`: Your email password or an app-specific token.
     - `EMAIL_TO`: The recipient’s email (can be the same as `SMTP_USER`).
  3. **For Gmail Users:**
     - Generate an app-specific token (not your regular password). Follow [this video](https://www.youtube.com/watch?v=GsXyF5Zb5UY) for instructions.
     - Use this app password (token) as `SMTP_PASS`.
- **Test It:** Run the script manually and check if you receive an email.

---

### Step 6: Test the Script Manually
- **Clock in**:
  ```bash
  python nueip_clock.py clock_in
  ```
- **Clock out**:
  ```bash
  python nueip_clock.py clock_out
  ```
- Verify the actions in NUEIP and check for errors in the terminal.

---

### Step 7: Automate with Crontab (macOS/Linux)
1. **Open crontab editor**:
   ```bash
   crontab -e
   ```
2. **Add cron jobs**:
   - **Do Not Forget To  Adjust File Paths and Times**
   ```cron
   # Clock in at 08:50 AM, weekdays
   50 8 * * 1-5 /path/to/python3 /path/to/nueip_clock.py clock_in >> /tmp/clock_in.log 2>&1

   # Clock out at 18:05 PM, weekdays
   05 18 * * 1-5 /path/to/python3 /path/to/nueip_clock.py clock_out >> /tmp/clock_out.log 2>&1
   ```
4. **Save and exit** (in vim, press `Esc`, type `:wq`, Enter).
5. **Check logs**:
   ```bash
   cat /tmp/clock_in.log
   cat /tmp/clock_out.log
   ```

---

### Step 8: Keep Your Mac Awake (Optional, macOS Only)
To prevent sleep from interrupting tasks:
- **Run in background**:
  ```bash
  caffeinate -dimsu &
  ```
  - Stop with `killall caffeinate`.
- **Run interactively**:
  ```bash
  caffeinate
  ```
  - Press `Ctrl + C` to stop.

---

### Step 9: Consider Regional Adjustments
- The script is set for **Taiwan** (holidays, time zones) and **macOS**. Adjust for other regions or OS:
  - Modify holiday lists.
  - Use a different scheduler (e.g., Task Scheduler on Windows).

---

### Important Notes
- This script is **only for companies using NUEIP**.
- Use at your own risk and ensure compliance with company policies.

---

By following these steps, you’ll have the NUEIP Auto Clock In/Out Script fully configured, with headless mode and email notifications set up as critical components for a smooth automation experience. Let me know if you need further assistance!
