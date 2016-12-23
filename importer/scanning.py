#!/usr/bin/env python

from PIL import Image
import fastzbarlight as zbarlight
import sys

file_path = sys.argv[1]
with open(file_path, 'rb') as image_file:
    image = Image.open(image_file)
    image.load()

codes = zbarlight.scan_codes('qrcode', image)
codes = [s.decode("utf-8") for s in codes]
print('QR codes: %s' % codes)

