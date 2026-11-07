# ROOTFALL style guide

Written page for `CA_StyleGuide_Sheet.png`. Agent 1 (concept art), rev A, 2026-11-07.
Source of truth for the colour values: `Tools/concept/sheetlib.py` (`PALETTE`). The sheet and this page are both built from it.

**Tone:** quiet, melancholy, tense. Nature has won. The world is 15 years after war and outbreak: everything man-made is
broken, rusted, rotten and overgrown. Warm light comes only from fire and from a low sun at dawn and dusk.
No jokes, no neon, no power fantasy.

## 1. Palette

| Group | Name | Hex | HSV sat. | Use |
|---|---|---|---|---|
| Greens | Deep Forest | `#2F3A2C` | 24% | Shadowed foliage, forest floor, deep ivy |
| Greens | Ivy | `#3F5236` | 34% | Ivy, creepers, conifer needles |
| Greens | Moss | `#5B6B47` | 34% | Moss, grass, broadleaf foliage |
| Greens | Lichen | `#8A9474` | 22% | Lichen, dry grass, foliage highlights |
| Rust | Old Rust | `#6E3B22` | 69% | Deep rust, rust streaks and stains |
| Rust | Rust Orange | `#9C4F26` | 76% | Main rust colour on all metal |
| Rust | Rust Bloom | `#B8683A` | 68% | Fresh rust, rust highlights (small areas) |
| Concrete | Shadow Concrete | `#3A3D3F` | 8% | Concrete in shade, wet cracks, voids |
| Concrete | Wet Concrete | `#5D6163` | 6% | Main concrete and asphalt, rain state |
| Concrete | Dry Concrete | `#8C8F8C` | 2% | Concrete in sun, dust, rubble |
| Concrete | Old Plaster | `#A7A294` | 11% | Render and plaster on ruined walls |
| Concrete | Weathered Brick | `#7A4A3A` | 52% | Exposed brick behind broken plaster |
| Bone | Bone White | `#D9D2C1` | 11% | Bone, paper, highlights, ghost lines |
| Wood | Bark | `#4A3A2C` | 41% | Bark on logs and stakes |
| Wood | Fresh-cut Wood | `#C9A26B` | 47% | Cut log ends, sharpened tips, new planks |
| Wood | Weathered Plank | `#8A7C66` | 26% | Scavenged and old planks |
| Wood | Rotten Wood | `#5A4E40` | 29% | Rotten beams, floors, fallen trees |
| Metal | Steel | `#6F7578` | 7% | Scrap sheet, plates, tools, frames |
| Metal | Weld Scorch | `#4A4644` | 8% | Heat-tinted and scorched steel at welds |
| Light | Firelight | `#E08A3C` | 73% | Fire, torch and lamp light (light only) |
| Light | Ember | `#B5471F` | 83% | Embers, glowing coals (light only) |
| Light | Sunset | `#D9A05B` | 58% | Low sun at dawn and dusk (light only) |
| Night | Night Sky | `#12161C` | 36% | Night sky, unlit interiors |
| Night | Moonlit Shadow | `#1C2430` | 42% | Night ambient, deepest fill |
| Gore | Dried Blood | `#4E2320` | 59% | Blood stains, wounds (never bright red) |
| Gore | Grave Skin | `#8C8A72` | 19% | Infected skin base tone |
| Ghost | Ghost Line | `#E3DED0` | 8% | Build ghost edge and fill (24%) |
| Ghost | Ghost Invalid | `#B5502E` | 75% | Ghost when placement is blocked |

**Rules**
- Large surfaces (foliage, concrete, plaster, bark, planks) stay at HSV saturation of 45% or less.
- Rust, Weathered Brick and Fresh-cut Wood are higher, so use them only in small areas: streaks, broken edges, cut ends.
- Firelight, Ember and Sunset are **light** colours. Use them for light sources and lit areas, never as paint on objects.
- No pure white, no pure black, no saturated blue, purple or red anywhere. Blood is `#4E2320`, never bright red.

## 2. Lighting moods

On the sheet these are drawn colour keys. The painted 5-panel mood strip is **Blocked** (image generation limit, see the report).

| Mood | Sky (top → horizon) | Key light | Shadow | Fog | Notes |
|---|---|---|---|---|---|
| Dawn | `#4E5A68` → `#C9A27A` | `#D9B48A`, sun 3–8° | `#3B4250` | `#B9B6AE` | ~3500 K, long shadows, ground mist in hollows, birdsong peak |
| Noon | `#8E9BA3` → `#BCC0BA` | `#E6E2D6`, high, hazy | `#4A4F4A` | `#C4C6C0` | ~5800 K, short shadows, colours still muted (no blue-sky postcard) |
| Overcast (default) | `#8C908E` → `#A6A9A5` | none (sky light only) | `#5C605C` | `#9A9E9C` | Default weather, soft, greens read richest |
| Rain | `#4F5658` → `#6B7275` | none | `#3A3F42` | `#7A8285` | Surfaces 20–30% darker, roughness −0.3, puddles, visibility ~150 m |
| Night + firelight | `#0E1116` → `#1C2430` | Fire `#E08A3C`, lights 8–12 m | `#0B0D10` | `#1C2430` | True dark, moon ambient `#1C2430` only |

