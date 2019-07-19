#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import re
import sys
import os

###############################################
# 颜色模块
###############################################
# 导出规则
cell_for_none   = 0
cell_for_server = 1
cell_for_client = 2
cell_ending     = 4
cell_for_type   = 8
cell_invalid    = -1

color_table = {}
color_table[(153, 204, 0)] = cell_for_server | cell_for_client
color_table[(255, 255, 0)] = cell_for_server
color_table[(255, 0, 0)] = cell_for_client
color_table[(150, 150, 150)] = cell_for_none
color_table[(0, 0, 0)] = cell_ending
color_table[(153, 153, 255)] = cell_for_type

def DEBUG(s):
    debug = False
    if debug:
        print(s)

def get_rule(color):
    if not color_table.has_key(color):
        return cell_invalid

    return color_table[color]

# 得到一个单元格的颜色
def get_cell_bgcolor(book, sheet, row, col):
    format_idx = sheet.cell_xf_index(row, col)
    formatting = book.xf_list[format_idx]
    return book.colour_map[formatting.background.pattern_colour_index]

def is_comment(sheet, row):
    val = str(sheet.cell_value(row, 0))
    DEBUG('[%d, 0] = %s' % (row, val))
    return val == u"" or val.startswith('//')

def extract_table_name(excel, sheet, row):
    for r in range(row, sheet.nrows):
        if is_comment(sheet, r):
            continue
        color = get_cell_bgcolor(excel, sheet, r, 0)
        if get_rule(color) <> cell_invalid:
            return (r, '')
        return (r + 1, sheet.cell_value(r, 0))

    raise RuntimeError('table name not found in file.')

def extract_column_info(excel, sheet, row):
    for r in range(row, sheet.nrows):
        if is_comment(sheet, r):
            continue
        color = get_cell_bgcolor(excel, sheet, r, 0)
        if get_rule(color) == cell_invalid:
            continue
        server_columns = {}
        client_columns = {}
        start_range = 0

        for i in range(start_range, sheet.ncols):
            val = sheet.cell_value(r, i)
            color = get_cell_bgcolor(excel, sheet, r, i)
            rule = get_rule(color)
            if rule == cell_invalid:
                continue
            if (rule & cell_for_server) <> 0:
                server_columns[i] = val
            if (rule & cell_for_client) <> 0:
                client_columns[i] = val
        return (r + 1, server_columns, client_columns)

    raise RuntimeError('column header not found in file')

def extract_column_type(excel, sheet, row, server_columns, client_columns):
    color = get_cell_bgcolor(excel, sheet, row, 0)

    server_types = {}
    client_types = {}
    start_range = 0
    
    if get_rule(color) != cell_for_type:
        return (row, server_types, client_types)

    for i in range(start_range, sheet.ncols):
        val = sheet.cell_value(row, i)
        color = get_cell_bgcolor(excel, sheet, row, i)
        if get_rule(color) == cell_for_type and val != '':
            if i in server_columns:
                server_types[server_columns[i]] = val
            if i in client_columns:
                client_types[client_columns[i]] = val
    return (row + 1, server_types, client_types)

def tidy(v):
    if type(v) == float:
        if str(v).endswith('.0'):
            return str(int(v))
    return str(v)

def extract_data(excel, sheet, row, columns):
    items = []
    columns = dict(set(columns.items()))

    for r in range(row, sheet.nrows):
        if is_comment(sheet, r):
            continue
        color = get_cell_bgcolor(excel, sheet, r, 0)
        if get_rule(color) == cell_ending:
            return items
        record = {}

        for i in range(0, sheet.ncols):
            val = sheet.cell_value(r, i)
            if i in columns and not (val == '' and columns[i] in record):
                record[columns[i]] = tidy(val)

        items.append(record)
    return items

def parse_excel(filename, page = 0):
    if not filename.endswith('.xls'):
        raise RuntimeError('xls file expected.')

    excel = xlrd.open_workbook(filename,
            formatting_info = True, encoding_override="utf-8")
    sheet = excel.sheets()[page]

    row = 5;    # we start at row 5
    row, table_name = extract_table_name(excel, sheet, row)
    if table_name == '':
        table_name = os.path.basename(filename)[:-4]
    row, server_columns, client_columns = extract_column_info(excel, sheet, row)
    row, server_types, client_types = extract_column_type(excel, sheet, row, server_columns, client_columns)
    items_c = extract_data(excel, sheet, row, client_columns)
    items_s = extract_data(excel, sheet, row, server_columns)
    return (table_name, server_columns, client_columns, items_s, items_c, server_types, client_types)


