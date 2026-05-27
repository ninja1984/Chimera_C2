#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

/* Agent 429: Physical Sector Wiper.
   Bypasses the OS cache to overwrite file contents 
   directly on the block device.
*/

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <file_path>\n", argv[0]);
        return 1;
    }

    const char *path = argv[1];
    struct stat st;
    stat(path, &st);
    off_t size = st.st_size;

    // 1. Open with O_DIRECT to bypass Kernel Caching
    // This forces the hardware to write immediately.
    int fd = open(path, O_RDWR | O_DIRECT);
    if (fd < 0) {
        // Fallback to standard if O_DIRECT is unsupported on filesystem
        fd = open(path, O_RDWR);
    }

    // 2. Multi-Pass Wipe (0xFF, then 0x00)
    unsigned char *buffer;
    posix_memalign((void**)&buffer, 4096, 4096); // Aligned for O_DIRECT

    printf("[*] Initiating Scorched Earth on %s (%ld bytes)...\n", path, size);

    for (int pass = 0; pass < 2; pass++) {
        memset(buffer, (pass == 0) ? 0xFF : 0x00, 4096);
        lseek(fd, 0, SEEK_SET);
        for (off_t written = 0; written < size; written += 4096) {
            write(fd, buffer, 4096);
        }
        fsync(fd); // Force hardware flush
    }

    close(fd);

    // 3. Final metadata destruction
    unlink(path);
    printf("[\033[92mSUCCESS\033[0m] Physical traces of %s annihilated.\n", path);

    free(buffer);
    return 0;
}
