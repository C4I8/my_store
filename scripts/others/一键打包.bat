echo off
path = %path%;c:\python27
echo on


python export_one.py ..\excel\MonsterAi.xls


python gen_dts.py
python dabao.py


pause