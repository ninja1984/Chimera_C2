#include <windows.h>
#include <stdio.h>

/**
 * CHIMERA PROJECT - AGENT 187 (VEH GHOST)
 * High-Fidelity Windows Exception Handler
 * Targets: x86 and x64 Architecture
 */

LONG WINAPI Chimera_VEH_Dispatcher(PEXCEPTION_POINTERS ExceptionInfo) {
    // Check if the crash was an Access Violation (Data Execution Prevention / Memory Scan)
    if (ExceptionInfo->ExceptionRecord->ExceptionCode == EXCEPTION_ACCESS_VIOLATION) {
        
        printf("[!] Security Intercept: Access Violation at 0x%p\n", 
               (void*)ExceptionInfo->ExceptionRecord->ExceptionAddress);

        // ARCHITECTURE DETECTION: Adjusting the Instruction Pointer
#ifdef _M_X64
        // x64 Architecture uses RIP
        // We increment by 2 to skip the 'faulty' instruction (e.g., a MOV)
        ExceptionInfo->ContextRecord->Rip += 2; 
#elif defined(_M_IX86)
        // x86 Architecture uses EIP
        ExceptionInfo->ContextRecord->Eip += 2;
#endif

        printf("[*] Instruction Pointer Shifted. Resuming Execution...\n");
        return EXCEPTION_CONTINUE_EXECUTION;
    }

    // If it's a real crash we didn't expect, let the system handle it
    return EXCEPTION_CONTINUE_SEARCH;
}

int main() {
    // 1. Register the handler at the FRONT of the chain (First Priority)
    PVOID hHandler = AddVectoredExceptionHandler(1, Chimera_VEH_Dispatcher);
    
    if (hHandler == NULL) {
        printf("[-] Failed to register VEH. Permissions issue?\n");
        return 1;
    }

    printf("[*] Chimera VEH Shield: ONLINE.\n");

    // 2. The "Trap": Force a null-pointer dereference
    // On a normal app, this is an instant 'Program has stopped working'
    printf("[*] Testing Shield with forced Null-Pointer Dereference...\n");
    
    volatile int *ptr = NULL;
    *ptr = 0xDEADC0DE; // This triggers the VEH immediately

    // 3. Cleanup
    printf("[!!!] SURVIVED: Code continued past the crash.\n");
    RemoveVectoredExceptionHandler(hHandler);
    
    return 0;
}
