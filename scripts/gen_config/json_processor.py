import json
import re

def isInt(v):
    try:
        int(v)
        return True
    except ValueError:
        return False

def isFloat(v):
    try:
        float(v)
        return True
    except ValueError:
        return False

def isArr(v):
    pattern = re.compile(r'(\{.*\})|(\[.*\])')
    match = pattern.match(v)
    if match:
        return True
    return False

def common_to_value(s):
    if isInt(s):
        return int(s)
    elif isFloat(s):
        return float(s)
    elif isArr(s):
        s = s.replace('{', '[')
        s = s.replace('}', ']')
        try:
            return json.loads(s)
        except ValueError:
            return s
    else:
	    return s
		
def try_arr_to_str(s):
    s = s.replace('{','')
    s = s.replace('}','')
    return s

def item_for_return(fields_desc,item):
    for k, f in fields_desc.items():
        item[k] = f(item[k])
    return (item, fields_desc.keys())

def None_if_empty_else_number_or_quote(s):
    if s == '':
        return None
    else:
        return try_to_number_else_str(s)


def try_to_number_else_str(s):
    if isInt(s):
        return int(s)
    elif isFloat(s):
        return float(s)
    elif s == '':
        return 0
    else:
        return s

def str_to_int(s):
    if isInt(s):
        return int(s)
    return 0

def str_to_json_arr(s):
    try:
        return json.loads('[' + s + ']')
    except ValueError:
        return s

def default_processor(item):
    for k in item.keys():
        item[k] = None_if_empty_else_number_or_quote(item[k])
    return item
	
def default_to_arr_processor(s):
    if s == '':
        s = '[]'
    else:
        s = s.replace('{', '[')
        s = s.replace('}', ']')
    return json.loads(s)

def try_to_element(s):
    if isFloat(s):
        return s
    else:
        return '"%s"' % s

def to_json_list(s):
    return json.loads(to_json_list_str(s))

def to_json_list_list(s):
    if s == '':
        return []

    tuples = [t.strip() for t in s.split(';')]
    tuples = [to_json_list_str(x) for x in tuples if x != '']
    return json.loads('[' + ','.join(tuples) + ']')

def to_json_list_str(s):
    if s == '':
        return '[]'

    tuples = [t.strip() for t in s.split(',')]
    tuples = ",".join([try_to_element(x) for x in tuples if x != ''])
    return '[' + tuples + ']'

def to_type_raw(s):
    s = s.replace('\\n', '\n')
    return s

def to_type_erl_term(s):
    if s == '':
        s = '[]'
    else:
        s = s.replace('{', '[')
        s = s.replace('}', ']')
        s = re.sub(r'([a-zA-Z]+)', r'"\1"', s)
    return json.loads(s)

TYPE_PROCESSOR = {
    "number" : try_to_number_else_str,
    "string" : to_type_raw,
    "list" : to_json_list,
    "tuple" : to_json_list,
    "string_list" : to_json_list,
    "tuple_list" : to_json_list_list,
    "list_list" : to_json_list_list,
    "erl_term" : to_type_erl_term,
}

def item_processor(item):
    fields_desc = {
        'effect' : to_json_list_list,
        'price' : str_to_json_arr
    }
    return item_for_return(fields_desc,item)

def jumppoint_processor(item):
    fields_desc = {
        'posX' : str_to_int,
        'posY' : str_to_int,
        'targetX' : str_to_int,
        'targetY' : str_to_int,
    }
    return item_for_return(fields_desc,item)

def npc_processor(item):
    fields_desc = {
        'position' : str_to_json_arr,
        'target_position' : str_to_json_arr,
        "btns" : str_to_json_arr,
        "consume_min" : str_to_json_arr,
        "gift" : to_json_list_list,
        "rank_reward" : to_json_list_list,
        "recruit" : str_to_int
    }
    return item_for_return(fields_desc,item)

def scene_processor(item):
    fields_desc = {
        'spawn_points' : str_to_json_arr,
        'gather_point' : str_to_json_arr,
        'jump_points' : str_to_json_arr,
        'monster_type':str_to_json_arr,
        "level_limit":str_to_json_arr,
        "map_lv":str_to_json_arr,
        "small_side":str_to_json_arr,
    }
    return item_for_return(fields_desc,item)

