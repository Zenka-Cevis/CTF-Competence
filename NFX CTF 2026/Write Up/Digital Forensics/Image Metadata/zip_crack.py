#!/usr/bin/env python3
"""
zip_crack.py — Dictionary/wordlist brute-forcer for password-protected ZIP files.

Usage:
    python3 zip_crack.py <target.zip> <wordlist.txt>

Only needs Python's built-in zipfile module (no john/fcrackzip required).
Works on classic ZipCrypto-encrypted zips.
"""

import sys
import zipfile
import os


def crack(zip_path: str, wordlist_path: str, extract_to: str = "extracted"):
    zf = zipfile.ZipFile(zip_path)

    with open(wordlist_path, "r", errors="ignore") as f:
        lines = f.read().splitlines()

    passwords = [l.strip() for l in lines if l.strip()]
    print(f"[*] Loaded {len(passwords)} candidate passwords")

    os.makedirs(extract_to, exist_ok=True)

    for i, pw in enumerate(passwords, 1):
        try:
            zf.extractall(path=extract_to, pwd=pw.encode())
            print(f"[+] PASSWORD FOUND: {pw!r}  (tried {i}/{len(passwords)})")
            print(f"[+] Files extracted to: {extract_to}/")
            return pw
        except RuntimeError:
            # wrong password
            continue
        except Exception:
            # corrupt extraction artifact from a near-miss, keep going
            continue

    print("[-] No password in the wordlist worked.")
    return None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <target.zip> <wordlist.txt>")
        sys.exit(1)

    crack(sys.argv[1], sys.argv[2])
