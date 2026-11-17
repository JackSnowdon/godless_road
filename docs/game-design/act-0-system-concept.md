# Godless Road — Act 0 System Contract

## Purpose

Act 0 is the first playable arc of Godless Road.

It proves the core survival loop:

> Choose where to camp, allocate limited people, act during the day,
> survive the night, and decide whether to remain or move.

The player leads a small caravan through a hostile, godless world for
14 in-game days. The goal is not conquest or expansion. The goal is to keep
the caravan alive long enough to find a viable future.

## Player promise

The player should feel that every day presents a difficult trade-off between:

- Safety
- Progress
- Mobility
- People
- Resources
- Information

No decision should be free. Every meaningful action should require the player
to give something up.

## Campaign structure

- The campaign is continuous.
- Act 0 lasts 14 in-game days.
- Each day has a clear day/night cycle.
- The player may save and reload at any point during development.
- Losing every Survivor ends the run.
- Heroes do not permanently die in Act 0.
- Heroes can be injured, exhausted, incapacitated, or unable to fight.

## Core loop

1. Review the caravan and camp status.
2. Choose whether to remain at the current camp or move.
3. Assign Followers to Scout, Worker, and Combatant roles.
4. Assign Heroes and their Retinues to camp duties, buildings, or missions.
5. Build, repair, scout, harvest, or launch a mission.
6. Prepare for the night using available information and resources.
7. Resolve the night defence.
8. Apply consequences: resources, injuries, morale, exposure, and damage.
9. Make the next daily decision.

## Day structure

Each day has five phases:

| Phase | Player activity | What resolves |
|---|---|---|
| Morning | Review status, threats, resources, and available actions | New threats, completed missions, overnight changes |
| Daytime | Assign crews, build, travel, scout, or launch missions | Production, construction, movement, mission progress |
| Dusk | Make final preparations and recall or reinforce crews | Returning crews, exposure increase, defensive readiness |
| Night | Issue limited orders and trigger skills during defence | Combat, casualties, damage, resource loss |
| Dawn | Review consequences and choose the next action | Survivor state, morale, exposure, new opportunities |

## What the player controls

The player controls the caravan at a strategic level.

The player can:

- Choose a camp square.
- Move the caravan one square per travel action.
- Establish, improve, or dismantle a camp.
- Assign Followers to roles.
- Assign Heroes to duties, buildings, or missions.
- Launch missions.
- Build, repair, and upgrade structures.
- Review scouting information.
- Prepare night defences.
- Issue a limited number of night orders.
- Trigger Hero abilities, traps, or emergency responses during night defence.
- Save and load the campaign.

The player does not directly control every individual Survivor during normal
gameplay. Followers are managed as role pools, crews, and assignments.

## What the game automates

The game automatically resolves:

- Resource production.
- Daily consumption.
- Building output.
- Mission progress.
- Travel time.
- Camp exposure growth.
- Enemy approach routes.
- Most combat during night defence.
- Building and trap behaviour.
- Hero passive camp effects.
- Injury and recovery progression.
- Campaign consequences.

The player prepares the camp and issues high-impact orders. The game resolves
the majority of the simulation.

## Out of scope for Act 0

The following are deliberately excluded from Act 0:

- Settlements.
- Trade economy.
- Diplomacy.
- Faction cities.
- Independent Heroes.
- Large procedural world generation.
- Full fog-of-war simulation.
- Complex enemy AI.
- Large-scale city building.
- Permanent settlements.
- Permadeath.
- Advanced crafting.
- Detailed individual Survivor simulation.
- Multiplayer.
- Mobile-specific controls.
- Final art, audio, and narrative content.

These systems may influence future data design, but they must not expand the
Act 0 implementation scope.

## Overmap

Act 0 uses a small square-grid overmap.

- Each square represents a region, not a single room or building.
- The caravan begins at one square.
- The camp initially occupies one square.
- The caravan moves one square per travel action.
- Terrain affects movement, resources, defence, exposure, and mission options.
- Nearby locations are represented as nodes or points of interest.
- Mission distance is measured in squares.
- Distance affects travel time, supply cost, mission duration, risk, and reward.
- The player begins with limited knowledge of the map.
- Scouting reveals information about nearby nodes, threats, and routes.

