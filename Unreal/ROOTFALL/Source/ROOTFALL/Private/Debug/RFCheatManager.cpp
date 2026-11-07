// ROOTFALL debug console commands (RF_*).

#include "Debug/RFCheatManager.h"

#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "Core/RFLog.h"
#include "Debug/RFDebugCommands.h"
#include "Debug/RFDebugCVars.h"

// Note on arguments: missing console arguments arrive as 0 / None, so every command treats
// 0 / None as "use the default".

void URFCheatManager::RF_Help()
{
	Say(TEXT("ROOTFALL debug commands (status in this build):"));
	for (const FRFDebugCommandInfo& Command : RFDebugCommands::GetAll())
	{
		FString Line = FString::Printf(TEXT("  %-20s [%s, %s] %s"),
			Command.Name,
			RFDebugCommands::StatusToString(Command.Status),
			Command.Milestone,
			Command.Description);
		if (Command.CVarName != nullptr)
		{
			Line += FString::Printf(TEXT(" (%s = %d)"), Command.CVarName, RFDebug::GetFlag(Command.CVarName) ? 1 : 0);
		}
		Say(Line);
		Say(FString::Printf(TEXT("      usage: %s"), Command.Usage));
	}
}

void URFCheatManager::RF_SpawnZombies(int32 Count, FName Variant)
{
	const int32 SafeCount = Count > 0 ? Count : 1;
	const FString VariantName = Variant.IsNone() ? FString(TEXT("Civilian")) : Variant.ToString();
	ReportNotImplemented(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_SpawnZombies),
		FString::Printf(TEXT("Count=%d Variant=%s"), SafeCount, *VariantName));
}

void URFCheatManager::RF_SpawnBanditGroup(int32 GroupSize)
{
	const int32 SafeSize = GroupSize > 0 ? FMath::Clamp(GroupSize, 2, 4) : 3;
	ReportNotImplemented(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_SpawnBanditGroup),
		FString::Printf(TEXT("Size=%d"), SafeSize));
}

void URFCheatManager::RF_SetTime(float Hour)
{
	const float SafeHour = FMath::Clamp(Hour, 0.f, 24.f);
	ReportNotImplemented(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_SetTime),
		FString::Printf(TEXT("Hour=%.2f"), SafeHour));
}

void URFCheatManager::RF_SetWeather(FName Weather)
{
	ReportNotImplemented(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_SetWeather),
		FString::Printf(TEXT("Weather=%s"), *Weather.ToString()));
}

void URFCheatManager::RF_GiveItem(FName ItemId, int32 Count)
{
	const int32 SafeCount = Count > 0 ? Count : 1;
	ReportNotImplemented(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_GiveItem),
		FString::Printf(TEXT("ItemId=%s Count=%d"), *ItemId.ToString(), SafeCount));
}

void URFCheatManager::RF_SetInfectionHours(float HoursSinceBite)
{
	const float SafeHours = FMath::Max(HoursSinceBite, 0.f);
	ReportNotImplemented(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_SetInfectionHours),
		FString::Printf(TEXT("HoursSinceBite=%.2f"), SafeHours));
}

void URFCheatManager::RF_God()
{
	const bool bGodMode = ToggleCommandFlag(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_God));

	// Until RF damage exists (M2), also block engine damage on the current pawn.
	if (const APlayerController* PlayerController = Cast<APlayerController>(GetOuter()))
	{
		if (APawn* Pawn = PlayerController->GetPawn())
		{
			Pawn->SetCanBeDamaged(!bGodMode);
		}
	}
}

void URFCheatManager::RF_ShowNoiseRadii()
{
	ToggleCommandFlag(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_ShowNoiseRadii));
}

void URFCheatManager::RF_ShowAIStates()
{
	ToggleCommandFlag(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_ShowAIStates));
}

void URFCheatManager::RF_ShowStructureHP()
{
	ToggleCommandFlag(GET_FUNCTION_NAME_CHECKED(URFCheatManager, RF_ShowStructureHP));
}

void URFCheatManager::Say(const FString& Message) const
{
	UE_LOG(LogRFDebug, Display, TEXT("%s"), *Message);

	if (APlayerController* PlayerController = Cast<APlayerController>(GetOuter()))
	{
		PlayerController->ClientMessage(Message);
	}
}

void URFCheatManager::ReportNotImplemented(FName Command, const FString& Arguments) const
{
	const FRFDebugCommandInfo* Info = RFDebugCommands::Find(Command);
	const TCHAR* Milestone = Info ? Info->Milestone : TEXT("a later milestone");
	Say(FString::Printf(TEXT("%s %s: not implemented until %s."), *Command.ToString(), *Arguments, Milestone));
}

bool URFCheatManager::ToggleCommandFlag(FName Command) const
{
	const FRFDebugCommandInfo* Info = RFDebugCommands::Find(Command);
	if (Info == nullptr || Info->CVarName == nullptr)
	{
		UE_LOG(LogRFDebug, Error, TEXT("%s has no rf.* flag in the debug command table."), *Command.ToString());
		return false;
	}

	const bool bNewValue = RFDebug::ToggleFlag(Info->CVarName);
	FString Message = FString::Printf(TEXT("%s = %d"), Info->CVarName, bNewValue ? 1 : 0);
	if (Info->Status != ERFDebugCommandStatus::Implemented)
	{
		Message += FString::Printf(TEXT(" (flag only: the system that reads it arrives in %s)"), Info->Milestone);
	}
	Say(Message);
	return bNewValue;
}
