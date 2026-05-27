import dns.resolver
import dns.zone
import dns.query
import threading
import queue
import sys
import os

class DNSReconAgent:
    """
    Chimera Agent 56: DNS Reconnaissance (The Completionist)
    Location: ~/chimera/agents/56_DNS_Recon/src/main.py
    """
    def __init__(self, domain, threads=40):
        self.domain = domain
        self.threads = threads
        self.task_queue = queue.Queue()
        self.live_hosts = []
        
        # Pathing: Look one directory up for subs.txt
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.wordlist_path = os.path.join(base_dir, "subs.txt")

    def _attempt_axfr(self):
        """Attempts a Zone Transfer (AXFR) on the domain's Name Servers."""
        print(f"[*] Agent 56: Attempting Zone Transfer (AXFR) for {self.domain}...")
        try:
            ns_answers = dns.resolver.resolve(self.domain, 'NS')
            for ns in ns_answers:
                ns_name = str(ns.target)
                try:
                    # Resolve NS name to IP for the query
                    ns_ip = dns.resolver.resolve(ns_name, 'A')[0].to_text()
                    print(f"[*] Agent 56: Querying NS: {ns_name} ({ns_ip})")
                    
                    zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, self.domain))
                    if zone:
                        print(f"[!!!] Agent 56: AXFR SUCCESSFUL on {ns_name} [!!!]")
                        for name, node in zone.nodes.items():
                            record_name = f"{name}.{self.domain}"
                            print(f"  [+] AXFR Record: {record_name}")
                            self.live_hosts.append({"host": record_name, "type": "AXFR"})
                except Exception:
                    print(f"[-] Agent 56: AXFR failed on {ns_name}")
        except Exception as e:
            print(f"[!] Agent 56: Could not retrieve Name Servers: {e}")

    def _load_wordlist(self):
        if not os.path.exists(self.wordlist_path):
            print(f"[!] Agent 56 Error: Wordlist missing at {self.wordlist_path}")
            return False
        with open(self.wordlist_path, 'r') as f:
            for line in f:
                word = line.strip()
                if word: self.task_queue.put(word)
        return True

    def _resolver_worker(self):
        while not self.task_queue.empty():
            sub = self.task_queue.get()
            target = f"{sub}.{self.domain}"
            try:
                answers = dns.resolver.resolve(target, 'A')
                ips = [str(rdata) for rdata in answers]
                print(f"[+] Agent 56: {target} -> {ips}")
                self.live_hosts.append({"host": target, "ips": ips, "type": "Brute"})
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
                pass
            finally:
                self.task_queue.task_done()

    def run(self):
        # Phase 1: The Goldmine Attempt
        self._attempt_axfr()
        
        # Phase 2: Active Brute Force
        if not self._load_wordlist(): return
        print(f"[*] Agent 56: Starting Brute Force on {self.domain}...")
        
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._resolver_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        self.task_queue.join()
        print(f"[*] Agent 56: Recon complete. Total unique records: {len(self.live_hosts)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_domain>")
        sys.exit(1)
    
    agent = DNSReconAgent(sys.argv[1])
    agent.run()
