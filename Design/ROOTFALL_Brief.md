# ROOTFALL --- Multi-Agent Game Build Prompt

Nov 6, 2026 · \@Ian

## How to use this prompt

Run three agents at once, not one after another: concept art, modeling
and development overlap, connected by a shared brief and one asset
manifest.

![three-agent pipeline · shared brief in, manifest
between](media/image1.png)

three-agent pipeline · shared brief in, manifest between

Development never waits on art: Agent 3 builds every system on greybox
and the UE5 Mannequin, then swaps in final assets as their manifest rows
reach Exported.

1.  Give **every** agent these sections: Shared brief, World and
    setting, Core systems, Realism systems, Enemies, and Handoff
    contract.

2.  Add each agent\'s own prompt section. Give Agent 3 the Milestones
    section too.

3.  Start Agent 1 on the style guide, the player-built structures sheet
    and the ruin kit sheet first; those unblock everyone.

4.  Start Agent 2 on the greybox kit right away from the dimensions in
    this document, then move to final assets as concept sheets land.

5.  Start Agent 3 on milestones M0 to M3 immediately.

6.  Review each agent\'s report at the end of every task and check the
    manifest before approving the next milestone.

## Shared brief (give to all three agents)

ROOTFALL (working title) is a first-person, single-player survival game
where you build and fortify a base in an overgrown, war-ruined world
while slow, endless zombie hordes and rare, loud bandits grind you down.
Movement, combat, building and crafting feel like *The Forest*; survival
simulation (moodles, body-part injuries, noise, infection) feels like
*Project Zomboid*.

**Design pillars**

1.  **Every action has a cost.** Chopping, hammering, welding, sprinting
    and shooting make noise, burn stamina and calories, and risk injury.

2.  **The horde is the weather.** One zombie is easy; thirty are a death
    sentence. Danger comes from numbers, noise and bad positioning,
    never from a single tough enemy.

3.  **Build to survive, not to decorate.** Bases are defensive machines:
    walls, spikes, pits, metal plating and chokepoints that zombies
    physically attack and break.

4.  **Nature has won.** Forest reclaims the ruins. Foliage blocks
    sightlines, muffles sound, hides loot and hides threats.

5.  **Death is a story.** A bite gives you exactly 48 in-game hours.
    When you die, the world keeps your base, your corpse and your
    mistakes.

**Tone:** quiet, melancholy, tense. Long stretches of birdsong and wind,
broken by groans, gunfire and shouting. No jokes, no neon, no power
fantasy.

**Camera and player:** first-person with full-body awareness (visible
legs and shadow), first-person arms for all interactions. A third-person
camera is out of scope.

**Engine and tools:** Unreal Engine 5.8, gameplay core in C++ with
Blueprint subclasses for tuning and content. Blender for all modeling,
rigging and asset export. Data-driven content (Data Assets and Data
Tables) so items, recipes, zombies and buildables are added without code
changes.

**Scope rule:** build a playable vertical slice first (one 1 km x 1 km
map, every core system working end to end), then expand.

**Hard rules for every agent**

-   Original content only. Nothing copied, traced or ripped from *The
    Forest*, *Project Zomboid* or any other game, film or artist. Use
    them as references for feel, never as assets.

-   Never claim a task is done without verifying it (compiles, imports
    cleanly, runs, matches the spec). If something cannot be verified,
    say so.

-   Never invent a missing requirement silently. Make the smallest
    reasonable assumption, write it in your report under
    \"Assumptions\", and keep going.

-   Follow the handoff contract (naming, folders, manifest) exactly; a
    misnamed file is a bug.

-   Report at the end of every task: what was done, how it was verified,
    what is blocked, what the next agent needs.

## World and setting

The world is a rural valley roughly 15 years after a war and an outbreak
collided: the war broke the towns, the outbreak emptied them, and the
forest took what was left. The player is a survivor who arrives with
almost nothing.

**Backstory (told only through environment and found notes)**

-   A regional war with an unnamed neighbor reached the valley:
    shelling, trenches, a fallen front line.

-   During the fighting, an infection spread through the troops and
    refugees. Military quarantine failed.

-   The army retreated, blowing the bridges behind it. Nobody came back.

**Visual rules for ruins and overgrowth**

-   Every man-made structure shows war damage (shell holes, collapsed
    floors, scorch marks, bullet pocking) and 15 years of neglect (rust,
    rot, broken glass, sagging roofs).

-   Ivy, moss, vines and creepers climb walls and pour out of windows.
    Saplings grow through roofs, road cracks and vehicle hulls.

-   Forests have physically swallowed parts of the map, with buildings,
    vehicles and roads still inside them.

-   Palette: desaturated greens, rust orange, wet concrete grey, bone
    white. Warm light only from fire and sunset.

**Biomes (vertical slice includes the first three)**

  ------------------------------------------------------------------------
  Biome             What it is                      Gameplay role
  ----------------- ------------------------------- ----------------------
  Overgrown town    Small town center: shops,       Best loot (medical,
                    houses, a church, a gas         tools, food), highest
                    station, a clinic,              zombie density, tight
                    half-collapsed apartment block  streets

  Deep forest       Dense old-growth trees over     Logs, sticks, stones,
                    buried structures: ranger       hunting; low
                    station, cabins, a crashed      visibility; ideal base
                    helicopter, a hidden bunker     land
                    hatch                           

  War zone edge     Trenches, craters, a burnt-out  Weapons, ammo, metal,
                    tank, a military checkpoint,    welding gear; mines;
                    sandbag nests, a field hospital bandit activity
                    tent camp                       

  Farmland          Overgrown fields, barns, silos, Seeds, tools, fuel,
                    a farmhouse                     livestock remnants

  River and lake    Destroyed bridge, a boathouse,  Water, fish, natural
                    a dam                           barriers

  Quarry and rail   Freight cars, cranes, gravel    Bulk scrap metal, rare
  yard                                              heavy tools
  ------------------------------------------------------------------------

