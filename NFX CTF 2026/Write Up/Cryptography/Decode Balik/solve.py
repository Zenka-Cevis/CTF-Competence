import sys, base64, zlib
import numpy as np
from PIL import Image

def b64(d):
    d = d.strip()
    return base64.b64decode(d + b"=" * (-len(d) % 4))

im = np.array(Image.open(sys.argv[1]).convert("RGBA"))
gray, alpha = im[:, :, 0].flatten(), im[:, :, 3].flatten()

s1 = bytes(gray[alpha != 0].tolist())
s2 = b64(s1)
s3 = zlib.decompress(s2)
s4 = b64(s3)

open(sys.argv[2], "wb").write(s4)
