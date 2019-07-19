# -*- coding: utf-8 -*-

def to_tuple_list(s):
    if s == '':
        return '[]'
    if s == '0':
        return '[]'

    tuples = [t.strip() for t in s.split(';') if t.strip() != '']
    tuples = [', '.join([ss.strip() for ss in t.split(',')]) for t in tuples]
    return '[' + ', '.join(['{%s}' % (t, ) for t in tuples]) + ']'

def to_list_list(s):
    if s == '':
        return '[]'

    tuples = [t.strip() for t in s.split(';') if t.strip() != '']
    tuples = [', '.join([ss.strip() for ss in t.split(',')]) for t in tuples]
    return '[' + ', '.join(['[%s]' % (t, ) for t in tuples]) + ']'

def to_int_list(s):
    tuples = s.split(',')
    return '[' + ', '.join([t for t in tuples]) + ']'

def to_slush_list(s):
    if s == '':
        return '[]'

    tuples = [t.strip() for t in s.split(',') if t.strip() != '']
    return '[' + ', '.join([add_slash(t) for t in tuples]) + ']'

def add_slash(s):
    return '<<"%s"/utf8>>' % (s, )

def to_tuple(s):
    return '{' + ', '.join([t.strip() for t in s.split(',')]) + '}'

## 加 大括号
def add_big_brackets(s):
    return '{%s}' % (s)

## 加 []
def to_list(s):
    return '[%s]' % (s)

def to_type_raw(s):
    return s

TYPE_PROCESSOR = {
    "number" : to_type_raw,
    "string" : add_slash,
    "list" : to_list,
    "tuple" : add_big_brackets,
    "string_list" : to_slush_list,
    "tuple_list" : to_tuple_list,
    "list_list" : to_list_list,
    "erl_term" : to_type_raw,
}

money_cost_type = {'1' : 'coin', '2' : 'silver', '3' : 'gold', '4' : 'gold_bound'}

def parse_money_cost_type(s):
    l = s.split(',')
    l[0] = money_cost_type[l[0]]
    return '{' + ', '.join(l) + '}'

def item_for_return(fields_desc,item):
    for k, f in fields_desc.items():
        item[k] = f(item[k])
    return (item, fields_desc.keys())

ALL_SKILL_EFFECTS = [
    # 加减属性效果
    'add_constitution',            
    'add_magical',                 
    'add_physical',                
    'add_endurance',               
    'add_quick',                   
    'add_hp_max',                  
    'add_mp_max',                  
    'add_physical_attack',         
    'add_magic_attack',            
    'add_physical_defense',        
    'add_magic_defense',           
    'add_agile',                   
    'add_heal',                    
    'add_heal_magnify',            
    'add_heal_mitigant',           
    'add_heal_crit',               
    'add_seal_hit',                
    'add_seal_dodge',              
    'add_hit',                     
    'add_dodge',                   
    'add_physical_crit',           
    'add_physical_tenacity',       
    'add_magic_crit',              
    'add_magic_tenacity',          
    'add_crit_magnify',            
    'add_crit_mitigant',           
    'add_physical_damage_magnify', 
    'add_physical_damage_mitigant',
    'add_magic_damage_magnify',    
    'add_magic_damage_mitigant',   
    'add_physical_immune',         
    'add_magic_immune',            
    'add_mp_consume',              
    'add_reflex',                  
    'add_reflex_damage',           
    'add_anti_reflex',             
    'add_weakness',                
    'add_anti_weakness',           
    'add_constitution_percent',            
    'add_magical_percent',                 
    'add_physical_percent',                
    'add_endurance_percent',               
    'add_quick_percent',                   
    'add_hp_max_percent',                  
    'add_mp_max_percent',                  
    'add_physical_attack_percent',         
    'add_magic_attack_percent',            
    'add_physical_defense_percent',        
    'add_magic_defense_percent',           
    'add_agile_percent',                   
    'add_heal_percent',                    
    'add_heal_magnify_percent',            
    'add_heal_mitigant_percent',           
    'add_heal_crit_percent',               
    'add_seal_hit_percent',                
    'add_seal_dodge_percent',              
    'add_hit_percent',                     
    'add_dodge_percent',                   
    'add_physical_crit_percent',           
    'add_physical_tenacity_percent',       
    'add_magic_crit_percent',              
    'add_magic_tenacity_percent',          
    'add_crit_magnify_percent',            
    'add_crit_mitigant_percent',           
    'add_physical_damage_magnify_percent', 
    'add_physical_damage_mitigant_percent',
    'add_magic_damage_magnify_percent',    
    'add_magic_damage_mitigant_percent',   
    'add_physical_immune_percent',         
    'add_magic_immune_percent',            
    'add_mp_consume_percent',              
    'add_reflex_percent',                  
    'add_reflex_damage_percent',           
    'add_anti_reflex_percent',             
    'add_weakness_percent',                
    'add_anti_weakness_percent',
    'add_attack', # 双攻
    'add_attack_percent',
    'add_defense', # 双防
    'add_defense_percent',
    'add_damage_magnify', # 伤害加深
    'add_damage_magnify_percent', 
    'add_absorb',
    'add_absorb_percent',
    #####
    'add_hp', # 加血,受治疗效果影响
    'add_abs_hp', # 加血,绝对值,不受治疗效果影响
    'add_mp', # 加魔
    ### 特殊技能效果
    'magic_damage_fluctuate', 
    'damage_fluctuate', # 伤害波动
    'revive', # 复活
    'remove_all_negative_buffs', # 移除所有负面BUFF
    'remove_all_positive_buffs', # 移除所有正面BUFF
    'remove_one_positive_buff',  # 移除一个正面BUFF
    'remove_one_negative_buff',  # 移除一个负面BUFF
    'combo', # 连击
    'anti_combo', # 连击抵抗
    'physical_crit', # 暴击祝福
    'armor_penetration', # 破甲
    'magic_attack_chance', 
    'physical_attack_chance',
    'anti_magic_attack_chance',
    'anti_physical_attack_chance',
    'linked', # 同生共死
    'absorb', 
    'lunhui', # 轮回
    'lunhui_po', # 轮回破
    'resent', #
    'flash', # 闪现
    'posui_ignore_defense', # 破碎忽视防御
    'skip_punch', # 隔山打牛
    'legacy', # 遗产
    'left_mp', 
    'remove_buff', # 移除BUFF
    'append_effect',
    'replace_effect',
    'mp_instead_hp',
    ### 特殊BUFF效果
    'defense', # 防御
    'invisible', # 隐身
    'netherworld', # 断魂
    'on_dead', # 
    'dead', # 不可被复活
    'freeze', # 冰冻 不可做任何操作
    'no_die', # 免死
    'add_hp3', # 二灯效果
    'seal_skill', # 不可使用法术技能
    'faint', # 眩晕
    'visible', # 鹰眼
    'rest', # 休息
    'immune_seal', # 免疫封印BUFF
    'stealth', # 潜行
    'set_hp', # 复活后设置血量
    'confine', # 禁锢
    'deny_passive_protection', # 不可被保护
    'reborn', # 重生
    'equipskill_seal', # 封印装备特技
]

