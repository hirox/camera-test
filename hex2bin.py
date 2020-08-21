# HEX Stream to Binary

import binascii

f = open('in.txt','rb')
o = open('out.txt','wb')

while True:
    b = f.read(2)
    if b == '':
        break
    b = binascii.unhexlify(b)
    o.write(b)

f.close()
o.close()