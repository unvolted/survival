// ROOTFALL debug console commands (RF_*).

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/CheatManager.h"
#include "RFCheatManager.generated.h"

/**
 * ROOTFALL debug console commands. Installed by ARFPlayerController (CheatClass), so the commands
 * work in Play-In-Editor and in non-shipping standalone builds. Type RF_Help in the console for
 * the list and the status of each command.
 *
 * Every command has an entry in RFDebugCommands::GetAll() (name, usage, milestone, status).
 * Commands whose system does not exist yet log "not implemented until M#".
 * The Show* commands toggle the rf.* flags in RFDebugCVars.h, which the systems read.
 */
UCLASS()
class ROOTFALL_API URFCheatManager : public UCheatManager
{
	GENERATED_BODY()

public:
	/** List every RF_* command with its usage and status. */
	UFUNCTION(Exec)
	void RF_Help();

	/** Spawn Count zombies of a variant at the crosshair trace hit. (M3) */
	UFUNCTION(Exec)
	void RF_SpawnZombies(int32 Count, FName Variant);

	/** Spawn a bandit group of GroupSize (2 to 4) near the crosshair. (M6) */
	UFUNCTION(Exec)
	void RF_SpawnBanditGroup(int32 GroupSize);

	/** Set the in-game time of day, 0 to 24 hours. (M2) */
	UFUNCTION(Exec)
	void RF_SetTime(float Hour);

	/** Set the weather: Clear, Overcast, Rain, Storm or Fog. (M7) */
	UFUNCTION(Exec)
	void RF_SetWeather(FName Weather);

	/** Give the player Count of an item from the item Data Table. (M5) */
	UFUNCTION(Exec)
	void RF_GiveItem(FName ItemId, int32 Count);

	/** Bite the player if needed and set the bite time so HoursSinceBite in-game hours have passed. (M2) */
	UFUNCTION(Exec)
	void RF_SetInfectionHours(float HoursSinceBite);

	/** Toggle rf.GodMode. The flag works now; the systems that honour it arrive in M2. */
	UFUNCTION(Exec)
	void RF_God();

	/** Toggle rf.ShowNoiseRadii. Drawing arrives in M1. */
	UFUNCTION(Exec)
	void RF_ShowNoiseRadii();

	/** Toggle rf.ShowAIStates. Drawing arrives in M3. */
	UFUNCTION(Exec)
	void RF_ShowAIStates();

	/** Toggle rf.ShowStructureHP. Drawing arrives in M4. */
	UFUNCTION(Exec)
	void RF_ShowStructureHP();

private:
	/** Writes a line to the log and to the player's console. */
	void Say(const FString& Message) const;

	/** Logs "<Command> <Arguments>: not implemented until M#." using the command table. */
	void ReportNotImplemented(FName Command, const FString& Arguments) const;

	/** Flips the rf.* flag a command owns and reports the new value. Returns the new value. */
	bool ToggleCommandFlag(FName Command) const;
};
