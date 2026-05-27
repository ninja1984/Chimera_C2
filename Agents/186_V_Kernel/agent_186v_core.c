#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/mm.h>
#include <linux/uaccess.h>
#include <linux/version.h>

#define DRIVER_NAME "chimera_186v"
#define CHIMERA_MAGIC 'C'
#define IOCTL_SET_TARGET_ADDR _IOW(CHIMERA_MAGIC, 0x01, unsigned long)

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Project Chimera");
MODULE_DESCRIPTION("Agent 186-V: Physical Memory Mapping Primitive");

static int major_num;
static struct cdev chimera_cdev;
static struct class *chimera_class;
static unsigned long target_physical_addr = 0;

static int chimera_open(struct inode *inode, struct file *file) {
    if (!capable(CAP_SYS_ADMIN)) return -EPERM;
    return 0;
}

static int chimera_release(struct inode *inode, struct file *file) {
    return 0;
}

static long chimera_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    switch (cmd) {
        case IOCTL_SET_TARGET_ADDR:
            if (copy_from_user(&target_physical_addr, (unsigned long __user *)arg, sizeof(target_physical_addr)))
                return -EFAULT;
            pr_info("[Chimera 186-V] Target physical address locked: 0x%lx\n", target_physical_addr);
            break;
        default:
            return -ENOTTY;
    }
    return 0;
}

static int chimera_mmap(struct file *file, struct vm_area_struct *vma) {
    unsigned long size = vma->vm_end - vma->vm_start;
    unsigned long pfn = target_physical_addr >> PAGE_SHIFT;

    if (target_physical_addr == 0) return -EINVAL;

    // Direct flag manipulation for modern 6.x kernels
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 3, 0)
    vm_flags_set(vma, VM_IO | VM_PFNMAP | VM_DONTEXPAND | VM_DONTDUMP);
#else
    vma->vm_flags |= VM_IO | VM_PFNMAP | VM_DONTEXPAND | VM_DONTDUMP;
#endif

    vma->vm_page_prot = pgprot_noncached(vma->vm_page_prot);

    // This maps the raw hardware page directly into the process memory
    if (remap_pfn_range(vma, vma->vm_start, pfn, size, vma->vm_page_prot)) {
        pr_err("[Chimera 186-V] remap_pfn_range failed for address 0x%lx\n", target_physical_addr);
        return -EAGAIN;
    }

    return 0;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = chimera_open,
    .release = chimera_release,
    .unlocked_ioctl = chimera_ioctl,
    .mmap = chimera_mmap,
};

static int __init chimera_init(void) {
    dev_t dev;
    if (alloc_chrdev_region(&dev, 0, 1, DRIVER_NAME) < 0) return -1;
    major_num = MAJOR(dev);
    cdev_init(&chimera_cdev, &fops);
    if (cdev_add(&chimera_cdev, dev, 1) < 0) {
        unregister_chrdev_region(dev, 1);
        return -1;
    }

#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 4, 0)
    chimera_class = class_create(DRIVER_NAME);
#else
    chimera_class = class_create(THIS_MODULE, DRIVER_NAME);
#endif
    device_create(chimera_class, NULL, dev, NULL, DRIVER_NAME);
    pr_info("[Chimera 186-V] Kernel Primitive Online on /dev/%s\n", DRIVER_NAME);
    return 0;
}

static void __exit chimera_exit(void) {
    device_destroy(chimera_class, MKDEV(major_num, 0));
    class_destroy(chimera_class);
    cdev_del(&chimera_cdev);
    unregister_chrdev_region(MKDEV(major_num, 0), 1);
    pr_info("[Chimera 186-V] Kernel Primitive Offline.\n");
}

module_init(chimera_init);
module_exit(chimera_exit);
