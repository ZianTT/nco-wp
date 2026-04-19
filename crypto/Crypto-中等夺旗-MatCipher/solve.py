from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import *


cipher = [208, 160, 93, 228, 196, 183, 1, 205, 121, 159, 158, 53, 212, 28, 135, 217]
flag_cipher_hex = "7d8b14bf8944d5bcb77ee36bdc16edb69e7ed585ea3ba35cee4008bbef1c997536b5faf1b699fd6a9acce6aef636dfd6"


messages_str = b"The staircase borrowed a whisper from tomorrow,folded it into a paper moon, and quietly forgot why the clouds were wearing shoes"
Zp = Zmod(257)
messages = list(messages_str)
assert len(messages) % 8 == 0
n_blocks = len(messages) // 8


M = []
for i in range(n_blocks):
    block = messages[i*8 : (i+1)*8]
    M.append([Zp(x) for x in block])

C = [Zp(x) for x in cipher]

M8 = matrix(Zp, M[:8])
C8 = vector(Zp, C[:8])
key = M8.solve_right(C8)
print("Recovered key (mod 257):", key)

# key = [79, 170, 244, 185, 229, 201, 71, 79]

key_bytes = bytes([int(x) for x in key])

aes = AES.new(md5(key_bytes).digest(), AES.MODE_ECB)
flag_cipher = bytes.fromhex(flag_cipher_hex)
flag = unpad(aes.decrypt(flag_cipher), 16)
print("Flag:", flag.decode())