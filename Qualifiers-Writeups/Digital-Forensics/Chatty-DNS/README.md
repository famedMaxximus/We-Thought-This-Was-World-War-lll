# Chatty DNS

**Category:** Digital Forensics / Network (DNS tunnelling)
**Status:** Solved (Verified)
**Flag:** `LsCTF2026{dns_can_talk_t00_much}` ✅ VERIFIED

---

## 1. Challenge Overview

> One workstation keeps resolving subdomains of a domain nobody here uses, and
> there is no web traffic to go with it. It looks like something is tunnelling
> data out over DNS. Work out what is leaving the network and recover it.

---

## 2. Initial Analysis

### Handout (`chatty-dns_capture.zip` → `chatty-dns_capture.pcap`)

A packet capture with normal DNS lookups (Google, Microsoft, local `.ls` sites) and one workstation querying an unfamiliar domain.

---

## 3. Investigation and Methodology

### Isolate the suspicious lookups

List the DNS queries. The odd domain stands out among the normal traffic:

```
$ tshark -r chatty-dns_capture.pcap -Y 'dns.flags.response==0' -T fields -e dns.qry.name
...
0.kree4rcwivmxstke.report.telemetry-sync.net
1.jezgkmssovrtcolk.report.telemetry-sync.net
2.lfltkztei5dhgyjr.report.telemetry-sync.net
3.heye2rccmzrfqvtk.report.telemetry-sync.net
4.mfedapi.report.telemetry-sync.net
```

`report.telemetry-sync.net` is the attacker domain. Each query has the classic DNS-tunnel shape:

```
<index>.<data-chunk>.report.telemetry-sync.net
```

- A leading **sequence number** (`0,1,2,3,4`) so the receiver can reassemble in order even if DNS reorders or retransmits.
- A **data label** made only of `[a-z2-7]`, i.e. lowercase **base32**.
- No A-record answers or web traffic follow, which confirms exfiltration rather than browsing.

Filter just these:

```
tshark -r chatty-dns_capture.pcap -Y 'dns.flags.response==0 && dns.qry.name contains "telemetry-sync"'
```

### Reassemble in order

Sort by the numeric index and concatenate the data labels:

```
kree4rcwivmxstke + jezgkmssovrtcolk + lfltkztei5dhgyjr + heye2rccmzrfqvtk + mfedapi
= kree4rcwivmxstkejezgkmssovrtcolklfltkztei5dhgyjrheye2rccmzrfqvtkmfedapi
```

---

## 4. Vulnerability / Technical Discovery

DNS used as a covert exfiltration channel. The QNAME carries base32-encoded data one label at a time, with sequence numbers for reassembly. Inside the base32 is a second base64 layer.

---

## 5. Exploitation / Solution

Two decoding layers:

```
# 1) base32 (uppercase + pad to a multiple of 8)
base32("KREE4RCW...MFEDAPI") -> THNDVEYyMDI2e2Ruc19jYW5fdGFsa190MDBfbXVjaH0=

# 2) that is base64 (prefix THNDVEYy -> LsCTF2026)
base64 -d -> LsCTF2026{dns_can_talk_t00_much}
```

`solve.py` reads the chunks straight from the pcap with tshark:

```
$ python3 solve.py
FLAG: LsCTF2026{dns_can_talk_t00_much}
```

---

## 6. Flag

```
LsCTF2026{dns_can_talk_t00_much}
```
(Verified: `solve.py` reproduces it from the original pcap)

---

## 7. Lessons Learned

1. **DNS is a strong covert channel.** It is almost never blocked, resolvers forward queries for any domain, and the QNAME can carry arbitrary encoded data.
2. **Tunnel indicators:** a never-before-seen domain, high-entropy base32 labels, sequence-numbered subdomains, and queries with no matching web or session traffic.
3. **Defences:** monitor NXDOMAIN rates and per-domain query volume and entropy, and restrict outbound DNS to approved resolvers.

---

## 8. Tools Used

- `tshark` (DNS query extraction)
- Python 3: `base64`, `subprocess`

---

## 9. Evidence and References

- `solve.py` — Extracts the tunnel chunks from the pcap and decodes them
- `evidence/README.md` — Original handout file list
