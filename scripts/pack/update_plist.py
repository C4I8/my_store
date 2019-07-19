#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plistlib
import os

def verify_name(key, i):
    f = key
    if key.find('/') != -1:
        list = key.split('/')
        f = list[len(list)-1]
    [n, e] = f.split('.')
    return n == '%05d' % (i, )

def plist_add_dir_name(f):
    basename = os.path.basename(f).split('.')[0]
    d = plistlib.readPlist(f)
    frames = {}
    i = 0
    for k, v in sorted(d['frames'].items()):
        #if not verify_name(k, i):
        #    raise RuntimeError('invalid png name found in %s : %s' % (f, k))
        if k.startswith(basename):
            print('%s: already added, skipped' % (f, ))
            return
        frames['%s/%s' % (basename, k)] = v
        i = i + 1
    d['frames'] = frames
    plistlib.writePlist(d, f)

def plist_process_dir(d):
    for f in os.listdir(d):
        if not f.endswith('plist'):
            continue
        print('begin to process %s ...' % (f, ))
        plist_add_dir_name(os.path.join(d, f))


if __name__ == '__main__':
    directories = [
        os.path.join('..', 'client', 'monster'),
        os.path.join('..', 'client', 'model'),
        os.path.join('..', 'client', 'npc'),
        os.path.join('..', 'client', 'effects'),
        os.path.join('..', 'client', 'pet'),
        os.path.join('..', 'client', 'gather'),
		os.path.join('..', 'client', 'mate'),
        os.path.join('..', 'client', 'rapier'),
    ]


    for d in directories:
        print('process directory %s ...' % (d, ))
        plist_process_dir(d)

