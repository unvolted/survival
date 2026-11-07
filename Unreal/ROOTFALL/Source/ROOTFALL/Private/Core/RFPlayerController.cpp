// ROOTFALL player controller.

#include "Core/RFPlayerController.h"

#include "Debug/RFCheatManager.h"

ARFPlayerController::ARFPlayerController()
{
	CheatClass = URFCheatManager::StaticClass();
}
