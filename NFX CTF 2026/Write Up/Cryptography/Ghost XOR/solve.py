ct = bytes.fromhex("02091b08180938337c3d1c7a3f10303e3c7c31147f7b3032133d722c243b1c2a74297a287e32")

known = b"NFXC"
key = bytes(c ^ p for c, p in zip(ct, known))
print("Key:", key)

flag = bytes(ct[i] ^ key[i % len(key)] for i in range(len(ct)))
print(flag.decode())
