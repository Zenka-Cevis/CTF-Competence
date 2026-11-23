import sys
from Crypto.Util.number import long_to_bytes

def load(path="output.txt"):
    d = {}
    for line in open(path):
        k, v = line.strip().split(" = ")
        d[k] = int(v)
    return d

def main():
    d = load(sys.argv[1] if len(sys.argv) > 1 else "output.txt")
    N, e, c, leak = d["N"], d["e"], d["c"], d["leak"]
    bits, leak_bits = d["bits"], d["leak_bits"]
    print("N bits:", N.bit_length())
    print("leak bits:", leak_bits)
    print("hint: q - p < 2^256  (twin-ish)")
    print("hint: you have top 32 bits of p")
    print("hint: Coppersmith small root on f(x) = (leak<<(bits/2-leak_bits) + x) | N")

if __name__ == "__main__":
    main()