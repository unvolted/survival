# ROOTFALL: Unreal Engine 5.8 project

First-person survival vertical slice. Spec: [`Design/ROOTFALL_Brief.md`](../../Design/ROOTFALL_Brief.md).
This folder is owned by the game-builder agent (Agent 3). Milestone reports are in [`Reports/`](../../Reports/).

**Current state: milestone M0 (Setup), written but NOT yet compiled or run.** Unreal Engine 5.8 is
only on the user's PC, which was not attached when M0 was written. Follow "Build and verify on the PC"
below to check it.

| | |
|---|---|
| Engine | Unreal Engine **5.8** (`"EngineAssociation": "5.8"` in `ROOTFALL.uproject`) |
| C++ module | `ROOTFALL` (`Source/ROOTFALL`), class prefix `RF`, API macro `ROOTFALL_API` |
| Targets | `ROOTFALLEditor` (editor), `ROOTFALL` (game) |
| Plugins enabled | Enhanced Input, StateTree, GameplayStateTree, PCG, CommonUI, Python Editor Script Plugin, Editor Scripting Utilities, Functional Testing Editor |
| Startup map | `/Game/RF/Maps/L_Test_Empty` (editor and game), made by `Scripts/create_test_map.py` |
| Game mode | `ARFGameMode` (global default): `ARFPlayerController` + engine `ADefaultPawn` until M1 |

## Layout

```
ROOTFALL.uproject
Config/          DefaultEngine.ini (maps, game mode, Lumen/VSM/Nanite, CommonUI viewport)
                 DefaultGame.ini   (project info, sandbox defaults [/Script/ROOTFALL.RFSandboxSettings])
                 DefaultInput.ini  (Enhanced Input as the default input classes)
                 DefaultEditor.ini (shared editor settings)
Source/ROOTFALL.Target.cs, ROOTFALLEditor.Target.cs
Source/ROOTFALL/ ROOTFALL.Build.cs
  Public/Core/      RFLog.h, RFGameMode.h, RFPlayerController.h
  Public/Debug/     RFCheatManager.h, RFDebugCommands.h, RFDebugCVars.h
  Public/Settings/  RFSandboxSettings.h
  Private/...       matching .cpp files, Tests/RFSetupTests.cpp
Content/RF/      Characters, Environment, Buildables, Weapons, Props, Foliage, Audio, UI, Data, Maps
                 (empty folders hold a .gitkeep until assets arrive)
Scripts/         create_test_map.py (+ .bat), check_naming.py, build_editor.bat, run_tests.bat
```

