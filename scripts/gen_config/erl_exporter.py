import os
import erl_processor

def to_full_path(basename):
    return os.path.join('../..', 'server', basename + '.erl')

def erl_header(module):
    return '-module(%s).\n' % (module, )

def erl_export(function):
    return '-export([%s]).\n' % (function, )

def erl_include(header):
    return '-include("%s").\n' % (header, )

def key_from_fields(self, item):
        a = item[self.key_fields[0]]
        b = item[self.key_fields[1]]
        return '{%s, %s}' % (a, b)

def gen_function_close_str(key_fields, add_field):
    names = ['none' for f in key_fields] + add_field
    return 'get(%s) -> invalid_parameter.\n' % (','.join(names))

def process_value_by_type(self, item, types):
    processed = []
    if self.processor:
        item = self.processor(item)
        if type(item) == tuple:
            item, processed = item
        else:
            processed = item.keys()

    if types:
        for f, t in types.items():
            if f not in processed:
                item[f] = erl_processor.TYPE_PROCESSOR[t](item[f])
                processed.append(f)

    return item

erl_file_header = """%%% !!! DO NOT EDIT !!!
%%% auto generated from xsl/xml
"""

class ErlSimpleConverter:
    def __init__(self, basename,
                 key_fields = ['id'],
                 value_field = 'value',
                 get_all = False,
                 compare_item = None,
                 processor = None):
        self.basename = basename
        self.key_fields = key_fields
        self.value_field = value_field
        self.function = 'get'
        self.processor = processor
        self.get_all = get_all
        self.compare_item = compare_item

    def gen_function_clause(self, item):
        return 'get(%s) -> %s;\n' % (
                self.function_args(item),
                item[self.value_field])

    def compare_function_clause(self, item):
        if self.compare_item[1] != None:
            return 'get(%s) when P >= %s andalso P =< %s -> %s;\n' % (self.function_args(item),
                            item[self.compare_item[0]],  item[self.compare_item[1]],
                            item[self.value_field])

        return 'get(%s) when P >= %s -> %s;\n' % (self.function_args(item),
                            item[self.compare_item[0]],
                            item[self.value_field])

    def function_args(self, item):
        key = [item[f] for f in self.key_fields]
        if self.compare_item != None:
            key.append('P')

        # print key
        return ', '.join(key)

    def gen_function_close_clause(self):
        return gen_function_close_str(self.key_fields, self.compare_item != None and ['none'] or [])

    def function_comment(self):
        return '%%get(%s)\n' % (', '.join(self.key_fields, ))

    def get_all_keys(self, items):
        if len(self.key_fields) == 1:
            return [int(item[self.key_fields[0]]) for item in items]

        if len(self.key_fields) == 2:
            return '[' + ', '.join([key_from_fields(self, item) for item in items]) + ']'

    def param_num(self):
        if self.compare_item != None:
            return len(self.key_fields) + 1
        return len(self.key_fields)

    def export(self, fields, items, types):
        erl = open(to_full_path(self.basename), 'wb')
        erl.write(erl_file_header)
        erl.write(erl_header(self.basename))
        erl.write(erl_export('get/%d' % (self.param_num(), )))
        if self.get_all:
            erl.write(erl_export('get_all/0'))

            erl.write('get_all() ->\n')
            erl.write('\t%s.\n\n' % (self.get_all_keys(items), ))

        erl.write(self.function_comment())
        for item in items:
            item = process_value_by_type(self, item, types)
            if self.compare_item != None:
                erl.write(self.compare_function_clause(item))
            elif item[self.value_field]:
                erl.write(self.gen_function_clause(item))
        erl.write(self.gen_function_close_clause())
        erl.write('\n')

        erl.close()

