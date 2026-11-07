# ConceptArtist — First batch (style guide, player-built structures, ruin kit)

Brief step 3: the style guide, player-built structures and ruin kit sheets that unblock Agents 2 and 3.

## Done

All in `Concept/`. Each sheet is 4096 px wide, PNG, sRGB (embedded ICC), with a 100 cm grid and cm dimensions where the brief asks:

| File | Contents |
|---|---|
| `CA_StyleGuide_Sheet.png` | Palette of 28 swatches (hex, use, HSV saturation); 5 drawn lighting-mood colour keys (dawn, noon, overcast, rain, night + firelight); 7 material swatches; overgrowth rules with a numbered diagram and a coverage table; 5 do / 5 don't thumbnails |
| `StyleGuide.md` | Written page: palette, lighting moods, material language, overgrowth rules, do / don't |
| `CA_Buildables_Walls_Sheet.png` | Log wall T1/T2/T3 (front elevation + end section), spike set T1/T2/T3 (front + side section at 20°), metal plate kit + 2 cm offset section detail, `SM_Build_Log` mesh, Intact / Damaged / Broken states, painted reference G01 (+ G03 crop) |
| `CA_Buildables_GateTower_Sheet.png` | Barricaded door/window T1/T2/T3, gate T1/T2/T3 (T3 = welded gate) with plan swing arcs, watchtower T1/T2/T3 + deck plan |
| `CA_Buildables_Traps_Sheet.png` | Spike pit (section + plan), barbed wire fence, noise trap, tripwire alarm, deadfall, snare, burn trench + fire ring (unlit / burning / burnt), each T1/T2/T3 |
| `CA_Buildables_Ghost_Sheet.png` | Ghost/blueprint look: piece-by-piece fill, next-slot pulse, snap points, in-world material strip, invalid state, plating ghost, daytime readability, material spec, free-form drag |
| `CA_RuinKit_Walls_Sheet.png` | Wall 400 / 200 / 100, Window_400, Door_400, Corner pillar, each Intact / Damaged / Overgrown; plan (grid, thickness, corner), section (storey stacking), separate meshes; painted reference G02 |
| `CA_RuinKit_FloorsRoofsStairs_Sheet.png` | Floor tile, roof slope, stairs, collapsed wall, collapsed floor, collapsed roof, rubble piles, each in 3 states |
| `_raw/G01_Buildables_Walls.png`, `_raw/G02_RuinKit_Walls.png`, `_raw/G03_Buildables_SpikeGateBarricade.png` | Raw generations kept for provenance |

Build scripts are in `Tools/concept/`: `sheetlib.py` (palette and drawing library), `build_styleguide.py`, `build_buildables.py`,
`build_ruinkit.py` and `build_all.py`. Running `python3 Tools/concept/build_all.py` rebuilds every sheet in about 25 s.

`Manifest/asset_manifest.csv` has 58 rows added, all owner `Agent 1`; Agent 2's rows were not touched:
- 7 sheet rows: `Concept Done`.
- 3 painted-reference rows: `Blocked`.
- 32 buildable and ruin rows: `Concept Done`. These are 24 T2/T3 tier rows, Tripwire T1–T3, the plate kit, the door leaf, and the collapsed floor, collapsed roof and second rubble pile.
- 1 `Planned` ruin row (gable end and ridge).
- 15 `Planned` rows for the remaining brief deliverables: environment keys, characters, props, foliage and UI.

### Image generation and credits

All generations used `recraft-v4.1-flash` with `generations_count: 1`, on 3 ElevenLabs flows (`ROOTFALL_CA_StyleGuide`,
`ROOTFALL_CA_RuinKit`, and one for buildables, `fCARBeArcomT72asmv1R`). An estimate call priced each image at 48.48 credits.

