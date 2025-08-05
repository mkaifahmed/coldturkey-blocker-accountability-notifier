# Cold Turkey Blocker Notifier for Accountability Partner

This is an open-source Windows tool that monitors [Cold Turkey](https://getcoldturkey.com/) website blocking activity and instantly emails your accountability partner whenever a blocked site is accessed. Designed for easy setup, robust background operation, and total user privacy.

---

## ✨ Features

- **Automatic Cold Turkey Monitoring**  
  Monitors the Cold Turkey `statsBlocked` database and detects every access attempt to a blocked site.

- **Automatic Email Notifications**  
  Sends your accountability partner an instant email with the blocked domain and timestamp whenever a block event occurs.

- **100% GUI First-Time Setup**  
  On first run, all credential prompts (Gmail, App Password, recipient email) are through friendly graphical dialogs—no command line needed, ever.

- **Gmail App Password Helper**  
  Explains the Google App Password process and automatically opens the App Passwords setup page for you.

- **Runs Silently in Background**  
  After setup, the app runs without a console window (using PyInstaller `--noconsole`).

- **Add to Windows Startup (by User Consent)**  
  After the first setup, you’re asked if you’d like the notifier to launch when Windows starts. If you agree, a shortcut is added automatically.

- **Local Config Storage**  
  Credentials are securely saved in a simple JSON file on your PC—never sent anywhere else.

- **Easy Reset**  
  Simply delete `ctnotifier_config.json` to re-run setup.

---

## 📦 Requirements

- **Windows 10 or 11**  
- **Cold Turkey installed and blocking (database must exist):**  
  By default, database path:  
  `C:\ProgramData\Cold Turkey\data-browser.db`
- **Python 3.x** (for building; not needed for EXE use)  
- **Required pip packages:**  
  - `pywin32`
  - `pyinstaller` (for building the EXE)

---

## 🛠️ Build From Source (Developer Install)

**1. Clone this repo and install Python dependencies:**
pip install pyinstaller
pip install pywin32

**2. Build the EXE with PyInstaller:**
pyinstaller --onefile --noconsole --icon=icon.ico coldturkey_monitor.py

- The output EXE will be in the `dist` directory.

**3. First Run (as EXE, not from Python):**
- `coldturkey_monitor.exe`  
- Enter your Gmail, app password, and partner’s email as prompted by the GUI setup.
- App will prompt for Windows auto-start consent.

---

## 🚀 First-Time Setup (for users)

1. **Download and run the EXE.**
2. **Credential Setup:**  
   GUI prompts for:
   - Your Gmail address
   - Your Gmail [App Password](https://myaccount.google.com/apppasswords)  
     (setup instructions and link provided by the app!)
   - Recipient email for notifications
3. **Startup Integration:**  
   - You’ll be asked if the app should auto-run at Windows login  
4. **That’s it!**  
   - The app now quietly watches for Cold Turkey blocks and notifies your partner.
   - All configs stored as `ctnotifier_config.json` in the working folder.

---

## 💡 Usage Notes

- **No console will appear after initial setup.**
- **All interactions are via friendly dialogs.**
- Reset by deleting the config file and running again.

---

## ⚠️ Troubleshooting

- **Error: `sys.stdin` or “unhandled exception: lost sys.stdin”**  
  > Fix: Always run the EXE, not the script, and ensure you’re using this latest GUI-only version.
- **No notification email is sent:**  
  > Double-check your Gmail App Password, internet connection, and recipient’s email address.
- **Database not found:**  
  > Cold Turkey must be installed and blocking for the database to exist.
- **Startup shortcut not appearing:**  
  > Make sure you click “Yes” when prompted, and that your antivirus is not blocking the shortcut creation.

---

## 🛡️ Privacy

- Your email and partner’s email stay on your device, never sent to anyone else.

---

## 📝 License

This project is public domain—use, modify, and distribute freely!

---

## 🙏 Contributions

Ideas & improvements welcome!  
Open an issue or pull request to help make this even better for others seeking accountability.

