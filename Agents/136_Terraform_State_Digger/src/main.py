import json, sys, os
def dig(path):
    with open(path, 'r') as f: data = json.load(f)
    secrets = {k: v for k, v in data.get('outputs', {}).items() if 'pass' in k.lower() or 'key' in k.lower()}
    print(json.dumps(secrets, indent=2))
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: 123_tf <state_file>"); sys.exit(1)
    dig(sys.argv[1])
