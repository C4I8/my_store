#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import shutil
import fnmatch

from atom import crop, pack, plist_add_prefix, plist_to_lua, optimize_png, optimize_jpg
from atom import png_quantize, png_quantize2


# 对资源的处理方式有以下几种：
# keep: 直接拷贝至目标目录
# pack: 小图打包成大的图，优化后输出至目标目录
# animate: 序列帧打包
# optimize: 图片优化大小后输出
# 默认打包为png格式

rules = {}
wildcard_rules = {}
# 打包规则文件 rules.txt
for l in open('rules.txt', 'r'):
    k, r = l.strip().split(',')
    if k.find('*') != -1 or k.find('?') != -1:
        wildcard_rules[k.strip()] = r.strip()
    else:
        rules[k.strip()] = r.strip()

# cache 根据md5索引
cache = 'cache'

# default settings
src = '../assets'
dst = '../output'

BATCH = 0           # 遇到问题时，记录问题，最后再解决
INTERACTIVE = 1     # 遇到问题时，等待解决

mode = INTERACTIVE  # 默认为batch模式

def ensure_dir(d):
    if d != '' and not os.path.exists(d):
        os.makedirs(d)

# make sure we have cache directory
ensure_dir("cache")
# ensure_dir("sheets")
failed = {}
def fail(p, reason):
    if p in failed:
        return
    failed[p] = reason
    open('failed.txt', 'wb').write(str(failed))

def update_rule(p, r):
    rules[p] = r
    f = open('rules.txt.1', 'wb')
    for k in sorted(rules.keys()):
        f.write('%s,%s\n' % (k, rules[k]))
    for k in sorted(wildcard_rules.keys()):
        f.write('%s,%s\n' % (k, wildcard_rules[k]))
    f.close()
    os.remove('rules.txt')
    os.rename('rules.txt.1', 'rules.txt')

def ask_for_rule(p):
    a = 'o'
    a = a.lower()[0]
    if a == 'k':
        update_rule(p, 'keep')
    elif a == 'p':
        update_rule(p, 'pack')
    elif a == 'a':
        update_rule(p, 'animate')
    elif a == 'o':
        update_rule(p, 'optimize')
    else:
        print 'please input k, p, a or o !!!'
        ask_for_rule(p)

def check_animation_files(directory):
    pngs = sorted(glob.glob1(directory, '*.png'))
    names = ['%05d.png' % i for i in range(0, len(pngs))]
    return pngs == names

def animate(p):
    if not check_animation_files('%s/%s' % (src, p)):
        if mode == BATCH:
            fail(p, 'naming error. should be 00000.png, 00001.png, ...')
        else:
            raw_input('%s: naming error, please fix. press enter when done.' % (p, ))
            animate(p)
            return

    s = '%s/%s' % (src, p)
    parent_dir, name = os.path.split(p)
    d = '%s/%s' % (dst, parent_dir)
    ensure_dir(d)

    crop(s)
    pack(s, '%s/%s' % (d, name))
    png_quantize('%s/%s.png' % (d, name))
    optimize_png('%s/%s.png' % (d, name))
    plist_add_prefix('%s/%s.plist' % (d, name), '%s/' % (name, ))

def pack_images(p):
    s = '%s/%s' % (src, p)
    parent_dir, name = os.path.split(p)
    d = '%s/%s' % (dst, parent_dir)
    ensure_dir(d)

    pack(s, '%s/%s' % (d, name))
    png_quantize2('%s/%s.png' % (d, name), 60)
    optimize_png('%s/%s.png' % (d, name))
    open('sheets/%s' % (p.replace('/', '_'), ), 'wb').write(
        plist_to_lua('%s/%s.plist' % (d, name), 'assets/%s.png' % (p, ), 'assets/%s/' % (p, )))
    os.remove('%s/%s.plist' % (d, name))

def optimize(p):
    if os.path.isdir('%s/%s' % (src, p)):
        for f in glob.glob1('%s/%s' % (src, p), '*'):
            optimize('%s/%s' %(p, f))
        return
    parent_dir, _ = os.path.split('%s/%s' % (dst, p))
    ensure_dir(parent_dir)
    shutil.copyfile('%s/%s' % (src, p), '%s/%s' % (dst, p))
    if p.endswith('.png'):
        png_quantize2('%s/%s' % (dst, p), 40)
        optimize_png('%s/%s' % (dst, p))
    else:
        optimize_jpg('%s/%s' % (dst, p))

def xcopy(s, d):
    import shutil
    if os.path.isdir(s):
        if os.path.exists(d):
            shutil.rmtree(d)
        shutil.copytree(s, d, ignore = shutil.ignore_patterns('.svn'))
    else:
        if os.path.exists(d):
            os.remove(d)
        shutil.copyfile(s, d)

def has_subdir(p):
    l = glob.glob1('%s/%s' % (src, p), '*')
    l1 = ['%s/%s/%s' % (src, p, i) for i in l]
    if any([os.path.isdir(i) for i in l1]):
        return True
    return False

def rule_for(p):
    if p in rules:
        return rules[p]
    for k, v in wildcard_rules.items():
        if fnmatch.fnmatch(p, k):
            return v
    return None

def has_rule_begin_with(p):
    for k in rules.keys():
        if k.startswith(p):
            return True
    for k in wildcard_rules.keys():
        if k.startswith(p):
            return True
    return False

def make(p):
    r = rule_for(p)
    if r:
        if r == 'keep':
            xcopy('%s/%s' % (src, p), '%s/%s' % (dst, p))
        elif r == 'animate':
            animate(p)
        elif r == 'pack':
            pack_images(p)
        elif r == 'optimize':
            optimize(p)
        else:
            fail(p, 'unknown rule')
    else:
        if os.path.isfile('%s/%s' % (src, p)):
            if mode == BATCH:
                fail(p, 'no rule')
            else:
                ask_for_rule(p)
                make(p)
        else:
            if not has_subdir(p) and not has_rule_begin_with(p):
                if mode == BATCH:
                    fail(p, 'no rule')
                else:
                    ask_for_rule(p)
                    make(p)
            else:
                for f in glob.glob1('%s/%s' % (src, p), '*'):
                    make('%s/%s' % (p, f))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        make(sys.argv[1])
        sys.exit(0)

    for f in glob.glob1(src, '*'):
        make(f)