The first overmap should be small enough that the player can understand it at
a glance, but large enough to create meaningful choices.

## Camp

The camp is a temporary, improvised refuge.

- The player must establish a camp before assigning camp roles or building.
- The War Tent is the first required camp structure.
- The War Tent enables role assignment, camp orders, and organised defence.
- The initial camp occupies one overmap square.
- Context-appropriate buildings may fit within the initial camp square.
- Additional adjacent squares may be claimed later as the caravan grows.
- Camp buildings may be portable, reusable, or site-bound.
- Moving camp costs time and supplies.
- Site-bound buildings and improvements may be lost or abandoned.
- Leaving a camp may leave evidence behind.

## Followers and roles

Act 0 uses three broad Follower roles:

| Role | Primary purpose | Typical assignments |
|---|---|---|
| Scout | Information and early warning | Scouting nodes, tracking threats, patrols |
| Worker | Production, construction, and support | Buildings, resource extraction, repairs |
| Combatant | Defence and dangerous work | Camp guard, mission escort, night defence |

Initial rules:

- Followers are represented as role pools, not individual units.
- The player assigns available Followers to roles.
- Followers assigned to a role may be further assigned to a building, mission,
  patrol, or camp duty.
- A Hero must retain a minimum Retinue.
- The minimum Retinue is initially five Followers per Hero.
- Retinue members are conceptually named and persistent, even if Act 0 does not
  yet simulate each one individually.
- A Hero’s Retinue cannot be fully reassigned away from that Hero.

## Heroes

Heroes are leaders, protectors, and specialists.

- There are three starting Heroes.
- Each Hero has an affinity: Ember, Verdant, or Aether.
- Each Hero has a Retinue.
- Each Hero has a Command Capacity.
- A Hero may lead a mission, support a building, or defend the camp.
- A Hero leading a mission is unavailable for camp defence until they return.
- A Hero at camp provides a meaningful camp effect, even if they are not on the
  frontline.
- An injured or exhausted Hero may provide reduced support but cannot fight.
- Heroes may work outside their preferred affinity, but with reduced effectiveness
  or increased risk.

Hero camp effects should be visible and understandable.

Example:

```text
Mara — Support
+10% Worker repair speed
+5% morale recovery
Can trigger Rootbind once during night defence
```

## Resources

Act 0 uses two resource layers.

### Survival resources

| Resource | Purpose | Main source | Main sink |
|---|---|---|---|
| Water | Keeps Followers alive and supports cooking | Streams, wells, rain collection | Daily consumption, cooking, medicine |
| Food | Keeps Followers alive and supports morale | Foraging, missions, basic production | Daily consumption, missions, travel |
| Materials | Builds, repairs, and improves the camp | Salvage, ruins, forests, mines | Construction, repairs, defences |

### Arcane resources

| Resource | Fantasy role | Main use |
|---|---|---|
| Ember | Fire, warmth, destruction, forging | Combat, fuel, forging, purification |
| Verdant | Growth, restoration, life | Food, healing, water purification, land recovery |
| Aether | Power, machinery, knowledge | Generators, wards, detection, advanced devices |

### Refined resources

Act 0 may introduce a small number of refined resources only where they create
a meaningful decision:

- Purified Water
- Preserved Food
- Timber
- Metal Components

Refined resources are not required for every system. They should be added only
when they create a new choice for the player.

### Conversion

Arcane resources may be converted into survival resources as a last resort.

Conversion must be:

- Expensive.
- Inefficient.
- Limited.
- Thematically costly.
- Clearly presented as an emergency option.

Arcane resources must not become a replacement for the survival economy.

## Economy rules

Every resource must have at least one source and one meaningful sink.

| Resource | Source | Sink | Pressure |
|---|---|---|---|
| Water | Streams, wells, rain | Daily use, cooking, medicine | Camp location and storage |
| Food | Foraging, missions, production | Daily use, missions, travel | Population and travel |
| Materials | Salvage, forests, mines | Building, repair, defence | Site depletion and maintenance |
| Ember | Relics, combat, rituals | Fuel, forging, warmth | Dangerous acquisition |
| Verdant | Living land, rituals, healing | Food, medicine, purification | Blighted terrain |
| Aether | Machines, relics, rifts | Power, wards, detection | Corruption and discovery |

