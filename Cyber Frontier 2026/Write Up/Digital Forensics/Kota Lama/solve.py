from PIL import Image
import hashlib

im = Image.open("capture-101.png").convert("RGB")
bits = []
for r, g, b in im.getdata():
    bits += [r & 1, g & 1, b & 1]

out = bytearray()
for i in range(0, len(bits) - 7, 8):
    byte = 0
    for bit in bits[i:i+8]:
        byte = (byte << 1) | bit   # MSB first
    if byte == 0:                  # berhenti di NUL pertama
        break
    out.append(byte)

print(out)
h = hashlib.sha256(bytes(out)).hexdigest()
print(f"CF2{{kota_lama_{h[:24]}}}")
