#!/usr/bin/env python3
import hashlib, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

MASTER = b"\x13\x37" * 16
PREFIX = b"user-input-goes-here:"

data = json.load(open("output.txt"))
counter = data["counter"]
iv = bytes.fromhex(data["iv_hex"])
ct = bytes.fromhex(data["ct_hex"])

key = hashlib.sha256(MASTER + counter.to_bytes(4, "little")).digest()[:32]

cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct), 16)

assert pt.startswith(PREFIX + b"|"), pt[:40]
flag = pt[len(PREFIX) + 1:]
print("FLAG:", flag.decode(errors="replace"))