class ErlRecordConverter:
    def __init__(self, basename,
                 key_fields = ['id'],
                 record_name = '',
                 header_file = 'data.hrl',
                 get_all = False,
                 processor = None,
                 include_key_fields = True,
                 compare_item = None,
         check_processor = None):
        self.basename = basename
        self.key_fields = key_fields
        self.record_name = record_name or basename
        self.header_file = header_file
        self.processor = processor
        self.get_all = get_all
        self.include_key_fields = include_key_fields
        self.compare_item = compare_item
        self.check_processor = check_processor

    def function_args(self, item):
        key = [item[f] for f in self.key_fields]
        if self.compare_item != None:
            key.append('P')

        # print key
        return ', '.join(key)

    def function_clause(self, item):
        return 'get(%s) ->' % (self.function_args(item), )

    def compare_function_clause(self, item):
        if self.compare_item[1] != None:
            return 'get(%s) when P >= %s andalso P =< %s ->' % (self.function_args(item),
                            item[self.compare_item[0]],  item[self.compare_item[1]])

        return 'get(%s) when P >= %s ->' % (self.function_args(item),
                            item[self.compare_item[0]])

    def record_body(self, fields, item):
        return ',\n'.join(['\t%s = %s' % (f, item[f])
            for f in fields
            if self.include_key_fields or f not in self.key_fields])

    def get_all_keys(self, items):
        if len(self.key_fields) == 1:
            return [int(item[self.key_fields[0]]) for item in items]

        if len(self.key_fields) == 2:
            return '[' + ', '.join([key_from_fields(self, item) for item in items]) + ']'

    def gen_function_clause(self, fields, item):
        return '\n'.join([
            self.function_clause(item),
            '\t#%s{' % (self.record_name, ),
            self.record_body(fields, item),
            '};\n'])

    def gen_compare_function_clause(self, fields, item):
        return '\n'.join([
            self.compare_function_clause(item),
            '\t#%s{' % (self.record_name, ),
            self.record_body(fields, item),
            '};\n'])

    def gen_function_close_clause(self):
        return gen_function_close_str(self.key_fields, self.compare_item != None and ['none'] or [])

    def function_comment(self):
        return '%%get(%s)\n' % (', '.join(self.key_fields), )

    def param_num(self):
        if self.compare_item != None:
            return len(self.key_fields) + 1
        return len(self.key_fields)

    def export(self, fields, items, types):
        erl = open(to_full_path(self.basename), 'wb')
        erl.write(erl_file_header)
        erl.write(erl_header(self.basename))
        erl.write(erl_include(self.header_file))
        erl.write(erl_export('get/%d' % (self.param_num(), )))

        if self.get_all:
            erl.write(erl_export('get_all/0'))
            erl.write('get_all() ->\n')
            erl.write('\t%s.\n\n' % (self.get_all_keys(items), ))

        erl.write(self.function_comment())

        if self.check_processor:
            for item in items:
                self.check_processor(item)

        for item in items:
            item = process_value_by_type(self, item, types)
            if self.compare_item != None:
                erl.write(self.gen_compare_function_clause(fields, item))
            else:
                erl.write(self.gen_function_clause(fields, item))
        erl.write(self.gen_function_close_clause())
        erl.write('\n')

        erl.close()

class ErlArrayConverter:
    def __init__(self, basename,
                 key_fields = ['id'],
                 processor = None):
            self.basename = basename
            self.key_fields = key_fields
            self.processor = processor

    def gen_function_clause(self, field, item):
        return 'get(%s) -> %s;\n' % (
                ', '.join([item[f] for f in self.key_fields] + [field]),
                item[field])

    def gen_function_close_clause(self):
        return gen_function_close_str(self.key_fields, ['_FIELD'])

    def export(self, fields, items, types):
        erl = open(to_full_path(self.basename), 'wb')
        erl.write(erl_file_header)
        erl.write(erl_header(self.basename))
        erl.write(erl_export('get/%d' % (len(self.key_fields) + 1, )))

        for item in items:
            item = process_value_by_type(self, item, types)
            [erl.write(self.gen_function_clause(field, item)) for field in fields]
        erl.write(self.gen_function_close_clause())
        erl.write('\n')

        erl.close()


