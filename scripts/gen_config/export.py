#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import export_one

reload(sys)
sys.setdefaultencoding('utf-8')

for f in os.listdir(os.path.join('../..', 'excel')):
    if not f.endswith('.xls'):
        continue
    print('begin to export %s ...' % (f, ))
    try:
        export_one.export(os.path.join('../..', 'excel', f))
    except Exception:
        print "error %s" % f




