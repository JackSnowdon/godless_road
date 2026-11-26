## Current position

The campaigns app now has a basic survival loop:

- Campaign time advances through six daily blocks.
- Advancing from Dusk begins the next day at Night.
- The day transition triggers daily Food and Water consumption.
- Consumption is atomic: insufficient Food or Water prevents the
  day from advancing and leaves resources unchanged.
- Caravan supplies are consumed; camp supplies remain in storage.
- InsufficientSuppliesError clearly represents a shortage outcome.

## Next tiny step

Design and implement a minimal campaign-state API.

The first endpoint should return the data needed by the React client:

- Campaign ID
- Current day
- Current block
- Caravan survivor count
- Caravan carry capacity
- Caravan stockpile resources
- Camp stockpile resources

## After that

Add a time-advancement endpoint that calls TimeService.advance_block()
and translates InsufficientSuppliesError into a clear API error response.