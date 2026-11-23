## Current position

The campaigns app now has a basic survival loop:

- Campaign time advances through six daily blocks.
- Advancing from Dusk begins the next day at Night.
- The day transition triggers daily Food and Water consumption.
- Consumption is atomic: insufficient Food or Water prevents the
  day from advancing and leaves resources unchanged.
- Caravan supplies are consumed; camp supplies remain in storage.

## Next tiny step

Introduce InsufficientSuppliesError so the time service can clearly
communicate that the caravan cannot afford another day.

## After that

Expose a minimal campaign-state and time-advancement API so the React
client can display the current day, block, resources, and caravan state.