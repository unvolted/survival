// ROOTFALL sandbox settings.

#include "Settings/RFSandboxSettings.h"

const URFSandboxSettings& URFSandboxSettings::Get()
{
	return *GetDefault<URFSandboxSettings>();
}

FName URFSandboxSettings::GetCategoryName() const
{
	return FName(TEXT("Game"));
}

FName URFSandboxSettings::GetSectionName() const
{
	// Identifier only; the name shown in Project Settings comes from the class DisplayName.
	return FName(TEXT("ROOTFALLSandbox"));
}
