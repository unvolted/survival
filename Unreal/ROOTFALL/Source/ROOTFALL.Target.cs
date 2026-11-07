// ROOTFALL game target (packaged game / -game runs).

using UnrealBuildTool;
using System.Collections.Generic;

public class ROOTFALLTarget : TargetRules
{
	public ROOTFALLTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("ROOTFALL");
	}
}
