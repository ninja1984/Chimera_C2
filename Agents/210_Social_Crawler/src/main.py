import http.client
import urllib.parse
import sys
import os
import re

def run_social_crawl(target_domain):
    """
    Scrapes public search results for technology stack mentions 
    linked to the target domain (OSINT).
    """
    print(f"[*] [Agent 197] Social-Crawler: Scoping {target_domain}...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    loot_path = os.path.join(script_dir, "..", "loot", "tech_stack_intel.txt")

    # We use a common search engine proxy or direct search query
    # In a military-grade setup, this would use a rotating proxy to avoid CAPTCHAs
    search_host = "www.google.com"
    query = f"site:linkedin.com \"{target_domain}\" OR site:stackoverflow.com \"{target_domain}\""
    encoded_query = urllib.parse.quote(query)
    
    conn = http.client.HTTPSConnection(search_host, timeout=10)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chimera-OSINT/1.0",
        "Accept": "text/html"
    }

    # Tech-stack keywords to look for in the results
    tech_keywords = [
        "nginx", "apache", "docker", "kubernetes", "react", 
        "python", "nodejs", "aws", "azure", "mongodb", "postgresql"
    ]
    
    intel_found = []

    try:
        conn.request("GET", f"/search?q={encoded_query}", headers=headers)
        res = conn.getresponse()
        if res.status == 200:
            content = res.read().decode('utf-8', errors='ignore').lower()
            
            for tech in tech_keywords:
                if tech in content:
                    print(f"[+] INTEL: Potential tech stack match found: {tech}")
                    intel_found.append(f"TECH_STACK_PROBABLE: {tech}")
        else:
            print(f"[!] Search engine blocked the request (Status: {res.status}). Proxy rotation required.")
    except Exception as e:
        print(f"[!] OSINT Crawl failed: {e}")
    finally:
        conn.close()

    if intel_found:
        if not os.path.exists(os.path.dirname(loot_path)):
            os.makedirs(os.path.dirname(loot_path))
        with open(loot_path, "a") as f:
            for item in intel_found:
                f.write(f"{item} (Found via {target_domain} crawl)\n")
        print(f"[*] Intelligence saved to: {loot_path}")
    else:
        print(f"[*] No clear tech-stack mentions found for {target_domain} in top results.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_domain>")
        sys.exit(1)
    
    run_social_crawl(sys.argv[1])
