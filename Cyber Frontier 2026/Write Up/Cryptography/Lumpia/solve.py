ct1 = bytes.fromhex("cad02fd0dbd2517592c115d1a37498fbb6b552b8a6a2474aaff724eae14c96f2bdf103e2fef6410af7")
ct2 = bytes.fromhex("c5c350fbf1e1054ab4ea0feffb4fdba8e7da52e6f0a04908f8e766bbeb4498a0b7e601b5aaaa01")
prefix = b"LUMPIA-ORDER-V3:"

mask = bytes(a ^ b for a, b in zip(ct1, prefix))
print("mask:", mask.hex())

pt2 = bytes(c ^ mask[i % 16] for i, c in enumerate(ct2))
print(pt2)
