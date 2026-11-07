// M0 automation tests (Automation RunTests RF.).

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "GameMapsSettings.h"
#include "HAL/IConsoleManager.h"
#include "Misc/PackageName.h"
#include "UObject/Class.h"
#include "Debug/RFCheatManager.h"
#include "Debug/RFDebugCommands.h"
#include "Debug/RFDebugCVars.h"
#include "Settings/RFSandboxSettings.h"

// Written as an expression (not a typed constant) so it compiles whether EAutomationTestFlags is the
// older namespaced enum or the enum class used by newer engine versions.
#define RF_SETUP_TEST_FLAGS (EAutomationTestFlags::EditorContext | EAutomationTestFlags::ClientContext | EAutomationTestFlags::ProductFilter)

// ---------------------------------------------------------------------------------------------
// RF.Setup.SandboxSettingsDefaults: the sandbox settings load from DefaultGame.ini and carry the
// defaults and ranges the brief specifies.
// ---------------------------------------------------------------------------------------------
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRFSandboxSettingsDefaultsTest, "RF.Setup.SandboxSettingsDefaults", RF_SETUP_TEST_FLAGS)

bool FRFSandboxSettingsDefaultsTest::RunTest(const FString& Parameters)
{
	const URFSandboxSettings* Settings = GetDefault<URFSandboxSettings>();
	if (!TestNotNull(TEXT("URFSandboxSettings class default object"), Settings))
	{
		return false;
	}

	// Code default is 0; only DefaultGame.ini sets 1, so 1 proves the ini section was read.
	TestEqual(TEXT("SettingsVersion (loaded from DefaultGame.ini)"), Settings->SettingsVersion, 1);

	// Values the brief states explicitly.
	TestEqual(TEXT("DayLengthMinutes (brief default 60)"), Settings->DayLengthMinutes, 60.f);
	TestTrue(TEXT("InfectionRule is Bite only (brief default)"), Settings->InfectionRule == ERFInfectionRule::BiteOnly);
	TestEqual(TEXT("InfectionHoursToDeath (brief default 48)"), Settings->InfectionHoursToDeath, 48.f);
	TestEqual(TEXT("ScratchInfectionChance (brief 7 percent)"), Settings->ScratchInfectionChance, 0.07f, 0.0001f);
	TestEqual(TEXT("LacerationInfectionChance (brief 25 percent)"), Settings->LacerationInfectionChance, 0.25f, 0.0001f);

	// Ranges the brief states.
	TestTrue(TEXT("DayLengthMinutes within 30..180"), Settings->DayLengthMinutes >= 30.f && Settings->DayLengthMinutes <= 180.f);
	TestTrue(TEXT("InfectionHoursToDeath within 24..96"), Settings->InfectionHoursToDeath >= 24.f && Settings->InfectionHoursToDeath <= 96.f);
	TestTrue(TEXT("MaxActiveBanditGroups within 0..2"), Settings->MaxActiveBanditGroups >= 0 && Settings->MaxActiveBanditGroups <= 2);
	TestTrue(TEXT("MaxActiveZombies is not negative"), Settings->MaxActiveZombies >= 0);

	return true;
}

// ---------------------------------------------------------------------------------------------
// RF.Setup.DebugCommands: every debug command the brief lists has a table entry, a matching
// UFUNCTION(Exec) on URFCheatManager, and (for the Show* / God commands) a registered rf.* flag.
// ---------------------------------------------------------------------------------------------
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRFDebugCommandsTest, "RF.Setup.DebugCommands", RF_SETUP_TEST_FLAGS)

