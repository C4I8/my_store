# -*- coding: utf-8 -*

def get_min_and_max(k, condition):
    if k in condition:
        return condition[k]
    return condition['all']

def check_count(s, condition):
    if s == '':
		return 'ok'
    for i in s.split(';'):
        c = i.split(',')
        minl, maxl = get_min_and_max(c[0], condition)
        if int(c[1]) < minl or int(c[1]) > maxl:
            raise RuntimeError('check count error %s' % (i))

def chapter_check_processor(item):
    condition = {}
    condition['all'] = (0, 100)
    check_count(item['reward'], condition)
    check_count(item['three_star_reward'], condition)
    return 'ok'

def quest_check_processor(item):
    condition = {}
    condition['add_exp'] = (0, 20000000)
    condition['add_abs_exp'] = (0, 20000000)
    condition['add_coin'] = (0, 20000000)
    condition['add_abs_coin'] = (0, 200000000)
    condition['add_mate_exp'] = (0, 10000000)
    condition['add_abs_mate_exp'] = (0, 10000000)
    condition['add_gold_bound'] = (0, 200)
    condition['add_mate'] = (0, 10000000000000000)
    condition['add_pet_exp'] = (0, 20000000)
    condition['all'] = (0, 100)
#    check_count(item['reward'], condition)
    return 'ok'
