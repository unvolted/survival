# ROOTFALL — project rules

ROOTFALL is a first-person survival game in **Unreal Engine 5.8**. The full spec is
[`Design/ROOTFALL_Brief.md`](Design/ROOTFALL_Brief.md): shared brief, world, core systems, realism systems,
enemies, the three agent prompts, the handoff contract and the milestones. It is the source of truth.
These rules say how to apply it in this repo.

## RULE: Three-agent pipeline (always use this)

All game content is made by **three subagents** in `.claude/agents/`. Never do a stage's job yourself.
Hand the work to the agent that owns it.

| Agent | Brief section | Makes | From |
|-------|---------------|-------|------|
| `concept-artist` | Agent 1 | concept images (`Concept/`) | the info in `Design/` |
| `modeler` | Agent 2 | Blender models, FBX, textures (`Source/Blender/`, `Export/`) | the concept images |
| `game-builder` | Agent 3 | the UE 5.8 project (`Unreal/ROOTFALL/`) | the exported models + the info |

**Data flow is fixed:** every final model is built from its concept images, and the game uses those final
models. **Timing overlaps** (brief, "How to use this prompt"):
- The three agents can run at the same time. The asset manifest connects them.
- `modeler` starts with the **greybox kit** (plain blocks at the brief's dimensions) right away. Final models
  wait for their concept sheet: a final model never starts before its manifest row says `Concept Done`.
- `game-builder` builds every system on greybox and the UE5 Mannequin, and swaps in final assets when their row
  reaches `Exported`. Systems never depend on a specific mesh.
- An asset whose look changes goes back to `concept-artist` first.

### Running the agents
1. Give every agent the brief path and its own section. The agent files already say which sections to read.
2. First run (brief step 3): `concept-artist` on the style guide, the player-built structures sheet and the ruin kit
   sheet; `modeler` on the greybox kit; `game-builder` on M0 → M3 in order.
3. Read each agent's report in `Reports/` and check `Manifest/asset_manifest.csv` before approving the next
   milestone. Tell the user what passed, what is blocked and what was assumed.

## Handoff contract (summary; the brief has the full version)

```
Design/            the brief (input)                     Export/FBX/        meshes + animations (modeler)
Concept/           CA_ images + StyleGuide.md (artist)   Export/Textures/   texture sets (modeler)
Source/Blender/    .blend files + build scripts (modeler) Unreal/ROOTFALL/  the UE 5.8 project (game-builder)
Manifest/asset_manifest.csv  one row per asset           Reports/           one report per agent per task
Tools/             shared helper scripts
```
- Prefixes `CA_ SM_ SK_ SKEL_ A_ T_ M_ MI_ BP_ ABP_ DA_ DT_ WBP_ SFX_ MS_ UCX_ SOCKET_`, PascalCase with
  underscores, tiers `T1/T2/T3`, states `_Intact/_Damaged/_Broken`. **A misnamed file is a bug.**
- Manifest status: `Planned, Concept Done, Greybox, Modeled, Textured, Rigged, Exported, Imported, In Game, Blocked`.
  Whoever changes an asset updates its row. Nothing counts as delivered until its row says so.
- Reports go in `Reports/<YYYY-MM-DD>_<Agent>_<Task>.md` with the headings **Done, Verified, Assumptions,
  Blocked, Next**.
- **Never claim something is done without verifying it.** If it can't be verified, say so.

## Environment facts

- **Images: keep cost low.** The ElevenLabs account is on the free tier. Default to `recraft-v4.1-flash` with
  **one** variation (~48 credits per image). Use `gemini-3.1-flash-lite-image` (~206 credits) only to edit an
  existing image, for example to fix drift between a character's views. Never use 4 variations. Price a batch with
  `estimate_only` first. If generation is "busy", stop and report; do not retry in the same turn. Dimensions,
  callouts and UI icons are drawn by the agent (SVG/Pillow), not generated. See `.claude/agents/concept-artist.md`.
- **Blender 5.2 LTS** runs headless in the cloud container as a Python module:
  `bash Tools/setup_blender.sh` installs it into `~/.venv-blender`, then run `~/.venv-blender/bin/python <script>`.
- **Unreal Engine 5.8 runs only on the user's PC**, attached to the session through Remote Control. Compiling,
  Play-In-Editor, automation tests, imports and Blueprint creation happen there (`_host` on Bash). Code is written
  and committed here, pushed, then pulled on the PC. If the PC is not attached, nothing in Unreal can be verified:
  say so, do not mark it done.
- Binary files go through **Git LFS** (`.gitattributes`). Commit per feature with a clear message.
