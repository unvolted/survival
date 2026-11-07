@echo off
rem Run the ROOTFALL automation tests headless and write a report.
rem Usage:  Scripts\run_tests.bat [Filter]     (default filter: RF.  -> every RF.* test)
rem Results: Saved\Logs\RF_Tests.log and Saved\Automation\Report\index.json
setlocal
if "%UE_ROOT%"=="" set "UE_ROOT=C:\Program Files\Epic Games\UE_5.8"
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
set "UPROJECT=%PROJECT_DIR%\ROOTFALL.uproject"
set "FILTER=%~1"
if "%FILTER%"=="" set "FILTER=RF."

if not exist "%UE_ROOT%\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" (
	echo UE 5.8 not found at "%UE_ROOT%". Set UE_ROOT to the engine folder.
	exit /b 2
)

"%UE_ROOT%\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "%UPROJECT%" -ExecCmds="Automation RunTests %FILTER%" -TestExit="Automation Test Queue Empty" -ReportExportPath="%PROJECT_DIR%\Saved\Automation\Report" -unattended -nopause -nullrhi -nosound -nosplash -log=RF_Tests.log
set "RESULT=%ERRORLEVEL%"
echo run_tests: exit code %RESULT%. Check the results, not only the exit code:
echo   findstr /C:"Test Completed" "%PROJECT_DIR%\Saved\Logs\RF_Tests.log"
echo   %PROJECT_DIR%\Saved\Automation\Report\index.json
exit /b %RESULT%
