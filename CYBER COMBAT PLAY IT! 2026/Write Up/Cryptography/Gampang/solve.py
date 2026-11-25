import hashlib

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

r = int("3eda649e8c449b80bd985fca344555954a58c9fbd7cd7d28259f1cf11ce5b877", 16)

s1 = int("4c5ee4d369c7ab3b6c806626e477a311c7c075a4d8742513bf6b50ff52611a7c", 16)
s2 = int("40ae2694d8be3d82048ef6a120550f3dbb70ef22822b3d3a3846f2469e277eae", 16)

sha = "1c6225c80416d5957b77da5bbaeec3ecbbba778b7c8bed616192f54293ad6d36"

z1 = int.from_bytes(hashlib.sha256(b"A").digest(), "big")
z2 = int.from_bytes(hashlib.sha256(b"B").digest(), "big")

k = (z1-z2) * pow(s1-s2, -1, N) % N
d = (s1*k-z1) * pow(r, -1, N) % N

z = int(sha, 16)
s = pow(k, -1, N) * (z+r*d) % N

print("Private key:", hex(d))
print("Signature r:", hex(r))
print("Signature s:", hex(s))