#!/usr/bin/env python

from BitVector import BitVector
from PIL import Image
from hilbertcurve.hilbertcurve import HilbertCurve
import sys
import math

img  = Image.open(sys.argv[1])

# build a list of hilbert curve coordinates
hc = HilbertCurve(int(math.log2(img.height)), 2)
locations = [hc.coordinates_from_distance(i) for i in range(hc.max_h+1)]

# iterate the pixels in transposed hilbert curve order
bitlist = [img.getpixel((y,x))[2] & 1 for (x,y) in locations]
BitVector(bitlist=bitlist).write_to_file(open("out.png", "wb"))

Image.open("out.png")
# from math import log
# from itertools import izip
# from string import printable
# from re import findall

# def grouped(iterable, n):
#     "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
#     return izip(*[iter(iterable)]*n)

# def dtoxy(n, d):
#     t = d 
#     rx = ry = x = y = 0
#     s = 1
#     while (s < n):
#         rx = 1 & (t/2)
#         ry = 1 & (t ^ rx)
#         x,y = rot(s,x,y,rx,ry)
#         x+=s*rx
#         y+=s*ry
#         t/=4
#         s*=2
#     return x, y

# def rot(n,x,y,rx,ry):
#     if ry == 0:
#         if rx == 1:
#             x = n-1 - x
#             y = n-1 - y
#         x, y = y, x
#     return x, y

# def get_bit(img, channel, x, y, index=0):
#     if channel in img.mode:
#         img_data = img.load()
#         channel_index = img.mode.index(channel)
#         color = img_data[x, y]
#         channel = color[channel_index]
#         plane = bin(channel)[2:].zfill(8)
#         return plane[abs(index-7)]

# img = Image.open('stego.png')
# pix = img.load()
# width, height = img.size
# n = 2**min(int(log(width, 2)), int(log(height, 2)))

# i = 0
# buff = []
# c = []
# for channel in 'RGB':
#     for index in range(8):
#         while i < height*width:
#             x, y = dtoxy(n,i)
#             c.append(get_bit(img, channel, x, y, index))
#             if len(c) == 8:
#                 num = int(''.join(c), 2)
#                 if chr(num) in printable:
#                     buff.append(chr(num))
#                 c = []
                
#             i += 1

#         print(findall(r'VolgaCTF{.*}', ''.join(buff)))

