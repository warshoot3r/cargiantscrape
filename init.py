import os
import signal
import subprocess
import sys
import time

def signal_handler(sig, frame):
    # Send SIGTERM to the main Python script and its subprocesses
    os.killpg(os.getpgid(main_process.pid), signal.SIGTERM)
    sys.exit(0)

if __name__ == "__main__":
    while True:
        main_process = subprocess.Popen(["python", "chatbot_autorun.py"])

        # Set up the signal handler to handle termination signals
        signal.signal(signal.SIGTERM, signal_handler)

        # Wait for the main process to finish
        main_process.wait()
        time.sleep(3600)