#!/home/dan/Chimera_Project/venv/bin/python3
import requests
import sys
import os
import random
from concurrent.futures import ThreadPoolExecutor

class DirectoryBruter:
    """
    Agent 03: High-Performance Directory/File Discovery.
    Implements multi-threaded HTTP probing with status code filtering
    and User-Agent randomization to bypass basic edge security.
    """
    def __init__(self, target_url, wordlist=None):
        self.target = target_url.rstrip('/')
        self.wordlist = wordlist if wordlist else "/usr/share/wordlists/dirb/common.txt"
        self.loot_file = f"/home/dan/Chimera_Project/agents/03_Directory_Bruter/loot/brute_{self.target.replace('://', '_').replace('/', '_')}.txt"
        
        # --- EVASION PRIMITIVES ---
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.0 Safari/537.36"
        ]

    def _probe_path(self, path):
        """Perform a single HTTP probe with randomized headers."""
        path = path.strip()
        if not path or path.startswith('#'):
            return

        url = f"{self.target}/{path}"
        headers = {'User-Agent': random.choice(self.user_agents)}
        
        try:
            # We use allow_redirects=False to see exactly where the server is pushing us
            r = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
            
            # Actionable Status Codes: 200 (OK), 204 (No Content), 301/302 (Redirect), 403 (Forbidden/Sensitive)
            if r.status_code in [200, 204, 301, 302, 401, 403]:
                result = f"[{r.status_code}] {url}"
                print(f"    [>] {result}")
                return result
        except Exception:
            pass
        return None

    def execute(self, threads=30):
        print(f"--- [AGENT 03: DIRECTORY BRUTEFORCE - {self.target}] ---")
        
        if not os.path.exists(self.wordlist):
            print(f"[!] FATAL: Wordlist not found at {self.wordlist}")
            return

        with open(self.wordlist, 'r') as f:
            paths = f.readlines()

        print(f"[*] THREADING: {threads} Workers | WORDLIST: {len(paths)} lines")
        
        discovered = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = executor.map(self._probe_path, paths)
            for r in results:
                if r:
                    discovered.append(r)

        # Intelligence Commitment
        if discovered:
            with open(self.loot_file, 'w') as f:
                f.write("\n".join(discovered))
            print(f"[!!!] BRUTE COMPLETE: {len(discovered)} paths committed to {self.loot_file}")
        else:
            print("[-] No actionable paths discovered.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <http://target.com> [wordlist_path]")
        sys.exit(1)
        
    url = sys.argv[1]
    wlist = sys.argv[2] if len(sys.argv) > 2 else None
    
    bruter = DirectoryBruter(url, wlist)
    bruter.execute()
