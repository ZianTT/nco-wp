byte_2060 = [int(x, 16) for x in "13 37 C0 DE 42 99 AA 55".split()]
byte_2040 = [int(x, 16) for x in "07 E8 4C 9D A5 1D D1 14 B2 C8 CB 5D 0B 78 FA 75 BE 4E 12 7E 88 8D 5E 7D 3B C6 3F EC 0D 11 D3 50".split()]

def reverse_rol1(v, n):
    n &= 7
    return ((v >> n) | (v << (8 - n))) & 0xFF

def solve():
    state = 0x5A
    flag = ""
    for i in range(32):
        reverse_rol1_val = reverse_rol1(byte_2040[i], i%5)
        t = state ^ reverse_rol1_val
        ch = t ^ byte_2060[i & 7]
        flag += chr(ch)
        state = reverse_rol1_val ^ byte_2040[i]
    return flag

if __name__ == "__main__":
    print(solve())



