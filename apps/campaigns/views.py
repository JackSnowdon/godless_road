from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.campaigns.models import Campaign
from apps.campaigns.serializers import CampaignStateSerializer


class CampaignStateView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        campaign = get_object_or_404(Campaign, pk=pk)

        serializer = CampaignStateSerializer(campaign)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )