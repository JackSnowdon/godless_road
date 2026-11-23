## Current position

The campaigns app has a working survival-resource foundation:
Campaign, Caravan, ResourceTemplate, Stockpile, ResourceAmount,
ResourceService and ConsumptionService

Resource transfers between camp and caravan are implemented and tested.
Caravan carry capacity is enforced on transfers into the caravan.

## Future consumption depth

The basic daily consumption system currently requires enough Food
and Water for every Survivor. A failed consumption changes nothing.

Later, expand this into a rationing and quality system:

- Tiered Food and Water provide different benefits.
- Higher-tier supplies may grant temporary daily buffs.
- Players may choose to ration limited supplies.
- Rationing Food creates slower, accumulating consequences.
- Rationing Water creates faster, more severe consequences.
- Water is more vital than Food.
- Severe shortages may lead to fatigue, morale loss, injury,
  or survivor loss.

Do not implement this until the basic time advancement loop is complete.