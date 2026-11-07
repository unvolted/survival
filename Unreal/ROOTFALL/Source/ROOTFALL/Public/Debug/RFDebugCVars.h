// ROOTFALL debug flags as console variables (rf.*).

#pragma once

#include "CoreMinimal.h"

/**
 * Debug flags as console variables, so they can be set from the console ("rf.ShowNoiseRadii 1"),
 * from the RF_* cheat commands (which toggle them), or from an ini [ConsoleVariables] section.
 *
 * Gameplay systems read the flags through the functions below, never through the cheat manager,
 * so they keep working when the cheat manager is compiled out of Shipping builds.
 * All of them are ECVF_Cheat: read-only from the console in Shipping.
 */
namespace RFDebug
{
	/** No damage, no needs drain, no infection progress. Read by stats, body health and infection (M2). */
	inline constexpr const TCHAR* CVarGodMode = TEXT("rf.GodMode");

	/** Draws noise event radii. Drawn by URFNoiseSubsystem (footstep noise, M1). */
	inline constexpr const TCHAR* CVarShowNoiseRadii = TEXT("rf.ShowNoiseRadii");

	/** Draws each AI's StateTree state above its head (zombies M3, bandits M6). */
	inline constexpr const TCHAR* CVarShowAIStates = TEXT("rf.ShowAIStates");

	/** Draws HP and damage state above each buildable piece (M4). */
	inline constexpr const TCHAR* CVarShowStructureHP = TEXT("rf.ShowStructureHP");

	ROOTFALL_API bool IsGodModeEnabled();
	ROOTFALL_API bool ShouldShowNoiseRadii();
	ROOTFALL_API bool ShouldShowAIStates();
	ROOTFALL_API bool ShouldShowStructureHP();

	/** Returns the value of a boolean rf.* flag, or false if no such console variable exists. */
	ROOTFALL_API bool GetFlag(const TCHAR* CVarName);

	/** Flips a boolean rf.* flag and returns its new value (false if no such console variable exists). */
	ROOTFALL_API bool ToggleFlag(const TCHAR* CVarName);
}
