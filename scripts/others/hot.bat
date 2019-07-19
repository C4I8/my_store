@setlocal enableextensions enabledelayedexpansion
@echo off

set pwd=%~dp0

if not x%pwd:publish=%==x%pwd% (
    echo "hot load 48 publish"
    for %%i in (%*) do curl -F "%%i=@../server/%%i.erl" 172.16.11.207:20008/data_upload
) else if not x%pwd:branch=%==x%pwd% (
    echo "hot load 48 stable "
    for %%i in (%*) do curl -F "%%i=@../server/%%i.erl" 172.16.11.207:20011/data_upload
) else (
    echo "hot load h5 trunk "
    for %%i in (%*) do curl -F "%%i=@../server/%%i.erl" 172.16.11.207:20008/data_upload
)

endlocal

pause
