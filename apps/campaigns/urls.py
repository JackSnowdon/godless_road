from django.urls import path

from apps.campaigns.views import CampaignStateView


urlpatterns = [
    path(
        "<int:pk>/state/",
        CampaignStateView.as_view(),
        name="campaign-state",
    ),
]