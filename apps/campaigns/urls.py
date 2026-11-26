from django.urls import path

from apps.campaigns.views import (
    CampaignAdvanceTimeView, 
    CampaignStateView,
)


urlpatterns = [
    path(
        "<int:pk>/state/",
        CampaignStateView.as_view(),
        name="campaign-state",
    ),
    path(
        "<int:pk>/advance-time/",
        CampaignAdvanceTimeView.as_view(),
        name="campaign-advance-time",
    ),
]