# GameBuilder — M0 Setup

Milestone M0 (brief: "UE 5.8 C++ project, folders, naming, manifest, version control, debug command
framework"). Acceptance: "Project compiles cleanly; an empty test map opens; one automation test runs and passes."

**Status: written, NOT verified.** The user's PC with Unreal Engine 5.8 was not attached to the session,
so nothing was compiled, opened or run in Unreal. M0 does not pass until the PC steps below are done.
M1 was not started.

## Done

Project `Unreal/ROOTFALL/`:

- `ROOTFALL.uproject`: `"EngineAssociation": "5.8"`, runtime module `ROOTFALL`. Plugins enabled: EnhancedInput,
  StateTree, GameplayStateTree, PCG, CommonUI, PythonScriptPlugin, EditorScriptingUtilities, FunctionalTestingEditor.
- `Source/ROOTFALL.Target.cs`, `Source/ROOTFALLEditor.Target.cs` (`BuildSettingsVersion.Latest`,
  `EngineIncludeOrderVersion.Latest`).
- `Source/ROOTFALL/ROOTFALL.Build.cs`: Core, CoreUObject, Engine, InputCore, EnhancedInput, DeveloperSettings
  (public). EngineSettings (private, for the test). GameplayTags, AIModule, NavigationSystem, StateTreeModule,
  GameplayStateTreeModule, UMG, Slate, SlateCore, CommonUI, CommonInput, PCG are listed now as well
  (private, commented with their milestone), so the M0 build already shows whether every required plugin is
  enabled and links.
- C++ (`Source/ROOTFALL/Public|Private/...`):
  - `Core/RFLog.h` + `ROOTFALL.cpp`: module (`IMPLEMENT_PRIMARY_GAME_MODULE`), log categories `LogRF`, `LogRFDebug`.
  - `Core/RFGameMode`: `ARFGameMode` (global default game mode), uses `ARFPlayerController`, engine
    `ADefaultPawn` until M1.
  - `Core/RFPlayerController`: `ARFPlayerController`, sets `CheatClass = URFCheatManager`.
  - `Settings/RFSandboxSettings`: `URFSandboxSettings : UDeveloperSettings` (Config=Game, DefaultConfig;
    Project Settings > Game > ROOTFALL Sandbox), with every sandbox option the brief lists: day length,
    zombie population / cap / speed / toughness / respawn, infection rule, hours to death, Zomboid-rule chances,
    loot abundance, bandit groups, tree regrowth. Enum `ERFInfectionRule { BiteOnly, ZomboidRules }`.
  - Debug command framework:
    - `Debug/RFCheatManager`: `URFCheatManager : UCheatManager` with one `UFUNCTION(Exec)` per brief command:
      `RF_Help`, `RF_SpawnZombies`, `RF_SpawnBanditGroup`, `RF_SetTime`, `RF_SetWeather`, `RF_GiveItem`,
      `RF_SetInfectionHours`, `RF_God`, `RF_ShowNoiseRadii`, `RF_ShowAIStates`, `RF_ShowStructureHP`.
    - `Debug/RFDebugCommands`: the command table (name, usage, brief wording, milestone, status, flag).
      `RF_Help` prints it; stubs print `RF_X <args>: not implemented until M#.`
    - `Debug/RFDebugCVars`: flags `rf.GodMode`, `rf.ShowNoiseRadii`, `rf.ShowAIStates`, `rf.ShowStructureHP`
      (`TAutoConsoleVariable<bool>`, `ECVF_Cheat`) with accessors `RFDebug::IsGodModeEnabled()` etc. for the systems.
    - Implemented in M0: `RF_Help`; the four flag toggles (`RF_God` also blocks engine damage on the pawn).
      Not implemented (stub + log): SpawnZombies (M3), SpawnBanditGroup (M6), SetTime (M2), SetWeather (M7),
      GiveItem (M5), SetInfectionHours (M2). Flag readers arrive in: noise radii M1, god mode M2, AI states M3,
      structure HP M4.
  - `Tests/RFSetupTests.cpp` (3 `IMPLEMENT_SIMPLE_AUTOMATION_TEST`s, Editor + Client context, ProductFilter):
    `RF.Setup.SandboxSettingsDefaults`, `RF.Setup.DebugCommands`, `RF.Setup.TestMap`.
- `Config/`: `DefaultEngine.ini` (EditorStartupMap and GameDefaultMap = `/Game/RF/Maps/L_Test_Empty`,
  GlobalDefaultGameMode = `ARFGameMode`, CommonUI viewport client, Lumen, VSM, Nanite, distance fields, no static
  lighting, extended luminance range, DX12), `DefaultGame.ini` (project info, sandbox defaults,
  `SettingsVersion=1`), `DefaultInput.ini` (EnhancedPlayerInput / EnhancedInputComponent as default classes,
  console key Tilde, no legacy mappings), `DefaultEditor.ini` (validate assets on save).
- `Content/RF/{Characters, Environment, Buildables, Weapons, Props, Foliage, Audio, UI, Data, Maps}/.gitkeep`.
- `Scripts/`:
  - `create_test_map.py` (editor Python) creates or refreshes `/Game/RF/Maps/L_Test_Empty` with a 100 m floor
    (`/Engine/BasicShapes/Plane`), a PlayerStart and a directional light. It is safe to run again: it adds only
    missing actors (found by label) and saves only when something changed. `--quit` closes the editor afterwards.
  - `create_test_map.bat`, `build_editor.bat`, `run_tests.bat` (Windows wrappers, `UE_ROOT` overridable).
  - `check_naming.py` (plain Python 3, read-only) checks Content/RF asset names and the manifest
    against the handoff contract; `--all` also checks `Concept/` and `Export/`.
- Version control: `Unreal/ROOTFALL/.gitignore` (repeats the root build-output rules, adds IDE files) and
  `Unreal/ROOTFALL/.gitattributes` (`*.bat` CRLF, sources LF). The repo root already sends `*.uasset`/`*.umap`
  to Git LFS.
- `Unreal/ROOTFALL/README.md`: engine, layout, naming, sandbox settings, debug commands, tests with the exact
  run command, PC build/verify steps, troubleshooting.
- Manifest: no rows added or changed (M0 imports no assets).

## Verified

What was checked here (cloud container, no Unreal):
- `ROOTFALL.uproject` parses as JSON (`python3 json.load`); EngineAssociation is `5.8`.
- `create_test_map.py` parses (Python `ast.parse`). It was not run, because it needs the Unreal editor.
- All 8 `.cpp` files pass `g++ -std=c++20 -fsyntax-only -Wall -Wextra` against a small hand-written mock of the UE
  types and macros (scratchpad only, not in the repo). This catches C++ syntax, typos and wrong member names
  against the mock. It is **not** a UE compile: UHT, the real engine headers, the module rules and linking were not checked.
- The C++ was checked by hand against the UE 5.x API: `UCLASS`/`UENUM`/`UPROPERTY`/`UFUNCTION(Exec)`,
  `GENERATED_BODY()` and `.generated.h` as the last include in every reflected header, `ROOTFALL_API` on
  exported classes and functions, Public/Private include paths, Build.cs dependencies for every include
  (DeveloperSettings for `UDeveloperSettings`, EngineSettings for `UGameMapsSettings`).
- `check_naming.py`: on the repo, 0 errors (Content/RF is empty, the manifest has only its header). On a scratch
  fixture with planted mistakes it caught every one (space in name, missing prefix, tier T4, texture with no
  suffix, map without `L_`, asset outside `Content/RF/`, duplicate asset_id, bad status, non-numeric triangles,
  bad FBX and concept names) and skipped `__ExternalActors__`.

Acceptance tests:

| Acceptance test | Result |
|---|---|
| Project compiles cleanly | **NOT verified (UE 5.8 PC not attached)** |
| An empty test map opens | **NOT verified (UE 5.8 PC not attached)**: the map does not exist until `create_test_map.py` runs on the PC |
| One automation test runs and passes | **NOT verified (UE 5.8 PC not attached)** |

Automation test results: none. No tests were run. Frame-time numbers: none (nothing ran, no Unreal Insights capture).

## Assumptions

- **Debug commands are `UFUNCTION(Exec)` on a `UCheatManager` subclass** named `RF_<Verb>`, plus `rf.*` console
  variables for the on/off flags. They work in PIE and non-shipping builds only. Commands that need a player
  (cursor trace, inventory) belong on the player's cheat manager.
- **Milestone per stub** (the brief does not give one): SetTime M2 (the infection clock needs in-game time),
  SetInfectionHours M2, god-mode consumers M2, SpawnZombies M3, ShowAIStates M3, ShowStructureHP M4, GiveItem M5,
  SpawnBanditGroup M6, SetWeather M7. ShowNoiseRadii drawing is M1 because the M1 acceptance test reads footstep
  noise from the noise debug view.
- **`RF_God` meaning:** no damage, no needs drain, no infection progress. M0 also clears `bCanBeDamaged` on the pawn.
- **Sandbox settings** are a `UDeveloperSettings` (project defaults in `DefaultGame.ini`). The brief says "Data Asset
  + save". The per-world copy stored in the save is planned for M5 with `URFSaveSubsystem`.
- **Sandbox values the brief does not give:** MaxActiveZombies 300 (top of the brief's 150 to 300 target),
  ZombieRespawnUnvisitedDays 3, TreeRegrowDays 14, MaxActiveBanditGroups default 2 (range 0 to 2), and
  multipliers 1.0 (population, speed, toughness, loot).
- **Naming prefixes not in the brief:** `L_` for maps (the task named the map `L_Test_Empty`), `IA_` / `IMC_` for
  Enhanced Input assets (M1). `check_naming.py` accepts them and prints a warning. They need approval to join the contract.
- **Test map contents:** "empty" means only a floor, a PlayerStart and one directional light, so you can stand
  in it. It is not World Partition (the 1 km map in M7 will be).
- **M0 pawn:** engine `ADefaultPawn` (free-fly, legacy default bindings) until `ARFCharacter` in M1.
  I expect its legacy bindings to still work with the Enhanced Input default classes, but this is not verified.
- **Map script runs in the full editor** (`UnrealEditor.exe -ExecutePythonScript=...`), not the `-run=pythonscript`
  commandlet, because the commandlet does not reliably support level creation.
- **Test filter:** `Automation RunTests RF.` (a substring filter). All project tests use the `RF.` prefix.
- **Third test `RF.Setup.TestMap`** was added on purpose. It fails until the map script has run, which turns the
  "map exists" step into an automated check.
- **CommonUI viewport client** is set now (`CommonGameViewportClient`), as CommonUI's setup requires.
- Agent-file template paths `game/` and `assets/models/` from the generic game-builder prompt were not used. The repo's
  `CLAUDE.md` and the task say `Unreal/ROOTFALL/`, `Export/`.

## Blocked

- **All three acceptance tests are blocked on the user's PC with UE 5.8** (Remote Control attach). Who: the user
  (attach the PC), then game-builder runs the steps below.
- Possible build risks to look at first on the PC (I could not check them without the engine):
  1. Plugin names in 5.8. `FunctionalTestingEditor` is the least certain. M0 does not need it; if UBT or the editor
     cannot find it, remove it from `ROOTFALL.uproject`.
  2. Module names `StateTreeModule`, `GameplayStateTreeModule`, `PCG`, `CommonUI`, `CommonInput`. Nothing in M0 uses
     them, so any that fail can be removed from `ROOTFALL.Build.cs` and fixed when their milestone starts.
  3. `IConsoleVariable::Set(bool, ...)` and `EAutomationTestFlags` were checked against the UE 5.x API from memory.
     The test flags are written as a plain expression, so they compile with either the namespaced enum or the enum class.

## Next

Steps on the PC (exact commands in `Unreal/ROOTFALL/README.md`, "Build and verify on the PC"):
1. `git pull` and `git lfs pull`.
2. (Optional) generate project files with UnrealBuildTool `-projectfiles`.
3. `Unreal\ROOTFALL\Scripts\build_editor.bat`: Build.bat `ROOTFALLEditor Win64 Development`. It must succeed with zero errors.
4. `python Unreal\ROOTFALL\Scripts\check_naming.py`: 0 errors.
5. `Unreal\ROOTFALL\Scripts\create_test_map.bat`: creates `Content/RF/Maps/L_Test_Empty.umap`.
6. Open the editor: `L_Test_Empty` opens. In PIE, run `RF_Help` and `RF_SpawnZombies 3`; there must be no new errors or warnings.
7. `Unreal\ROOTFALL\Scripts\run_tests.bat`: `RF.Setup.SandboxSettingsDefaults`, `RF.Setup.DebugCommands` and
   `RF.Setup.TestMap` all succeed (`Saved/Logs/RF_Tests.log`, `Saved/Automation/Report/index.json`).
8. Commit `L_Test_Empty.umap` (LFS), update this report with the real build and test results and a first
   Unreal Insights frame-time capture of the empty map, then start M1.

For the other agents: M0 imports no assets. When an asset reaches `Exported`, game-builder imports it into
`Content/RF/<Category>/` from M1 on. `check_naming.py --all` can be used by anyone to check their own file names
and the manifest before handoff (read-only).

Known bugs: none known. Nothing has run yet, so none could be found.
