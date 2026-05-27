#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

/* Agent 424: Virtual Console Sniffer.
   Reads from /dev/vcsX to capture the current 
   text displayed on a target terminal.
*/

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <vcs_device>\n", argv[0]);
        printf("Example: %s /dev/vcs1\n", argv[0]);
        return 1;
    }

    char *vcs_dev = argv[1];
    int fd = open(vcs_dev, O_RDONLY);
    if (fd < 0) {
        perror("open vcs");
        return 1;
    }

    // Standard console is usually 80x25 characters
    unsigned char buffer[2000]; 
    int bytes_read = read(fd, buffer, sizeof(buffer));

    if (bytes_read > 0) {
        printf("--- [DUMPING SCREEN CONTENT: %s] ---\n", vcs_dev);
        for (int i = 0; i < bytes_read; i++) {
            // Filter non-printable characters to keep it clean
            if (buffer[i] >= 32 && buffer[i] <= 126) {
                putchar(buffer[i]);
            } else if (buffer[i] == 0 || buffer[i] == ' ') {
                putchar(' ');
            }
            // Add a newline every 80 chars (standard width)
            if ((i + 1) % 80 == 0) putchar('\n');
        }
        printf("\n--- [END DUMP] ---\n");
    }

    close(fd);
    return 0;
}
