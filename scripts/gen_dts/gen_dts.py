
import os
import sys
import json
from zlib import crc32
from zlib import adler32

reload(sys)
sys.setdefaultencoding('utf-8')

excludeFile=["chinese.json"]

def writejson(jsoncontent, filename):
    '''writejson'''
    if jsoncontent:
        with open(filename, "wb") as jsonfp:
            json.dump(jsoncontent, jsonfp, separators=(',', ':'),
                      sort_keys=True, ensure_ascii=True, encoding='utf-8')


def readjson(jsonfile):
    '''readjson'''
    with open(jsonfile, "rb") as jsonfp:
        return json.load(jsonfp)


def get_file_crc32(filename):
    '''get_file_crc32'''
    with open(filename, "rb") as filep:
        filedata = filep.read()
        return hex(long(crc32(filedata)) & 0xFFFFFFFFL)[
            2:-1] + 'x' + hex(long(adler32(filedata)) & 0xFFFFFFFFL)[2:-1]

'''


type0 :=
    'any'                       |
    'null'                      |
    'number'                    |
    'string'                    |
    'boolean'                   |
    ('Array', type|None, len|0) |
    ('Tuple', [type...])        |
    ('Object', {key:[type, isoption]})

type := type0 | [type0...]


'''

def process(t, info):
    if t == 'any':
        return 'any'
    if t == 'number':
        info['has_number'] = True
    elif t == 'string':
        info['has_string'] = True
    elif t == 'boolean':
        info['has_boolean'] = True
    elif t == 'null':
        info['has_null'] = True
    elif t[0] == 'Array':
        if info['a_Array']:
            at = combineType(info['a_Array'][1], t[1])
            alen = info['a_Array'][2] if info['a_Array'][2] == t[2] else 0
            if alen != info['a_Array'][2] or at != info['a_Array'][1]:
                info['a_Array'] = ('Array', at, alen)
        else:
            info['a_Array'] = t
    elif t[0] == 'Tuple':
        info['a_Tuple'][getTypeDesc(t)] = t
    elif t[0] == 'Object':
        if info['a_Object']:
            td = t[1]
            d = info['a_Object'][1]
            for k in d:
                if not d[k][1] and not (k in td):
                    d[k][1] = True
            for k in td:
                v1 = td[k]
                if k in d:
                    v2 = d[k]
                    v2[1] = combineType(v2[1], v1[1])
                    v2[2] = v2[2] or v1[2]
                else:
                    d[k] = v1[:]
        else:
            v0 = t[1]
            v1 = {}
            for k in v0:
                v1[k] = v0[k][:]
            info['a_Object'] = ('Object', v1)

def combineType(type1, type2):
    info = {
        'has_number' : False,
        'has_string' : False,
        'has_boolean' : False,
        'has_null': False,
        'a_Array' : False,
        'a_Tuple' : {},
        'a_Object' : False,
    }
    if type1 == 'any' or type2 == 'any':
        return 'any'
    if type1 == None:
        return type2
    if type2 == None:
        return type1
    if type1 == 'number' or type1 == 'string' or type1 == 'boolean' or type1 == 'null':
        if type2 == type1:
            return type1
        elif isinstance(type2, list):
            if type1 in type2:
                return type2
            else:
                ret = type2[:]
                ret.append(type1)
                return ret
        else:
            return[type1, type2]
    elif type2 == 'number' or type2 == 'string' or type2 == 'boolean' or type2 == 'null':
        if type1 == type2:
            return type2
        elif isinstance(type1, list):
            if type2 in type1:
                return type1
            else:
                ret = type1[:]
                ret.append(type2)
                return ret
        else:
            return[type2, type1]
    else:
        if isinstance(type1, list):
            for t in type1:
                if process(t, info) == 'any':
                    return 'any'
        else:
            if process(type1, info) == 'any':
                return 'any'
        if isinstance(type2, list):
            for t in type2:
                if process(t, info) == 'any':
                    return 'any'
        else:
            if process(type2, info) == 'any':
                return 'any'

        ts = []
        if info['has_boolean']:
            ts.append('boolean')
        if info['has_null']:
            ts.append('null')
        if info['has_number']:
            ts.append('number')
        if info['has_string']:
            ts.append('string')
        if info['a_Array']:
            ts.append(info['a_Array'])
        a_Tuple = info['a_Tuple']
        for k in a_Tuple:
            ts.append(a_Tuple[k])
        if info['a_Object']:
            ts.append(info['a_Object'])
        if len(ts) <= 0:
            return'any'
        elif len(ts) == 1:
            return ts[0]
        else:
            return ts

