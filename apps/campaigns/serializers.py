from decimal import Decimal

from rest_framework import serializers

from apps.campaigns.models import Campaign, Caravan, Stockpile
from apps.campaigns.services import ResourceService


BLOCK_NAMES = {
    1: "Night",
    2: "Dawn",
    3: "Morning",
    4: "Afternoon",
    5: "Evening",
    6: "Dusk",
}


class CaravanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    survivor_count = serializers.IntegerField(read_only=True)
    carry_capacity = serializers.IntegerField(read_only=True)
    carried_weight = serializers.SerializerMethodField()
    available_capacity = serializers.SerializerMethodField()

    def _format_decimal(self, value: Decimal) -> str:
        return str(value.quantize(Decimal("0.01")))

    def get_carried_weight(self, caravan: Caravan) -> str:
        stockpile = caravan.campaign.stockpiles.get(
            context=Stockpile.Context.CARAVAN,
        )

        resource_service = ResourceService(stockpile)

        return self._format_decimal(
            resource_service.get_carried_weight()
        )

    def get_available_capacity(self, caravan: Caravan) -> str:
        stockpile = caravan.campaign.stockpiles.get(
            context=Stockpile.Context.CARAVAN,
        )

        resource_service = ResourceService(stockpile)

        return self._format_decimal(
            resource_service.get_available_capacity()
        )


class ResourceAmountSerializer(serializers.Serializer):
    slug = serializers.CharField(source="resource.slug", read_only=True)
    name = serializers.CharField(source="resource.name", read_only=True)
    category = serializers.CharField(
        source="resource.category",
        read_only=True,
    )
    quantity = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )


class CampaignStateSerializer(serializers.Serializer):
    campaign_id = serializers.IntegerField(source="id", read_only=True)
    current_day = serializers.IntegerField(read_only=True)
    current_block = serializers.IntegerField(read_only=True)
    current_phase = serializers.SerializerMethodField()
    caravan = CaravanSerializer(read_only=True)
    caravan_resources = serializers.SerializerMethodField()
    camp_resources = serializers.SerializerMethodField()

    def get_current_phase(self, campaign: Campaign) -> str:
        return BLOCK_NAMES[campaign.current_block]

    def get_caravan_resources(self, campaign: Campaign) -> list:
        return self._get_resource_amounts(
            campaign,
            Stockpile.Context.CARAVAN,
        )

    def get_camp_resources(self, campaign: Campaign) -> list:
        return self._get_resource_amounts(
            campaign,
            Stockpile.Context.CAMP,
        )

    def _get_resource_amounts(
        self,
        campaign: Campaign,
        context: str,
    ) -> list:
        stockpile = campaign.stockpiles.filter(context=context).first()

        if stockpile is None:
            return []

        return [
            ResourceAmountSerializer(resource_amount).data
            for resource_amount in stockpile.resource_amounts.all()
        ]