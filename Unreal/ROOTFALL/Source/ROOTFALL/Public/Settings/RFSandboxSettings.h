// ROOTFALL sandbox settings: every sandbox option from the brief in one place.

#pragma once

#include "CoreMinimal.h"
#include "Engine/DeveloperSettings.h"
#include "RFSandboxSettings.generated.h"

/** Which wounds can carry the zombie infection (brief: Realism systems > Zombie infection). */
UENUM(BlueprintType)
enum class ERFInfectionRule : uint8
{
	/** Only bites infect (default). */
	BiteOnly		UMETA(DisplayName = "Bite only"),
	/** Bites always infect; scratches and lacerations have a hidden chance to infect. */
	ZomboidRules	UMETA(DisplayName = "Zomboid rules"),
};

/**
 * Project defaults for the sandbox options (Project Settings > Game > ROOTFALL Sandbox,
 * stored in Config/DefaultGame.ini under [/Script/ROOTFALL.RFSandboxSettings]).
 *
 * The brief's URFSandboxSettings is "Data Asset + save": these are the defaults a new world starts
 * from. The per-world copy that is written into the save game arrives with URFSaveSubsystem (M5).
 */
UCLASS(Config = Game, DefaultConfig, meta = (DisplayName = "ROOTFALL Sandbox"))
class ROOTFALL_API URFSandboxSettings : public UDeveloperSettings
{
	GENERATED_BODY()

public:
	/** Shortcut for the project defaults (the class default object). */
	static const URFSandboxSettings& Get();

	//~ UDeveloperSettings
	virtual FName GetCategoryName() const override;
	virtual FName GetSectionName() const override;
	//~ End UDeveloperSettings

	/**
	 * Version of the settings layout. The code default is 0; DefaultGame.ini sets 1. The
	 * RF.Setup.SandboxSettingsDefaults test uses this to prove the ini section is being read.
	 */
	UPROPERTY(Config, VisibleAnywhere, BlueprintReadOnly, Category = "Meta")
	int32 SettingsVersion = 0;

	// ---- Time -------------------------------------------------------------------------------

	/** Real minutes per in-game day. Brief: default 60, range 30 to 180. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Time", meta = (ClampMin = "30", ClampMax = "180"))
	float DayLengthMinutes = 60.f;

	// ---- Zombies ----------------------------------------------------------------------------

	/** Scales the zombie density of every zone (town high, forest low). */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Zombies", meta = (ClampMin = "0.0", ClampMax = "4.0"))
	float ZombiePopulationMultiplier = 1.f;

	/** Cap on zombies simulated as full actors near the player (brief target: 150 to 300). */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Zombies", meta = (ClampMin = "0", ClampMax = "1000"))
	int32 MaxActiveZombies = 300;

	/** Scales zombie movement speed. 1.0 = shamblers at about 1.2 m/s with a 2 to 3 m lunge. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Zombies", meta = (ClampMin = "0.5", ClampMax = "3.0"))
	float ZombieSpeedMultiplier = 1.f;

	/** Scales zombie toughness (head trauma needed to kill, body damage to stagger). */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Zombies", meta = (ClampMin = "0.25", ClampMax = "4.0"))
	float ZombieToughnessMultiplier = 1.f;

	/** Whether zombies slowly respawn into areas the player has not visited. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Zombies")
	bool bZombieRespawn = true;

	/** In-game days an area must go unvisited before zombies respawn there (the brief's "N days"). */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Zombies", meta = (ClampMin = "0.5", ClampMax = "60.0", EditCondition = "bZombieRespawn"))
	float ZombieRespawnUnvisitedDays = 3.f;

	// ---- Infection --------------------------------------------------------------------------

	/** Which wounds can infect. Brief default: Bite only. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Infection")
	ERFInfectionRule InfectionRule = ERFInfectionRule::BiteOnly;

	/** In-game hours from bite to death. Brief: default 48, range 24 to 96. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Infection", meta = (ClampMin = "24", ClampMax = "96"))
	float InfectionHoursToDeath = 48.f;

	/** Chance a scratch infects under Zomboid rules. Brief: 7%. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Infection", meta = (ClampMin = "0.0", ClampMax = "1.0", EditCondition = "InfectionRule == ERFInfectionRule::ZomboidRules"))
	float ScratchInfectionChance = 0.07f;

	/** Chance a laceration infects under Zomboid rules. Brief: 25%. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Infection", meta = (ClampMin = "0.0", ClampMax = "1.0", EditCondition = "InfectionRule == ERFInfectionRule::ZomboidRules"))
	float LacerationInfectionChance = 0.25f;

	// ---- Loot -------------------------------------------------------------------------------

	/** Scales how much loot containers hold. Below 1 = rarer loot. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Loot", meta = (ClampMin = "0.0", ClampMax = "4.0"))
	float LootAbundanceMultiplier = 1.f;

	// ---- Bandits ----------------------------------------------------------------------------

	/** Most bandit groups active on the map at once. Brief: 0 to 2. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "Bandits", meta = (ClampMin = "0", ClampMax = "2"))
	int32 MaxActiveBanditGroups = 2;

	// ---- World ------------------------------------------------------------------------------

	/** Whether felled trees slowly regrow from their stumps. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "World")
	bool bTreesRegrow = true;

	/** In-game days for a felled tree to regrow. */
	UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category = "World", meta = (ClampMin = "1.0", ClampMax = "120.0", EditCondition = "bTreesRegrow"))
	float TreeRegrowDays = 14.f;
};