def getType(v):
    if isinstance(v, int) or isinstance(v, float) or isinstance(v, long):
        return "number"
    elif isinstance(v, list):
        nv = len(v)
        if nv == 0:
            return ('Array', None, 0)
        if nv == 1:
            return ('Tuple', [getType(v[0])])
        if nv == 2:
            return ('Tuple', [getType(v[0]), getType(v[1])])
        if nv == 3:
            return ('Tuple', [getType(v[0]), getType(v[1]), getType(v[2])])
        if nv == 4:
            return ('Tuple', [getType(v[0]), getType(v[1]), getType(v[2]), getType(v[3])])
        ret = getType(v[0])
        i = 1
        while i < nv:
            ret = combineType(ret, getType(v[i]))
            i = i + 1
        return ('Array', ret, nv)
    elif isinstance(v, tuple):
        ts = []
        n = len(v)
        i = 0
        while i < n:
            ts.append(getType(v[i]))
            i = i + 1
        return ('Tuple', ts)
    elif isinstance(v, dict):
        ts = {}
        for k in v:
            ts[k] = [getType(v[k]), False]
        return ("Object", ts)
    elif isinstance(v, bool):
        return "boolean"
    elif isinstance(v, str) or isinstance(v, unicode):
        return"string"
    elif v == None:
        return 'null'
    else:
        return "any"

def getTypeDesc(t, b = False):
    if isinstance(t, list):
        n = len(t)
        if n <= 0:
            return 'any'
        elif n == 1:
            return getTypeDesc(t[0], b)
        else:
            ret = ''
            tts = None
            tt = True
            for v in t:
                if isinstance(v, tuple) and 'Tuple' == v[0]:
                    for vt in v[1]:
                        if True == tt:
                            tt = vt
                            tts = getTypeDesc(tt)
                        elif tts != getTypeDesc(tt):
                            tt = False
                            tts = None
                            break
            if tts:
                for i in range(n):
                    v = t[i]
                    if isinstance(v, tuple) and 'Array' == v[0] and None == v[1]:
                        t[i] = ('Array', tt, v[2])
            for v in t:
                if ret == '':
                    ret = getTypeDesc(v)
                else:
                    ret = ret + '|' + getTypeDesc(v)
            if b:
                return '(' + ret + ')'
            else:
                return ret
    elif t == 'number' or t == 'string' or t == 'boolean' or t == 'null':
        return t
    elif isinstance(t, tuple):
        if 'Array' == t[0]:
            if 0 < t[2] and t[2] <= 4:
                tn = getTypeDesc(t[1])
                ret = tn
                for _i in range(t[2] - 1):
                    ret = ret + ',' + tn
                return '[' + ret + ']'
            else:
                return getTypeDesc(t[1], True) + '[]'
        elif 'Tuple' == t[0]:
            ret = ''
            i = 0
            ts = t[1]
            n = len(ts)
            if 0 == n:
                return 'any[]'
            while i < n:
                if 0 == i:
                    ret = getTypeDesc(ts[i])
                else:
                    ret = ret + ',' + getTypeDesc(ts[i])
                i = i + 1
            return '[' + ret + ']'
        elif 'Object' == t[0]:
            ret = ''
            d = t[1]
            for k in d:
                v = d[k]
                if v[1]:
                    ret = ret + k + '?:' + getTypeDesc(v[0]) + ','
                else:
                    ret = ret + k + ':' + getTypeDesc(v[0]) + ','
            return '{' + ret + '}'
    return 'any'

def getInterfaceName(s):
    s = s[:s.index('.json')]
    arr = s.split('_')
    result = []
    for e in arr:
        result.append(e[0].upper() + e[1:])
    return 'I' + ('').join(result) + 'Config'

content = ""
content2 = """/// <reference path="config.d.ts" />
namespace Config{
    export function chinese(): any{ return ConfigUtil.$('chinese') }

"""

special = {}
with open('dts.json') as file:
    special = json.load(file)

