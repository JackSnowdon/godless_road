const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function getCampaignState(campaignId) {
  const response = await fetch(
    `${API_BASE_URL}/api/campaigns/${campaignId}/state/`
  );

  if (!response.ok) {
    throw new Error("Failed to load campaign state.");
  }

  return response.json();
}

export async function advanceCampaignTime(campaignId) {
  const response = await fetch(
    `${API_BASE_URL}/api/campaigns/${campaignId}/advance-time/`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));

    throw new Error(data.detail ?? "Failed to advance time.");
  }

  return response.json();
}