- Exposure is fixed per mood. Eye adaptation must not brighten the night.
- Fog colour = horizon colour. Shadows are never pure black, and at night unlit areas fall to Night Sky `#12161C`.
- Light draws zombies and bandits, so a bright warm light also makes the player more visible.

## 3. Material language

| Material | Colours | Surface | Where / how |
|---|---|---|---|
| Rust | Rust Orange, Old Rust, Rust Bloom | rough 0.8–0.95, not metallic where rusted (mask) | Streaks run down from edges, bolts and welds; worst at the bottom of sheets |
| Wet concrete | Wet / Shadow / Dry Concrete | rough 0.85 dry → 0.35 wet; 25% darker when wet | Damp band at wall bases, stains under ledges and sills, cracks |
| Rotten wood | Rotten Wood | rough 0.95, soft rounded edges | Grain splits, moss and pale fungus. Ruins only, never on player builds |
| Moss | Moss, Lichen | rough 1.0, slight subsurface | Tops, ledges, shaded bases; decal or vertex blend |
| Ivy | Ivy, Deep Forest, Moss | leaf cards, leaves 4–8 cm | Climbs from soil, hangs from lintels and roof edges, leaves face the light |
| Fresh-cut logs | Bark + Fresh-cut Wood | bark rough 0.9, cut end 0.7 | Bright clean ends = "the player made this". Tone ends to `#C9A26B` |
| Welded steel | Steel + Weld Scorch | bare steel metallic 1.0, rough 0.45–0.6 | Lumpy weld bead, 3–5 cm heat-tint ring; new welds bright, rust creeps in later |

Swatches on the sheet are crops of the generated paintings in `Concept/_raw/`. Rotten wood has no generated source, so its
swatch is drawn.

## 4. Overgrowth rules (how much foliage per surface)

Growth follows light, water and gravity. It starts at the soil and at wet horizontal surfaces, and it always needs a contact surface.

| # | Surface | Coverage | Rule |
|---|---|---|---|
| 1 | Ground, verges | 70–100% | Grass, ferns, shrubs, leaf litter |
| 2 | Roads, floors open to the sky | 20–50% | Cracks only; saplings in wide cracks |
| 3 | Exterior walls | 0–70% | Ivy from the ground up; denser on shaded faces and corners; moss band 0–40 cm |
| 4 | Ledges, sills, wall tops, flat roofs | 60–100% | Moss, grass tufts, saplings on broken tops |
| 5 | Pitched roofs | 20–50% | Moss on tiles; saplings at holes and gutters |
| 6 | Openings | 30–60% | Ivy curtains hang from lintels and pour out of windows |
| 7 | Interiors | 0–15% | Only within ~2 m of openings or under roof holes |
| 8 | Metal, vehicles | 0–20% | Rust first; grass through floors, saplings through hulls |
| 9 | Player-built | 0% | Fresh wood and steel always read as new |
| 10 | Forest-swallowed zones | 80–100% | Trees inside buildings, roofs gone |

Never: floating foliage, ivy without a contact surface, green on freshly built player pieces, or uniform coverage.
Overgrowth is a separate layer (ivy cards, moss decals), so any ruin state can be overgrown in-engine (Agent 2 rule, PCG scatter by Agent 3).

## 5. Five do, five don't

| Do | Don't |
|---|---|
| Warm light only from fire (and low sun) | Neon or coloured artificial light |
| Ivy rises from soil and pours from openings | A uniform bright-green carpet or floating foliage |
| Every ruin shows war damage (shell holes, pocking, scorch) and neglect (rust, rot, damp) | Clean, freshly painted or pastel buildings |
| Player builds are rough, functional, fresh-cut, with visible joins | Ornamental, symmetrical, decorative builds |
| A muted, painterly render where value carries the read | Black cartoon outlines and saturated colour |

Also: no logos, real brands, real insignia or likenesses; nothing traced from another game. Silhouettes must read in the dark.

## Files

- `CA_StyleGuide_Sheet.png`: this guide as one sheet
- `CA_Buildables_Walls_Sheet.png`, `CA_Buildables_GateTower_Sheet.png`, `CA_Buildables_Traps_Sheet.png`,
  `CA_Buildables_Ghost_Sheet.png`: player-built structures
- `CA_RuinKit_Walls_Sheet.png`, `CA_RuinKit_FloorsRoofsStairs_Sheet.png`: modular ruin kit
- `_raw/`: raw image generations (provenance). Rebuild every sheet with `python3 Tools/concept/build_all.py`.