Gameplay is C++ (Actor Components and Subsystems). Blueprints only for content and tuning.
`.uasset`/`.umap` files are binary: they are made by editor Python scripts in `Scripts/`, run on the PC,
and committed through Git LFS (see the repo's `.gitattributes`). Never commit `Binaries/`,
`Intermediate/`, `Saved/` or `DerivedDataCache/` (ignored by `.gitignore`).

## Naming

The brief's handoff contract: prefixes `SM_ SK_ SKEL_ A_ T_ M_ MI_ BP_ ABP_ DA_ DT_ WBP_ SFX_ MS_`
(plus `CA_`, `UCX_`, `SOCKET_` outside Unreal), PascalCase with underscores, tiers `T1/T2/T3`,
states `_Intact/_Damaged/_Broken`, textures end in `_BC/_N/_ORM/_E`. Assumed additions (not in the brief):
`L_` for maps, `IA_`/`IMC_` for Enhanced Input actions and mapping contexts. Check names and the manifest:

```
python3 Unreal/ROOTFALL/Scripts/check_naming.py          # Content/RF + Manifest/asset_manifest.csv
python3 Unreal/ROOTFALL/Scripts/check_naming.py --all    # also Concept/ and Export/
```

## Sandbox settings

All sandbox options are in `URFSandboxSettings` (Project Settings > Game > ROOTFALL Sandbox), saved to
`Config/DefaultGame.ini`: day length, zombie population / cap / speed / toughness / respawn, infection rule
and time to death, Zomboid-rule infection chances, loot abundance, bandit groups, tree regrowth.
C++: `URFSandboxSettings::Get().DayLengthMinutes`. Keep `SettingsVersion=1` in the ini (a test checks it).

## Debug commands

Open the console with `` ` `` (Tilde) in Play-In-Editor or a non-shipping build. `RF_Help` lists every
command and its status. Commands without their system yet print `not implemented until M#`.

| Command | Brief item | Status in M0 |
|---|---|---|
| `RF_Help` | (list commands) | works |
| `RF_SpawnZombies <Count> [Variant]` | spawn N zombies at cursor | not implemented until M3 |
| `RF_SpawnBanditGroup [Size 2..4]` | spawn bandit group | not implemented until M6 |
| `RF_SetTime <Hour>` | set time | not implemented until M2 |
| `RF_SetWeather <Clear\|Overcast\|Rain\|Storm\|Fog>` | set weather | not implemented until M7 |
| `RF_GiveItem <ItemId> [Count]` | give item | not implemented until M5 |
| `RF_SetInfectionHours <HoursSinceBite>` | set infection hours | not implemented until M2 |
| `RF_God` | god mode | toggles `rf.GodMode` (and blocks engine damage on the pawn); RF damage/needs honour it from M2 |
| `RF_ShowNoiseRadii` | show noise radii | toggles `rf.ShowNoiseRadii`; drawing from M1 |
| `RF_ShowAIStates` | show AI states | toggles `rf.ShowAIStates`; drawing from M3 |
| `RF_ShowStructureHP` | show structure HP | toggles `rf.ShowStructureHP`; drawing from M4 |

The flags are console variables and can also be set directly: `rf.ShowNoiseRadii 1`, `rf.GodMode 0`.
Systems read them through `RFDebug::ShouldShowNoiseRadii()` etc. (`Debug/RFDebugCVars.h`), never through
the cheat manager. To add a command: add a `UFUNCTION(Exec)` to `URFCheatManager` and a row to
`RFDebugCommands::GetAll()`; the `RF.Setup.DebugCommands` test checks the two match.

## Automation tests

| Test | Checks |
|---|---|
| `RF.Setup.SandboxSettingsDefaults` | sandbox settings load from `DefaultGame.ini` with the brief's defaults and ranges |
| `RF.Setup.DebugCommands` | every brief debug command has a table row, an `Exec` UFUNCTION and its `rf.*` flag |
| `RF.Setup.TestMap` | `/Game/RF/Maps/L_Test_Empty` exists and is the game default map (fails until the map script has run) |

Run them (Scripts/run_tests): `Scripts\run_tests.bat` on Windows, or the exact command:

```
"%UE_ROOT%\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "<repo>\Unreal\ROOTFALL\ROOTFALL.uproject" -ExecCmds="Automation RunTests RF." -TestExit="Automation Test Queue Empty" -ReportExportPath="<repo>\Unreal\ROOTFALL\Saved\Automation\Report" -unattended -nopause -nullrhi -nosound -nosplash -log=RF_Tests.log
```

`RF.` is a substring filter on test names. In the editor: Tools > Test Automation, filter `RF.`, Start Tests.
Results: `Saved/Logs/RF_Tests.log` (lines `Test Completed. Result={Success} ... Path={RF.Setup...}`; the
exact result word can differ between engine versions) and `Saved/Automation/Report/index.json`
(`succeeded`, `failed` counts). Check the results, not only the exit code.

## Build and verify on the PC

Assumes Windows and the Epic launcher engine at `C:\Program Files\Epic Games\UE_5.8`; set `UE_ROOT`
if it is elsewhere. All commands run from the repo root unless noted. M0 is accepted when steps 3, 5, 6
and 7 pass.

1. **Get the code.** `git pull` then `git lfs pull` (Git LFS must be installed: `git lfs install`).
2. **Generate project files** (only needed for Visual Studio / Rider):
   ```
   "%UE_ROOT%\Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.exe" -projectfiles -project="%CD%\Unreal\ROOTFALL\ROOTFALL.uproject" -game -rocket -progress
   ```
   (or right-click `ROOTFALL.uproject` > Generate Visual Studio project files).
3. **Build the editor target:** `Unreal\ROOTFALL\Scripts\build_editor.bat`, which runs
   ```
   "%UE_ROOT%\Engine\Build\BatchFiles\Build.bat" ROOTFALLEditor Win64 Development -Project="%CD%\Unreal\ROOTFALL\ROOTFALL.uproject" -WaitMutex
   ```
   Pass: exit code 0, `Result: Succeeded`, zero errors and no new warnings from `Source/ROOTFALL`.
   If UBT says a plugin cannot be found, see "If something fails" below.
4. **Check names:** `python Unreal\ROOTFALL\Scripts\check_naming.py` (0 errors).
5. **Create the test map:** `Unreal\ROOTFALL\Scripts\create_test_map.bat`, which runs
   ```
   "%UE_ROOT%\Engine\Binaries\Win64\UnrealEditor.exe" "%CD%\Unreal\ROOTFALL\ROOTFALL.uproject" -ExecutePythonScript="%CD%\Unreal\ROOTFALL\Scripts\create_test_map.py --quit" -log=RF_CreateTestMap.log
   ```
   The first launch warns that the startup map is missing; that is expected. Pass:
   `Saved/Logs/RF_CreateTestMap.log` contains `[create_test_map] Saved /Game/RF/Maps/L_Test_Empty` and
   `Content/RF/Maps/L_Test_Empty.umap` exists. Running it again prints `Nothing to do`.
   The script path must not contain spaces (the engine splits the argument on spaces); if it does, open the
   editor and use Tools > Execute Python Script... instead. The full editor is used on purpose: level
   creation through the `-run=pythonscript` commandlet is not reliable.
6. **Open the empty test map:** start the editor (`UnrealEditor.exe "<path>\ROOTFALL.uproject"`). It opens
   `L_Test_Empty` (floor, PlayerStart, light). Press Play: you fly with the default pawn; open the console
   and run `RF_Help`, `RF_ShowNoiseRadii` and `RF_SpawnZombies 3` (expect `not implemented until M3`).
   Pass: the map opens and the Output Log shows no new errors or warnings from ROOTFALL (`LogRF`, `LogRFDebug`).
   Headless alternative: `UnrealEditor.exe "<path>\ROOTFALL.uproject" /Game/RF/Maps/L_Test_Empty -game -windowed -ResX=1280 -ResY=720 -log`
   and look for `LoadMap` of `L_Test_Empty` and `ROOTFALL game mode started` in the log.
7. **Run the automation tests:** `Unreal\ROOTFALL\Scripts\run_tests.bat` (command above). Pass: all three
   `RF.Setup.*` tests succeed.
8. **Commit** `Content/RF/Maps/L_Test_Empty.umap` (goes to LFS) and push.

On Linux or macOS use `Engine/Build/BatchFiles/Linux/Build.sh` / `Mac/Build.sh` with the platform
`Linux` / `Mac`, and `Engine/Binaries/<Platform>/UnrealEditor-Cmd` / `UnrealEditor` for the same arguments.

### If something fails

- *Plugin not found* (UBT or editor): a plugin was renamed in 5.8. `FunctionalTestingEditor` is the most
  likely one and M0 does not need it; remove its entry from `ROOTFALL.uproject` and rebuild. Report any other.
- *Module not found* for `StateTreeModule`, `GameplayStateTreeModule`, `PCG`, `CommonUI` or `CommonInput`:
  nothing in M0 uses these yet. Remove that line from `ROOTFALL.Build.cs` and report it.
- *`RF.Setup.TestMap` fails:* step 5 has not been run, or `GameDefaultMap` in `DefaultEngine.ini` was changed.

## Assets used

None yet. M0 uses only engine content (`/Engine/BasicShapes/Plane`, `PlayerStart`, `DirectionalLight`)
in the test map. Imported assets and their manifest rows are listed here from M1 on.