| # | Result | Prompt |
|---|---|---|
| G01 | OK, 48 credits | Game concept art of three defensive log wall segments side by side, orthographic front elevation, each wall ten thick horizontal logs stacked, rough axe-cut ends. Left: raw bark logs #4A3A2C with pale fresh-cut ends #C9A26B. Middle: same log wall reinforced with weathered nailed planks #8A7C66. Right: same log wall with rusty scrap steel sheets #6F7578 and #9C4F26 welded on, visible weld beads. Muted desaturated colours, flat neutral grey background, even lighting, no text. |
| G02 | OK, 48 credits | Game concept art sheet of modular ruined house wall panels, orthographic front elevations in a grid of four columns and three rows: plain wall, wall with window opening, wall with door opening, outside corner piece. Top row intact plastered brick and wet concrete #5D6163. Middle row war-damaged: shell holes, bullet pocking, scorch marks, exposed brick and rebar #9C4F26. Bottom row overgrown with ivy #3F5236 and moss #5B6B47 climbing from the base. Flat neutral grey background, even lighting, no text. |
| G03 | OK, 48 credits | Game concept art of survival base fortifications side by side, orthographic front elevation: a stacked log wall with sharpened wooden stakes angled outward; a heavy welded gate of rusty steel sheets #6F7578 on a square steel frame with large hinges, set between log posts; a ruined brick doorway barricaded with nailed planks #8A7C66; a window covered by a welded rusty metal sheet #9C4F26. Bark #4A3A2C, fresh wood #C9A26B. Flat neutral grey background, even lighting, no text. |
| G04–G08 | Refused: 429 `free_tier_image_limit_reached`, no charge | Traps row, watchtower T1–T3, ruin floors/roofs/stairs/collapsed/rubble, 5-panel lighting-mood strip, 7 material swatches |

**Total: 3 generations, about 145 credits. No edits, no retries.** The 5 refused calls had been sent together before
the first refusal came back, and none was retried after it. Their exact prompts are in this session's flow history for a later run.

## Verified

- Every final PNG was opened with Pillow: 4096 px wide (2200–3340 px tall), RGB, sRGB ICC profile embedded. The raw files are 1344 × 768; they are provenance only and not deliverables.
- Every final sheet was looked at in full with the Read tool after its last change, and again after layout fixes. I fixed overlaps, clipped
  drawings that spilled out of their boxes, wrong crown-stake numbers, out-of-bounds cracks and a mis-drawn collapsed roof.
- Dimensions on the sheets come from the same numbers the drawings use (one constant per value in the scripts), so a drawing
  and its label cannot disagree.
- Brief numbers are checked on the sheets: 30 cm logs, 10 logs = 300 cm, 400 cm max segment, plates 2 cm proud, ruin walls
  400 × 300 × 20, fillers 200 and 100, floor tiles 400 × 400.
- **NOT verified:** that the generated paintings are dimensionally right. They are not, and each painting carries a drift caveat on its sheet.
  Nothing was imported or checked in Unreal; that is not this stage's job.

## Assumptions

The brief does not specify these. Each is the smallest reasonable reading, and each is drawn and labelled on its sheet:

1. **Output location:** `CLAUDE.md` says concept output goes in `assets/concepts/<asset>/` with a `brief.md`. The task, the brief's handoff
   contract and `.claude/agents/concept-artist.md` all say `Concept/CA_*.png`. I followed the task (`Concept/`). `CLAUDE.md` should be updated to match.
2. **Tiers:** T2 = T1 plus planks on the outside face. T3 = T2 plus scrap plates. Metal always sits on existing wood.
3. **Simple traps:** noise trap, tripwire, deadfall, snare and burn trench have T2/T3 variants that are my **proposals** (the brief gives
   only rope, rocks, sticks, string, cans and fuel for them). They are marked "confirm" on the sheet and in the manifest.
4. **Log wall:** logs stacked tangent (no notching). Planks 25 × 4 × 300 at 50/150/250/350. Wall depth is 30 (T1), 34 (T2), 37 (T3).
5. **Plates:** 2 cm proud is read as the plate's back face sitting 2 cm in front of the outermost wood face, on welded tabs.
   Plate kit is 100×150, 100×100 and 50×150, 1 cm thick, one mesh per plate, 8 plates per 400 wall.
