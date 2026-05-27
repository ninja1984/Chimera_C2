import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

sys.path.append('/home/dan/Chimera_Project')
from core.db_handler import ChimeraDB

class ChimeraSpider:
    def __init__(self, base_url, db):
        self.base_url = base_url
        self.db = db
        self.visited = set()
        self.to_visit = [base_url]
        self.domain = urlparse(base_url).netloc

    def crawl(self):
        print(f"[*] Starting crawl on {self.base_url}...")
        
        while self.to_visit:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue
            
            try:
                r = requests.get(url, timeout=5)
                self.visited.add(url)
                
                if r.status_code == 200:
                    print(f"\033[92m[+] Indexed: {url}\033[0m")
                    self.db.report_finding("46_Web_Spider", "URL_Indexed", {
                        "url": url,
                        "status": 200
                    })
                    
                    # Parse for more links
                    soup = BeautifulSoup(r.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        full_url = urljoin(self.base_url, link['href'])
                        
                        # Only stay on the target domain
                        if urlparse(full_url).netloc == self.domain and full_url not in self.visited:
                            self.to_visit.append(full_url)
                            
            except Exception as e:
                print(f"[!] Error crawling {url}: {e}")

def run():
    db = ChimeraDB()
    os.system('clear')
    print("\033[33m" + "="*60)
    print("   CHIMERA AGENT 46 :: AUTONOMOUS WEB SPIDER")
    print("="*60 + "\033[0m")

    target_url = input("[?] Target URL: ").strip()
    if not target_url.startswith("http"):
        target_url = f"http://{target_url}"

    spider = ChimeraSpider(target_url, db)
    spider.crawl()

    print(f"\n[*] Crawl complete. {len(spider.visited)} URLs indexed in Neo4j.")
    db.close()

if __name__ == "__main__":
    run()
