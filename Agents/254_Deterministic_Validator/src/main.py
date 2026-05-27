#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
import requests

class DeterministicValidator:
    """
    Agent 319 Pro: Hybrid Validation Engine.
    Categorizes findings as [VERIFIED] (Deterministic proof) 
    or [FLAGGED] (Heuristic suspicion) to reduce AI hallucinations.
    """
    def __init__(self):
        self.canary_id = "CHIMERA-VSS-9921-X"
        self.status_codes = {
            "verified": "[\033[92mVERIFIED\033[0m]", # Green
            "flagged": "[\033[93mFLAGGED - UNVERIFIED\033[0m]" # Yellow
        }

    def _analyze_response_heuristics(self, response_text, status_code):
        """Heuristic check for common indicators of a successful 'hit' without proof."""
        indicators = ["sql syntax", "uid=", "root:", "mysql_fetch", "stack trace", "Internal Server Error"]
        for indicator in indicators:
            if indicator.lower() in response_text.lower():
                return True, f"Suspicious pattern found: '{indicator}'"
        if status_code == 500:
            return True, "Target returned 500 Error (Potential Crash/Overflow)"
        return False, None

    def validate_file_read(self, retrieved_content, raw_response):
        """Checks for Canary first, then falls back to Heuristics."""
        if self.canary_id in retrieved_content:
            return "verified", "Canary string confirmed in file content."
        
        is_suspicious, reason = self._analyze_response_heuristics(raw_response, 200)
        if is_suspicious:
            return "flagged", f"Heuristic Match: {reason}"
        
        return None, "No evidence of vulnerability found."

    def validate_sqli(self, fast_url, slow_url):
        """Timing analysis with a fallback for 'Flagged' if timing is inconsistent."""
        start = time.time()
        r1 = requests.get(fast_url, timeout=10)
        t1 = time.time() - start
        
        start = time.time()
        r2 = requests.get(slow_url, timeout=10)
        t2 = time.time() - start
        
        # High Confidence: Clear timing difference
        if t2 > (t1 + 4):
            return "verified", f"Deterministic timing delta: {t2:.2f}s vs {t1:.2f}s"
        
        # Medium Confidence: Response changed or error code triggered
        if r1.status_code != r2.status_code or "error" in r2.text.lower():
            return "flagged", "Response behavior changed during injection attempt."
            
        return None, "Timing and behavior remained consistent."

    def execute(self, vuln_type, evidence_content, raw_resp=""):
        print("--- [AGENT 319: HYBRID VALIDATION SEQUENCE] ---")
        
        status = None
        message = ""

        if vuln_type == "file_read":
            status_key, message = self.validate_file_read(evidence_content, raw_resp)
        elif vuln_type == "sqli":
            # Expects evidence as 'fast_url,slow_url'
            f, s = evidence_content.split(',')
            status_key, message = self.validate_sqli(f, s)
        else:
            status_key, message = None, "Unsupported vulnerability type."

        if status_key:
            prefix = self.status_codes.get(status_key)
            print(f"{prefix} {message}")
            return status_key
        else:
            print(f"[!] REJECTED: {message}")
            return "null"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./main.py <type> <evidence_data> [optional_raw_resp]")
        sys.exit(1)
    
    raw = sys.argv[3] if len(sys.argv) > 3 else ""
    DeterministicValidator().execute(sys.argv[1], sys.argv[2], raw)
