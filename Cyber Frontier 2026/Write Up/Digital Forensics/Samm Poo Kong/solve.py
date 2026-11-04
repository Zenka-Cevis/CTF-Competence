import csv, hashlib, zlib
from collections import defaultdict

rows = list(csv.DictReader(open("fragments.csv")))
target = "1ee8c5ff4e045d1a6897b591fdf59582f006be4f1a35d9bd15d9a3897c5f6a9e"

# kelompokkan per transfer
tr = defaultdict(dict)
for r in rows:
    tr[r["transfer"]][int(r["position"])] = bytes.fromhex(r["hex"])

# cari kombinasi 5 fragmen (satu per posisi) dari transfer berbeda
pos_map = defaultdict(list)
for r in rows:
    pos_map[int(r["position"])].append(bytes.fromhex(r["hex"]))

import itertools
for combo in itertools.product(*[pos_map[p] for p in range(5)]):
    blob = b"".join(combo)
    if hashlib.sha256(blob).hexdigest() == target:
        print("[+] MATCH!")
        data = zlib.decompress(blob)
        print(data.decode(errors="replace"))
        break
else:
    print("[-] tidak ada match, cek asumsi")
