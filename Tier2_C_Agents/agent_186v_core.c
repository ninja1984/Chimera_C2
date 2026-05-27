#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/icmp.h>

static struct nf_hook_ops nfho;

static unsigned int watch_packets(void *priv, struct sk_buff *skb, const struct nf_hook_state *state) {
    struct iphdr *iph;
    struct icmphdr *icmph;

    if (!skb) return NF_ACCEPT;

    iph = ip_hdr(skb);
    if (!iph) return NF_ACCEPT;

    if (iph->protocol == IPPROTO_ICMP) {
        icmph = icmp_hdr(skb);
        if (!icmph) return NF_ACCEPT;
        
        if (icmph->type == ICMP_ECHO) {
            // This is our heartbeat. It sees you before the firewall does.
            printk(KERN_INFO "[Chimera] Network Heartbeat from %pI4\n", &iph->saddr);
        }
    }

    return NF_ACCEPT; 
}

int init_module(void) {
    nfho.hook = watch_packets;
    nfho.hooknum = NF_INET_PRE_ROUTING; 
    nfho.pf = PF_INET;
    nfho.priority = NF_IP_PRI_FIRST;    
    
    nf_register_net_hook(&init_net, &nfho);
    printk(KERN_INFO "[Chimera] Tier 3: Nervous System Online.\n");
    return 0;
}

void cleanup_module(void) {
    nf_unregister_net_hook(&init_net, &nfho);
    printk(KERN_INFO "[Chimera] Tier 3: Nervous System Offline.\n");
}

MODULE_LICENSE("GPL");