SKILL_TYPE_MAP = {
    '1' : 'active_skill',       # 主动技能
    '2' : 'trigger_skill',      # 被动触发技能
    '3' : 'attribute_skill',    # 被动属性技能
    '4' : 'assist_skill',       # 辅助技能
}

ATTACK_TYPE_MAP = { '1' : 'single', '2' : 'aoe' }

TARGET_TYPE_MAP = {
    '1' : 'alliance', # 己方
    '2' : 'enemy',    # 敌方
    '3' : 'master',   # 主人
}

TARGET_ENTITY_TYPE_MAP = {
    '1' : 'monster', # 怪物
    '2' : 'role',    # 主角
}

TARGET_AREA_MAP = {
    '0' : 'none',
    '1' : 'actor_circle',  # 以攻击者为中心的圆形
    '2' : 'target_circle', # 以受击者为中心的圆形
    '3' : 'actor_to_target_rectangle', # 从攻击者到受击者之间的矩形区域
    '4' : 'actor_to_target_triangle',  # 从攻击者到受击者之间的三角形区域
}

ACTOR_SHIFT_MAP = {
    '0' : 'none',
    '1' : 'to_target', # 移动到离目标距离为N的地方
    '2' : 'towards_target', # 朝目标移动N距离
}

TARGET_SHIFT_MAP = {
    '0' : 'none',
    '1' : 'push', # 将受击方击退N距离
    '2' : 'pull', # 将受击方朝攻击方拉M距离
    '3' : 'to_actor', # 将受击方拉到距离攻击方X距离处
}

FRIEND_TARGET_TYPE_MAP = {
    '0' : 'none',
    '1' : 'all',                # 所有
    '2' : 'single_alive',       # 未死亡单体
    '3' : 'single_dead',        # 死亡单体
    '4' : 'all_dead',           # 1 + 所有死亡单位
    '5' : 'all_alive',          # 1 + 所有未死亡单位
    '6' : 'plus_random',        # 1 + random
    '7' : 'self',               # 自己
    '8' : 'plus_self',          # 1 + self
    '9' : 'plus_self_buff',     # 1 + self buff
    '10' : 'single',            # 单体
    '11' : 'plus_random_2',     # 1 + random 2
}

