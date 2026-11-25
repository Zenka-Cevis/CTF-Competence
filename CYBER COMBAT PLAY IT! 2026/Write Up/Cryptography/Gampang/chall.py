#!/usr/bin/env python3
import hashlib
import os
import secrets
import json
from ecdsa.curves import SECP256k1

FLAG = open("flag.txt", "rb").read()

G = SECP256k1.generator
N = SECP256k1.order
D = secrets.randbelow(N - 1) + 1
K = secrets.randbelow(N - 1) + 1

def sign(message: bytes):
    z = int.from_bytes(hashlib.sha256(message).digest(), "big") % N
    r = (G * K).x() % N
    return r, (pow(K, -1, N) * (z + r * D)) % N

P = G * D
sha = hashlib.sha256(FLAG.encode()).digest()
T = sign(FLAG.encode())

def banner():
    print("\n============ MENU ============")
    print("1. Sign message")
    print("2. Submit signature")
    print("3. Exit")

def main():
    data = {"x": int(P.x()), "y": int(P.y()), "sha": sha.hex()}
 
    print(json.dumps(data))

    while True:
        banner()
        choice = input("> ").strip()
        if choice == "1":
            try:
                r, s = sign(bytes.fromhex(input("Message (hex): ").strip()))
                print(f"r = {r:064x}\ns = {s:064x}")
            except ValueError:
                print("Invalid input!")
        elif choice == "2":
            try:
                r = int(input("Signature r (hex): "), 16)
                s = int(input("Signature s (hex): "), 16)
                if (r, s) == T:
                    print(f"\n[+] Correct signature!\n[+] FLAG: {FLAG}")
                else:
                    print("\n[-] Invalid signature!")
            except ValueError:
                print("Invalid signature format!")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
