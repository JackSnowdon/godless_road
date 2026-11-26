import { useEffect, useState } from "react";
import {
  advanceCampaignTime,
  getCampaignState,
} from "../api/campaigns.js";

const CAMPAIGN_ID = 1;

export default function CampaignPage() {
  const [campaign, setCampaign] = useState(null);
  const [error, setError] = useState(null);
  const [isAdvancing, setIsAdvancing] = useState(false);

  useEffect(() => {
    async function loadCampaign() {
      try {
        const state = await getCampaignState(CAMPAIGN_ID);

        setCampaign(state);
      } catch (loadError) {
        setError(loadError.message);
      }
    }

    loadCampaign();
  }, []);

  async function handleAdvanceTime() {
    setIsAdvancing(true);
    setError(null);

    try {
      const nextState = await advanceCampaignTime(CAMPAIGN_ID);

      setCampaign(nextState);
    } catch (advanceError) {
      setError(advanceError.message);
    } finally {
      setIsAdvancing(false);
    }
  }

  if (error) {
    return (
      <main>
        <h1>Godless Road</h1>
        <p>{error}</p>
      </main>
    );
  }

  if (!campaign) {
    return (
      <main>
        <h1>Godless Road</h1>
        <p>Loading campaign…</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Godless Road</h1>

      <section>
        <h2>
          Day {campaign.current_day} — {campaign.current_phase}
        </h2>

        <p>
          Survivors: {campaign.caravan.survivor_count}
        </p>

        <p>
          Carry capacity: {campaign.caravan.available_capacity} available
        </p>
      </section>

      <section>
        <h2>Caravan supplies</h2>

        {campaign.caravan_resources.length === 0 ? (
          <p>The caravan has no supplies.</p>
        ) : (
          <ul>
            {campaign.caravan_resources.map((resource) => (
              <li key={resource.slug}>
                {resource.name}: {resource.quantity}
              </li>
            ))}
          </ul>
        )}
      </section>

      <button
        onClick={handleAdvanceTime}
        disabled={isAdvancing}
      >
        {isAdvancing ? "Advancing…" : "Advance time"}
      </button>
    </main>
  );
}