SKILL_EXTRA_EFFECT_CONDITION_MAP = {
    '1' : 'none',
    '2' : 'when_hp_lower_than',
    '3' : 'when_attack_hit',
    '4' : 'when_die',
    '5' : 'when_first',
    '6' : 'target_type',
}

PASSIVE_SKILL_TARGET_MAP = {
    '0' : 'none',
    '1' : 'self',
    '2' : 'attacker',
    '3' : 'all_enemies',
    '4' : 'all_alliances',
    '5' : 'hitted',             # 被击中的对象
    '6' : 'enemy_front_row',
    '7' : 'enemy_back_row',
    '8' : 'lowest_hp',
}


def parse_trigger_condition(s):
    if s == '':
        return 'none'
    l = s.split(',')
    l[0] = trigger_condition_type[l[0]]
    return '{' + ', '.join(l) + '}'

def parse_skill_aim(s):
    if s == '':
        return 'normal'
    return skill_aim_type[s]

def parse_effect_condition(s):
    if s == '':
        return 'none'
    l = s.split(',')
    l[0] = effect_condition_type[l[0]]
    return '{' + ', '.join(l) + '}'

def parse_effects(s):
    if s == '':
        return '[]'
    if s.find('^') < 0:
        effects = [parse_single_effect(e) for e in s.split(';') if e.strip() != '']
        return '[' + ', '.join(effects) + ']'
    else:
        effects = [parse_single_effect(e) for e in s.split('^') if e.strip() != '']
        return '[' + ', '.join(effects) + ']'

def parse_effect_param(s):
    if s.find('*') < 0:
        return s
    else:
        return '{' + ', '.join(s.split('*')) + '}'

def parse_single_effect(s):
    l = [i.strip() for i in s.split(',') if s.strip() != '']
    #if l[0] not in ALL_SKILL_EFFECTS:
    #    raise RuntimeError('unkwown skill effect: %s' % (l[0]))
    if l[0] == 'append_effect' or l[0] == 'replace_effect':
        columnName = l[1]
        columnValue= ','.join(l[2:])
        return '{' + l[0] + ', ' + l[1] + ', ' + core_skill_column_processor(columnName, columnValue) + '}'
    else:
        return '{' + ', '.join(map(parse_effect_param, l)) + '}'


def parse_with_map(s, m):
    l = [t.strip() for t in s.split(',') if t.strip() != '']
    if len(l) == 1:
        return m[l[0]]
    else:
        l[0] = m[l[0]]
        return '{' + ', '.join(l) + '}'

def parse_damage_aim(s):
    return parse_with_map(s, ATTACK_TARGET_TYPE_MAP)

def parse_friend_aim(s):
    return parse_with_map(s, FRIEND_TARGET_TYPE_MAP)

def parse_extra_effect_condition(s):
    return parse_with_map(s, SKILL_EXTRA_EFFECT_CONDITION_MAP)

def parse_passive_skill_aim(s):
    return parse_with_map(s, PASSIVE_SKILL_TARGET_MAP)



def core_skill_column_processor(columnName, columnValue):
    if columnName == 'type':
        return SKILL_TYPE_MAP[columnValue]
    elif columnName == 'attack_type':
        return ATTACK_TYPE_MAP[columnValue]
    elif columnName == 'additional_attribute':
        return parse_effects(columnValue)
    elif columnName == 'damage_max':
        return to_tuple(columnValue)
    elif columnName == 'damage_aim':
        return to_tuple(columnValue)
    elif columnName == 'aim_grow':
        return to_int_list(columnValue)
    elif columnName == 'buff_grow':
        return to_int_list(columnValue)
    elif columnName == 'extra_effect_condition':
        return parse_extra_effect_condition(columnValue)
    elif columnName == 'extra_effect':
        return parse_effects(columnValue)
    elif columnName == 'extra_buff':
        return to_tuple_list(columnValue)
    elif columnName == 'first_extra_effect':
        return parse_effects(columnValue)
    elif columnName == 'first_extra_buff':
        return to_tuple_list(columnValue)
    elif columnName == 'friend_aim':
        return to_tuple(columnValue)
    elif columnName == 'mp':
        return to_tuple(columnValue)
    elif columnName == 'hp':
        return to_tuple(columnValue)
    elif columnName == 'visible':
        return (columnValue or '0')
    elif columnName == 'round_max':
        return (columnValue or '99')
    elif columnName == 'battle_max':
        return (columnValue or '99')
    elif columnName == 'friend_effect':
        return parse_effects(columnValue)
    elif columnName == 'first_friend_buff':
        return to_tuple_list(columnValue)
    elif columnName == 'friend_buff':
        return to_tuple_list(columnValue)
    elif columnName == 'damage_percent':
        return to_int_list(columnValue)
    elif columnName == 'pre_round_agile':
        return (columnValue or '0')
    elif columnName == 'beckon':
        return to_tuple(columnValue)
    elif columnName == 'passive_effect':
        return parse_effects(columnValue)
    elif columnName == 'trigger_rate':
        return (columnValue or '0')
    elif columnName == 'trigger_timing':
        return (columnValue or 'none')
    elif columnName == 'trigger_condition':
        return to_tuple_list(columnValue)
    elif columnName == 'trigger_skill_aim':
        return to_tuple(columnValue)
    elif columnName == 'trigger_effect':
        return parse_effects(columnValue)
    elif columnName == 'trigger_buff':
        return to_tuple_list(columnValue)
    elif columnName == 'attack_percent':
        return to_int_list(columnValue)
    elif columnName == 'damage_value':
        return to_tuple_list(columnValue)
    elif columnName == 'hp_limit':
        return to_tuple(columnValue)
    elif columnName == 'armor_penetration':
        return to_tuple_list(columnValue)
    elif columnName == 'first_armor_penetration':
        return to_tuple(columnValue)
    elif columnName == 'extra_friend_aim':
        return to_tuple(columnValue)
    elif columnName == 'extra_friend_effect':
        return parse_effects(columnValue)
    elif columnName == 'extra_friend_buff':
        return to_tuple_list(columnValue)


