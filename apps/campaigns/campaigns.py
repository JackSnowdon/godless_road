from decimal import Decimal

from django.db.models import Sum

from apps.campaigns.models import Stockpile


class ResourceService:
    def __init__(self, stockpile: Stockpile):
        self.stockpile = stockpile

    def get_resource_amount(self, resource) -> Decimal:
        amount = self.stockpile.resource_amounts.filter(
            resource=resource,
        ).first()

        if amount is None:
            return Decimal("0")

        return amount.quantity

    def get_carried_weight(self) -> Decimal:
        if self.stockpile.context != Stockpile.Context.CARAVAN:
            return Decimal("0")

        result = self.stockpile.resource_amounts.aggregate(
            total_weight=Sum(
                "quantity" * "resource__weight_per_unit"
            )
        )

        return result["total_weight"] or Decimal("0")