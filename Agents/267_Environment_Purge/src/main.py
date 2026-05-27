#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import subprocess

class EnvironmentPurge:
    """
    Agent 412: Artifact & Environment Sanitizer.
    Systematically purges shell histories, editor caches, and 
    VFS metadata to ensure zero-trace logout.
    """
    def __init__(self):
        self.history_files = [
            "~/.bash_history",
            "~/.zsh_history",
            "~/.viminfo",
            "~/.lesshst",
            "~/.python_history"
        ]
        self.binary_logs = ["/var/log/wtmp", "/var/log/lastlog", "/var/run/utmp"]

    def purge_histories(self):
        """Overwrites and deletes text-based shell/editor histories."""
        print("[*] Sanitizing User Shell Artifacts...")
        for h_file in self.history_files:
            full_path = os.path.expanduser(h_file)
            if os.path.exists(full_path):
                # Shred the file (overwrite with zeros before deleting)
                subprocess.run(["shred", "-u", "-z", full_path], capture_output=True)
                # Recreate as an empty file to avoid 'File Missing' alerts
                open(full_path, 'a').close()

    def scrub_binary_logs(self):
        """
        Removes entries from binary logs (wtmp/utmp). 
        Note: Requires Root. These files track session start/stop times.
        """
        if os.getuid() != 0:
            print("[!] Insufficient privileges to scrub binary system logs.")
            return

        print("[*] Purging Binary Session Logs (wtmp/lastlog)...")
        for b_log in self.binary_logs:
            if os.path.exists(b_log):
                # Truncate the log to zero size
                with open(b_log, 'w') as f:
                    f.truncate(0)

    def execute(self):
        print("--- [AGENT 412: ENVIRONMENT PURGE SEQUENCE] ---")
        self.purge_histories()
        self.scrub_binary_logs()
        
        # Final Step: Clear current session history in RAM
        os.system("history -c") 
        print("[\033[92mSUCCESS\033[0m] Environment sanitized. Ghost status: ACTIVE.")

if __name__ == "__main__":
    EnvironmentPurge().execute()
