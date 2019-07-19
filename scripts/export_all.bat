echo off
path = %path%;c:\python27
echo on
cd %~dp0
cd gen_config
python export.py 
cd ..\gen_dts
python gen_dts.py
cd ..\pack
python pack.py

cd %~dp0
call copyData.cmd

pause