The economy should create scarcity without making the player feel permanently
starved. Sources and sinks must remain visible and understandable. [346][351]

## Missions

Missions are the caravan’s main way to gain resources, information, and progress.

A mission must define:

- A goal.
- A location.
- A distance from camp.
- An expected duration.
- A risk profile.
- Required or preferred crew composition.
- Potential rewards.
- Possible complications.
- Consequences for success, partial success, withdrawal, and failure.

Mission duration is calculated from:

```text
Travel time + objective time + return time
```

Distance affects:

- Travel time.
- Food and water consumption.
- Carry capacity.
- Return risk.
- Reward potential.
- Hero availability.
- Camp exposure.

Act 0 should include at least:

- One scouting mission.
- One salvage or resource mission.
- One threat-clearing mission.

## Camp exposure

Camp exposure represents how closely the world has noticed the caravan.

- Exposure begins low when a new camp is established.
- Exposure rises while the caravan remains in one place.
- Exposure rises faster at resource-rich or high-activity locations.
- Exposure rises after certain missions, building activity, or noisy actions.
- Exposure may be reduced by moving camp, concealment, scouting, or destroying
  enemy scouts.
- Night attacks begin after exposure reaches a defined threshold.
- Higher exposure produces larger, more organised, or more frequent attacks.
- Reaching maximum exposure triggers a major assault, pursuit, or forced
  evacuation decision.

The player must always be able to see current exposure and understand what is
increasing it.

## Night defence

Night defence is a mostly automated camp defence encounter.

- Night attacks begin only after camp exposure reaches the attack threshold.
- A typical camp has 2–4 approach routes.
- Routes are determined by terrain and camp location.
- Routes have a direction and a character, such as narrow ravine, open road,
  forest trail, or ruined street.
- Enemies approach through routes appropriate to the threat and terrain.
- Defenders, buildings, traps, and Hero effects operate automatically.
- The player issues a limited number of orders during the defence.
- The player can trigger Hero abilities, traps, emergency repairs, or fallback
  orders.
- Daytime choices must visibly affect the night defence.
- A failed defence causes resource loss, structural damage, injuries, morale loss,
  and increased exposure.

The player should never feel that a Hero at camp is doing nothing. Heroes
assigned to camp provide support effects, command benefits, or limited abilities.

## Randomness and information

Randomness should create risk management, not replace player decision-making.

- Major mission and defence outcomes should be based on visible factors.
- Unknown nodes may contain uncertain information.
- Scouting reduces uncertainty.
- Hero skills, equipment, and preparation reduce risk.
- The player should understand what was known, what was uncertain, and what
  preparation changed.
- Randomness should not be presented as a simple “success chance” where possible.

Mission outcomes may include:

- Full success.
- Partial success.
- Withdrawal.
- Failure.
- Disaster.

Each outcome should have understandable causes and consequences.

## Progression

Act 0 progression should expand options without removing scarcity.

Progression may come from:

- Hero experience.
- Foreman experience.
- Building upgrades.
- New building types.
- Better equipment.
- New mission types.
- Larger Retinues.
- Improved scouting.

New capability should create new needs:

- A larger caravan requires more food and water.
- Better defences require more maintenance.
- More Heroes require more arcane resources.
- Better missions require preparation and equipment.
- Future settlements will require supply lines and protection.

## Crisis and recovery

The game should avoid softlocks and unwinnable resource spirals.

In a crisis, the player should always have at least two imperfect options.

A crisis may remove comfort, safety, or efficiency, but it should not remove
the player’s ability to act.

Every crisis should offer choices with real trade-offs between:

- Safety
- Progress
- Mobility
- People
- Resources
- Information

Resource scarcity should escalate through Caution, Critical, Dire, and Terminal
states. It should create pressure and force difficult decisions, but it should
not immediately end the run.

The run ends only when every Survivor is lost.

