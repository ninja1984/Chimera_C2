#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <unistd.h>

#define DEVICE_PATH "/dev/chimera_186v"
#define CHIMERA_MAGIC 'C'
#define IOCTL_SET_TARGET_ADDR _IOW(CHIMERA_MAGIC, 0x01, unsigned long)

int main() {
    int fd = open(DEVICE_PATH, O_RDWR);
    if (fd < 0) {
        perror("[-] Failed to open device. Are you root?");
        return 1;
    }

    // Attempt to map the first 4KB of the BIOS/System low memory (0x100000)
    unsigned long phys_addr = 0x100000; 
    size_t size = 4096;

    printf("[*] Requesting map of physical address: 0x%lx\n", phys_addr);
    if (ioctl(fd, IOCTL_SET_TARGET_ADDR, &phys_addr) < 0) {
        perror("[-] IOCTL failed");
        return 1;
    }

    void *map = mmap(NULL, size, PROT_READ, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        perror("[-] mmap failed");
        return 1;
    }

    printf("[+] Success! Physical 0x%lx mapped to virtual %p\n", phys_addr, map);
    printf("[*] Dumping first 16 bytes:\n");
    for(int i = 0; i < 16; i++) {
        printf("%02x ", ((unsigned char*)map)[i]);
    }
    printf("\n");

    munmap(map, size);
    close(fd);
    return 0;
}
