// ROOTFALL default game mode.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "RFGameMode.generated.h"

/**
 * Project-wide default game mode (GlobalDefaultGameMode in DefaultEngine.ini).
 *
 * M0: uses ARFPlayerController (which owns URFCheatManager) and the engine's free-fly
 * ADefaultPawn. ARFCharacter replaces the pawn in M1.
 */
UCLASS()
class ROOTFALL_API ARFGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	ARFGameMode();

	virtual void StartPlay() override;
};
