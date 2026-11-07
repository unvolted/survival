// ROOTFALL editor target. Build this one ("ROOTFALLEditor") to open the project in the editor.

using UnrealBuildTool;
using System.Collections.Generic;

public class ROOTFALLEditorTarget : TargetRules
{
	public ROOTFALLEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("ROOTFALL");
	}
}
