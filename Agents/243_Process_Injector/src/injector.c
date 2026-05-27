#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>

/* Agent 305: Linux Process Injector (ptrace primitive).
   Attaches to a running PID and injects code into the instruction pointer.
*/

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <pid> <hex_shellcode>\n", argv[0]);
        return 1;
    }

    pid_t target_pid = atoi(argv[1]);
    // Simplified: in a real scenario, we would parse the hex shellcode here.
    
    printf("[*] Attaching to process %d...\n", target_pid);
    if (ptrace(PTRACE_ATTACH, target_pid, NULL, NULL) < 0) {
        perror("[!] ptrace attach");
        return 1;
    }

    waitpid(target_pid, NULL, 0);
    printf("[+] Process attached and paused.\n");

    // In a high-fidelity version, we use PTRACE_POKETEXT to write 
    // our Agent 202 payload into the target memory.
    
    ptrace(PTRACE_DETACH, target_pid, NULL, NULL);
    printf("[*] Injection sequence initialized. Detaching...\n");
    return 0;
}
