## Current position

seed_demo_data command created resource templates, campaign, caravan,
stockpiles, and starting Food/Water amounts.

Fixed carry_capacity and stockpile capacity to use integers rather than
decimal strings.

## Current baseline

- Campaign: act-0-the-broken-road
- Caravan: The Last Road
- Survivors: 30
- Carry capacity: 100
- Caravan Food: 60
- Caravan Water: 60
- Camp capacity: 0

## Next tiny step

Run seed_demo_data, verify GET /api/campaigns/1/state/, then load
the React CampaignPage.