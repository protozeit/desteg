#/usr/bin/env python

import argparse
import sys
import random
import numpy as np
from PIL import Image
from string import printable
from itertools import groupby

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def set_bit(v, index, x):
    mask = 1 << index
    v &= ~mask
    if x:
        v |= mask
    return v

def get_plane(img, channel, index=0):
    if channel in img.mode:
        plane_data = np.zeros(img.size, dtype=np.uint8)
        print(img.size)
        img_data = img.load()

        channel_index = img.mode.index(channel)

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                color = img_data[x, y]
                channel = color[channel_index]
                plane = bin(channel)[2:].zfill(8)

                plane_data[x, y] = int(plane[abs(index-7)])
        return plane_data

def set_plane(img, channel, data, index=0):
    if channel in img.mode:
        # new_data = np.zeros((*img.size, len(img.mode)), dtype=np.uint8)
        new_image = Image.new(img.mode, img.size)
        new_image_data = new_image.load()
        img_data = img.load()
        channel_index = img.mode.index(channel)

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                try:
                    pixel = list(img_data[x, y])
                    pixel[channel_index] = set_bit(pixel[channel_index], index, data[x,y])
                    new_image_data[x, y] = tuple(pixel)
                except IndexError:
                    pass
        return new_image


# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument(dest='input', help="input image")
parser.add_argument(dest='output', help="output image")
parser.add_argument('-c', '--channel', type=str, help="channel to overwrite, for example: -c B")
parser.add_argument('-s', '--severity', type=int, help="controls how destructive the overwriting is")

# Parse and print the results
args = parser.parse_args()

# print(args.input)
# print(args.output)
# print(args.channel)

index = 0 if args.severity is None else clamp(args.severity, 0, 7)
img = Image.open(args.input)


if args.channel:
    if not args.channel in img.mode:
        print('channel not in mode')
        sys.exit(1)
    plane_data = get_plane(img, args.channel, index=index)
    for x in range(plane_data.shape[0]):
        for y in range(plane_data.shape[1]):
            # plane_data[x, y] ^= random.getrandbits(1)
            plane_data[x, y] ^= 1

    x = set_plane(img, args.channel, plane_data, index=index)
    x.save(args.output)
else:
    for ch in img.mode:
        plane_data = get_plane(img, ch)
        for x in range(plane_data.shape[0]):
            for y in range(plane_data.shape[1]):
                plane_data[x, y] ^= 1

        d = set_plane(img, ch, plane_data)
        d.save(args.output)