##    #item['extra_friend_aim'] = to_tuple(item['extra_friend_aim'])
##    #item['extra_friend_effect'] = parse_effects(item['extra_friend_effect'])
##    #item['extra_friend_buff'] = to_tuple_list(item['extra_friend_buff'])


def core_skill_processor(item):
    item['type'] = core_skill_column_processor('type', item['type'])
    item['attack_type'] = core_skill_column_processor('attack_type', item['attack_type'])
    item['additional_attribute'] = core_skill_column_processor('additional_attribute', item['additional_attribute'])
    item['damage_max'] = core_skill_column_processor('damage_max', item['damage_max'])
    item['damage_aim'] = core_skill_column_processor('damage_aim', item['damage_aim'])
    item['aim_grow'] = core_skill_column_processor('aim_grow', item['aim_grow'])
    item['buff_grow'] = core_skill_column_processor('buff_grow', item['buff_grow'])
    item['extra_effect_condition'] = core_skill_column_processor('extra_effect_condition', item['extra_effect_condition'])
    item['extra_effect'] = core_skill_column_processor('extra_effect', item['extra_effect'])
    item['extra_buff'] = core_skill_column_processor('extra_buff', item['extra_buff'])
    item['first_extra_effect'] = core_skill_column_processor('first_extra_effect', item['first_extra_effect'])
    item['first_extra_buff'] = core_skill_column_processor('first_extra_buff', item['first_extra_buff'])
    item['friend_aim'] = core_skill_column_processor('friend_aim', item['friend_aim'])
    item['mp'] = core_skill_column_processor('mp', item['mp'])
    item['hp'] = core_skill_column_processor('hp', item['hp'])
    item['visible'] = core_skill_column_processor('visible', item['visible']) 
    item['round_max'] = core_skill_column_processor('round_max', item['round_max'])
    item['battle_max'] = core_skill_column_processor('battle_max', item['battle_max'])
    item['friend_effect'] = core_skill_column_processor('friend_effect', item['friend_effect'])
    item['first_friend_buff'] = core_skill_column_processor('first_friend_buff', item['first_friend_buff'])
    item['friend_buff'] = core_skill_column_processor('friend_buff', item['friend_buff'])
    item['damage_percent'] = core_skill_column_processor('damage_percent', item['damage_percent'])
    item['pre_round_agile'] = core_skill_column_processor('pre_round_agile', item['pre_round_agile']) 
    item['beckon'] = core_skill_column_processor('beckon', item['beckon'])
    item['passive_effect'] = core_skill_column_processor('passive_effect', item['passive_effect'])
    item['trigger_rate'] = core_skill_column_processor('trigger_rate', item['trigger_rate']) 
    item['trigger_timing'] = core_skill_column_processor('trigger_timing', item['trigger_timing'])
    item['trigger_condition'] = core_skill_column_processor('trigger_condition', item['trigger_condition'])
    item['trigger_skill_aim'] = core_skill_column_processor('trigger_skill_aim', item['trigger_skill_aim'])
    item['trigger_effect'] = core_skill_column_processor('trigger_effect', item['trigger_effect'])
    item['trigger_buff'] = core_skill_column_processor('trigger_buff', item['trigger_buff'])
    item['attack_percent'] = core_skill_column_processor('attack_percent', item['attack_percent'])
    item['damage_value'] = core_skill_column_processor('damage_value', item['damage_value'])
    item['hp_limit'] = core_skill_column_processor('hp_limit', item['hp_limit'])
    item['armor_penetration'] = core_skill_column_processor('armor_penetration', item['armor_penetration'])
    item['first_armor_penetration'] = core_skill_column_processor('first_armor_penetration', item['first_armor_penetration'])
    item['extra_friend_aim'] = core_skill_column_processor('extra_friend_aim', item['extra_friend_aim'])
    item['extra_friend_effect'] = core_skill_column_processor('extra_friend_effect', item['extra_friend_effect'])
    item['extra_friend_buff'] = core_skill_column_processor('extra_friend_buff', item['extra_friend_buff'])
    return item