Emergency actions may be expensive, inefficient, or morally costly, but they
should provide a path through extreme situations.

## Act 0 difficulty intent

Act 0 is a teaching arc, not a brutal survival challenge.

Its purpose is to help the player understand and enjoy the core loop:

- Choose a camp location.
- Allocate Followers and Heroes.
- Run simple missions.
- Develop a basic camp.
- Survive a readable night threat.
- Decide whether to remain or move.

Early failures should be recoverable. Resource scarcity, camp exposure, and
night threats should create tension without creating a punishing spiral.

The first three days should focus on establishing the caravan and learning the
core systems. Pressure should rise gradually across the 14-day arc.

The player should finish Act 0 feeling capable, curious, and motivated to
continue beyond the initial region.

## Failure states

The campaign ends if every Survivor is lost.

A Hero may be injured or incapacitated, but cannot permanently die in Act 0.

A failed mission or night defence should create consequences, not an immediate
run-ending state:

- Lost resources.
- Injured Followers.
- Damaged buildings.
- Reduced morale.
- Increased exposure.
- Lost opportunities.
- Delayed progress.

The game should avoid a downward spiral where one early failure makes recovery
impossible.

## Acceptance criteria

Act 0 is complete when the following are true.

### Campaign

- A new campaign can be started.
- The player can save and load the campaign.
- The campaign advances through a day/night cycle.
- The campaign reaches day 14.
- Losing all Survivors ends the run.
- Heroes cannot permanently die during Act 0.

### Overmap

- The player can see a square-grid overmap.
- The player can identify their current camp square.
- The player can identify nearby nodes.
- The player can move the caravan one square per travel action.
- Terrain affects at least one meaningful gameplay factor.
- Distance affects mission duration, supply cost, or risk.

### Camp

- The player can establish a camp.
- The player must place a War Tent before organising the camp.
- The player can assign Followers to Scout, Worker, and Combatant roles.
- The player can assign Heroes to camp duties, buildings, or missions.
- Each Hero retains a minimum Retinue.
- The player can build at least three basic structures.
- The player can see camp exposure.
- Camp exposure rises over time.
- Moving camp resets or reduces exposure.

### Missions

- The player can launch at least three mission types.
- A mission requires a crew.
- A mission consumes supplies.
- A mission takes time.
- A mission returns resources, information, injuries, or consequences.
- A Hero leading a mission is unavailable at camp until they return.
- Mission results are influenced by crew composition, Hero presence, distance,
  supplies, and scouting information.

### Night defence

- Night attacks begin after camp exposure reaches its threshold.
- The camp has between two and four approach routes.
- Terrain determines the routes.
- The player can prepare defences before the attack.
- The player can issue a limited number of orders during the attack.
- The player can trigger at least one Hero ability or trap.
- Buildings and defenders operate automatically.
- A successful defence preserves the camp.
- A failed defence causes meaningful but recoverable consequences.

### Economy

- Water, Food, and Materials are consumed daily.
- Ember, Verdant, and Aether affect Hero, building, or mission systems.
- Every resource has at least one source and one sink.
- The player can see current resource stockpiles.
- The player can identify why a resource is rising or falling.
- Arcane conversion is possible but costly and limited.

### Player understanding

After playing Act 0, a player should be able to answer:

1. Why did we camp here?
2. Who is doing what?
3. What are we short of?
4. Why is camp exposure rising?
5. What will attack tonight?
6. Which route is most dangerous?
7. What did our daytime choices change?
8. Should we stay or move tomorrow?

## Definition of done

Act 0 is done when a player can complete a 14-day campaign using the systems
above, understand the consequences of their decisions, and reach at least one
meaningful end state without needing systems that are explicitly out of scope.

## Open questions

These questions should be answered during implementation, not before it:

- Exact starting Survivor counts.
- Exact starting resource amounts.
- Exact Hero Command Capacity values.
- Exact camp exposure thresholds.
- Exact mission durations and rewards.
- Exact night-defence wave composition.
- Exact building costs and production rates.
- Exact terrain modifiers.
- Exact map size and node placement.

These are balance values, not system boundaries. They should be tuned through
playtesting after the systems exist.