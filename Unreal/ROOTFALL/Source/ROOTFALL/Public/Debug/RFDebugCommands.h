// ROOTFALL debug command table: one entry per debug command the brief asks for.

#pragma once

#include "CoreMinimal.h"

/** How far a debug command works in the current build. */
enum class ERFDebugCommandStatus : uint8
{
	/** Fully working. */
	Implemented,
	/** Sets its rf.* flag now; the system that reads the flag arrives in the listed milestone. */
	FlagOnly,
	/** Logs "not implemented until M#" and does nothing else. */
	NotImplemented,
};

/** One debug command. Name must match a UFUNCTION(Exec) on URFCheatManager (checked by RF.Setup.DebugCommands). */
struct FRFDebugCommandInfo
{
	/** Console name, for example RF_SpawnZombies. */
	const TCHAR* Name;
	/** Usage line shown by RF_Help. */
	const TCHAR* Usage;
	/** What the command does (the brief's wording). */
	const TCHAR* Description;
	/** Milestone in which the command becomes fully working, for example TEXT("M3"). */
	const TCHAR* Milestone;
	/** Status in the current build. Update it when the command is implemented. */
	ERFDebugCommandStatus Status;
	/** rf.* console variable the command toggles, or nullptr. */
	const TCHAR* CVarName;
};

namespace RFDebugCommands
{
	/** Every RF_* debug command, in the order RF_Help lists them. */
	ROOTFALL_API const TArray<FRFDebugCommandInfo>& GetAll();

	/** The table entry for a command, or nullptr. */
	ROOTFALL_API const FRFDebugCommandInfo* Find(FName CommandName);

	ROOTFALL_API const TCHAR* StatusToString(ERFDebugCommandStatus Status);
}
