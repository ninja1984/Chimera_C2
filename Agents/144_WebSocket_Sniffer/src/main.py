import sys
import websocket
import json
import os
import threading

def on_message(ws, message):
    """
    Callback for intercepted frames. Scans for 'admin', 'password', or 'token'.
    """
    print(f"\n[!] INTERCEPTED FRAME: {message}")
    
    # Automated sensitive data detection
    sensitive_keywords = ["admin", "pass", "token", "auth", "session", "key"]
    if any(key in message.lower() for key in sensitive_keywords):
        print("[!!!] SENSITIVE DATA DETECTED IN WEBSOCKET STREAM [!!!]")
        with open("../loot/ws_intercept.log", "a") as f:
            f.write(f"PID {os.getpid()} - {message}\n")

def on_error(ws, error):
    print(f"[-] WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("[*] WebSocket Connection Closed.")

def start_sniffer(url, injection_payload=None):
    """
    Weaponized Sniffer: Connects and maintains the socket. 
    If a payload is provided, it injects it immediately after handshake.
    """
    print(f"[*] Attaching to Sovereign Socket: {url}")
    
    def run():
        ws = websocket.WebSocketApp(url,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
        
        # Primitive for Frame Injection
        if injection_payload:
            def on_open(ws):
                print(f"[*] Injecting Frame: {injection_payload}")
                ws.send(injection_payload)
            ws.on_open = on_open
            
        ws.run_forever()

    # Run in thread to allow for future multi-socket scaling
    t = threading.Thread(target=run)
    t.start()
    t.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 131_ws_sniff <wss_url> [optional_injection_json]")
        sys.exit(1)
    
    payload = sys.argv[2] if len(sys.argv) > 2 else None
    start_sniffer(sys.argv[1], payload)
