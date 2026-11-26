from django.urls import path

from apps.campaigns.views import (
    CampaignAdvanceTimeView, 
    CampaignStateView,
)


urlpatterns = [
    path(
        "campaigns/<int:pk>/state/",
        CampaignStateView.as_view(),
        name="campaign-state",
    ),
    path(
        "campaigns/<int:pk>/advance-time/",
        CampaignAdvanceTimeView.as_view(),
        name="campaign-advance-time",
    ),
]