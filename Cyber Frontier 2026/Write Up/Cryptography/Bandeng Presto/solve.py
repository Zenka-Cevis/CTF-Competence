import csv, json, hashlib, hmac, itertools

# --- GF(2^8) dengan polinomial 0x11B ---
def gmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return r

def ginv(a):
    for i in range(1, 256):
        if gmul(a, i) == 1:
            return i

# --- 1. Baca share & verifikasi commitment ---
valid = []
with open("device-shares.csv") as f:
    for row in csv.DictReader(f):
        x = row["x"].strip()
        y = bytes.fromhex(row["share_hex"].strip())
        h = hashlib.sha256(x.encode() + b":" + y).hexdigest()
        ok = h == row["provisioning_commitment_sha256"].strip()
        print(row["device"], "VALID" if ok else "REJECT")
        if ok:
            valid.append((int(x), y))

# --- 2. Interpolasi Lagrange di x=0 (threshold 2) ---
def recover(s1, s2):
    (x1, y1), (x2, y2) = s1, s2
    inv = ginv(x1 ^ x2)
    l1 = gmul(x2, inv)
    l2 = gmul(x1, inv)
    return bytes(gmul(a, l1) ^ gmul(b, l2) for a, b in zip(y1, y2))

# --- 3. Key stream: SHA256(secret || counter32be) ---
def keystream(secret, n):
    out, c = b"", 0
    while len(out) < n:
        out += hashlib.sha256(secret + c.to_bytes(4, "big")).digest()
        c += 1
    return out[:n]

# --- 4. Baca archive, verifikasi HMAC, dekripsi ---
with open("archive.enc") as f:
    arc = json.load(f)
ct = bytes.fromhex(arc["ciphertext_hex"])
mac = bytes.fromhex(arc["hmac_sha256"])

s1, s2 = valid[0], valid[1]          # cukup 2 share valid
secret = recover(s1, s2)
print("secret:", secret.hex())

calc = hmac.new(secret, ct, hashlib.sha256).digest()
if not hmac.compare_digest(calc, mac):
    raise SystemExit("HMAC gagal, jangan dekripsi")

pt = bytes(a ^ b for a, b in zip(ct, keystream(secret, len(ct))))
print("plaintext:", pt.decode())
print("FLAG: CF2{bandeng_presto_%s}" % hashlib.sha256(pt).hexdigest()[:24])
