# Who's the Gateway

**Category:** Digital Forensics / Network (ARP spoofing)
**Status:** Solved (Verified)
**Flag:** `LsCTF2026{arp_l13d_ab0ut_th3_gat3way}` ✅ VERIFIED

---

## 1. Challenge Overview

> A workstation on `192.168.50.0/24` suddenly started sending its traffic to the
> wrong machine. Someone on the LAN convinced it they were the gateway.
>
> **Mission:** Show that the redirect happened, then read the credentials it exposed.

---

## 2. Initial Analysis

### Handout (`whos-the-gateway_capture.zip` → `whos-the-gateway_capture.pcap`)

```
$ tshark -r whos-the-gateway_capture.pcap -q -z io,phs
  ... arp  frames:20 ... http frames:16 ... tls ... dns ... ntp ...
```

A small LAN capture: some ARP, a little HTTP, and the usual connectivity-check noise. The brief points at ARP, so start there.

---

## 3. Investigation and Methodology

### Find the ARP anomaly and the host behind it

List every ARP **reply** (`opcode 2`) and the IP→MAC bindings it claims:

```
$ tshark -r whos-the-gateway_capture.pcap -Y 'arp.opcode==2' \
         -T fields -e arp.src.proto_ipv4 -e arp.src.hw_mac | sort | uniq -c
      6 192.168.50.1   00:25:9c:47:9c:53    <-- gateway claimed by attacker (x6)
      1 192.168.50.1   00:25:9c:61:aa:5e    <-- the real gateway (x1)
      2 192.168.50.41  00:1a:8c:7e:e2:65
      2 192.168.50.90  b8:27:eb:5a:07:78
      1 192.168.50.77  00:0c:29:04:ae:ed
      1 192.168.50.23  00:50:56:ed:ac:1e
```

The gateway IP `192.168.50.1` is bound to **two different MAC addresses**. The legitimate gateway (`00:25:9c:61:aa:5e`) answers once. The attacker at **`00:25:9c:47:9c:53`** sends **six gratuitous ARP replies** claiming to be `192.168.50.1`. This is ARP cache poisoning: the attacker tells the victim "I am the gateway" so the victim's upstream traffic goes through the attacker's machine (man-in-the-middle).

The poisoned victim is `192.168.50.77`. Right after the spoof, its traffic is visible to the attacker.

### Read the credential the redirect exposed

```
$ tshark -r whos-the-gateway_capture.pcap -Y 'http.request' \
         -T fields -e ip.src -e ip.dst -e http.host -e http.request.uri
192.168.50.77  192.168.50.10  intranet.local  /portal/login   <-- the target
...
```

The victim (`.77`) requests `http://intranet.local/portal/login` with **HTTP Basic Authentication**:

```
$ tshark -r whos-the-gateway_capture.pcap -Y 'http.authorization' \
         -T fields -e http.authorization
Basic aGVscGRlc2s6NGM3MzQzNTQ0NjMyMzAzMjM2N2I2MTcyNzA1ZjZjMzEzMzY0...
```

### Indicators

| Role | IP | MAC |
|---|---|---|
| Real gateway | 192.168.50.1 | 00:25:9c:61:aa:5e |
| **Attacker (spoofer)** | claims 192.168.50.1 | **00:25:9c:47:9c:53** |
| Victim (poisoned) | 192.168.50.77 | 00:0c:29:04:ae:ed |
| Intranet web server | 192.168.50.10 | — |

- Exposed credential: `helpdesk` : (hex-encoded flag)
- Exposed URL: `http://intranet.local/portal/login`

---

## 4. Vulnerability / Technical Discovery

| Component | Flaw |
|-----------|------|
| ARP | No authentication; any host can forge replies and impersonate the gateway |
| Intranet login | Cleartext HTTP Basic auth, readable once traffic is redirected |
| Password | Hex-encoded ASCII, not protected |

---

## 5. Exploitation / Solution

HTTP Basic auth is `base64(user:pass)`. Decode once:

```
$ echo 'aGVscGRlc2s6NGM3MzQzNTQ0NjMyMzAzMjM2N2I2...' | base64 -d
helpdesk:4c73435446323032367b6172705f6c3133645f61623075745f7468335f676174337761797d
```

The user is `helpdesk`; the "password" is a **hex string**. Decode it:

```
$ python3 -c "print(bytes.fromhex('4c73435446...7d').decode())"
LsCTF2026{arp_l13d_ab0ut_th3_gat3way}
```

`solve.py` reproduces the whole chain from the pcap:

```
$ python3 solve.py whos-the-gateway_capture.pcap
[*] ARP replies per IP:
    192.168.50.1     00:25:9c:47:9c:53  x6  <-- SPOOFER
    192.168.50.1     00:25:9c:61:aa:5e  x1
    ...
[*] Basic auth user: helpdesk
[+] FLAG: LsCTF2026{arp_l13d_ab0ut_th3_gat3way}
```

---

## 6. Flag

```
LsCTF2026{arp_l13d_ab0ut_th3_gat3way}
```
(Verified: `solve.py` reproduces it from the original pcap)

---

## 7. Lessons Learned

1. **ARP has no authentication.** Any host on the LAN can forge replies and impersonate the gateway.
2. **The tell** is one IP (especially the gateway) mapped to two MACs, often with a burst of gratuitous replies.
3. **The redirect only pays off because of cleartext.** Don't run intranet logins over plain HTTP; enable dynamic ARP inspection or static ARP entries for critical gateways.

---

## 8. Tools Used

- `tshark` (ARP reply aggregation, HTTP header extraction)
- Python 3: `base64`, `subprocess`, `collections`

---

## 9. Evidence and References

- `solve.py` — Flags the spoofed gateway MAC, extracts and decodes the Basic auth credential
- `evidence/README.md` — Original handout file list

> Note: on the solving host, `tshark` drops privileges and could not read files under the home directory. Run the solver against a copy of the pcap in a world-readable path (e.g. `/tmp`) if you get a permission error.
