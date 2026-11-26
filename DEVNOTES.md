## Current position

The campaigns app now exposes a read-only campaign-state endpoint:

GET /api/campaigns/<id>/state/

It returns the current day, block, phase, caravan capacity,
and resources held in the caravan and camp stockpiles.

## Next tiny step

Add POST /api/campaigns/<id>/advance-time/.

The endpoint should call TimeService.advance_block(), return the
updated campaign state, and translate InsufficientSuppliesError into
a 400 Bad Request response.

## First test

test_advance_time_endpoint_advances_one_block