**Points of interest that matter to systems**

-   Houses and shops: lootable containers, barricadable doors and
    windows, generators.

-   Military sites: welding torch, propane tanks, firearms, ammo, mines,
    military rations.

-   Clinic and field hospital: bandages, disinfectant, suture kits,
    antibiotics, splints.

-   Vehicles: scrap metal source (cut with a hacksaw or torch), fuel
    siphoning. Vehicles are not drivable in the slice.

-   Structures inside forests: safe-looking but often hold dormant
    zombies or bandit stashes.

**Time, weather and seasons**

-   Default: 1 in-game day = 60 real minutes (sandbox setting, 30 to
    180).

-   Dynamic weather: clear, overcast, rain, storm, fog. Rain and wind
    mask noise; fog cuts vision for player and zombies alike.

-   Seasons (post-slice): summer to winter in a configurable cycle;
    winter brings snow, cold moodles, and leafless foliage that opens
    sightlines.

-   Night is truly dark. Light sources are visible from far away and
    draw zombies and bandits.

## Core systems: movement, combat, building, crafting

These systems should feel like *The Forest*: physical, hands-on,
diegetic (the player opens a book, holds a log, lays items on a mat),
with Zomboid-level consequences layered on top.

### Movement

-   Walk, sprint (drains stamina), crouch (quieter, slower, smaller
    visual profile), jump, vault low obstacles, climb ladders and ropes,
    swim (drains stamina fast; heavy loads sink you).

-   Stamina bar plus a separate long-term **Energy** value that drops
    with exertion, hunger and lack of sleep and caps max stamina.

-   Encumbrance from inventory weight: Heavy Load moodle slows movement,
    raises noise and stamina drain.

