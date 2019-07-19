#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import subprocess
import glob
import hashlib
import shutil

def md5sum_of(f):
    return hashlib.md5(open(f, 'rb').read()).hexdigest()

##---------------------------------------------------------------------------

def get_max_box(boxes):
    left = min([l for (l, u, r, d) in boxes])
    upper = min([u for (l, u, r, d) in boxes])
    right = max([r for (l, u, r, d) in boxes])
    down = max([d for (l, u, r, d) in boxes])
    return (left, upper, right, down)

def do_get_real_bbox(image):
    imageComponents = image.split()
    if len(imageComponents) < 4:
        print('no alpha channel found!!!!!')
        return image.getbbox()
    rgbImage = Image.new("RGB", image.size, (0,0,0))
    rgbImage.paste(image, mask = imageComponents[3])
    return rgbImage.getbbox()

def get_real_bbox(image):
    bbox = image.getbbox()
    if bbox == (0, 0, image.size[0], image.size[1]) or bbox is None:
        bbox = do_get_real_bbox(image)
    if bbox is None:
        return (0, 0, image.size[0], image.size[1])
    else:
        l, u, r, d = bbox
        width, height = image.size
        if l > width - r:
            l = width - r
        else:
            r = width - l
        return (l, u, r, d)

def do_crop(image, bbox):
    l, u, r, d = bbox
    width = r - l
    height = d - u

    if width > image.size[0]:
        l = (image.size[0] - width) / 2
        r = l + width
    if height > image.size[1]:
        u = image.size[1] - height
        d = u + height

    return image.crop((l, u, r, d))

def crop(directory):
    pngs = glob.glob('%s/*.png' % (directory, ))
    images = [Image.open(png) for png in pngs]
    bboxes = [get_real_bbox(i) for i in images]
    max_box = get_max_box(bboxes)

    cropped = [do_crop(i, max_box) for i in images]
    for i in range(0, len(images)):
        cropped[i].save(pngs[i])

##---------------------------------------------------------------------------
from config import TexturePacker

tp_cache = {}

for l in open('tp_cache.txt', 'r'):
    d, a, m = l.strip().split(',')
    tp_cache[d.strip()] = (a.strip(), m.strip())

def update_tp_cache(d, a, m):
    tp_cache[d] = (a, m)
    f = open('tp_cache.txt.1', 'wb')
    for k in sorted(tp_cache.keys()):
        f.write('%s,%s,%s\n' % (k, tp_cache[k][0], tp_cache[k][1]))
    f.close()
    os.remove('tp_cache.txt')
    os.rename('tp_cache.txt.1', 'tp_cache.txt')

algorithms = [
    '--algorithm MaxRects --maxrects-heuristics best',
    '--algorithm MaxRects --maxrects-heuristics shortSide',
    '--algorithm MaxRects --maxrects-heuristics longSide',
    '--algorithm MaxRects --maxrects-heuristics area',
    '--algorithm MaxRects --maxrects-heuristics bottomLeft',
    '--algorithm MaxRects --maxrects-heuristics contactPoint',
    '--basic-order ascending --algorithm Basic --basic-sort-by best',
    '--basic-order ascending --algorithm Basic --basic-sort-by name',
    '--basic-order ascending --algorithm Basic --basic-sort-by width',
    '--basic-order ascending --algorithm Basic --basic-sort-by height',
    '--basic-order ascending --algorithm Basic --basic-sort-by area',
    '--basic-order ascending --algorithm Basic --basic-sort-by circumference',
    '--basic-order descending --algorithm Basic --basic-sort-by best',
    '--basic-order descending --algorithm Basic --basic-sort-by name',
    '--basic-order descending --algorithm Basic --basic-sort-by width',
    '--basic-order descending --algorithm Basic --basic-sort-by height',
    '--basic-order descending --algorithm Basic --basic-sort-by area',
    '--basic-order descending --algorithm Basic --basic-sort-by circumference',
]

