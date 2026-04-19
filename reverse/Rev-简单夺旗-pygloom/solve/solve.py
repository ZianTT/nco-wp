TARGET = [125, 119, 138, 22, 33, 107, 109, 123, 60, 154, 73, 170, 192, 94, 179, 190, 182, 125, 206, 140, 144, 149, 157, 254, 20, 177, 246, 26, 200, 55, 48, 224, 229, 233, 62, 67]
DECODED = ''.join([chr(((num - index * 7) ^ 0x33) & 0xFF) for index, num in enumerate(TARGET)])
print(DECODED)