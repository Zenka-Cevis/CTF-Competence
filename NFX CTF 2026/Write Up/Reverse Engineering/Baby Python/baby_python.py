#!/usr/bin/env python3
import base64
import sys

_enc = b'fTNmNHNfdDBuXzNyNF9zZDFrX3RwMXJjc19uMGh0eXB7WEZO'


def main():
    if len(sys.argv) < 2:
        print(f"Pemakaian: {sys.argv[0]} <flag>")
        return 2
    candidate = sys.argv[1].encode()
    if candidate[::-1] == base64.b64decode(_enc):
        print("Correct! Python membaca dari belakang.")
        return 0
    print("Wrong!")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
