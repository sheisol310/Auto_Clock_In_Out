#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import smtplib
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

#########################
# CONFIGURATION
#########################

# enable the app to work in headless mode (without GUI)
enable_headless = False
#########################
# enable email notification
enable_email_notification = True
# Email notification settings (using your Gmail + App Password)
# SMTP settings (default for Gmail, you can change it to your SMTP server)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your email address"
EMAIL_TO = "your email address or the recipient's email address"
SMTP_PASS = "gmail app token, or other app token"

#########################
# NUEIP login details
COMPANY_CODE = "your company code"
EMPLOYEE_ID = "your employee ID"
PASSWORD = "your password"
#########################
# Special days configuration:
HOLIDAYS = [
    "2025-01-01",  # Republic Day/New Year's Day
    "2025-01-27",  # Lunar New Year Holiday
    "2025-01-28",  # Lunar New Year's Eve
    "2025-01-29",  # Lunar New Year's Day
    "2025-01-30",  # Lunar New Year Holiday
    "2025-01-31",  # Lunar New Year Holiday
    "2025-02-01",  # Lunar New Year Holiday
    "2025-02-02",  # Lunar New Year Holiday
    "2025-02-28",  # Peace Memorial Day
    "2025-04-03",  # Children's Day/Tomb Sweeping Day Holiday
    "2025-04-04",  # Tomb Sweeping Day
    "2025-04-04",  # Children's Day
    "2025-05-01",  # Labor Day
    "2025-05-30",  # Dragon Boat Festival Holiday
    "2025-05-31",  # Dragon Boat Festival
    "2025-10-06",  # Mid-Autumn Festival
    "2025-10-10",  # National Day
]
SPECIAL_WORKDAYS = [
    # e.g. "2025-03-30",
]
LEAVE_DAYS = [
    # e.g. "2025-04-01",
]


#########################
# UTILITY FUNCTIONS
#########################

def send_notification(subject, body):
    """Send an email notification using Gmail SMTP if notifications are enabled."""
    if not enable_email_notification:
        return
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = EMAIL_TO
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print("[INFO] Email notification sent successfully.")
    except Exception as e:
        print(f"[WARN] Failed to send email notification: {e}")


def is_today_a_workday():
    """
    Determine if today is a workday.
    Skips if today is weekend (Saturday or Sunday) or if it's in HOLIDAYS,
    unless it is explicitly in SPECIAL_WORKDAYS.
    """
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if today_str in HOLIDAYS:
        print(f"[INFO] Today ({today_str}) is marked as a holiday.")
        return False
    
    if today_str in LEAVE_DAYS:
        print(f"[INFO] Today ({today_str}) is marked as a leave day.")
        return False
    
    if today_str in SPECIAL_WORKDAYS:
        print(f"[INFO] Today ({today_str}) is a special workday.")
        return True
    
    weekday = datetime.datetime.now().weekday()  # Monday=0 ... Sunday=6
    if weekday >= 5:
        print(f"[INFO] Today is weekend (weekday={weekday}). Skipping clock action.")
        return False
    
    return True


#########################
# MAIN FUNCTIONALITY
#########################

def clock_in_or_out(action="clock_in"):
    """
    Launch Chrome via Selenium, log into NUEIP, and perform clock in or out.
    Then, send an email notification with a success or error message.
    """
    
    # Check if today is a workday. If not, report failure with an error message.
    if not is_today_a_workday():
        
        msg = (f"Clock action '{action}' failed on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
               f"because it is a weekend, holiday, or leave day.")
        print("[ERROR]", msg)
        send_notification("Clock Action Failed - Non Workday", msg)
        return
    
    try:
        # Create a Service object from webdriver_manager
        service = Service(ChromeDriverManager().install())
        # Set Chrome options
        options = webdriver.ChromeOptions()
        
        # Add options for headless mode if specified
        if enable_headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        
        # Launch Chrome using that service and options
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        error_msg = f"Failed to launch Chrome WebDriver: {e}"
        print("[ERROR]", error_msg)
        send_notification("NUEIP Clock Script Error", error_msg)
        return
    
    try:
        # 1. Navigate to the login page
        driver.get("https://portal.nueip.com/home")
        
        # 2. Set up an explicit wait (up to 60 seconds)
        wait = WebDriverWait(driver, 60)
        
        # 3. Wait for the login button to be clickable and fill out the login form
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.login-button")))
        
        company_field = driver.find_element(By.NAME, "inputCompany")
        employee_field = driver.find_element(By.NAME, "inputID")
        password_field = driver.find_element(By.NAME, "inputPassword")
        
        # Set values and dispatch input events
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            company_field,
            COMPANY_CODE
        )
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            employee_field,
            EMPLOYEE_ID
        )
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            password_field,
            PASSWORD
        )
        
        # 4. Click the login button
        login_button.click()
        
        # 5. Wait until the clock area loads by waiting for an element with class 'por-punch-clock'
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'por-punch-clock')]")))
        
        # 6. Build XPath for the punch button based on the action
        if action == "clock_in":
            # "上班" button for clock in
            punch_xpath = (
                "//div[contains(@class,'por-punch-clock')]//button[contains(@class,'punch-button') "
                "and .//span[text()='上班']]"
            )
        else:
            # "下班" button for clock out
            punch_xpath = (
                "//div[contains(@class,'por-punch-clock')]//button[contains(@class,'punch-button') "
                "and .//span[text()='下班']]"
            )
        
        # 7. Wait for the punch button to be clickable
        try:
            punch_button = wait.until(EC.element_to_be_clickable((By.XPATH, punch_xpath)))
            print("[INFO] Punch button found.")
        except TimeoutException:
            raise NoSuchElementException(f"Punch button for '{action}' not found.")
        
        # 8. Click the punch button
        punch_button.click()
        # print(f"[TEST] Clicked the punch button.")
        time.sleep(3)
        
        # 9. Report success
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success_msg = f"Successfully executed '{action}' on {now}."
        print("[SUCCESS]", success_msg)
        send_notification(f"Clock {action.replace('_', ' ').title()} Success", success_msg)
    
    except (NoSuchElementException, TimeoutException) as e:
        error_msg = f"Error during '{action}': {e}"
        print("[ERROR]", error_msg)
        send_notification(f"NUEIP Clock {action.replace('_', ' ').title()} Error", error_msg)
    except Exception as ex:
        error_msg = f"Unexpected error during '{action}': {ex}"
        print("[ERROR]", error_msg)
        send_notification(f"NUEIP Clock {action.replace('_', ' ').title()} Error", error_msg)
    finally:
        # Keep browser open a bit for observation (if not headless), then quit
        time.sleep(5)
        driver.quit()


def main():
    if len(sys.argv) < 2:
        print("Usage: python nueip_clock.py [clock_in | clock_out]")
        sys.exit(1)
    
    action = sys.argv[1]
    if action not in ("clock_in", "clock_out"):
        print("Invalid argument. Use 'clock_in' or 'clock_out'.")
        sys.exit(1)
    
    clock_in_or_out(action)


if __name__ == "__main__":
    main()