cmd = [TexturePacker,
       '%s',                   # algorithm
       '--trim',
       '--enable-rotation',
       '--allow-free-size',
       '--opt RGBA8888',
       '--sheet "%s"',
       '--data "%s"',
       "%s"
      ]

def get_image_size(f):
    i = Image.open(f)
    w, h = i.size
    return w * h

def pack(directory, out):
    png = out + '.png'
    plist = out + '.plist'

    if directory in tp_cache:
        al, md5 = tp_cache[directory]
        subprocess.call(' '.join(cmd) % (al, png, plist, directory))
        if md5sum_of(png) == md5:
            print 'tp cache hitted for %s' % (directory, )
            return png, plist

    name = os.path.basename(directory)
    tmp_png = name + '.png'
    tmp_plist = name + '.plist'

    best_algorithm = ''
    best_md5 = ''
    smallest = 2048*2048        # max size of sheet

    for al in algorithms:
        subprocess.call(' '.join(cmd) % (al, tmp_png, tmp_plist, directory))
        size = get_image_size(tmp_png)
        if size < smallest:
            smallest = size
            best_algorithm = al
            best_md5 = md5sum_of(tmp_png)
        os.remove(tmp_png)
        os.remove(tmp_plist)

    update_tp_cache(directory, best_algorithm, best_md5)
    subprocess.call(' '.join(cmd) % (best_algorithm, png, plist, directory))
    return png, plist

##---------------------------------------------------------------------------
import plistlib

def plist_add_prefix(plist, prefix):
    d = plistlib.readPlist(plist)
    frames = {}
    for k, v in d['frames'].items():
        if not k.startswith(prefix):
            k = prefix + k
            frames[k] = v
    d['frames'] = frames
    plistlib.writePlist(d, plist)

def to_rect(s):
    s = s.replace('{', '').replace('}', '')
    return 'CCRect(%s)' % (s, )

def to_size(s):
    s = s.replace('{', '').replace('}', '')
    return 'CCSize(%s)' % (s, )

def to_point(s):
    s = s.replace('{', '').replace('}', '')
    return 'CCPoint(%s)' % (s, )

def plist_to_lua(plist, png, prefix):
    d = plistlib.readPlist(plist)
    frames = []
    for k, v in d.frames.items():
        s = '["%s%s"] = { texture = "%s", rect = %s, offset = %s, size = %s, rotated = %d },\n' % (
            prefix, k, png, to_rect(v["frame"]), to_point(v["offset"]),
            to_size(v['sourceSize']), 1 if v['rotated'] else 0)
        frames.append(s)
    return ''.join(frames)


##---------------------------------------------------------------------------

from config import TruePNG, PNGOut, JpegOptim
import os
import shutil

def optimize_png(png):
    md5 = md5sum_of(png)
    cached = 'cache/%s.png' % (md5, )
    if os.path.exists(cached):
        print('cache hitted, %s' % (md5, ))
        shutil.copyfile(cached, png)
        return

    # first run TruePNG on file
    subprocess.call(' '.join([TruePNG, '/o3', '"%s"' % (png, )]))
    subprocess.call(' '.join([PNGOut, '"%s"' % (png, )]))

    shutil.copyfile(png, cached)

def optimize_jpg(jpg):
    md5 = md5sum_of(jpg)
    cached = 'cache/%s.jpg' % (md5, )
    if os.path.exists(cached):
        print('cache hitted, %s' % (md5, ))
        shutil.copyfile(cached, jpg)
        return

    subprocess.call(' '.join([JpegOptim, '-s', '-m 80', '"%s"' % (jpg, )]))
    shutil.copyfile(jpg, cached)

##---------------------------------------------------------------------------

from config import PNGQuant
def png_quantize(png):
    subprocess.call(' '.join([PNGQuant, '-v', '-f', '--speed 1', '--ext .png', '"%s"' % (png, )]))

def png_quantize2(png, quality):
    subprocess.call(' '.join([PNGQuant, '-v', '-f', '--speed 1', '--ext .png',
                     '--quality %d-100' % (quality, ), '"%s"' % (png, )]))









