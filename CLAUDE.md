# Survival — project rules

## RULE: Three-agent asset pipeline (always use this)

All game content in this repo is produced by **three specialised subagents, run in order**.
Each stage builds on the previous stage's output. Do not skip a stage or do one stage's job yourself:
whenever work needs new or changed art, models or gameplay, hand it to these agents in this order.

```
design/  (game info)
   │
   ▼
1. concept-artist   → generates reference images from the info
   │                   writes: assets/concepts/<asset>/
   ▼
2. modeler          → builds 3D models using those images as reference
   │                   writes: assets/models/<asset>/
   ▼
3. game-builder     → builds the game from the models + the info
                       writes: game/
```

| Stage | Agent (`.claude/agents/`) | Reads | Writes |
|-------|---------------------------|-------|--------|
| 1 | `concept-artist` | `design/` | `assets/concepts/<asset>/` (images + `brief.md`) |
| 2 | `modeler` | `assets/concepts/<asset>/`, `design/` | `assets/models/<asset>/` (`.glb`/model code + `model.md`) |
| 3 | `game-builder` | `assets/models/`, `design/` | `game/` |

### How to run it

1. Make sure the game info exists in `design/` (write or update it with the user first if it is missing).
2. Run `concept-artist` and wait for it to finish. Check `assets/concepts/<asset>/` has images.
3. Run `modeler` on those concepts and wait for it to finish. Check `assets/models/<asset>/` has a model.
4. Run `game-builder` with the models and the info.
5. Independent assets can go through stages 1–2 in parallel, but each asset must finish
   stage 1 before its stage 2 starts, and all needed models must exist before stage 3.
6. A small fix to existing game code that needs no new art or models can go straight to
   `game-builder`. A change to an asset's look starts again at stage 1 for that asset.

### Hand-off contract

- **Asset names** are lowercase kebab-case (`stone-axe`, `wolf`, `campfire`) and stay the same
  in all three folders.
- `assets/concepts/<asset>/brief.md`: what the asset is, the prompt used, the views generated, and
  which image is the main reference.
- `assets/models/<asset>/model.md`: file name and format, scale (1 unit = 1 metre), origin/pivot,
  forward axis (−Z), polygon/part count, and which concept images it follows.
- If a stage cannot finish (no image credits, a missing reference), it says so in its notes file and
  reports back. The next stage does not start on a missing input.
