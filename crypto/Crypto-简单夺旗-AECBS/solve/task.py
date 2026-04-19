import os
import random
from hashlib import md5

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from secret import flag

key = os.urandom(16)
main_cipher = AES.new(key, AES.MODE_ECB)
BLOCK_SIZE = 16

def load_wordlist(filename: str):
    words = []
    with open(filename, 'r') as f:
        for line in f:
            words.append(line.strip().split(' ')[1])
    return words

BIP39_wordlist = load_wordlist('BIP39.txt')

def KeyGen(n=24):
    keys = [random.choice(BIP39_wordlist) for _ in range(n)]
    commitments = [main_cipher.encrypt(pad(word.encode(), BLOCK_SIZE)) for word in keys]
    return keys, commitments

with open("output.txt", 'w') as f:
    for _ in range(700):
        keys, commitments = KeyGen()
        for key, commitment in zip(keys, commitments):
            f.write(f"{key}: {commitment.hex()}\n")

keys, commitments = KeyGen()
flag_key = md5(''.join(keys).encode()).digest()
cipher = AES.new(flag_key, AES.MODE_ECB)
flag_ciphertext = cipher.encrypt(pad(flag, BLOCK_SIZE))

with open("output.txt", 'a') as f:
    for commitment in commitments:
        f.write(f"{commitment.hex()}\n")
    f.write(f"{flag_ciphertext.hex()}\n")