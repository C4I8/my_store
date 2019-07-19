#!/usr/bin/python

import os
import shutil
from plist_to_json import plist_to_json
from update_plist import plist_add_dir_name

def isTarget(d):
    if not os.path.isdir(d):
        return False
    empty=True
    for f in os.listdir(d):
        empty=False
        path=os.path.join(d, f)
        if not os.path.isfile(path) or f.split('.')[1] != 'png':
            return False
    return not empty

def packInDir(d, l):
    for f in os.listdir(d):
        path=os.path.join(d, f)
        if isTarget(path):
            l.append(path)
        elif os.path.isdir(path):
            packInDir(path, l)

result = []
packInDir(".", result)

if not os.path.exists('output'):
    os.mkdir('output')

for e in result:
    name = e.replace(os.path.sep, "_")
    name = name[2:]
    plist = name + ".plist"
    png = name + ".png"
    output="output"
    plist_path = os.path.join('.', output, plist)
    png_path = os.path.join('.', output, png)
    os.system('TexturePacker \
            --algorithm MaxRects \
            --maxrects-heuristics best \
            --trim --disable-rotation --allow-free-size \
            --opt RGBA8888 --sheet %s --data %s %s' % (png_path, plist_path, e))
    plist_add_dir_name(plist_path)
    plist_to_json(plist_path)
    os.remove(plist_path)
