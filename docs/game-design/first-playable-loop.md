# Godless Road — First Playable Loop

## One-sentence pitch

Lead a desperate caravan through a hostile, godless world: choose where to camp,
allocate Survivors to Heroes and jobs, run missions for resources, and defend the
camp through the night.

## Core question

> Do we stay here another day, or move before the world finds us?

## Core loop

1. Choose a camp square on the overmap.
2. Place the War Tent and establish a temporary camp.
3. Assign Followers to Scout, Worker, and Combatant roles.
4. Assign Heroes and their Retinues to buildings, jobs, or missions.
5. Run daytime missions or develop the camp.
6. Face a night defence shaped by terrain, camp exposure, and daytime choices.
7. Resolve rewards, injuries, morale, resources, and camp exposure.
8. Decide whether to remain, move, or prepare for a larger threat.

## First playable scope

### Must have

- One small square-grid overmap.
- One caravan with a camp location.
- One-square camp footprint.
- One square of movement per travel action.
- Three starting Heroes.
- Followers as aggregate role pools: Scouts, Workers, Combatants.
- Hero Retinues with a minimum crew size.
- A War Tent as the first required camp structure.
- Basic buildings and job assignments.
- Basic resources.
- Simple daytime missions.
- Camp exposure.
- Night defence with 2–4 terrain-defined approach routes.
- Day/night cycle.
- Simple mission rewards and consequences.

### Should have

- Scouting reports that reveal nearby nodes and night threats.
- Foremen who improve crew effectiveness and camp setup.
- Terrain that affects movement, defence, resources, and exposure.
- Portable, reusable, and site-bound buildings.
- Multi-day missions.
- Mission rewards affected by distance and travel logistics.

### Could have

- Individual named Followers.
- Follower traits, injuries, and progression.
- Enemy corpse barricades.
- Deeper mission generation.
- Settlement foundations.
- Trade routes.
- Faction cities and independent Heroes.

### Explicitly out of scope

- Settlements.
- Trade economy.
- Diplomacy.
- Large procedural worlds.
- Complex enemy AI.
- Full city building.
- Permanent base building.
- Permadeath.
- Advanced combat systems.
- Multiplayer.

## Player-facing resources

For the first version, use three broad resource families:

- Food: keeps Survivors alive and supports morale.
- Materials: builds, repairs, and improves the camp.
- Aether: powers advanced structures, defence, and Hero abilities.

These should remain broad categories rather than dozens of highly specific
resources at first.

## Hero and crew model

- Heroes lead crews.
- Each Hero has a minimum Retinue.
- Workers are a flexible caravan population pool.
- Retinue members are named, persistent Followers attached to a Hero.
- A Hero’s presence improves crew safety, effectiveness, morale, or mission access.
- Heroes may operate outside their preferred affinity, but with reduced effectiveness
  or increased risk.

## Camp and movement

- The camp begins as one overmap square.
- Context-appropriate buildings can initially fit within that square.
- Additional adjacent squares may be claimed later as the caravan grows.
- Moving the camp costs time and supplies.
- Some improvements travel with the caravan; others are site-bound.
- Leaving a camp may leave traces, increasing future danger or revealing information.

## Night defence

- Night attacks begin after camp exposure reaches a defined threshold.
- Terrain determines 2–4 approach routes.
- Routes have a direction and a character, such as narrow ravine, open road,
  forest trail, or ruined street.
- The player improves, blocks, funnels, or deliberately leaves routes open.
- Heroes and Combatants defend the camp.
- Workers can repair, support, and maintain defences.
- Daytime choices should visibly affect the night threat.

## Success criteria

The first playable version succeeds if a player can:

1. Choose a camp location.
2. Understand what is nearby.
3. Allocate Followers and Heroes.
4. Complete at least one daytime mission.
5. Experience a night defence influenced by those choices.
6. Decide whether staying or moving is the better next choice.

## Next implementation slice

Start with the smallest complete strategic foundation:

1. Define the initial resource types.
2. Create the Caravan aggregate state.
3. Create the overmap grid and camp placement.
4. Add Followers as role pools.
5. Add the War Tent and basic camp buildings.