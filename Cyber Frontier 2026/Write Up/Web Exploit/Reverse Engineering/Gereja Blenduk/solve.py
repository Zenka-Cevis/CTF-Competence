import struct, json, hashlib
from pathlib import Path

p = Path('.')
b = (p/'program.bin').read_bytes()
assert len(b)==148 and b[:4]==b'BLV5'
a = struct.unpack('<72H', b[4:])

# Matriks 8x8 dan RHS di GF(257)
M = [[a[8*i+j] for j in range(8)] for i in range(8)]
rhs = [a[64+i] for i in range(8)]
MOD = 257

# Gaussian elimination GF(257)
A = [row[:] + [rhs[i]] for i,row in enumerate(M)]
n = 8
for col in range(n):
    piv = next(r for r in range(col,n) if A[r][col] % MOD)
    A[col], A[piv] = A[piv], A[col]
    inv = pow(A[col][col], -1, MOD)
    A[col] = [(x*inv) % MOD for x in A[col]]
    for r in range(n):
        if r != col and A[r][col]:
            f = A[r][col]
            A[r] = [(A[r][k] - f*A[col][k]) % MOD for k in range(n+1)]

v = [A[i][n] % MOD for i in range(n)]
print('v =', v)
assert all(x <= 255 for x in v), "ada 256, ga bisa jadi byte"

# invert: v = (s*197 + 31) & 255  → s*197 ≡ v-31 (mod 256)
inv197 = pow(197, -1, 256)
s = bytes((( (x - 31) % 256) * inv197) % 256 for x in v)
print('serial =', s)

# buka vault
x = bytes.fromhex(json.loads((p/'vault.json').read_text())['ciphertext_hex'])
k = hashlib.sha256(s).digest()
z = b''.join(hashlib.sha256(k + i.to_bytes(4,'big')).digest() for i in range((len(x)+31)//32))
print('FLAG:', bytes(p^q for p,q in zip(x,z)).decode())
