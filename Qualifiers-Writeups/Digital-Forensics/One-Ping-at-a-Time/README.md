# One Ping at a Time

**Category:** Digital Forensics / Network (ICMP covert channel)
**Status:** Solved (Verified)
**Flag:** `LsCTF2026{p1ng_by_p1ng_1t_c0m3s}` ✅ VERIFIED

---

## 1. Challenge Overview

> A ping sweep is running across 10.13.37.0/24. Most of it is routine, but one
> host is being pinged in a way the others are not, and those echoes are carrying
> more than padding. Recover the message hidden inside the ICMP traffic.

---

## 2. Initial Analysis

### Handout (`one-ping-at-a-time_capture.zip` → `one-ping-at-a-time_capture.pcap`)

A capture of an ICMP ping sweep across `10.13.37.0/24`, with one host receiving unusual echo requests.

---

## 3. Investigation and Methodology

### Separate the covert pings from the sweep

Group the ICMP echo requests (`icmp.type==8`) by destination, ident and payload size:

```
$ tshark -r one-ping-at-a-time_capture.pcap -Y 'icmp.type==8' \
         -T fields -e ip.dst -e icmp.ident -e icmp.seq -e data.len | sort | uniq -c
...
1  10.13.37.9   3415    9   32     <- sweep: 32-byte payload, ident varies per host
1  10.13.37.8   3193    8   32
1  10.13.37.7   16962   7    2     <- covert: SAME ident 16962, tiny 2-byte payload
1  10.13.37.7   16962   8    2
...
```

The sweep sends one 32-byte ping per host with a different ident each time. The **covert** channel, all aimed at `10.13.37.7`, stands out on three counts:

- a **fixed ident 16962** (`0x4242` = `"BB"`),
- **2-byte** payloads instead of the 32-byte sweep padding,
- a run of **sequence numbers** (0,1,2,…) to allow reassembly.

Filter: `icmp.type==8 && icmp.ident==16962` → 44 packets.

### Reassemble in order

Sort by `icmp.seq` and concatenate the 2-byte payloads:

```
seq 0: "54"  seq 1: "48"  seq 2: "4e"  seq 3: "44" ...
-> 54484e44564559794d44493265334178626d6466596e6c66634446755a3138786446396a4d47307a6333303d
```

Each payload is two ASCII characters, so the stream spells a long **hex string**.

---

## 4. Vulnerability / Technical Discovery

ICMP echo payloads are attacker-controlled and rarely inspected. Here they carry an ASCII-hex string, which wraps a base64 string, which wraps the flag.

---

## 5. Exploitation / Solution

```
# 1) the payload bytes are ASCII hex -> un-hex
54484e44...6333303d  ->  THNDVEYyMDI2e3AxbmdfYnlfcDFuZ18xdF9jMG0zc30=

# 2) that is base64 (prefix THNDVEYy -> LsCTF2026)
base64 -d  ->  LsCTF2026{p1ng_by_p1ng_1t_c0m3s}
```

`solve.py` pulls the payloads straight from the pcap:

```
$ python3 solve.py
FLAG: LsCTF2026{p1ng_by_p1ng_1t_c0m3s}
```

---

## 6. Flag

```
LsCTF2026{p1ng_by_p1ng_1t_c0m3s}
```
(Verified: `solve.py` reproduces it from the original pcap)

---

## 7. Lessons Learned

1. **`ping` is a classic covert/exfil channel.** Echo payloads can hold anything.
2. **Giveaways:** one destination pinged far more than a sweep would, a constant identifier, and payloads whose size and content don't match normal `ping` padding.
3. **Defences:** baseline ICMP payload sizes and volume, alert on high ICMP rates to a single host, and inspect or strip echo payloads at the perimeter.

---

## 8. Tools Used

- `tshark` (ICMP field extraction)
- Python 3: `base64`, `subprocess`

---

## 9. Evidence and References

- `solve.py` — Isolates the covert pings and decodes the message
- `evidence/README.md` — Original handout file list
