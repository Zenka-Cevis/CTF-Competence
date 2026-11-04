import hashlib, hmac, zlib, struct, random
from PIL import Image

PHRASE = "lentera-menjaga-arah"
NONCE  = "TM-7419"
IMG    = "kamera-42.png"

key = hashlib.sha256(f"{PHRASE}|{NONCE}".encode()).digest()

img = Image.open(IMG).convert("RGB")
W, H = img.size
px = img.load()

# kandidat row-major: y luar, x dalam
cands = [(x, y) for y in range(H) for x in range(W) if (x + 2*y) % 5 == 0]

seed = int.from_bytes(hashlib.sha256(NONCE.encode()).digest(), "big")
random.Random(seed).shuffle(cands)

# baca bit LSB kanal B, MSB-first per byte
bits = [px[x, y][2] & 1 for (x, y) in cands]
data = bytearray()
for i in range(0, len(bits) - 7, 8):
    b = 0
    for j in range(8):
        b = (b << 1) | bits[i + j]
    data.append(b)
data = bytes(data)

# parse frame
assert data[:3] == b"TM3", f"magic salah: {data[:3]!r}"
length = struct.unpack(">H", data[3:5])[0]
ct  = data[5:5+length]
tag = data[5+length:5+length+16]

# verifikasi HMAC
expect = hmac.new(key, ct, hashlib.sha256).digest()[:16]
print("HMAC ok:", hmac.compare_digest(tag, expect))

# dekripsi XOR keystream blok SHA256(key || counter_be)
def keystream(n):
    out = b""
    c = 0
    while len(out) < n:
        out += hashlib.sha256(key + struct.pack(">I", c)).digest()
        c += 1
    return out[:n]

ks = keystream(len(ct))
compressed = bytes(a ^ b for a, b in zip(ct, ks))
payload = zlib.decompress(compressed)
print(payload)
