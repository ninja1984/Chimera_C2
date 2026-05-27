#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <stdint.h>

void check_dmi_strings() {
    const char *dmi_paths[] = {
        "/sys/class/dmi/id/sys_vendor",
        "/sys/class/dmi/id/product_name",
        "/sys/class/dmi/id/chassis_vendor"
    };

    printf("[*] Probing Hardware DNA...\n");
    for (int i = 0; i < 3; i++) {
        FILE *fp = fopen(dmi_paths[i], "r");
        if (fp) {
            char vendor[256];
            if (fgets(vendor, sizeof(vendor), fp)) {
                printf("  [>] %s: %s", dmi_paths[i], vendor);
                if (strstr(vendor, "VMware") || strstr(vendor, "VirtualBox") || strstr(vendor, "QEMU") || strstr(vendor, "Innotek")) {
                    printf("      [!!!] ALERT: Virtualization Brand Identified.\n");
                }
            }
            fclose(fp);
        }
    }
}

void check_interrupts() {
    // Real machines have thousands of keyboard/mouse interrupts. Sandboxes have 0.
    FILE *fp = fopen("/proc/interrupts", "r");
    if (fp) {
        char line[512];
        int found_activity = 0;
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "keyboard") || strstr(line, "mouse") || strstr(line, "psmouse")) {
                printf("[+] Human Interface Device (HID) Activity Detected.\n");
                found_activity = 1;
                break;
            }
        }
        if (!found_activity) printf("[!!!] WARNING: No Keyboard/Mouse activity in kernel logs. Potential headless sandbox.\n");
        fclose(fp);
    }
}

int main() {
    struct sysinfo info;
    sysinfo(&info);
    
    printf("\n--- CHIMERA AGENT 317-V3: DEEP-STATE PROFILER ---\n");
    
    // 1. BIOS/Vendor Strings
    check_dmi_strings();

    // 2. Human Presence Check
    check_interrupts();

    // 3. Environment Check
    if (access("/.dockerenv", F_OK) == 0) {
        printf("[!] Status: Inside Docker Container.\n");
    }

    // 4. Resource Density
    int cores = sysconf(_SC_NPROCESSORS_ONLN);
    long ram_mb = info.totalram / 1024 / 1024;
    printf("[*] Resources: %d Cores | %ld MB RAM\n", cores, ram_mb);
    
    if (cores < 2 || ram_mb < 2048) {
        printf("[!!!] WARNING: Resource Exhaustion. This feels like a Honeytrap.\n");
    }

    printf("\n--- ANALYSIS COMPLETE ---\n");
    return 0;
}
