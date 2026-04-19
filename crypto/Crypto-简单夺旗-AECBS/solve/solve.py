from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

with open("output.txt", 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

mapping = {}
flag_cipher_line = "2237a82d5dd03dbf1fc349631aedee12ee65d1bf600c06b8a879bb5e48a0fbec35dd7e2e3d9e630733b4215eac5e1c86"

for line in lines:
    if ':' in line:
        key, commitment = line.split(': ')
        mapping[commitment] = key

keys = []
for commitment in lines[-25:-1]:
    keys.append(mapping[commitment])
flag_key = md5(''.join(keys).encode()).digest()
cipher = AES.new(flag_key, AES.MODE_ECB)
flag_ciphertext = bytes.fromhex(flag_cipher_line)
flag = cipher.decrypt(flag_ciphertext)
flag = unpad(flag, AES.block_size).decode()
print(flag)