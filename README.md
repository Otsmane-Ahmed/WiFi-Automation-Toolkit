# Wi-Fi Attack Automation Script

## Description
This script automates the process of **Wi-Fi network scanning, packet capture, and deauthentication attacks** to help security researchers capture WPA/WPA2 handshakes for penetration testing.

## Features
- **Monitor Mode Activation** – Automatically enables monitor mode on `wlan0`.
- **Wi-Fi Network Scanning** – Lists nearby Wi-Fi networks with `airodump-ng`.
- **Packet Capture** – Captures WPA/WPA2 handshakes and saves them as `.cap` files.
- **Deauthentication Attack** – Disconnects all devices from a target network.
- **Multi-Terminal Execution** – Runs deauth attack in a separate terminal.
- **Automatic Cleanup** – Restores Wi-Fi settings when stopped.

## Tested Environment
- **OS:** Kali Linux
- **Wireless Adapter:** TP-Link TL-WN722N (rtl-wn722n chipset)

## Installation

**Note:** After running `iwconfig`, ensure that your network card is recognized as `wlan0`. If it appears as a different name (e.g., `wlan1` or `wlp3s0`), you must modify the script accordingly.

### Prerequisites
Ensure you have the necessary dependencies installed:

```bash
sudo apt update && sudo apt install aircrack-ng
```

### Enable Monitor Mode
Before running the script, ensure your wireless card supports monitor mode:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

## Usage
### Running the Script
To launch the attack, execute:

```bash
python3 wifiauto.py
```

### Step-by-Step Process
1. **Scan for nearby networks** – The script starts `airodump-ng` to list available Wi-Fi networks.
2. **Select a target** – Enter the BSSID and channel of the target network.
3. **Start Packet Capture** – Captures packets in the current terminal.
4. **Launch Deauth Attack** – Opens a new terminal to deauthenticate all connected devices.

### Example Output
#### **Scanning for Networks**
```
Preparing wireless interface...
[NOTE] Wait a few seconds to allow the network card to scan nearby networks before stopping the scan.
Scanning for nearby networks... Press CTRL + C to stop the scan.
```
```
Preparing wireless interface...
Scanning for nearby networks... Press CTRL + C to stop the scan.
```

#### **Starting Capture & Deauth Attack**
```
Enter the target channel: 6
Enter the target BSSID (e.g., 00:14:22:33:44:55): 00:14:22:33:44:55
Starting packet capture in this terminal...
[+] Capturing packets...
Starting deauthentication of all devices in a new window...
[NOTE] Once you see that the 4-way handshake is captured, you can stop both terminals.
```
```
Enter the target channel: 6
Enter the target BSSID (e.g., 00:14:22:33:44:55): 00:14:22:33:44:55
Starting packet capture in this terminal...
[+] Capturing packets...
Starting deauthentication of all devices in a new window...
```

### Stopping the Attack
To stop the attack and restore normal Wi-Fi functionality, press **CTRL + C** in both terminals, or run:

```bash
sudo airmon-ng stop wlan0mon
```

## Verification
To confirm that the 4-way handshake has been successfully captured, open the generated `.cap` file with **Wireshark** and search for `EAPOL`. If results appear, the capture was successful.

## Disclaimer
This tool is intended **for educational and security research purposes only**. Unauthorized use against networks you do not own is **illegal and unethical**. i am  not responsible for any misuse of this tool.

## License
This project is released under the **MIT License**.
