#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
from xls_to_records import parse_excel
import gen_json
import gen_erl

reload(sys)
sys.setdefaultencoding('utf-8')

def export(f):
    if not f.endswith('.xls'):
        print('error: support xls only')
        return
    basename = os.path.basename(f)
    print('exporting %s to json ...' % (f, ))
    _, s_fields, c_fields, s_items, c_items, s_types, c_types = parse_excel(f)
    c_fields = [n for (_, n) in sorted(c_fields.items())]
    gen_json.export(basename, c_fields, c_items, c_types)

    print('\nexporting %s to erl ...' % (f, ))
    s_fields = [n for (_, n) in sorted(s_fields.items())]
    gen_erl.export(basename, s_fields, s_items, s_types)

if __name__ == '__main__':
    export(sys.argv[1])


