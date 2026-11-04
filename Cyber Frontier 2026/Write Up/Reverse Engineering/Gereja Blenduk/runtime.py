import sys,struct,json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
s=sys.argv[1].encode('ascii') if len(sys.argv)==2 else b''
if len(s)!=8:raise SystemExit('serial: 8 ASCII bytes')
b=(p/'program.bin').read_bytes()
if len(b)!=148 or b[:4]!=b'BLV5':raise SystemExit('invalid program')
a=struct.unpack('<72H',b[4:]);v=[(x*197+31)&255 for x in s]
for i in range(8):
 if sum(a[8*i+j]*v[j] for j in range(8))%257!=a[64+i]:raise SystemExit('serial rejected')
x=bytes.fromhex(json.loads((p/'vault.json').read_text())['ciphertext_hex']);k=hashlib.sha256(s).digest()
z=b''.join(hashlib.sha256(k+i.to_bytes(4,'big')).digest() for i in range((len(x)+31)//32))
print(bytes(a^b for a,b in zip(x,z)).decode())
