## Current position

The campaigns app has a working survival-resource foundation:
Campaign, Caravan, ResourceTemplate, Stockpile, ResourceAmount,
and ResourceService.

Resource transfers between camp and caravan are implemented and tested.
Caravan carry capacity is enforced on transfers into the caravan.

## Next tiny step

Add daily Food and Water consumption for the caravan.

Create a ConsumptionService or extend ResourceService with a method that
consumes the required Food and Water for the caravan’s current Survivor count.

## First test to write

test_daily_consumption_removes_food_and_water