json_name_keys = {}
with open('../json_name_keys.json') as file:
    json_name_keys = json.load(file)

hash_path = os.path.normpath(os.path.join('../..', 'code', 'config.hash'))
hash_value = {}
if os.path.isfile(hash_path):
    hash_value = readjson(hash_path)
    if not('dts.json' in hash_value) or not('json_name_keys.json' in hash_value) or hash_value['dts.json'] != get_file_crc32('dts.json') or hash_value['json_name_keys.json'] != get_file_crc32('../json_name_keys.json'):
        hash_value = {}


for f in os.listdir(os.path.join('../..', 'config', 'jsons')):
    if not f.endswith('.json'):
        continue
    if f in excludeFile:
        continue
    name = f[:f.index('.json')]

    interfaceName = getInterfaceName(f)
    if interfaceName in special:
        content += "interface %s {\n" % (interfaceName,)
        for (k, v) in special[interfaceName].items():
            content += ("    %s: %s;\n") % (k, v)
        content += "}\n"

        content2 += ("        export function %s(): {[index: string]:%s}{ return ConfigUtil.$('%s') }\n") % (name, interfaceName, name)
        continue

    cfg_json_path = os.path.join('../..', 'config', 'jsons', f)
    cfg_hash = get_file_crc32(cfg_json_path)
    if not(cfg_json_path in hash_value) or(hash_value[cfg_json_path][0] != cfg_hash):
        content0 = ''
        content20 = ''
        with open(cfg_json_path) as file:
            content0 += "interface %s {\n" % (interfaceName,)
            if name in json_name_keys:
                keys = json_name_keys[name]
                if(len(keys)==1):
                    content20 = ("        export function %s(): {[%s: string]:%s}{ return ConfigUtil.$('%s') }\n")%(name, keys[0], interfaceName, name)
                    content2 += content20
                    ts = {}
                    ic = 0
                    for (k, v) in json.load(file).items():
                        if ic > 6666:
                            break
                        ic = ic + 1
                        for (k2, v2) in v.items():
                            if k2 in ts:
                                ts[k2] = combineType(ts[k2], getType(v2))
                            else:
                                ts[k2] = getType(v2)
                    for k in ts:
                        content0 += ("    %s: %s;\n") % (k, getTypeDesc(ts[k]))
                elif(len(keys)==2):
                    content20 = ("        export function %s(): {[%s: string]:{[%s: string]:%s} }{ return ConfigUtil.$('%s') }\n")%(name, keys[0], keys[1], interfaceName, name)
                    content2 += content20
                    ts = {}
                    ic = 0
                    for (k, v) in json.load(file).items():
                        if ic > 6666:
                            break
                        for (k2, v2) in v.items():
                            if ic > 6666:
                                break
                            ic = ic + 1
                            for(k3, v3) in v2.items():
                                if k3 in ts:
                                    ts[k3] = combineType(ts[k3], getType(v3))
                                else:
                                    ts[k3] = getType(v3)
                    for k in ts:
                        content0 += ("    %s: %s;\n") % (k, getTypeDesc(ts[k]))
            else:
                content20 = ("        export function %s(): {[index: string]:%s}{ return ConfigUtil.$('%s') }\n")%(name, interfaceName, name)
                content2 += content20
                ts = {}
                ic = 0
                for(k, v) in json.load(file).items():
                    if ic > 6666:
                        break
                    ic = ic + 1
                    for (k2, v2) in v.items():
                        if k2 in ts:
                            ts[k2] = combineType(ts[k2], getType(v2))
                        else:
                            ts[k2] = getType(v2)
                for k in ts:
                    content0 += ("    %s: %s;\n") % (k, getTypeDesc(ts[k]))
            content0 += "}\n"
        content += content0
        hash_value[cfg_json_path] = [cfg_hash, content0, content20]
    else:
        hv = hash_value[cfg_json_path]
        content += hv[1]
        content2 += hv[2]

content2 += "}\n"
hash_value['dts.json'] = get_file_crc32('dts.json')
hash_value['json_name_keys.json'] = get_file_crc32('../json_name_keys.json')
writejson(hash_value, hash_path)

with open(os.path.join('../..', 'code', 'config.d.ts'), "w") as file:
    file.write(content)

with open(os.path.join('../..', 'code', 'config.ts'), "w") as file:
    file.write(content2)
