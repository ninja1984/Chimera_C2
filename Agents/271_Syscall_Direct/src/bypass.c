#define _GNU_SOURCE
#include <stdio.h>
#include <signal.h>
#include <ucontext.h>
#include <unistd.h>
#include <sys/syscall.h>

/* Agent 416: Linux 'VEH-Style' Exception Handler & Direct Syscalls.
   Bypasses libc hooks by using raw 'syscall' and handles SIGTRAP 
   to evade active debugging/instrumentation.
*/

void exception_handler(int sig, siginfo_t *info, void *ucontext) {
    ucontext_t *ctx = (ucontext_t *)ucontext;
    
    printf("[\033[91mTRAP DETECTED\033[0m] Signal: %d at RIP: %p\n", sig, (void*)ctx->uc_mcontext.gregs[REG_RIP]);
    
    // VE-Style Recovery: Increment RIP to skip the offending instruction (1 byte for INT3)
    // This allows the agent to survive a 'Software Breakpoint' set by an analyst.
    ctx->uc_mcontext.gregs[REG_RIP] += 1;
    
    printf("[*] Recovery: Incremented RIP. Resuming execution...\n");
}

int main() {
    struct sigaction sa;
    sa.sa_sigaction = exception_handler;
    sa.sa_flags = SA_SIGINFO;
    sigemptyset(&sa.sa_mask);

    // Register our 'VEH' for Traps and Segmentation Faults
    sigaction(SIGTRAP, &sa, NULL);
    sigaction(SIGSEGV, &sa, NULL);

    printf("--- [AGENT 416: DIRECT SYSCALL & EXCEPTION RECOVERY] ---\n");

    // 1. Direct Syscall Bypass: writing to STDOUT (1) without using printf/write from libc
    // Using inline assembly to trigger syscall 1 (write) directly.
    const char *msg = "[+] Success: Direct Kernel Syscall (Bypassing Libc Hooks)\n";
    asm volatile (
        "mov $1, %%rax\n"   // syscall number for sys_write
        "mov $1, %%rdi\n"   // file descriptor 1 (stdout)
        "mov %0, %%rsi\n"   // message pointer
        "mov $58, %%rdx\n"  // message length
        "syscall\n"
        :
        : "r"(msg)
        : "rax", "rdi", "rsi", "rdx"
    );

    // 2. Trigger a Trap to test our 'VEH' handler
    printf("[*] Testing Recovery: Triggering intentional SIGTRAP...\n");
    asm("int3"); 

    printf("[\033[92mCOMPLETE\033[0m] Agent survived the trap and continued.\n");

    return 0;
}
