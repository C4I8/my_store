#!/bin/bash
#python export.py 
python export_one.py ../excel/Item.xls

python gen_dts.py

python dabao.py