6. **Spike set:** a separate add-on mesh. 2 rows × 8 stakes Ø8 × 140 at 20°, plus a crown of 8 stakes; total height 380.
7. **Gate:** posts Ø40; clear opening 320; leaves 160 × 280; 90° inward; T3 has a drop bar.
8. **Watchtower:** 200 × 200 footprint, deck at 400, parapet to 500, ladder through a 60 × 60 hatch.
9. **Ruin openings:** window 100 × 120 with sill at 90; door 100 × 220 (aligned to Agent 2's greybox). Corner is a 30 × 30 × 300 pillar
   on the grid point (also aligned to the greybox). Wall centrelines are on grid lines.
10. **Roof:** rise 200 over 400 (26.6°). Stairs: 15 × 20 rise, 15 × 26.7 tread, 100 wide.
11. **Collapsed pieces and rubble:** their states are Fresh / Weathered / Overgrown, mapped to `_Intact` / `_Damaged` / `_Overgrown`.
12. **Overgrown variants:** shown on the Damaged mesh. Ivy and moss are separate cards and decals, so any state can be overgrown in-engine.
13. **Ghost colour:** bone-white `#E3DED0` rather than a sci-fi cyan, to keep the no-neon rule. Invalid placement is rust `#B5502E`.
14. **Concept image editing:** two crops were processed to fit the palette, and the sheets say so. G03 crops have their saturation reduced, and the DON'T #3 thumbnail
    is G02 deliberately brightened and tinted as a counter-example. Raw files are unchanged.

## Blocked

These are **Blocked: image generation limit** (ElevenLabs free tier, daily image limit hit after 3 images on 2026-11-07). The fix is a
retry on a later day or a paid plan; the user or lead decides.
- Painted lighting-mood strip. Drawn hex keys stand in for it on the style guide sheet.
- Painted references for traps, watchtower, gate (G03's gate came out as a bare frame) and the ruin floors/roofs/stairs/collapsed/rubble sheet.
  The drawn sheets are authoritative, so **modelling is not blocked**.

The manifest has Blocked rows for these: `CA_LightingMoods_Painted`, `CA_Buildables_Painted_TrapsTower`, `CA_RuinKit_Painted_FloorsRoofs`.

## Next

**For Agent 2 (modeler):** model from the drawn elevations, not the paintings. The paintings are for look and materials only and each has a drift caveat.
Your greybox and these sheets differ in a few places. Please reconcile them, or log under your Assumptions why the greybox stays:

| Item | Greybox (Agent 2) | Concept (this batch) |
|---|---|---|
| Metal plate | one 400 × 300 × 1 sheet | 8 plates 100 × 150 × 1, one mesh per plate (one deposit per plate) |
| Barbed wire | 130 tall, posts at x 100/300 | 125 tall, posts at 0/200/400 (shared end posts) |
| Gate | clear 360 × 280, leaves 179 wide, 5 cm gap | posts Ø40, clear 320, leaves 160 × 280, 10 cm gap |
| Barricade | door 4 planks, window 3 planks | door 6 + diagonal, window 4 + diagonal (T2) |
| Watchtower | 230 × 230 deck | 200 × 200 footprint, deck 220 × 220 with overhang |
| Spike pit | 9 stakes × 60 | 16 stakes Ø6 × 75 (4 × 4 on a 50 cm grid) |
| Noise trap | string at 25 cm | string at 40 cm, 3 clusters of 3 cans |
| Deadfall | posts + crossbar, weight dropped from 180 | log Ø30 × 230 propped at 62 cm on a figure-4 trigger |
| Snare | 60 cm stake, 24 cm noose | springpole ~280, noose Ø40 on the ground, trigger peg |
| Burn trench | 60 × 30 channel, berms | 60 wide × 40 deep, no berms |
| Collapsed wall | broken top 300 → 40 | broken top 150 → 60 with a rubble skirt |
| Rubble | 200 × 160 × 80 | 200 × 200 × 80 and 400 × 200 × 120 |

Already the same as the greybox: wall pivot and centreline on the grid line, corner pillar, door and window openings, floor slab z −20…0,
roof 200 over 400, stairs, spiked wall (16 stakes, 20°), log wall (10 × 30), plate 2 cm stand-off.

**Also for Agent 2:** split every buildable into the elements the player deposits (one log, plank, plate, stake set, post or leaf each),
named in fill order (`Log_00`…). The ghost sheet depends on this. Concept rows for the T1 pieces are your existing Greybox rows; please fill in
their `concept_file` (Agent 1 did not edit your rows).

**For Agent 3 (game developer):**
- Ghost material spec is on `CA_Buildables_Ghost_Sheet.png` panel B.
- Lighting-mood hex keys and exposure rules are on the style guide sheet and in `Concept/StyleGuide.md`. Night must not be brightened by auto-exposure.
- Overgrowth coverage per surface type (table in `StyleGuide.md` §4) is the rule set for PCG ivy/moss scatter.

**For the next Agent 1 run:** retry the 5 refused generations (prompts in the ElevenLabs flows), then environment keys and character turnarounds.
UI icons should be drawn, not generated.
