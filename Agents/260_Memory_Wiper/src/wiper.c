#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>

/* Agent 405: Hardened C-Native Memory Guard.
   Uses mlock() to prevent swapping to disk and 
   volatile pointers to prevent compiler optimization of the wipe.
*/

void secure_wipe(void *v, size_t n) {
    // Volatile prevents the compiler from saying "This memory is 
    // never used again, so I'll skip the memset to save time."
    volatile unsigned char *p = v;
    while (n--) *p++ = 0;
}

int main() {
    size_t key_size = 32;
    char *secret_key = malloc(key_size);
    strncpy(secret_key, "MILITARY_GRADE_AES_KEY_2026_!!", key_size);

    // 1. PIN THE MEMORY: Prevent the OS from writing this to the SWAP file on disk.
    if (mlock(secret_key, key_size) != 0) {
        perror("mlock");
        return 1;
    }

    printf("[*] Memory Guard Active. Key Pinned at: %p\n", (void*)secret_key);

    // 2. SIMULATE EMERGENCY (Wait for signal or forensic tool detection)
    // In a real op, this would be a loop checking /proc/modules for 'lime'
    sleep(5); 

    // 3. THE WIPE
    secure_wipe(secret_key, key_size);
    munlock(secret_key, key_size);
    free(secret_key);

    printf("[!!!] MEMORY SANITIZED DETERMINISTICALLY.\n");
    return 0;
}
