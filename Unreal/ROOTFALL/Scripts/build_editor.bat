@echo off
rem Build the ROOTFALLEditor target (Win64 Development).
rem Usage:  Scripts\build_editor.bat          (set UE_ROOT if the engine is not in the default folder)
setlocal
if "%UE_ROOT%"=="" set "UE_ROOT=C:\Program Files\Epic Games\UE_5.8"
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
set "UPROJECT=%PROJECT_DIR%\ROOTFALL.uproject"

if not exist "%UE_ROOT%\Engine\Build\BatchFiles\Build.bat" (
	echo UE 5.8 not found at "%UE_ROOT%". Set UE_ROOT to the engine folder, for example:
	echo   set "UE_ROOT=D:\Epic Games\UE_5.8"
	exit /b 2
)

call "%UE_ROOT%\Engine\Build\BatchFiles\Build.bat" ROOTFALLEditor Win64 Development -Project="%UPROJECT%" -WaitMutex
set "RESULT=%ERRORLEVEL%"
echo build_editor: exit code %RESULT% (0 = succeeded). Full log: %LOCALAPPDATA%\UnrealBuildTool\Log.txt
exit /b %RESULT%
