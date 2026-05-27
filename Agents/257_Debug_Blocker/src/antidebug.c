#include <sys/ptrace.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

/* Agent 402: Self-Trace Anti-Debugger.
   If ptrace(PTRACE_TRACEME) fails, a debugger is already present.
*/

void __attribute__ ((constructor)) anti_debug_init() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
        // Debugger detected!
        exit(1);
    }
    // Successfully traced ourselves; detach so we can continue
    ptrace(PTRACE_DETACH, 0, 1, 0);
}

int main() {
    // This code only runs if no debugger was detected
    printf("SAFE\n");
    return 0;
}
