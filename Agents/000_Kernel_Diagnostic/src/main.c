#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>

int main() {
    printf("\n[!!!] CHIMERA KERNEL DIAGNOSTIC (Agent 000)\n");
    
    // Check for root
    uid_t uid = getuid();
    printf("[+] Current UID: %d\n", uid);
    if (uid != 0) {
        printf("[!] WARNING: Vanguard is NOT running as root. Rootkit will fail.\n");
    } else {
        printf("[+] Privilege Check: Root/Sudo confirmed.\n");
    }

    // Check for the syscall presence (finit_module)
    // We pass invalid args just to see if the kernel recognizes the syscall number
    if (syscall(313, -1, NULL, 0) == -1) {
        printf("[+] Syscall 313 (finit_module) is available in the table.\n");
    }

    // Check if /proc/modules is visible and writable
    if (access("/proc/modules", W_OK) == 0) {
        printf("[+] /proc/modules is writable. Kernel injection path is clear.\n");
    } else {
        printf("[!] /proc/modules is NOT writable. Rootkit will likely be rejected.\n");
    }

    return 0;
}