bool FRFDebugCommandsTest::RunTest(const FString& Parameters)
{
	// Brief, Agent 3 > Debug and test tools.
	const TCHAR* const BriefCommands[] =
	{
		TEXT("RF_SpawnZombies"),		// spawn N zombies at cursor
		TEXT("RF_SpawnBanditGroup"),	// spawn bandit group
		TEXT("RF_SetTime"),				// set time
		TEXT("RF_SetWeather"),			// set weather
		TEXT("RF_GiveItem"),			// give item
		TEXT("RF_SetInfectionHours"),	// set infection hours
		TEXT("RF_God"),					// god mode
		TEXT("RF_ShowNoiseRadii"),		// show noise radii
		TEXT("RF_ShowAIStates"),		// show AI states
		TEXT("RF_ShowStructureHP"),		// show structure HP
	};

	for (const TCHAR* Name : BriefCommands)
	{
		TestNotNull(*FString::Printf(TEXT("Command table has %s"), Name), RFDebugCommands::Find(FName(Name)));
	}

	const UClass* CheatClass = URFCheatManager::StaticClass();
	for (const FRFDebugCommandInfo& Command : RFDebugCommands::GetAll())
	{
		const UFunction* Function = CheatClass->FindFunctionByName(FName(Command.Name));
		if (TestNotNull(*FString::Printf(TEXT("URFCheatManager has a function %s"), Command.Name), Function))
		{
			TestTrue(*FString::Printf(TEXT("%s is UFUNCTION(Exec)"), Command.Name), Function->HasAnyFunctionFlags(FUNC_Exec));
		}

		TestTrue(*FString::Printf(TEXT("%s names a milestone"), Command.Name),
			Command.Milestone != nullptr && FCString::Strlen(Command.Milestone) > 0);

		if (Command.Status == ERFDebugCommandStatus::FlagOnly)
		{
			TestNotNull(*FString::Printf(TEXT("%s (flag only) names an rf.* flag"), Command.Name), Command.CVarName);
		}

		if (Command.CVarName != nullptr)
		{
			TestNotNull(*FString::Printf(TEXT("Console variable %s is registered"), Command.CVarName),
				IConsoleManager::Get().FindConsoleVariable(Command.CVarName));
		}
	}

	// Toggling a flag flips it and toggling again restores it.
	const bool bBefore = RFDebug::GetFlag(RFDebug::CVarShowNoiseRadii);
	TestTrue(TEXT("ToggleFlag flips rf.ShowNoiseRadii"), RFDebug::ToggleFlag(RFDebug::CVarShowNoiseRadii) == !bBefore);
	TestTrue(TEXT("ToggleFlag restores rf.ShowNoiseRadii"), RFDebug::ToggleFlag(RFDebug::CVarShowNoiseRadii) == bBefore);
	TestTrue(TEXT("ShouldShowNoiseRadii matches the flag"), RFDebug::ShouldShowNoiseRadii() == bBefore);

	return true;
}

// ---------------------------------------------------------------------------------------------
// RF.Setup.TestMap: the empty test map exists (made by Scripts/create_test_map.py) and is the
// game default map. EditorStartupMap is set next to it in DefaultEngine.ini.
// Fails until create_test_map.py has been run on the PC; that is intended.
// ---------------------------------------------------------------------------------------------
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FRFTestMapTest, "RF.Setup.TestMap", RF_SETUP_TEST_FLAGS)

bool FRFTestMapTest::RunTest(const FString& Parameters)
{
	const FString MapPackage = TEXT("/Game/RF/Maps/L_Test_Empty");

	TestTrue(TEXT("/Game/RF/Maps/L_Test_Empty exists (run Scripts/create_test_map.py)"), FPackageName::DoesPackageExist(MapPackage));

	// GetGameDefaultMap() returns the package name in UE5; strip an object suffix in case it does not.
	FString DefaultMap = UGameMapsSettings::GetGameDefaultMap();
	int32 DotIndex = INDEX_NONE;
	if (DefaultMap.FindChar(TEXT('.'), DotIndex))
	{
		DefaultMap = DefaultMap.Left(DotIndex);
	}
	TestEqual(TEXT("GameDefaultMap is L_Test_Empty"), DefaultMap, MapPackage);

	return true;
}

#undef RF_SETUP_TEST_FLAGS

#endif // WITH_DEV_AUTOMATION_TESTS
