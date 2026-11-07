@echo off
rem Create (or refresh) /Game/RF/Maps/L_Test_Empty with the full editor, then quit.
rem Usage:  Scripts\create_test_map.bat        (build ROOTFALLEditor first)
setlocal
if "%UE_ROOT%"=="" set "UE_ROOT=C:\Program Files\Epic Games\UE_5.8"
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
set "UPROJECT=%PROJECT_DIR%\ROOTFALL.uproject"
set "SCRIPT=%PROJECT_DIR%\Scripts\create_test_map.py"

if not exist "%UE_ROOT%\Engine\Binaries\Win64\UnrealEditor.exe" (
	echo UE 5.8 not found at "%UE_ROOT%". Set UE_ROOT to the engine folder.
	exit /b 2
)

"%UE_ROOT%\Engine\Binaries\Win64\UnrealEditor.exe" "%UPROJECT%" -ExecutePythonScript="%SCRIPT% --quit" -log=RF_CreateTestMap.log
echo create_test_map: check "%PROJECT_DIR%\Saved\Logs\RF_CreateTestMap.log" for "[create_test_map] Saved" or "Nothing to do".
echo Then commit Content\RF\Maps\L_Test_Empty.umap (Git LFS).
