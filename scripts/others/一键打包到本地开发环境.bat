@echo off
path = %path%;c:\python27

rem 请在此处配置本地服配套的 服务器、客户端、文档 路径
set SERVER=D:\qyj\1_environment\_Trunk\Server\
set CLIENT=D:\qyj\1_environment\_Trunk\Client\project\
set DOC=D:\qyj\1_environment\Docs\trunk\product\

echo 本工具运行过程中请不要做任何svn操作！
echo 请确保系统当前没有在重复运行本工具！
echo 如果正在重复运行本工具，请点击右上角关闭按钮，待上一次工具运行结束再开始运行本工具！
echo ================按任意键开始打包====================
pause

del %DOC%\config\*.zip
svn update %DOC%\server
svn update %DOC%\config

rem 请在此处编辑需要打包的EXCEL表配置，可配置多行
python export_one.py ..\excel\Xunbao.xls


python gen_dts.py
python dabao.py

echo ================结束打包====================
echo.
echo ================按任意键开始更新本地服SVN====================
pause

del %CLIENT%\resource\config\*.zip
del %CLIENT%\manifest.json
del %CLIENT%\resource\default.*.json
svn update %SERVER%
svn update %CLIENT%
echo ================结束更新本地服SVN====================
echo.
echo ================按任意键开始复制代码到本地服环境====================
pause

XCOPY %DOC%\config\*.*	%CLIENT%\resource\config /s/y/i
XCOPY %DOC%\server\*.erl	%SERVER%\data /s/y/i
echo ================结束复制代码到本地服环境====================
echo.
echo ================按任意键开始编译本地服====================
pause

cd %SERVER%\tools\
call make.bat
echo ================结束编译本地服====================
echo.
echo 恭喜！完成一键打包到本地开发环境！
echo 按任意键结束本次运行！
echo.
pause