#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
#include <unistd.h>

/* Agent 415: Hook Detector.
   Checks the memory of libc functions for 'JMP' (0xe9) instructions.
   If found, an EDR or Debugger has hooked the function.
*/

void check_function_integrity(const char* func_name) {
    void* handle = dlopen("libc.so.6", RTLD_LAZY);
    unsigned char* func_ptr = (unsigned char*)dlsym(handle, func_name);

    if (!func_ptr) return;

    printf("[*] Auditing %s at %p: ", func_name, (void*)func_ptr);

    // 0xE9 is the 'JMP' instruction used by almost all EDR hooks
    if (func_ptr[0] == 0xe9) {
        printf("[\033[91mHOOKED\033[0m] -> EDR/AV Detected!\n");
    } else {
        printf("[\033[92mCLEAN\033[0m] -> Standard Prologue.\n");
    }
    
    dlclose(handle);
}

int main() {
    printf("--- [AGENT 415: MEMORY INTEGRITY AUDIT] ---\n");
    
    // We check the functions Chimera relies on most
    check_function_integrity("ptrace");
    check_function_integrity("fork");
    check_function_integrity("execve");
    check_function_integrity("system");

    return 0;
}
