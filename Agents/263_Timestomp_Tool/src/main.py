#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
import random
import subprocess

class TimelineGhost:
    """
    Agent 408 (Hardened): Advanced Forensic Timestomper.
    Synchronizes file timestamps with legitimate system 'Reference' 
    files while injecting sub-second jitter to evade pattern analysis.
    """
    def __init__(self):
        # High-traffic reference files that likely have old timestamps
        self.references = ["/etc/hosts", "/etc/passwd", "/bin/ls", "/etc/fstab"]

    def stomp(self, target_path, reference_path=None):
        """Matches target timestamps to a reference file with jitter."""
        if not os.path.exists(target_path):
            print(f"[!] Target {target_path} not found.")
            return False

        if not reference_path:
            reference_path = random.choice(self.references)

        print(f"[*] Blending {target_path} with {reference_path}...")

        try:
            # 1. Get reference stats
            ref_stat = os.stat(reference_path)
            ref_atime = ref_stat.st_atime
            ref_mtime = ref_stat.st_mtime

            # 2. Inject sub-second jitter (± 500ms) 
            # This prevents 'Identical Timestamp' alerts in forensic tools
            jitter = random.uniform(-0.5, 0.5)
            new_atime = ref_atime + jitter
            new_mtime = ref_mtime + jitter

            # 3. Apply Access and Modify times
            os.utime(target_path, (new_atime, new_mtime))

            # 4. Addressing 'ctime' (The Sieve)
            # You cannot directly set ctime in Linux User-land (it updates on any change).
            # Professional Trick: Set the System Clock back, touch the file, set it forward.
            # This requires Root/CAP_SYS_TIME.
            self._attempt_ctime_stomp(target_path, ref_mtime)

            print(f"[\033[92mSUCCESS\033[0m] {target_path} now mimics {reference_path}")
            return True
        except Exception as e:
            print(f"[!] Stomp failed: {e}")
            return False

    def _attempt_ctime_stomp(self, target, target_time):
        """Advanced: Manipulates system clock to force a specific ctime."""
        # Note: This is 'Loud' on the network (NTP drift) but 'Quiet' on the disk.
        try:
            formatted_time = time.strftime('%Y%m%d%H%M.%S', time.localtime(target_time))
            # Only attempt if we have high privileges
            if os.getuid() == 0:
                subprocess.run(["date", "-s", formatted_time], capture_output=True)
                subprocess.run(["touch", target], capture_output=True)
                # In a real op, we'd immediately resync with NTP here
                print("[+] C-Time manipulation attempted via Clock Drift.")
        except: pass

    def execute(self, target_file):
        print("--- [AGENT 408: TIMELINE GHOST ACTIVE] ---")
        self.stomp(target_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <file_to_hide>")
        sys.exit(1)
    TimelineGhost().execute(sys.argv[1])