def equip_processor(item):
    fields_desc = {
        "gem_type":str_to_json_arr,
        'attribute_basic_view':to_json_list_list,
        "forge_cost":to_json_list_list,
        "lv_up_cost":to_json_list_list,
        "forge_special_cost":str_to_json_arr,
        "gem_type":str_to_json_arr,
        #"last_cost_coin":str_to_json_arr,
        #"last_cost_item":str_to_json_arr,
    }
    return item_for_return(fields_desc,item)

def mission_processor(item):
    fields_desc = {
        "person_lv":str_to_json_arr,
        "prev_id":str_to_json_arr,
        "dialogue1":str_to_json_arr,
        "dialogue2":str_to_json_arr,
        "dialogue3":str_to_json_arr,
        "dialogue4":str_to_json_arr,
        'award_display':str_to_json_arr,
        'location':str_to_json_arr,
        'submit':str_to_json_arr,
        'target':to_json_list_list,
        "condition":to_json_list_list,
    }
    return item_for_return(fields_desc,item)

def skill_processor(item):
    def ss_processor(s):
        s = s.strip(" {}")
        arr = s.split(',')
        result = dict()
        for e in arr:
            e = [try_to_number_else_str(e2) for e2 in e.strip().split(':')]
            if len(e) >= 2:
                result[e[0]] = e[1].strip('"')
        if not len(result.keys()):
            return None
        return result
    return item_for_return(fields_desc,item)

def functioncondition_processor(item):
    fields_desc = {
        'variable' : common_to_value,
	}
    return item_for_return(fields_desc,item)
    
def missionsetting_processor(item):
    fields_desc = {
        'variable' : common_to_value,
    }
    return item_for_return(fields_desc,item)

def exp_processor(item):
    fields_desc = {
        'exp' : try_arr_to_str,
    }
    return item_for_return(fields_desc,item)
	
def jump_to_processor(item):
    fields_desc = {
        'need_value' : str_to_json_arr,
    }
    return item_for_return(fields_desc,item)
	
def pet_processor(item):
    fields_desc = {
        'get_method' : str_to_json_arr,
    }
    return item_for_return(fields_desc,item)

def core_skill_processor(item):
    def aimp(s):
        return s.split(',')
    return item_for_return(fields_desc,item)
	
def skill_learn_processor(item):
    fields_desc = {
        'study_level' : default_to_arr_processor,
        'skill' : str_to_json_arr,
        'passive_effect' : str_to_json_arr,
        'skill_point' : str_to_json_arr,
    }
    return item_for_return(fields_desc,item)

def mate_attribute_processor(item):
    fields_desc = {
        'skill' : str_to_json_arr,
    }
    return item_for_return(fields_desc,item)

def buff_processor(item):
    def _doRounds(s):
        arr = s.split(',')
        for i in range(1, len(arr)):
            arr[i] = int(arr[i])
        return arr
    def _doEffect(s):
        arr = s.split(';')
        for i, ss in enumerate(arr):
            arr[i] = [try_to_number_else_str(e) for e in ss.split(',')]
        return arr
    fields_desc = {
        'hanging_point' : str_to_json_arr,
        'duration' : _doRounds,
        'effect' : _doEffect
    }
    return item_for_return(fields_desc,item)

def class_model_processor(item):
    fields_desc = {
        'class_choose' : str_to_json_arr
    }
    return item_for_return(fields_desc,item)

def equipGems_processor(item):
    fields_desc = {
        'gem_effect' : str_to_json_arr,
        'merge_need' : str_to_json_arr
    }
    return item_for_return(fields_desc,item)

def announcement_processor(item):
    fields_desc = {
        'position' : str_to_json_arr
    }
    return item_for_return(fields_desc,item)

def array_processor(item):
    fields_desc = {
        'attr1' : to_json_list_list,
        'attr2' : to_json_list_list,
        'attr3' : to_json_list_list,
        'attr4' : to_json_list_list,
        'attr5' : to_json_list_list,
        'big_on' : str_to_json_arr,
        'small_on' : str_to_json_arr
    }
    return item_for_return(fields_desc,item)

def title_processor(item):
    fields_desc = {
        'effect_player' : to_json_list_list,
    }
    return item_for_return(fields_desc,item)