##def core_skill_processor(item):
##    item['type'] = SKILL_TYPE_MAP[item['type']]
##    item['attack_type'] = ATTACK_TYPE_MAP[item['attack_type']]
##    item['additional_attribute'] = parse_effects(item['additional_attribute'])
##    item['damage_max'] = to_tuple(item['damage_max'])
##    item['damage_aim'] = to_tuple(item['damage_aim'])
##    item['aim_grow'] = to_int_list(item['aim_grow'])
##    item['buff_grow'] = to_int_list(item['buff_grow'])
##    item['extra_effect_condition'] = parse_extra_effect_condition(item['extra_effect_condition'])
##    item['extra_effect'] = parse_effects(item['extra_effect'])
##    item['extra_buff'] = to_tuple_list(item['extra_buff'])
##    item['first_extra_effect'] = parse_effects(item['first_extra_effect'])
##    item['first_extra_buff'] = to_tuple_list(item['first_extra_buff'])
##    item['friend_aim'] = to_tuple(item['friend_aim'])
##    item['mp'] = to_tuple(item['mp'])
##    item['hp'] = to_tuple(item['hp'])
##    #item['coin_cost'] = item['coin_cost'] or '0'
##    item['visible'] = item['visible'] or '0'
##    item['round_max'] = item['round_max'] or '99'
##    item['battle_max'] = item['battle_max'] or '99'
##    #item['exclude_undead'] = item['exclude_undead'] or '0'
##    #item['use_soul'] = item['use_soul'] or '0'
##    #item['soul_damage_percent'] = item['soul_damage_percent'] or '0'
##    #item['soul_armor_penetration'] = item['soul_armor_penetration'] or '0'
##    #item['soul_damage_value'] = to_tuple_list(item['soul_damage_value'] or '0,0')
##    item['friend_effect'] = parse_effects(item['friend_effect'])
##    #item['extra_friend_aim'] = to_tuple(item['extra_friend_aim'])
##    #item['extra_friend_effect'] = parse_effects(item['extra_friend_effect'])
##    #item['extra_friend_buff'] = to_tuple_list(item['extra_friend_buff'])
##    item['first_friend_buff'] = to_tuple_list(item['first_friend_buff'])
##    item['friend_buff'] = to_tuple_list(item['friend_buff'])
##    item['damage_percent'] = to_int_list(item['damage_percent'])
##    item['pre_round_agile'] = item['pre_round_agile'] or '0'
##    item['beckon'] = to_tuple(item['beckon'])
##    item['passive_effect'] = parse_effects(item['passive_effect'])
##    item['trigger_rate'] = item['trigger_rate'] or '0'
##    item['trigger_timing'] = (item['trigger_timing'] or 'none')
##    item['trigger_condition'] = to_tuple_list(item['trigger_condition'])
##    item['trigger_skill_aim'] = to_tuple(item['trigger_skill_aim'])
##    item['trigger_effect'] = parse_effects(item['trigger_effect'])
##    item['trigger_buff'] = to_tuple_list(item['trigger_buff'])
##    item['attack_percent'] = to_int_list(item['attack_percent'])
##    item['damage_value'] = to_tuple_list(item['damage_value'])
##    item['hp_limit'] = to_tuple(item['hp_limit'])
##    item['armor_penetration'] = to_tuple_list(item['armor_penetration'])
##    item['first_armor_penetration'] = to_tuple(item['first_armor_penetration'])
##    #item['buff_extra_round'] = item['buff_extra_round'] or '0'
##    #item['fix_by'] = to_int_list(item['fix_by'])
##    return item

def skill_core_processor(item):
    item['type'] = SKILL_TYPE_MAP[item['type']]
    item['target_type'] = TARGET_TYPE_MAP[item['target_type']]
    item['attack_type'] = ATTACK_TYPE_MAP[item['attack_type']]
    item['damage_percent'] = to_int_list(item['damage_percent'])
    item['target_area_type'] = parse_with_map(item['target_area_type'], TARGET_AREA_MAP)
    item['actor_shift'] = parse_with_map(item['actor_shift'], ACTOR_SHIFT_MAP)
    item['target_shift'] = parse_with_map(item['target_shift'], TARGET_SHIFT_MAP)
    item['actor_buff'] = to_tuple_list(item['actor_buff'])
    item['target_buff'] = to_tuple_list(item['target_buff'])
    item['extra_effects'] = to_int_list(item['extra_effects'])
    item['passive_effects'] = parse_effects(item['passive_effects'])
    item['trigger_effects'] = to_int_list(item['trigger_effects'])
    item['cd'] = item['cd'] or '0'
    return item

