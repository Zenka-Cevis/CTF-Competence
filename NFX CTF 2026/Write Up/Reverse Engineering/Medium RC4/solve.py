def rc4(key, data):
    S = list(range(256)); j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xff
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = bytearray()
    for b in data:
        i = (i + 1) & 0xff
        j = (j + S[i]) & 0xff
        S[i], S[j] = S[j], S[i]
        out.append(b ^ S[(S[i] + S[j]) & 0xff])
    return bytes(out)

key = b"n0t_s3cur3_k3y_2026"
ct  = bytes.fromhex("ada1e2de80fab7a465572a79e3ecf825690a5cca49dff6caa4c29c36d2485f17bb3e29d201f7009c9d31")
print(rc4(key, ct))
