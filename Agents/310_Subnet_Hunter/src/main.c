#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

void scan_host(const char* base_ip, int i) {
    struct sockaddr_in target;
    int sock;
    char ip[16];
    
    sprintf(ip, "%s.%d", base_ip, i);
    
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return;

    // Set non-blocking for fast scanning
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);

    target.sin_family = AF_INET;
    target.sin_port = htons(22); // Target SSH for lateral movement potential
    inet_aton(ip, &target.sin_addr);

    connect(sock, (struct sockaddr *)&target, sizeof(target));

    // Give it a tiny window to respond
    usleep(50000); // 50ms is plenty for a local subnet

    struct sockaddr_in tmp;
    socklen_t len = sizeof(tmp);
    if (getpeername(sock, (struct sockaddr*)&tmp, &len) == 0) {
        printf("[+] Found Potential Target: %s (Port 22 Open)\n", ip);
    }
    
    close(sock);
}

int main() {
    printf("\n--- CHIMERA PHASE 3 RECON: SUBDOMAIN HUNTER ---\n");
    
    // We'll hardcode 127.0.0 for the local test, but we can automate prefix detection next
    const char* base_ip = "127.0.0"; 
    
    for (int i = 1; i < 255; i++) {
        if (i == 1) continue; // Skip self/gateway for speed if needed
        scan_host(base_ip, i);
    }
    
    printf("--- RECON COMPLETE ---\n");
    return 0;
}
