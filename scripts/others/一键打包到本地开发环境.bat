@echo off
path = %path%;c:\python27

rem ���ڴ˴����ñ��ط����׵� ���������ͻ��ˡ��ĵ� ·��
set SERVER=D:\qyj\1_environment\_Trunk\Server\
set CLIENT=D:\qyj\1_environment\_Trunk\Client\project\
set DOC=D:\qyj\1_environment\Docs\trunk\product\

echo ���������й������벻Ҫ���κ�svn������
echo ��ȷ��ϵͳ��ǰû�����ظ����б����ߣ�
echo ��������ظ����б����ߣ��������Ͻǹرհ�ť������һ�ι������н����ٿ�ʼ���б����ߣ�
echo ================���������ʼ���====================
pause

del %DOC%\config\*.zip
svn update %DOC%\server
svn update %DOC%\config

rem ���ڴ˴��༭��Ҫ�����EXCEL�����ã������ö���
python export_one.py ..\excel\Xunbao.xls


python gen_dts.py
python dabao.py

echo ================�������====================
echo.
echo ================���������ʼ���±��ط�SVN====================
pause

del %CLIENT%\resource\config\*.zip
del %CLIENT%\manifest.json
del %CLIENT%\resource\default.*.json
svn update %SERVER%
svn update %CLIENT%
echo ================�������±��ط�SVN====================
echo.
echo ================���������ʼ���ƴ��뵽���ط�����====================
pause

XCOPY %DOC%\config\*.*	%CLIENT%\resource\config /s/y/i
XCOPY %DOC%\server\*.erl	%SERVER%\data /s/y/i
echo ================�������ƴ��뵽���ط�����====================
echo.
echo ================���������ʼ���뱾�ط�====================
pause

cd %SERVER%\tools\
call make.bat
echo ================�������뱾�ط�====================
echo.
echo ��ϲ�����һ����������ؿ���������
echo ������������������У�
echo.
pause