def skill_trigger_processor(item):
    item['condition']  = to_tuple_list(item['condition'])
    item['aim'] = to_tuple(item['aim'])
    item['effects'] = parse_effects(item['effects'])
    return item

def skill_buff_processor(item):
    item['status'] = to_tuple(item['status'])
    item['attribute'] = parse_effects(item['attribute'])
    if item['effect'] :
        item['effect'] = to_int_list(item['effect'])
    else:
        item['effect'] = '[]'
    item['duration'] = item['duration'] or '0'
    item['cd'] =  item['cd'] or '0'
    item['max_times'] = item['max_times'] or '0'
    item['can_clean'] = item['can_clean'] or '1'
    item['clean_on_dead'] = item['clean_on_dead'] or '1'
    if item['value'] :
        item['value'] = parse_effect_param(item['value'])
    else:
        item['value'] = 'none'
    return item

def class_skill_processor(item):
    item['skill_id'] = to_int_list(item['skill_id'])
    return item

def buff_processor(item):
    item['duration'] = to_tuple_list(item['duration'])
    item['effect'] = parse_effects(item['effect'])
    item['time_max'] = item['time_max'] or '0'
    item['damage_max'] = to_tuple(item['damage_max'])
    item['pri'] = item['pri'] or '0'
    item['group'] = item['group'] or '0'
    item['is_poison'] = item['is_poison'] or '0'
    item['type'] = to_tuple_list(item['type'])
    return item


def spawnpoint_processor(item):
    item['locations'] = to_tuple_list(item['locations'])
    item['exp'] = item['exp'] or '0, 0'
    item['exp'] = add_big_brackets(item['exp'])
    item['coin_reward'] = item['coin_reward'] or '0, 0'
    item['coin_reward'] = add_big_brackets(item['coin_reward'])
    item['silver_reward'] = item['silver_reward'] or '0, 0'
    item['silver_reward'] = add_big_brackets(item['silver_reward'])
    item['drop_number'] = to_tuple_list(item['drop_number'])
    item['drop_items'] = to_tuple_list(item['drop_items'])
    item['drop_item_must'] = to_tuple_list(item['drop_item_must'])
    item['draw'] = to_tuple_list(item['draw'])
    item['vip_draw'] = to_tuple_list(item['vip_draw'])
    item['reward'] = to_tuple_list(item['reward'])
    item['type'] = add_big_brackets(item['type'])
    item['draw_or_not'] = item['draw_or_not'] or '0'
    item['name'] = add_slash(item['name'])
    item['monster1'] = to_tuple_list(item['monster1'])
    item['monster2'] = to_tuple_list(item['monster2'])
    item['monster3'] = to_tuple_list(item['monster3'])
    item['monster4'] = to_tuple_list(item['monster4'])
    item['monster5'] = to_tuple_list(item['monster5'])
    item['monster6'] = to_tuple_list(item['monster6'])
    item['monster7'] = to_tuple_list(item['monster7'])
    item['monster8'] = to_tuple_list(item['monster8'])
    item['monster9'] = to_tuple_list(item['monster9'])
    item['monster10'] = to_tuple_list(item['monster10'])
    item['monster11'] = to_tuple_list(item['monster11'])
    item['monster12'] = to_tuple_list(item['monster12'])
    item['monster13'] = to_tuple_list(item['monster13'])
    item['monster14'] = to_tuple_list(item['monster14'])
    item['max_limit'] = to_tuple_list(item['max_limit'])
    return item

monster_type = {'1' : 'normal_monster', 
                '2' : 'small_boss',
                '3' : 'big_boss'}

PATROL_TYPE = {'0':'none', '1':'circle', '2':'line', '3':'path_point'}

def monster_processor(item):
    item['name'] = add_slash(item['name'])
    item['skill'] = to_int_list(item['skill'])
    item['ai'] = to_int_list(item['ai'])
    item['reward'] = to_tuple_list(item['reward'])
    return item

def monster_type_processor(item):
    item['type'] = monster_type[item['type']]
    item['patrol_type'] = parse_with_map(item['patrol_type'], PATROL_TYPE)
    return item

def monster_ai_processor(item):
    item['conditions'] = to_tuple_list(item['conditions'])
    item['action'] = to_tuple_list(item['action'])
    return item

def professional_processor(item):
    item['skill'] = to_int_list(item['skill'])
    item['skillai'] = to_int_list(item['skillai'])
    return item


