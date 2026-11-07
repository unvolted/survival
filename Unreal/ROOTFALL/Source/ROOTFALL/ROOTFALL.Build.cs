// ROOTFALL game module.

using UnrealBuildTool;

public class ROOTFALL : ModuleRules
{
	public ROOTFALL(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		// Used by M0 code (game mode, cheat manager, sandbox settings, automation tests).
		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"DeveloperSettings",
		});

		PrivateDependencyModuleNames.AddRange(new string[]
		{
			"EngineSettings", // UGameMapsSettings, read by the RF.Setup.TestMap automation test
		});

		// Modules from the engine features the brief requires. Nothing in M0 includes them yet;
		// they are declared now so the M0 build already proves every plugin is enabled and links.
		PrivateDependencyModuleNames.AddRange(new string[]
		{
			"GameplayTags",             // M1+: item, surface and moodle tags
			"AIModule",                 // M3: zombie / bandit controllers, perception
			"NavigationSystem",         // M3: zombie pathing
			"StateTreeModule",          // M3: zombie and bandit StateTrees (StateTree plugin)
			"GameplayStateTreeModule",  // M3: StateTree AI component (GameplayStateTree plugin)
			"UMG",                      // M2: HUD widgets (moodle stack, health panel)
			"Slate",
			"SlateCore",
			"CommonUI",                 // M2: HUD layers and menus (CommonUI plugin)
			"CommonInput",              // M2: input routing for CommonUI (CommonUI plugin)
			"PCG",                      // M7: forest, foliage and overgrowth scatter (PCG plugin)
		});
	}
}
