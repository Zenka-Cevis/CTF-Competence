import struct

def tea_decrypt_block(v0, v1, k):
    delta = 0x9e3779b9
    s = (delta * 32) & 0xffffffff
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k[2]) ^ (v0 + s) ^ ((v0 >> 5) + k[3]))) & 0xffffffff
        v0 = (v0 - (((v1 << 4) + k[0]) ^ (v1 + s) ^ ((v1 >> 5) + k[1]))) & 0xffffffff
        s = (s - delta) & 0xffffffff
    return v0, v1

key = [0x1337beef, 0xcafebabe, 0xdeadc0de, 0x0badf00d]
ct_hex = "d08b910e9e3d818eeadab483cfc8fd8a083b44836a130476724d7205905af697db1395e7c74c5385"
ct = bytes.fromhex(ct_hex)

out = b""
for i in range(0, len(ct), 8):
    v0, v1 = struct.unpack("<II", ct[i:i+8])
    d0, d1 = tea_decrypt_block(v0, v1, key)
    out += struct.pack("<II", d0, d1)

print(out)
print(out.rstrip(b"\x00").decode(errors="replace"))