-   Carrying: up to 2 logs on the shoulder (hands busy, can\'t fight); a
    craftable **log sled** to drag up to 8 logs.

-   Footstep noise depends on speed and surface (gravel, glass, metal,
    wood, grass, water). Crouching on grass is nearly silent; sprinting
    on glass is not.

-   Fall damage by height, with leg injuries (sprains, fractures) above
    a threshold.

### Combat

-   Melee is the core: light attack, heavy (charged) attack, block,
    shove (pushes zombies back, costs stamina, the key tool against
    groups). Every swing costs stamina; at zero stamina attacks are slow
    and weak.

-   Hit locations matter: zombies die only from destroying the head (or
    enough head trauma); limb hits stagger, cripple or knock down. A
    knocked-down zombie can be stomped.

-   Weapons have durability, weight, reach, swing speed, stamina cost,
    knockback and noise. Tiers: improvised (stick, rock, crafted club,
    crafted spear) → scavenged (crowbar, machete, fire axe,
    sledgehammer) → upgraded (any weapon + nails, wire, metal plates).

-   Throwables: rocks, spears, molotovs, pipe bombs, noise-maker decoys
    (bottle, alarm clock).

-   Ranged: craftable bow and arrows (quiet), scavenged firearms
    (pistol, shotgun, bolt rifle) that are deadly but extremely loud and
    draw every zombie in a large radius. Ammo is rare; reloading is
    manual and interruptible.

-   No lock-on, no auto-aim, no hit markers. Feedback through animation,
    sound and gore.

-   Being grabbed: a zombie that reaches you grapples; you get a short
    window to shove or strike free. While grappled, nearby zombies get
    free attacks, which is how groups kill you.

### Building (The Forest model)

-   A **Survival Book** (opened in-hand) holds blueprints in tabs:
    Shelter, Storage, Utility, Defense, Traps, Metalwork.

-   Selecting a blueprint shows a translucent **ghost** in the world.
    The player places it (snapping to terrain and other pieces), then
    fills it by physically adding materials one unit at a time: logs,
    sticks, rocks, rope, nails, planks, scrap metal. The ghost turns
    solid piece by piece.

-   **Free-form building:** custom walls, floors, roofs and foundations
    placed by dragging points along a line or area; length decides the
    log cost.

-   Tree felling: trees take several axe hits, fall with physics, and
    split into logs. Stumps stay. Trees regrow slowly (sandbox setting).

-   Structures have HP per piece and a material tier. Repair with a
    hammer plus a small amount of matching material. Players can
    deconstruct their own pieces for a partial refund.

-   Building is loud (hammering, chopping, sawing), so building at night
    or near a town is a real risk.

### Fortifications and metalwork

The Forest-style building gains a metal tier. Metal is always applied on
top of existing wood pieces, so the feel stays the same: place ghost,
add materials.

  ------------------------------------------------------------------------
  Fortification   Materials              What it does
  --------------- ---------------------- ---------------------------------
  Palisade /      Logs                   Basic perimeter; zombies bash it
  defensive wall                         

  Spiked wall     Wall + sharpened       Damages zombies that attack it
                  sticks                 

  Spike pit       Dug pit (shovel) +     Kills or traps zombies that fall
                  sharpened sticks +     in; must be cleared and re-armed
                  cover                  

  Barbed wire     Wooden posts + barbed  Slows and damages; zombies tangle
  fence           wire                   

  Barricaded      Planks + nails (or     Seals ruined buildings
  door/window     metal sheet + welding) Zomboid-style

  Metal plating   Scrap metal sheets     Raises a piece\'s HP and stops
                  welded onto wall       spike/claw damage
                  pieces                 

  Welded gate     Metal frame + sheets + Strong, openable chokepoint
                  hinges                 

  Watchtower      Logs + ladder          Height, sightlines, ranged
                                         position

  Noise trap      String + tin cans      Rattles when crossed; warns the
                                         player

  Tripwire alarm, Rope, rocks, sticks    Forest-style traps for zombies
  deadfall, snare                        and animals

  Fire ring /     Dug trench + fuel      Lit to block a horde (also lights
  burn trench                            you up)
  ------------------------------------------------------------------------

**Welding rules:** needs a welding torch, a propane tank (fuel units)
and a welding mask (without the mask: eye damage chance). Welding is
loud and glows brightly. The Metalworking skill speeds work and lowers
fuel use.

### Crafting and skills

-   Forest-style **crafting mat**: open the inventory, lay items on the
    mat, valid combinations glow, confirm to craft. Recipes are learned
    from the Survival Book, found magazines and notes.

-   Workstations for advanced recipes: workbench, campfire, smokehouse,
    rain collector, metal workbench.

-   Zomboid-style skills that level by doing: Carpentry, Metalworking,
    Fitness, Strength, Blade, Blunt, Aiming, First Aid, Foraging,
    Trapping, Cooking, Sneaking. Skills raise speed, success and
    quality, never unlock power fantasies.

### Survival needs and base life

-   Hunger, thirst, fatigue, temperature, boredom and stress (all
    tracked by moodles, next section).

-   Food spoils; cook, dry, smoke or can it. Water must be boiled or
    purified unless from a rain collector.

-   Sleep restores Energy but leaves you blind to the world; zombies can
    attack your base while you sleep, and the sleep can be interrupted
    by noise.

-   Generators give power for lights and tools, but they hum constantly
    and draw zombies.

### Persistence and death

-   The world saves everything: felled trees, built pieces and their HP,
    looted containers, dropped items, corpses.

-   On death, your character reanimates as a zombie in your gear. You
    start a new survivor in the same world and can hunt down your old
    self to recover the gear.

-   Sandbox settings expose zombie population, speed, toughness,
    infection rules, loot rarity, day length, bandit frequency and
    respawn.

## Realism systems: moodles, injuries, infection, sound

These systems are *Project Zomboid*-level in depth and always visible to
the player through moodles, the health panel and audio, never through
raw numbers.

### Moodles

Moodles are small icons stacked on the right edge of the screen. Each
has 4 severity levels shown by border color (level 1 pale, level 4 red)
and a tooltip. A new or worsening moodle pulses once with a soft sound.

  ------------------------------------------------------------------------
  Moodle            Driven by             Effect at high levels
  ----------------- --------------------- --------------------------------
  Hungry / Starving Calories              Stamina regen down, then HP loss

  Thirsty / Parched Hydration             Faster fatigue, then HP loss

  Tired / Exhausted Sleep debt            Slower actions, blurry vision,
                                          falls asleep

  Endurance         Stamina and Energy    Weak, slow attacks; can\'t
                                          sprint

  Heavy Load        Carry weight          Slower, louder, more stamina
                                          drain

  Panic             Zombies in view,      Aim sway, shaking hands, slower
                    sudden scares         crafting

  Stressed          Ongoing danger,       Lowers panic resistance; feeds
                    smoking withdrawal,   Unhappy
                    pain                  

  Bored / Unhappy   Monotony, darkness,   Slower skill gain; Depressed at
                    eating cold food      max

  Wet               Rain, swimming        Speeds up cold; chance of a cold

  Cold /            Temperature,          Slow movement, HP loss
  Hypothermia       clothing, wetness     

  Hot /             Heat, exertion, heavy Faster thirst, fatigue
  Hyperthermia      clothing              

  Pain              Injuries              Slower actions, can\'t sleep

  Bleeding          Open wounds           HP loss until bandaged

  Injured           Overall HP            Reduced max stamina and speed

  Queasy / Sick     Bad food, dirty       Vomiting, weakness
                    water, wound          
                    infection, zombie     
                    infection             

  Has a Cold        Wetness and cold      Sneezing and coughing (noise)

  Drunk             Alcohol               Calms stress; ruins aim and
                                          balance

  Bitten            Zombie bite           Permanent; begins the infection
                                          clock
  ------------------------------------------------------------------------

### Body-part injuries

-   Health panel shows a body diagram split into 17 parts: head, neck,
    upper torso, lower torso, groin, and left/right upper arm, forearm,
    hand, thigh, shin, foot.

-   Each part tracks its own wounds, bandage state (clean/dirty),
    infection and pain.

  --------------------------------------------------------------------------
  Injury       Common cause                Treatment
  ------------ --------------------------- ---------------------------------
  Scratch      Zombie claws, thorns, glass Disinfect + bandage

  Laceration   Zombie claws, blades, falls Disinfect + bandage; stitch if
               through glass               deep

  Deep wound   Blades, bullets, spike      Stitch (suture kit or needle and
               traps, explosions           thread) + bandage

  Bite         Zombies                     Disinfect + bandage (stops
                                           bleeding, not infection)

  Glass shard  Broken windows, gunfire     Remove with tweezers or a knife,
  / embedded                               then treat as deep wound
  bullet                                   

  Fracture     Falls, sledgehammer hits,   Splint (sticks + rope or a
               being trampled              scavenged splint); heals over
                                           days

  Sprain       Falls, sprinting over rough Rest; slows movement
               ground                      

  Burn         Fire, molotovs, welding     Clean bandage; heals slowly
               without gloves              
  --------------------------------------------------------------------------

-   Dirty bandages and untreated wounds can become **wound infections**
    (curable with disinfectant and antibiotics). This is separate from
    zombie infection, which antibiotics do not cure.

-   Clothing gives per-part protection against scratches and bites
    (leather jacket on arms, boots on feet). Clothing gets holes and can
    be patched.

### Zombie infection: a bite means 48 hours

A bite (anywhere) is always fatal. From the moment of the bite the
player has **48 in-game hours** to live. Bites are shown immediately
with the Bitten moodle so the player knows. Each stage is driven by a
single infection timer stored in the save.

  -----------------------------------------------------------------------
  Time since bite  Stage      What the player experiences
  ---------------- ---------- -------------------------------------------
  0 to 12 h        Bitten     No symptoms beyond the wound

  12 to 24 h       Feverish   Queasy level 1-2, body temperature rises,
                              mild stamina cap reduction

  24 to 40 h       Sick       Queasy 3, vomiting, max stamina and carry
                              weight reduced, vision edges darken

  40 to 48 h       Dying      Sick 4, frequent coughing (loud),
                              staggering, screen desaturates, character
                              falls asleep randomly

  48 h             Death      Character dies; reanimates as a zombie
                              after 1-3 in-game minutes
  -----------------------------------------------------------------------

-   Sandbox options: \"Bite only\" (default) or \"Zomboid rules\"
    (scratches 7% and lacerations 25% chance to infect, hidden until
    symptoms appear); time-to-death 24 to 96 h (default 48).

-   Sleeping, painkillers and food can ease symptoms but never stop the
    clock. Use the final 48 hours as gameplay: secure the base, write a
    note, stash gear for the next survivor.

### Sound and noise

Every noisy action creates a **noise event** with a world position,
loudness and radius. Zombies and bandits inside the radius hear it and
move to investigate; louder noises reach further and wake dormant
zombies. Walls, buildings and dense foliage reduce effective radius;
rain and wind reduce it further.

  -----------------------------------------------------------------------
  Action                                        Base radius (m)
  --------------------------------------------- -------------------------
  Crouch-walk                                   2

  Walk                                          5

  Sprint                                        15

  Breaking glass                                25

  Chopping a tree                               30

  Generator running (continuous)                30

  Hammering / building                          35

  Welding                                       40

  Bandit shouting                               60

  Bow shot                                      8

  Pistol shot                                   120

  Shotgun shot                                  150

  Rifle shot                                    200

  Explosion                                     250
  -----------------------------------------------------------------------

**Audio design requirements**

-   Fully spatialized 3D audio with occlusion and attenuation
    (MetaSounds, Audio Gameplay Volumes for interiors).

-   Distinct, readable zombie vocal layers: idle groan, alert moan (when
    they notice you), attack snarl, and a horde bed that grows with
    group size so the player can hear a crowd before seeing it.

-   Bandits are loud on purpose: shouted taunts, calls to each other,
    whistles and gunfire, so the player hears them coming and so they
    pull zombies in.

-   Ambient layers per biome: wind through broken windows, creaking
    metal, birds (birds go silent when zombies or bandits are near,
    which is a tell).

-   Dynamic music: near-silence by default; low tension layers when
    threats are near; no music during full combat, only sound.

-   Accessibility: optional on-screen sound indicators and subtitles for
    zombie, bandit and footstep sounds.

## Enemies: zombies, bandits, wildlife

Zombies are the constant pressure: slow, numerous and relentless.
Bandits are the rare, loud spike of danger. Wildlife is food and
occasional trouble.

### Zombies

**Core behavior**

-   Slow shamblers by default (walk speed about 1.2 m/s, a short lunge
    of 2-3 m when within reach). Player walk is about 1.6 m/s and sprint
    about 5 m/s, so one zombie is escapable; a crowd in a narrow street
    is not.

-   Senses: hearing (noise events, main sense), sight (forward cone,
    short range at night, reduced by foliage and fog), smell is not
    used.

-   States: Dormant (standing or lying still, wakes on noise) → Wander →
    Investigate (moves to last noise or sighting) → Chase → Attack →
    Lost (searches the area, then wanders).

-   Herding: zombies that see other zombies moving follow them, so one
    noise can pull a whole street. Hordes drift slowly across the map
    over days.

-   Kill condition: head destroyed or enough head trauma. Body damage
    staggers and knocks down. Leg damage creates crawlers.

-   Lethality comes from grabs plus numbers: each zombie\'s attack can
    scratch, lacerate or bite the body part it hits, based on clothing
    protection and whether the player is grappled.

-   Population: density per zone (town high, forest low), configurable
    total population and slow respawn into areas the player hasn\'t
    visited for N in-game days. Target 150-300 active zombies in the
    vertical slice, with distant ones simulated cheaply.

**Attacking structures**

-   Zombies that hear or see the player behind a structure, or that bump
    into one while investigating, attack it (\"thumping\").

-   Damage per hit is small; damage stacks with every zombie hitting the
    same piece, so 20 zombies break a wall fast.

-   Metal-plated pieces take heavily reduced damage. Spiked walls damage
    attackers each hit. Barbed wire slows and damages zombies passing
    through it.

-   Zombies pile up against walls; a big enough crowd can create a body
    ramp over low walls (post-slice feature).

**Variants (all are the same infected; just different states of decay or
gear)**

  -------------------------------------------------------------------------
  Variant    Difference                               Where
  ---------- ---------------------------------------- ---------------------
  Civilian   Baseline                                 Everywhere

  Soldier    Helmet and vest: head and torso need     War zone, checkpoints
             more hits; can drop military loot        

  Rotten     Weaker, slower, quieter; hard to hear    Deep forest,
                                                      buildings

  Crawler    Crawls, hides in tall grass, grabs       Anywhere
             ankles                                   

  Bloated    Bursts when killed: blinding gas         Rare, towns
             (Queasy)                                 
  -------------------------------------------------------------------------

No special super-zombies. The threat must always come from numbers.

### Bandits

-   Rare: 0-2 bandit groups active on the map at once (sandbox setting).
    Groups of 2-4 humans with melee and firearms.

-   **Loud by design:** they shout to each other, taunt the player,
    whistle signals and fire guns freely. That noise pulls zombies, so a
    bandit encounter often turns into a three-way fight the player can
    exploit.

-   Behavior: patrol between camps and points of interest; investigate
    player noise and smoke; ambush on roads; occasionally raid a player
    base at night.

-   Tactics: use cover, flank, retreat when hurt, call for help, finish
    downed players. Bandits can be scared off by losses and will loot
    your base if you\'re away.

-   Danger: far more accurate and smarter than zombies, so a careless
    player dies fast. Careful players can avoid, ambush or lure zombies
    onto them.

-   Bandit camps: small fortified sites with loot, tents and a fire
    (visible at night). Clearing one is a major event.

### Wildlife

-   Deer and rabbits (hunt for meat and hide), birds (ambient and alarm
    tell), fish (rivers and lake).

-   Feral dogs (rare packs; dangerous at night, can be lured with meat).

-   Animals flee from zombies and loud noise; carcasses attract zombies
    over time.

## Agent 1 prompt: Concept Artist

**Role.** You are the lead concept artist for ROOTFALL. Read the Shared
brief, World and setting, Core systems, Realism systems and Enemies
sections before drawing anything. Your art is the single source of truth
for how the game looks; the 3D modeler builds exactly what you draw, so
clarity beats beauty.

**Goal.** Produce a complete, consistent visual package for the vertical
slice: style guide, environment keys, modular building references,
characters and enemies as modeling-ready turnarounds, props,
player-built structures, and UI.

**Deliverables, in this order**

1.  **Style guide** (one sheet plus a written page): palette with hex
    values, lighting moods (dawn, noon, overcast, rain, night with
    firelight), material language (rust, wet concrete, rotten wood,
    moss, ivy, fresh-cut logs, welded steel), overgrowth rules (how much
    foliage per surface type), and 5 do / 5 don\'t examples.

2.  **Environment keys** (one painting each): overgrown town street,
    deep forest with a buried cabin, war zone edge with a burnt tank and
    trenches, player base at night under zombie attack.

3.  **Modular ruin kit sheet**: walls, corners, floors, roofs, stairs,
    windows, doors, collapsed pieces and rubble, each drawn intact,
    damaged and overgrown, on a 100 cm grid.

4.  **Player-built structures sheet**: every buildable in the
    Fortifications table at each material tier (log, log + plank,
    metal-plated), plus the ghost/blueprint look.

5.  **Characters** (orthographic front, side and back, plus a 3/4 view,
    T-pose, next to a 180 cm scale figure): player survivor (2 outfits),
    5 zombie variants, 3 bandit types, first-person arms with sleeves.

6.  **Props and items**: weapons (each tier and upgrade), tools (axe,
    hammer, saw, shovel, crowbar, welding torch, welding mask, propane
    tank), medical items, food, containers, the Survival Book (closed
    and open pages).

7.  **Foliage set**: 4 tree species (living and dead), shrubs, ferns,
    grass, ivy and creeper decals, moss.

8.  **UI**: moodle icon set (every moodle in 4 severity borders), health
    panel body diagram, inventory crafting mat, Survival Book layout,
    item icons.

**Specifications**

-   Images at least 2048 px on the long edge, PNG, sRGB. Turnarounds on
    a flat neutral grey background with no perspective distortion.

-   Every sheet carries written callouts: real-world dimensions in
    centimeters, materials, which parts are separate meshes or moving
    parts (doors, hinges, magazines), wear and damage notes.

-   Moodle icons as 256 x 256 px PNGs with transparent backgrounds,
    readable at 48 px.

-   Name every file per the handoff contract (prefix CA\_) and add a row
    to the asset manifest for each.

**Consistency rules**

-   Same character must look identical across every view. If an image
    tool produces drift (changed clothing, proportions or face),
    regenerate or correct it before delivering.

-   Keep silhouettes readable at a distance and in the dark; zombies
    must be distinguishable from bandits by silhouette alone.

-   Original designs only: no logos, real brands, real military insignia
    or likenesses of real people.

**Self-check before handoff.** Re-read the brief and confirm every
deliverable exists, every file name matches the contract, every sheet
has dimensions, and every character has front, side and back views that
match. List anything you couldn\'t make and why.

## Agent 2 prompt: 3D Modeler (Blender)

**Role.** You are the 3D artist for ROOTFALL, working in the current
stable version of Blender. You turn the Concept Artist\'s sheets into
game-ready, Unreal-ready assets. Read the Shared brief, the Concept
Artist\'s style guide and every sheet\'s callouts before modeling. If a
sheet is unclear, model the most reasonable reading and log it under
Assumptions.

**Goal.** Deliver every vertical-slice asset as a clean .blend source
plus an exported FBX and textures that import into Unreal Engine 5.8 at
correct scale, orientation and materials on the first try.

**Deliverables, in priority order**

1.  **Greybox kit first** (simple blocks at final dimensions) for the
    ruin kit and player buildables, so the Game Developer can build
    levels while you finish detail.

2.  Player-built structures: every Fortifications table piece at each
    tier (log, plank-reinforced, metal-plated), each with intact,
    damaged and destroyed versions.

3.  Modular ruin kit with intact, damaged and overgrown variants.

4.  Characters: player survivor, 5 zombie variants, 3 bandit types,
    first-person arms.

5.  Weapons, tools, props, medical items, containers, the Survival Book
    (with an opening animation).

6.  Foliage: trees (with a felled-trunk and log-segment version for
    chopping), shrubs, grass, ferns, ivy strips and cards, moss.

7.  Vehicles and war wrecks: tank hull, cars, crashed helicopter
    (static, with scrap-able panels as separate meshes).

**Scale, orientation and export**

-   Scene units: Metric, Unit Scale 1.0. Model at real-world size (1
    Blender unit = 1 m = 100 Unreal units).

-   Apply all transforms (rotation and scale) before export. Pivot at
    the logical placement point: bottom center for props, bottom corner
    on the grid for modular pieces, grip point for held items.

-   Characters face -Y in Blender (Blender\'s Front view), the same
    convention as the UE5 Mannequin.

-   Export FBX per asset with Smoothing set to Face, \"Add Leaf Bones\"
    off, and only the asset\'s own objects selected.

-   **Verify every first export of a new asset type in Unreal** (a 180
    cm reference character must measure 180 cm, root bone scale must be
    1.0, the asset must face the expected direction). Fix the export
    preset before batch-exporting the rest. Save the working preset and
    note its settings in your report.

**Modular grid**

-   Ruin kit snaps on a 100 cm grid: wall pieces 400 cm wide and 300 cm
    tall (also 200 cm and 100 cm fillers), wall thickness 20 cm, floor
    tiles 400 x 400 cm.

-   Player-built log pieces use a 30 cm log diameter. A log wall segment
    is 10 stacked logs (300 cm tall) and up to 400 cm long; free-form
    walls are built from one repeatable log mesh with cut ends.

-   Metal plates for welding are separate meshes that sit 2 cm proud of
    the wood surface so they layer onto any wall piece without
    z-fighting.

**Topology and budgets (triangles)**

  -----------------------------------------------------------------------
  Asset type             Budget
  ---------------------- ------------------------------------------------
  Player body + head     40-60k

  First-person arms      15-25k

  Zombie / bandit        20-35k

  Held weapon or tool    3-10k

  Small prop             300-3k

  Modular wall piece     Nanite-eligible: detail freely; otherwise 2-8k

  Tree (LOD0)            10-40k
  -----------------------------------------------------------------------

-   Clean quads while modeling; triangulation happens on export. No
    non-manifold geometry or flipped normals on anything solid.

-   Static meshes, including foliage, are built to be Nanite-eligible.
    Skeletal meshes need LODs (LOD0 to LOD3, about 50% triangle
    reduction each), named per the contract. Also deliver LODs for trees
    in case the Game Developer measures foliage faster without Nanite.

**UVs and textures**

-   Texel density: 1024 px/m for anything seen up close (held items,
    arms, characters, buildables), 512 px/m for large environment
    pieces. Use tiling materials plus trim sheets for the ruin kit.

-   PBR metal/roughness. Texture sets per material: BaseColor (sRGB),
    Normal, ORM packed (R = ambient occlusion, G = roughness, B =
    metallic; linear, not sRGB). Emissive only where needed.

-   Blender bakes OpenGL-style normal maps; Unreal expects
    DirectX-style. Flip the green channel on export, or tell the Game
    Developer to tick \"Flip Green Channel\" on import. State which you
    did in the manifest.

-   Power-of-two texture sizes (512 to 4096). Overgrowth uses separate
    ivy/moss decal textures so any piece can be overgrown in-engine.

**Collision and sockets**

-   Custom collision as convex hulls named UCX\_\[MeshName\]*00,
    UCX*\[MeshName\]\_01 and so on, exported in the same FBX. Every
    player buildable and ruin piece gets custom collision.

-   Sockets as empties named SOCKET\_\[Name\] (for example
    SOCKET_Muzzle, SOCKET_Grip, SOCKET_PlateMount).

**Rigging and animation**

-   Every humanoid uses a skeleton with the same hierarchy and bone
    names as the UE5 Mannequin (root, pelvis, spine_01 and so on), root
    bone at the origin, armature object named \"Armature\". This lets
    the Game Developer retarget Epic\'s free animation content with the
    IK Retargeter and share animations between player, zombies and
    bandits.

-   Animate in Blender only what free content can\'t provide:
    first-person arm actions (chop, swing light/heavy, block, shove,
    hammer, saw, weld, dig, bandage, eat, drink, read book, carry log),
    zombie-specific moves (shamble, lunge, grab, thump wall, crawl,
    stand up), and the Survival Book opening.

-   Export animations as separate FBX files (animation only, same
    skeleton), with root motion only where the contract says so.

**Self-check before handoff.** For each asset: correct name, correct
scale in Unreal, applied transforms, collision present, textures correct
color space, manifest row updated with triangle count and status.
Deliver the .blend sources too.

## Agent 3 prompt: Game Developer (Unreal Engine 5 + Blender)

**Role.** You are the lead gameplay and technical developer for ROOTFALL
in Unreal Engine 5.8, using C++ for systems and Blueprints for content
and tuning. You integrate the Concept Artist\'s visuals and the 3D
Modeler\'s assets, and use Blender only for integration fixes
(collision, pivots, re-exports), never to change the art direction. Read
every section of this document before writing code.

**Goal.** Ship the vertical slice: one 1 km x 1 km map where every
system in this document works together, follow the milestones in order,
and do not start a milestone until the previous one passes its
acceptance tests.

**Do not wait for final art.** Start immediately with greybox meshes and
the UE5 Mannequin, then swap in final assets as they arrive in the
manifest. Systems must never depend on a specific mesh.

### Architecture

Every system is a self-contained C++ Actor Component or Subsystem with
Blueprint-exposed events, so systems can be tested alone and reused by
player, zombies and bandits.

  --------------------------------------------------------------------------------
  System         C++ class (suggested)          Responsibility
  -------------- ------------------------------ ----------------------------------
  Player         ARFCharacter                   First-person body + arms, Enhanced
                                                Input, interaction traces

  Movement       URFMovementComponent (extends  Sprint, crouch, vault, climb,
                 UCharacterMovementComponent)   swim, encumbrance, surface-based
                                                footstep noise

  Stats          URFSurvivalStatsComponent      Hunger, thirst, fatigue, Energy,
                                                stamina, temperature, wetness,
                                                stress, boredom

  Moodles        URFMoodleComponent             Reads stats/health, computes
                                                moodle levels, fires
                                                OnMoodleChanged

  Body health    URFBodyHealthComponent         17 body parts, wounds, bandages,
                                                infection, pain, healing over time

  Infection      URFInfectionComponent          48 h timer from bite, symptom
                                                stages, death and reanimation

  Inventory      URFInventoryComponent          Items, weight, equipment slots,
                                                durability

  Crafting       URFCraftingComponent           Crafting-mat recipe matching from
                                                a Data Table

  Building       URFBuildComponent +            Blueprint ghost placement,
                 ARFBuildGhost +                snapping, material deposit,
                 ARFBuildablePiece              free-form lines, tiers, repair,
                                                deconstruct

  Structure HP   URFStructureHealthComponent    Per-piece HP, damage states (mesh
                                                swap), tier resistances, spike
                                                damage-back

  Noise          URFNoiseSubsystem              Receives noise events, applies
                 (UWorldSubsystem)              occlusion and weather, notifies
                                                listeners via a spatial grid

  Combat         URFMeleeComponent,             Swings, stamina cost, hit
                 URFRangedComponent             locations, shove, grapple escape,
                                                firearms

  Zombies        ARFZombie + StateTree          Senses, states, herding, structure
                                                attacks, variants from Data Assets

  Horde sim      URFHordeSubsystem              Distant zombies as lightweight
                                                data groups; spawn actors near the
                                                player, despawn far away

  Bandits        ARFBandit + StateTree + EQS    Patrol, shout, cover, flank,
                                                retreat, raid

  Skills         URFSkillsComponent             XP by action, level effects

  Time/weather   URFWorldStateSubsystem         Day length, weather, seasons,
                                                light levels

  Save           URFSaveSubsystem + USaveGame   Every persistent actor keyed by a
                                                stable GUID

  Settings       URFSandboxSettings (Data       All sandbox options in one place
                 Asset + save)                  
  --------------------------------------------------------------------------------

### Engine features to use

-   **World Partition** for the map, **PCG framework** for forest,
    foliage and overgrowth scatter (with rules for ivy on ruins and
    trees inside buildings), **Nanite** for static meshes, **Lumen** and
    **Virtual Shadow Maps** for lighting, true darkness at night (no
    forced auto-exposure brightening).

-   **Enhanced Input** for all controls. **CommonUI/UMG** for HUD:
    moodle stack, health panel, inventory crafting mat, Survival Book,
    paper map (no minimap, no quest markers).

-   **StateTree** (or Behavior Trees) for AI. **Significance Manager**
    and **Animation Budget Allocator** to throttle distant zombies;
    evaluate vertex-animated impostors for very distant hordes.

-   **MetaSounds**, attenuation and occlusion settings, and Audio
    Gameplay Volumes for interiors.

-   **IK Retargeter** to retarget Epic\'s free animation content onto
    the project skeleton.

-   Data Tables and Primary Data Assets for items, recipes, buildables,
    zombie variants and bandit loadouts. Adding a new item must never
    require C++.

### Key implementation rules

-   **Building must feel like The Forest:** place a ghost, then add each
    material by hand, one unit at a time, with a sound and a visible
    piece appearing. Metal plating and welding use the same flow on top
    of existing pieces.

-   **Structure damage stacks:** each zombie hit applies damage to the
    piece it touches; spiked pieces deal damage back each hit; metal
    tier resists. Damaged states swap meshes at 66% and 33% HP; at 0 HP
    the piece breaks into physics debris and leaves a gap.

-   **Noise drives everything:** every action that makes sound calls the
    Noise Subsystem with the radius from the noise table. Draw radii
    with a debug console command.

-   **Infection timer is authoritative:** stored as \"in-game time of
    bite\" in the save, not as a countdown, so it stays correct across
    save, load and time-skips from sleeping.

-   **Death flow:** on death, spawn a zombie with the player\'s
    appearance and inventory at the death location, then start character
    creation in the same world.

-   **Bandits must be loud:** every bandit action broadcasts its shout
    or gunshot as a noise event that zombies also hear.

### Debug and test tools (build these early)

-   Console commands: spawn N zombies at cursor, spawn bandit group, set
    time, set weather, give item, set infection hours, god mode, show
    noise radii, show AI states, show structure HP.

-   Automation tests (UE Automation / Functional Tests) for: infection
    reaches death exactly 48 in-game hours after the bite including
    across save/load; noise events reach only listeners in range; 20
    zombies break an unplated log wall faster than 5; metal plating
    reduces damage; every recipe in the Data Table is craftable and
    produces its output.

### Working rules

-   After every feature: compile with zero errors, run in
    Play-In-Editor, check the Output Log for new errors and warnings,
    run the automation tests. A feature isn\'t done until all four pass.

-   Use version control (Git with Git LFS for binary assets, or
    Perforce). Commit per feature with a clear message.

-   Performance target: 60 fps at 1080p on an RTX 3060-class GPU with
    150 active zombies near the player. Profile with Unreal Insights at
    every milestone.

-   When an asset is missing or broken, keep working with a placeholder,
    log it in the manifest as Blocked with the reason, and tell the 3D
    Modeler exactly what to fix.

-   Report at the end of every milestone: what works, test results,
    frame-time numbers, known bugs, assumptions.

## Handoff contract (all agents)

All three agents share one folder structure, one naming scheme and one
asset manifest. The manifest is how agents talk to each other: nothing
counts as delivered until its row says so.

### Folder structure

ROOTFALL/\
Concept/ CA\_ images and style guide (Agent 1)\
Source/Blender/ .blend source files (Agent 2)\
Export/FBX/ exported meshes and animations (Agent 2)\
Export/Textures/ exported texture sets (Agent 2)\
Unreal/ROOTFALL/ the UE 5.8 project (Agent 3)\
Content/RF/Characters, Environment, Buildables, Weapons, Props, Foliage,
Audio, UI, Data, Maps\
Manifest/asset_manifest.csv\
Reports/ one report per agent per task

### Naming

  ------------------------------------------------------------------------------
  Prefix           Asset type                Example
  ---------------- ------------------------- -----------------------------------
  CA\_             Concept image             CA_Zombie_Soldier_Turnaround.png

  SM\_             Static mesh               SM_Build_LogWall_T1_Intact

  SK\_             Skeletal mesh             SK_Zombie_Civilian_01

  SKEL\_           Skeleton                  SKEL_RF_Humanoid

  A\_              Animation sequence        A_FPArms_Chop_Heavy

  T\_              Texture (suffix \_BC,     T_LogWall_N
                   \_N, \_ORM, \_E)          

  M\_ / MI\_       Material / material       MI_RustMetal_Plate
                   instance                  

  BP\_             Blueprint                 BP_Buildable_SpikePit

  ABP\_            Animation Blueprint       ABP_Zombie

  DA\_ / DT\_      Data Asset / Data Table   DA_Zombie_Soldier, DT_Recipes

  WBP\_            Widget Blueprint          WBP_MoodleStack

  SFX\_ / MS\_     Sound wave / MetaSound    MS_Zombie_HordeBed

  UCX\_ / SOCKET\_ Collision hull / socket   UCX_SM_Build_LogWall_T1_Intact_00
                   (inside FBX)              
  ------------------------------------------------------------------------------

Buildable tiers use T1 (log), T2 (plank-reinforced), T3 (metal-plated);
damage states use \_Intact, \_Damaged, \_Broken. Names use PascalCase
with underscores, no spaces.

### Asset manifest

One row per asset, updated by whoever changes its status. Status values:
Planned, Concept Done, Greybox, Modeled, Textured, Rigged, Exported,
Imported, In Game, Blocked.

asset_id,type,concept_file,blend_file,export_file,triangles,normal_map_format,status,owner,notes\
Zombie_Civilian_01,Character,CA_Zombie_Civilian_Turnaround.png,Zombie_Civilian_01.blend,SK_Zombie_Civilian_01.fbx,28400,DirectX,Imported,Agent
3,Retargeted shamble OK\
Build_LogWall_T1,Buildable,CA_Buildables_Sheet.png,Build_LogWall.blend,SM_Build_LogWall_T1_Intact.fbx,6200,DirectX,Exported,Agent
2,Damaged and Broken states included

### Report template (every agent, every task)

-   Done: what was produced (file names).

-   Verified: how each item was checked.

-   Assumptions: anything decided without a clear spec.

-   Blocked: what is missing and who must fix it.

-   Next: what the next agent needs to know.

## Milestones and acceptance tests

The vertical slice is done when all nine milestones pass, in order. Each
test is something a person can do in the build and see succeed.

1.  **M0 Setup.** UE 5.8 C++ project, folders, naming, manifest, version
    control, debug command framework.

    -   Project compiles cleanly; an empty test map opens; one
        automation test runs and passes.

2.  **M1 Player and movement (greybox).** First-person body and arms,
    walk, sprint, crouch, jump, vault, climb, swim, stamina,
    encumbrance, footstep noise.

    -   Sprinting drains stamina and stops at zero; carrying two logs
        blocks attacking; footsteps on glass are louder than on grass
        (shown by the noise debug view).

3.  **M2 Survival and health.** Stats, all moodles, 17-part body health,
    wounds and treatments, wound infection, zombie infection timer,
    death and reanimation.

    -   A bite shows the Bitten moodle at once; symptoms appear on
        schedule; death happens at exactly 48 in-game hours, including
        after sleeping and after a save/load; the dead player rises as a
        zombie carrying their gear.

4.  **M3 Combat, zombies and noise.** Melee, shove, grapple escape, bow,
    one firearm, zombie states, herding, head-kill rule, noise
    subsystem, horde simulation.

    -   One zombie is easy to kill; 15 zombies in a street reliably
        overwhelm a player who stands still; a pistol shot pulls zombies
        from about 120 m; a crouching player passes a zombie\'s back
        unnoticed.

5.  **M4 Building and fortifications.** Survival Book, ghost placement,
    hand-deposited materials, free-form walls, tree felling, all
    fortifications, welding, structure HP, zombie structure attacks.

    -   A log wall goes up one log at a time; welding a plate onto it
        raises its HP; 20 zombies break an unplated wall clearly faster
        than 5; a spike pit kills a zombie that walks into it and then
        needs re-arming.

6.  **M5 Inventory, crafting, skills, loot and save.** Crafting mat,
    recipes, workstations, skills, lootable containers, full world
    persistence.

    -   Craft a spear, a bandage and a spiked wall from looted and
        gathered materials; quit and reload: felled trees, built pieces
        with their HP, looted containers and corpses are all as they
        were.

7.  **M6 Bandits and wildlife.** Bandit groups, camps, raids, deer,
    rabbits, birds, feral dogs.

    -   A bandit group can be heard well before it is seen; its gunfire
        draws zombies into the fight; birds go quiet when threats are
        near.

8.  **M7 World and art integration.** 1 km x 1 km map with the first
    three biomes, PCG foliage and overgrowth, final assets from the
    manifest, weather, day-night, full audio.

    -   Every manifest asset marked In Game appears correctly lit and
        scaled; nights are dark enough that a flashlight matters; rain
        lowers noise radii.

9.  **M8 Polish and performance.** Sandbox settings menu, accessibility
    options, bug fixing, profiling.

    -   60 fps at 1080p on an RTX 3060-class GPU with 150 zombies near
        the player; a new player survives the first night only by
        building or hiding, and dies when careless; all automation tests
        pass.
