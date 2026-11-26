from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.campaigns.models import Campaign
from apps.campaigns.serializers import CampaignStateSerializer
from apps.campaigns.services import (
    InsufficientSuppliesError,
    TimeService,
)


class CampaignStateView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        campaign = get_object_or_404(Campaign, pk=pk)

        serializer = CampaignStateSerializer(campaign)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CampaignAdvanceTimeView(APIView):
    def post(self, request: Request, pk: int) -> Response:
        campaign = get_object_or_404(Campaign, pk=pk)

        time_service = TimeService(campaign)

        try:
            time_service.advance_block()
        except InsufficientSuppliesError as error:
            return Response(
                {"detail": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        campaign.refresh_from_db()

        serializer = CampaignStateSerializer(campaign)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )