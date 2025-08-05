import os
import sys
import json
import sqlite3
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

import tkinter as tk
from tkinter import simpledialog, messagebox
import webbrowser

CONFIG_FILE = "ctnotifier_config.json"
STARTUP_SHORTCUT_NAME = "ColdTurkeyBlockerNotifier.lnk"
DB_PATH = r"C:\ProgramData\Cold Turkey\data-browser.db"
LOG_FILE = "coldturkey_monitor.log"
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

# --- UTILITIES FOR WINDOWS STARTUP INTEGRATION ---
def get_startup_dir():
    return os.path.join(
        os.environ['APPDATA'],
        r'Microsoft\Windows\Start Menu\Programs\Startup'
    )

def add_to_startup():
    try:
        import pythoncom
        from win32com.client import Dispatch
        shortcut_path = os.path.join(get_startup_dir(), STARTUP_SHORTCUT_NAME)
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(sys.argv[0])
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = exe_path
        shortcut.save()
        return True
    except Exception as e:
        log_to_file(f"Startup add failed: {e}")
        return False

def is_in_startup():
    return os.path.exists(os.path.join(get_startup_dir(), STARTUP_SHORTCUT_NAME))

def prompt_startup_consent():
    root = tk.Tk()
    root.withdraw()
    ans = messagebox.askyesno(
        "Run at Startup?",
        "Should Cold Turkey Blocker Notifier run automatically when you log in to Windows?"
    )
    root.destroy()
    return ans

# --- GUI-ONLY CREDENTIAL PROMPT ---
def gui_prompt():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(
        "First-time Setup", 
        "This is your first time running Cold Turkey Blocker Notifier.\n\n"
        "Please enter your details. These will be stored locally."
    )

    email = simpledialog.askstring("Email Address", "Enter your Gmail address:", parent=root)
    if not email: sys.exit()
    messagebox.showinfo(
        "Get Gmail App Password",
        "Google requires 'App Passwords' for access.\n\n"
        "1. Turn on 2-Step Verification.\n"
        "2. Go to the App Passwords page (will open now).\n"
        "3. Generate a new password for 'Mail'."
    )
    webbrowser.open("https://myaccount.google.com/apppasswords")
    password = simpledialog.askstring("App Password", "Paste your App Password here:\n(App Passwords are NOT your Gmail login password)", show="*", parent=root)
    if not password: sys.exit()
    recipient = simpledialog.askstring("Recipient Email", "Enter recipient email address:", parent=root)
    if not recipient: sys.exit()

    config = {
        "email_address": email,
        "email_password": password,
        "recipient": recipient,
        "startup_checked": False  # marks if user has ever been asked about startup
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)
    root.destroy()

def get_config():
    if not os.path.exists(CONFIG_FILE):
        gui_prompt()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def set_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)

def log_to_file(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

# --- EMAIL SENDING ---
def send_email(email_address, email_password, recipient, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_address
    msg["To"] = recipient
    try:
        with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, recipient, msg.as_string())
        return True
    except Exception as e:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        log_to_file(f"[{now_str}] Email send failed: {e}")
        return False

def get_latest_blocked_domains(last_seen_timestamp):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT date, domain FROM statsBlocked WHERE date > ? ORDER BY date ASC", (last_seen_timestamp,))
    results = cur.fetchall()
    conn.close()
    return results

def get_current_max_date():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT MAX(date) FROM statsBlocked")
    result = cur.fetchone()
    conn.close()
    return result[0] if result and result[0] else 0

# --- MAIN LOGIC ---
def main():
    config = get_config()
    # Only ask about startup shortcut once, and only if not present already
    if not config.get("startup_checked"):
        if not is_in_startup():
            if prompt_startup_consent():
                if add_to_startup():
                    log_to_file("Added to startup.")
                else:
                    log_to_file("Failed to add to startup.")
        config['startup_checked'] = True
        set_config(config)

    email_address = config["email_address"]
    email_password = config["email_password"]
    recipient = config["recipient"]

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("Cold Turkey Notifier Log\n")
    if not os.path.exists(DB_PATH):
        log_to_file("Database file not found.")
        return
    last_seen = get_current_max_date()
    log_to_file("Monitoring started.")
    while True:
        new_blocks = get_latest_blocked_domains(last_seen)
        for date, domain in new_blocks:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
            log_message = f"[{now_str}] Blocked: {domain}"
            log_to_file(log_message)
            send_email(
                email_address, email_password, recipient,
                "Cold Turkey Blocked",
                f"Your friend tried to visit: {domain} at {now_str}"
            )
            if date > last_seen:
                last_seen = date
        time.sleep(10)

if __name__ == "__main__":
    main()
