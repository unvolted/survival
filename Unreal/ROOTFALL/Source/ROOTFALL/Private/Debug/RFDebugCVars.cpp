// ROOTFALL debug flags as console variables (rf.*).

#include "Debug/RFDebugCVars.h"

#include "HAL/IConsoleManager.h"
#include "Core/RFLog.h"

namespace
{
	TAutoConsoleVariable<bool> CVarRFGodMode(
		RFDebug::CVarGodMode,
		false,
		TEXT("ROOTFALL: god mode. No damage, no needs drain, no infection progress. Read by the survival systems from M2 on."),
		ECVF_Cheat);

	TAutoConsoleVariable<bool> CVarRFShowNoiseRadii(
		RFDebug::CVarShowNoiseRadii,
		false,
		TEXT("ROOTFALL: draw noise event radii. Drawing arrives with footstep noise in M1."),
		ECVF_Cheat);

	TAutoConsoleVariable<bool> CVarRFShowAIStates(
		RFDebug::CVarShowAIStates,
		false,
		TEXT("ROOTFALL: draw each AI's state (Dormant, Wander, Investigate, Chase, Attack, Lost). Drawing arrives in M3."),
		ECVF_Cheat);

	TAutoConsoleVariable<bool> CVarRFShowStructureHP(
		RFDebug::CVarShowStructureHP,
		false,
		TEXT("ROOTFALL: draw HP and damage state of buildable pieces. Drawing arrives in M4."),
		ECVF_Cheat);
}

bool RFDebug::IsGodModeEnabled()
{
	return CVarRFGodMode.GetValueOnGameThread();
}

bool RFDebug::ShouldShowNoiseRadii()
{
	return CVarRFShowNoiseRadii.GetValueOnGameThread();
}

bool RFDebug::ShouldShowAIStates()
{
	return CVarRFShowAIStates.GetValueOnGameThread();
}

bool RFDebug::ShouldShowStructureHP()
{
	return CVarRFShowStructureHP.GetValueOnGameThread();
}

bool RFDebug::GetFlag(const TCHAR* CVarName)
{
	if (IConsoleVariable* Var = IConsoleManager::Get().FindConsoleVariable(CVarName))
	{
		return Var->GetBool();
	}
	return false;
}

bool RFDebug::ToggleFlag(const TCHAR* CVarName)
{
	IConsoleVariable* Var = IConsoleManager::Get().FindConsoleVariable(CVarName);
	if (!Var)
	{
		UE_LOG(LogRFDebug, Error, TEXT("ToggleFlag: no console variable named %s."), CVarName);
		return false;
	}

	const bool bNewValue = !Var->GetBool();
	// SetByConsole so the toggle wins over values set earlier from code or ini.
	Var->Set(bNewValue, ECVF_SetByConsole);
	return Var->GetBool();
}
