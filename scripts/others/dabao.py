import os
import zipfile
import json
import zlib
zlib.Z_DEFAULT_COMPRESSION = 9

def writejson(jsoncontent):
    '''writejson'''
    if jsoncontent:
        return json.dumps(jsoncontent, separators=(',', ':'), sort_keys=True, ensure_ascii=True, encoding='utf-8')
    else:
        return '{}'


def readjson(jsonfile):
    '''readjson'''
    with open(jsonfile, "rb") as jsonfp:
        return json.load(jsonfp, encoding='utf-8')


def make_zip(source_dir, output_filename):
    if os.path.isfile(output_filename):
        os.remove(output_filename)
    zipf = zipfile.ZipFile(output_filename, 'w', zipfile.zlib.DEFLATED)
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            #zipf.write(pathfile, arcname)
            zipf.writestr(arcname, writejson(readjson(pathfile)))
    zipf.close()


if __name__ == '__main__':
    target = os.path.join('..', 'config', 'jsons')
    output = os.path.join('..', 'config', 'data.zip')
    make_zip(target, output)
