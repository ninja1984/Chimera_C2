import os
import sys
import subprocess
import fcntl
import struct

# Tun/Tap constants
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

def create_ghost_interface(iface_name="ghi0"):
    """
    Weaponized Ghost Interface: Creates a persistent TUN/TAP device 
    for covert data routing.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Network interface manipulation requires UID 0.")
        sys.exit(1)

    print(f"[*] Provisioning Ghost Interface: {iface_name}...")

    try:
        # Open the tun device clone shift
        tun = os.open("/dev/net/tun", os.O_RDWR)
        
        # Structure for the interface request
        ifr = struct.pack("16sH", iface_name.encode(), IFF_TUN | IFF_NO_PI)
        fcntl.ioctl(tun, TUNSETIFF, ifr)

        print(f"[!] {iface_name} allocated. Configuring IP stack...")

        # Bring the interface up and assign a non-standard internal IP
        subprocess.run(["ip", "addr", "add", "10.255.255.1/30", "dev", iface_name], check=True)
        subprocess.run(["ip", "link", "set", iface_name, "up"], check=True)

        print(f"[!!!] SUCCESS: Ghost Interface {iface_name} is LIVE.")
        print("[*] Note: To hide from 'ip link', use Agent 180 (Netlink Filter).")

        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: GHOST_INTERFACE | Name: {iface_name} | IP: 10.255.255.1\n")

        # Keep the process alive to hold the FD open
        while True:
            import time
            time.sleep(100)

    except Exception as e:
        print(f"[-] Interface Fault: {e}")

if __name__ == "__main__":
    create_ghost_interface()
