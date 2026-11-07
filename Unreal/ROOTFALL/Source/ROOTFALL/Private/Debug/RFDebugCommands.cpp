// ROOTFALL debug command table.

#include "Debug/RFDebugCommands.h"

#include "Debug/RFDebugCVars.h"

const TArray<FRFDebugCommandInfo>& RFDebugCommands::GetAll()
{
	// Brief, Agent 3 > Debug and test tools: "spawn N zombies at cursor, spawn bandit group, set time,
	// set weather, give item, set infection hours, god mode, show noise radii, show AI states,
	// show structure HP". Milestones follow the brief's milestone list.
	static const TArray<FRFDebugCommandInfo> Commands =
	{
		{ TEXT("RF_Help"),             TEXT("RF_Help"),
		  TEXT("List every RF_* debug command and its status"),
		  TEXT("M0"), ERFDebugCommandStatus::Implemented, nullptr },

		{ TEXT("RF_SpawnZombies"),     TEXT("RF_SpawnZombies <Count> [Variant=Civilian|Soldier|Rotten|Crawler|Bloated]"),
		  TEXT("Spawn N zombies at the cursor (crosshair trace hit)"),
		  TEXT("M3"), ERFDebugCommandStatus::NotImplemented, nullptr },

		{ TEXT("RF_SpawnBanditGroup"), TEXT("RF_SpawnBanditGroup [Size=2..4]"),
		  TEXT("Spawn a bandit group near the cursor"),
		  TEXT("M6"), ERFDebugCommandStatus::NotImplemented, nullptr },

		{ TEXT("RF_SetTime"),          TEXT("RF_SetTime <Hour 0..24>"),
		  TEXT("Set the in-game time of day"),
		  TEXT("M2"), ERFDebugCommandStatus::NotImplemented, nullptr },

		{ TEXT("RF_SetWeather"),       TEXT("RF_SetWeather <Clear|Overcast|Rain|Storm|Fog>"),
		  TEXT("Set the current weather"),
		  TEXT("M7"), ERFDebugCommandStatus::NotImplemented, nullptr },

		{ TEXT("RF_GiveItem"),         TEXT("RF_GiveItem <ItemId> [Count=1]"),
		  TEXT("Add an item from the item Data Table to the player's inventory"),
		  TEXT("M5"), ERFDebugCommandStatus::NotImplemented, nullptr },

		{ TEXT("RF_SetInfectionHours"), TEXT("RF_SetInfectionHours <HoursSinceBite>"),
		  TEXT("Bite the player (if needed) and move the bite time so this many in-game hours have passed"),
		  TEXT("M2"), ERFDebugCommandStatus::NotImplemented, nullptr },

		{ TEXT("RF_God"),              TEXT("RF_God"),
		  TEXT("Toggle god mode (rf.GodMode): no damage, no needs drain, no infection progress"),
		  TEXT("M2"), ERFDebugCommandStatus::FlagOnly, RFDebug::CVarGodMode },

		{ TEXT("RF_ShowNoiseRadii"),   TEXT("RF_ShowNoiseRadii   (or: rf.ShowNoiseRadii 0|1)"),
		  TEXT("Toggle drawing of noise event radii"),
		  TEXT("M1"), ERFDebugCommandStatus::FlagOnly, RFDebug::CVarShowNoiseRadii },

		{ TEXT("RF_ShowAIStates"),     TEXT("RF_ShowAIStates     (or: rf.ShowAIStates 0|1)"),
		  TEXT("Toggle drawing of each AI's current state"),
		  TEXT("M3"), ERFDebugCommandStatus::FlagOnly, RFDebug::CVarShowAIStates },

		{ TEXT("RF_ShowStructureHP"),  TEXT("RF_ShowStructureHP  (or: rf.ShowStructureHP 0|1)"),
		  TEXT("Toggle drawing of buildable piece HP"),
		  TEXT("M4"), ERFDebugCommandStatus::FlagOnly, RFDebug::CVarShowStructureHP },
	};
	return Commands;
}

const FRFDebugCommandInfo* RFDebugCommands::Find(FName CommandName)
{
	for (const FRFDebugCommandInfo& Command : GetAll())
	{
		if (FName(Command.Name) == CommandName)
		{
			return &Command;
		}
	}
	return nullptr;
}

const TCHAR* RFDebugCommands::StatusToString(ERFDebugCommandStatus Status)
{
	switch (Status)
	{
	case ERFDebugCommandStatus::Implemented:	return TEXT("works");
	case ERFDebugCommandStatus::FlagOnly:		return TEXT("flag only");
	case ERFDebugCommandStatus::NotImplemented:	return TEXT("not implemented");
	}
	return TEXT("unknown");
}
