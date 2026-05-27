#include <stdio.h>
#include <sys/utsname.h>
#include <sys/sysinfo.h>

int main() {
    struct utsname name;
    struct sysinfo info;

    if (uname(&name) == 0) {
        printf("[+] System Name: %s\n", name.sysname);
        printf("[+] Release    : %s\n", name.release);
        printf("[+] Machine    : %s\n", name.machine);
    }

    if (sysinfo(&info) == 0) {
        printf("[+] Uptime     : %ld seconds\n", info.uptime);
        printf("[+] Total RAM  : %lu MB\n", info.totalram / 1024 / 1024);
    }

    printf("[!!!] FOUNDRY TEST SUCCESSFUL: ELF EXECUTED IN RAM\n");
    return 0;
}