def class_processor(item):
    item['include_skill_group'] = to_int_list(item['include_skill_group'])
    item['int_level'] = to_int_list(item['int_level'])
    item['name'] = add_slash(item['name'])
    item['bless_id'] = to_int_list(item['bless_id'])
    item['bless_num'] = to_tuple_list(item['bless_num'])
    item['bless_skill_id'] = to_int_list(item['bless_skill_id'])
    item['bless_skill_num'] = to_tuple_list(item['bless_skill_num'])
    item['pet_bless_id'] = to_int_list(item['pet_bless_id'])
    item['pet_bless_num'] = to_tuple_list(item['pet_bless_num'])
    item['pet_bless_skill_id'] = to_int_list(item['pet_bless_skill_id'])
    item['pet_bless_skill_num'] = to_tuple_list(item['pet_bless_skill_num'])
    return item

def class_model_processor(item):
    item['class_choose'] = to_int_list(item['class_choose'])
    return item

def mate_processor(item):
    fields_desc = {
        'hire_cost' : parse_money_cost_type
    }
    return item_for_return(fields_desc, item)

def mate_attribute_processor(item):
    item['skill'] = to_int_list(item['skill'])
    return item

AI_CONDITION_MAP = {
    'none' : 'none',
    '1' : 'alliance_dead',
    '2' : 'alliance_hp_lower_than',
    '3' : 'all_alliance_hp_higher_than',
    '4' : 'alliances_more_than',
    '5' : 'alliance_has_class',
    '6' : 'all_alliances_die',
    '7' : 'alliance_does_not_have_buff',
    '8' : 'any_alliance_has_buff',
    '9' : 'any_alliance_hp_lower_than',
    '10' : 'round',
    '11' : 'enemy_not_seal',
    '12' : 'enemy_more_than',
    '13' : 'enemy_has_class',
    '14' : 'any_enemy_hp_lower_than',
    '15' : 'any_alliance_mp_lower_than',
    '16' : 'enemy_has_pet',
    '17' : 'master_has_target',
    '18' : 'enemy_has_invisible_pet',       #敌方存在隐身宠
    '19' : 'is_visible',                    #天眼
    '20' : 'enemy_has_invisible_physical_pet',                    #隐身物宠
    '21' : 'enemy_has_invisible_assist_pet',                    #隐身辅助宠
    '22' : 'enemy_has_physical_pet',                    #物宠
    '23' : 'enemy_has_magical_pet',                     #法宠
    '24' : 'enemy_has_assist_pet',                      #法宠
    '25' : 'is_assist_pet',                             #辅助宠
    '26' : 'enemy_has_invisible',                       #敌方存在隐身或潜行单位
    '27' : 'soul_higher_than',                          #自己的灵魂大于等于n
    '28' : 'hp_lower_than',                             #自己血量低于
    '29' : 'summon_objs_less_than',                     #召唤的单位数量小于
    '30' : 'alliances_less_than',                       #友方少于n
    '31' : 'alliance_monster_dead',                     #友方怪物死亡
    '32' : 'enemy_has_npc',                             #敌方有非主角单位
    '33' : 'master_hp_lower_than',                      #友方非宠血量
    '34' : 'any_enemy_anger_higher_than',               #存在怒气大于n的敌方单位
    '35' : 'has_skill',                                 #拥有技能
    '36' : 'enemy_has_sex',                             #敌方拥有性别为n的主角
    '37' : 'enemy_has_player',                          #敌方存在主角
    '38' : 'has_buff',                                  #自己拥有buff
    '39' : 'master_has_recent_target',                  #主人选择过目标
    '40' : 'enemy_has_physical_defense_lower',          #场上存在物理防御低于自己m倍攻击的角色
    '41' : 'enemy_has_magical_defense_lower',           #敌方存在法术防御低于自己n倍攻击的角色
    '42' : 'enemy_has_pet_type',                        #敌方存在特定类型的宠物
    '43' : 'enemy_has_buff',                            #敌方存在特定类型的buff
    '44' : 'any_enemy_player_hp_lower_than',            #敌方存在血量低于x的主角
    '45' : 'round_ge',                                  # 回合数大于N
    '46' : 'round_module',                              # 46,A,B 回合数满足 N mod A == B
    '47' : 'any_alliance_has_buffs',                    # 47,[Id1,Id2,...] 友方角色拥有所有buff
    '48' : 'enemy_less_than',                           # 敌方<=n
    '49' : 'alliance_player_dead',                      # 友方主角死亡
    '50' : 'enemy_player_mp_lt_ge',                     # 50,x,m 敌方有>=x个主角蓝量低于m
    '51' : 'enemy_no_buff_ge',                          # 51,x,buff_id 敌方有>=x个单位没有buff
    '52' : 'alliance_seal_ge',                          # 52,N 友方有>=x个单位被封印
    '53' : 'self_seal',                                 # 53 自己被封印
    '54' : 'alliances_pet_le',                          # 54,x 己方宠物数量<=x
    '55' : 'self_no_buff_id',                           # 55,buff_id 自己没这个buff
    '56' : 'self_hp_rate_ge',                           # 56,x 自己血量>=x
    '57' : 'enemy_sealed_le',                           # 57,x 敌方有<=x个单位被封印（不包括兽王召唤的兔子）
    '58' : 'enemy_not_seal_le',                         # 58,x 敌方有<=x个单位没被封印（不包括兽王召唤的兔子）
    '59' : 'alliance_reviveable_ge',                    # 59,x 己方可被复活单位>=x
    '60' : 'alliance_except_pet_seal_ge',               # 60,x 己方被封印的非宠单位>=x（不包括兽王召唤的兔子）
    '61' : 'left_summon_pet_count_ge',                  # 61,x 自己剩余可召唤宠物数量>=x
    '62' : 'left_summon_pet_times_ge',                  # 62,x 自己剩余可召唤宠物次数>=x
    '63' : 'enemy_player_and_mate_ge',                  # 63,x 敌方存活的伙伴和主角>=x
}

