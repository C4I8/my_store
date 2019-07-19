import json
import os
import json_processor


json_name_keys = {}
with open('../json_name_keys.json') as file:
    json_name_keys = json.load(file)

def to_full_path(basename):
    return os.path.join('../..', 'config', 'jsons', basename + '.json')

def process_value_by_type(self, item, types):
    processed = []
    if self.processor:
        item = self.processor(item)
        if type(item) == tuple:
            item, processed = item
        else:
            processed = item.keys()
    elif types:
        for f, t in types.items():
            if f not in processed:
                item[f] = json_processor.TYPE_PROCESSOR[t](item[f])
                processed.append(f)

    for k, v in item.items():
        if k not in processed:
            item[k] = json_processor.None_if_empty_else_number_or_quote(v)

    return item

class JsonRecordExporter:
    def __init__(self,
                 basename,
                 key_field,
                 processor = None):
        self.basename = basename
        self.key_field = key_field
        self.processor = processor

    def export(self, fields, items, types):
        content = {};
        if(self.basename in json_name_keys):
            print('[json_name_keys.json]==> use keys',json_name_keys[self.basename])

        for item in items:
            item = process_value_by_type(self, item, types)
            # print(json_name_keys)
            if(self.basename in json_name_keys):
                keys =json_name_keys[self.basename]
                # print('use keys',keys)
                if(len(keys)==1):
                    content[item[keys[0]]]=item
                elif len(keys)==2:
                    if content.has_key(item[keys[0]]) == False:
                        content[item[keys[0]]]={}
                    content[item[keys[0]]][item[keys[1]]] = item
            else:
                if self.key_field in item:
                    content[item[self.key_field]] = item

        with open(to_full_path(self.basename), 'wb') as file:
            json.dump(content, file, sort_keys=True, separators=(',', ': '), ensure_ascii=False, indent = 4, encoding='utf-8')
