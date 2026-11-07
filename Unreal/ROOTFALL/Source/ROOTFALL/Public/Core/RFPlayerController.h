// ROOTFALL player controller.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "RFPlayerController.generated.h"

/**
 * ROOTFALL player controller.
 *
 * M0: only installs URFCheatManager as the cheat class, so the RF_* debug commands work in
 * Play-In-Editor and in non-shipping standalone builds. Enhanced Input mapping contexts are added
 * here in M1.
 */
UCLASS()
class ROOTFALL_API ARFPlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	ARFPlayerController();
};
