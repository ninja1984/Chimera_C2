#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* Agent 404: Control Flow Obfuscation via Opaque Predicates.
   This code is designed to confuse decompilers like Ghidra 
   by creating 'Impossible' logic paths.
*/

int main() {
    int x = 5;
    int y = 10;

    // Opaque Predicate: (x*x) is always positive, so this is always TRUE.
    // However, a static analyzer has a hard time proving this across complex math.
    if ((x * x) + (y * y) >= 0) {
        printf("--- [AGENT 404: EXECUTING PROTECTED LOGIC] ---\n");
        // Actual Chimera payload would go here
    } else {
        // 'Dead Code' - Ghidra will spend time analyzing this, 
        // but it will NEVER execute in reality.
        printf("DEBUG: Initiating system recovery...\n");
        for(int i=0; i<1000; i++) { x += i; } 
    }

    return 0;
}
