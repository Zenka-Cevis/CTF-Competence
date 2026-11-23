from math import isqrt
from Crypto.Util.number import long_to_bytes, inverse

d = {}
for line in open("output.txt"):
    k, v = line.strip().split(" = ")
    d[k] = int(v)

N, e, c, leak = d["N"], d["e"], d["c"], d["leak"]
bits, leak_bits = d["bits"], d["leak_bits"]

# Fermat
a = isqrt(N)
if a*a < N:
    a += 1

while True:
    b2 = a*a - N
    b = isqrt(b2)
    if b*b == b2:
        p, q = a - b, a + b
        if p * q == N:
            break
    a += 1

# pastikan p adalah yang punya leak di top bits
shift = bits//2 - leak_bits
if (p >> shift) != leak:
    p, q = q, p

assert (p >> shift) == leak
print("[+] p =", p)
print("[+] q =", q)
print("[+] q-p bit length:", (q-p).bit_length())

phi = (p-1)*(q-1)
d_priv = inverse(e, phi)
m = pow(c, d_priv, N)
flag = long_to_bytes(m).decode()
print("[+] FLAG:", flag)
