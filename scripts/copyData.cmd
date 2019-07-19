@echo off
pushd "%~dp0"
rem -------------------------------------------------
rem copy到y-client
rem -------------------------------------------------
set dest1=..\..\y-client\src\game\config
set dest2=..\..\y-client\resource\config\jsons

if exist "%dest1%" (
	del /Q "%dest1%\config.d.ts"
	del /Q "%dest1%\config.hash"
	del /Q "%dest1%\config.ts"
	copy /Y ..\code\config.d.ts "%dest1%\"	
	copy /Y ..\code\config.hash "%dest1%\"
	copy /Y ..\code\config.ts "%dest1%\"
)
if exist "%dest2%" (
	del /Q "%dest2%\*.json"
	copy /Y ..\config\jsons\*.json "%dest2%\"	
)
if exist C:\"Program Files"\7-Zip (
	start C:\"Program Files"\7-Zip\7z a -tzip "%dest2%\..\data.zip" "%dest2%\"
)
popd



if "%1"=="" pause
GOTO:EOF
