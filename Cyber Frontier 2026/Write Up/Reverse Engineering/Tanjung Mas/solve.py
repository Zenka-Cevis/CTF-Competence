MASK = 0xFFFFFFFF

def rol(x, n):
    x &= MASK
    return ((x << n) | (x >> (32 - n))) & MASK

def f(x, k):
    return (rol(x ^ k, 5) + rol(x, 13)) & MASK

# Key: 16 uint32 dari 0x2080..0x20bf (baca 4 byte, little-endian)
hexdata = bytes.fromhex(
    "f78840baa2dbdfb39dd2754182457716"
    "d5c509ea525b20580895b6825332bf9b"
    "98f2495105b6aa0ec43e4383b828094c"
    "a4a975b0ff9bb61386d6260e8f3ab8a9"
)
keys = [int.from_bytes(hexdata[i:i+4], 'little') for i in range(0, 64, 4)]
assert len(keys) == 16

# Target
s15 = 0xbdae4507
s16 = 0x781b2a2c

# Recover mundur: state_{i-1} = f(state_i, key[i]) ^ state_{i+1}
s = {16: s16, 15: s15}
for i in range(15, -1, -1):
    s[i-1] = (f(s[i], keys[i]) ^ s[i+1]) & MASK

A = s[-1]   # word pertama (4 byte pertama)
B = s[0]    # word kedua (4 byte terakhir)

serial = A.to_bytes(4, 'little') + B.to_bytes(4, 'little')
print("Serial :", serial)
print("Hex    :", serial.hex())
print("Printable:", repr(serial))
