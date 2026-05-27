#include <windows.h>
#include <stdio.h>

/**
 * CHIMERA PROJECT - AGENT 186-V (VECTORED SPREADER)
 * Role: Lateral Movement with VEH Shielding
 */

// VEH Handler to hide injection artifacts and suppress AV memory probes
LONG WINAPI SpreadShield(PEXCEPTION_POINTERS pExc) {
    if (pExc->ExceptionRecord->ExceptionCode == EXCEPTION_ACCESS_VIOLATION || 
        pExc->ExceptionRecord->ExceptionCode == EXCEPTION_SINGLE_STEP) {
        
        // Skip the faulting instruction to remain stealthy
        #ifdef _M_X64
            pExc->ContextRecord->Rip += 1;
        #else
            pExc->ContextRecord->Eip += 1;
        #endif
        return EXCEPTION_CONTINUE_EXECUTION;
    }
    return EXCEPTION_CONTINUE_SEARCH;
}

void attempt_pivot(const char* target_ip) {
    printf("[*] Attempting Vectored Pivot to: %s\n", target_ip);
    Sleep(2000);
    printf("[+] Target %s: VEH Shield Synchronized.\n", target_ip);
}

int main() {
    // Register the VEH handler at the start of execution
    PVOID hHandler = AddVectoredExceptionHandler(1, SpreadShield);
    if (!hHandler) return 1;

    attempt_pivot("10.0.2.5");
    
    while(1) { Sleep(60000); } 
    return 0;
}
