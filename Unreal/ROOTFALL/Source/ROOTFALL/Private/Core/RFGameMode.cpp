// ROOTFALL default game mode.

#include "Core/RFGameMode.h"

#include "Core/RFLog.h"
#include "Core/RFPlayerController.h"

ARFGameMode::ARFGameMode()
{
	PlayerControllerClass = ARFPlayerController::StaticClass();
	// DefaultPawnClass stays the AGameModeBase default (ADefaultPawn) until ARFCharacter exists (M1).
}

void ARFGameMode::StartPlay()
{
	Super::StartPlay();

	UE_LOG(LogRF, Display, TEXT("ROOTFALL game mode started. Type RF_Help in the console for debug commands."));
}
