import os, sys
def wipe(path):
    if not os.path.exists(path): return
    size = os.path.getsize(path)
    with open(path, "ba+", buffering=0) as f:
        for _ in range(3): # Gutmann-style pass
            f.seek(0); f.write(os.urandom(size))
    os.remove(path)
    print(f"[!] Path Purged: {path}")
if __name__ == "__main__": wipe(sys.argv[1])
