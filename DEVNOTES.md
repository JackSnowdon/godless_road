## Current position

The Django API now supports the first campaign interaction loop:

- GET /api/campaigns/<id>/state/ returns campaign, caravan,
  and stockpile state.
- POST /api/campaigns/<id>/advance-time/ advances one time block.
- The day boundary triggers atomic Food and Water consumption.
- Insufficient supplies return a 400 response and leave state unchanged.

## Next tiny step

Create the React API module and first CampaignPage.

The page should display current time, caravan capacity, and resources,
then allow the player to advance time.

## First React tests

- getCampaignState requests the campaign state endpoint
- advanceCampaignTime posts to the advance time endpoint