def skill_ai_processor(item):
    def parse_ai_conditions(conditions):
        conditions = conditions.split(';')
        conditions = [parse_with_map(c, AI_CONDITION_MAP) for c in conditions]
        return '[' + ','.join(conditions) + ']'

    item['conditions'] = parse_ai_conditions(item['conditions'])
    item['aim'] = add_big_brackets(item['aim'])
    item['actions'] = to_tuple_list(item['actions'])
    return item

def skill_learn_processor(item):
    item['passive_effect'] = parse_effects(item['passive_effect'])
    item['skill_point'] = add_big_brackets(item['skill_point'])
    item['skill'] = to_int_list(item['skill'])
    return item

NPC_CONSUME_MAP = {
    '1' : 'coin',
    '2' : 'silver',
    '3' : 'gold',
    '4' : 'bound_gold',
    '5' : 'gang_contribute',
    '6' : 'charm',
    '7' : 'arena_point', 
    '8' : 'charged',
}

def npc_processor(item):
    item['name'] = add_slash(item['name'])
    item['target_position'] = to_tuple(item['target_position'])
    item['recruit'] = item['recruit'] or '0'
    item['favor_min'] = item['favor_min'] or '0'
    if item['consume_min'] :
        consumes = item['consume_min'].split(';')
        s = [parse_with_map(c, NPC_CONSUME_MAP) for c in consumes]
        item['consume_min'] = '[' + ','.join(s) + ']'
    else:
        item['consume_min'] = '[]'
    item['gift'] = to_tuple_list(item['gift'])
    item['rank_reward'] = to_tuple_list(item['rank_reward'])
    return item

CARRIAGE_COST_MAP = {
    '1' : 'coin',
    '2' : 'silver',
    '3' : 'gold',
    '4' : 'bound_gold',
}

def carriage_processor(item):
    item['name'] = add_slash(item['name'])
    if item['cost'] :
        consumes = item['cost'].split(';')
        s = [parse_with_map(c, CARRIAGE_COST_MAP) for c in consumes]
        item['cost'] = '[' + ','.join(s) + ']'
    else:
        item['cost'] = '[]'
    return item


TITLE_OBTAIN_MAP = {
    '0' : 'initial',
    '1' : 'first_add_money',
    '2' : 'level_up'
}

def title_processor(item):
    item['title_name'] = add_slash(item['title_name'])
    item['task'] = to_tuple(item['task'])
    item['effect_player']= to_tuple_list(item['effect_player'])
    item['effect_mate']= item['effect_mate'] or 0
    item['type'] = item['type'] or '1'
    item['deadline']= to_tuple(item['deadline']) or '{0, 0, 0}, {0, 0, 0}'
    item['effective_time']= item['effective_time'] or -1
    return item

def gang_authority_processor(item):
    item['id'] = item['id']
    item['position_type'] = item['position_type']
    item['position_number']= item['position_number']
    item['position_change']= to_int_list(item['position_change'])
    item['position_dismissal']= to_int_list(item['position_dismissal'])
    item['allow_in_limit']= item['allow_in_limit']
    item['can_levelup'] = item['can_levelup']
    item['allow_in']= item['allow_in']
    item['message']= item['message']
    item['beast']= item['beast']
    item['warehouse']= item['warehouse']
    return item

def gang_level_up_processor(item):
    item['level'] = item['level']
    item['human_number'] = item['human_number']
    item['funding']= item['funding']
    item['skill_limit']= item['skill_limit']
    return item


def battle_point_processor(item):
    item['attr'] = item['attr']
    item['e1'] = to_list(item['e1'])
    return item
