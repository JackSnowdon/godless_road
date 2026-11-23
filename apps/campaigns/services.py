from decimal import Decimal

from django.db import transaction
from django.db.models import DecimalField, F, Sum

from apps.campaigns.models import (
    Campaign,
    Caravan,
    ResourceAmount,
    ResourceTemplate,
    Stockpile,
)


class ResourceService:
    def __init__(self, stockpile: Stockpile):
        self.stockpile = stockpile

    def get_resource_quantity(self, resource) -> Decimal:
        resource_amount = self.stockpile.resource_amounts.filter(
            resource=resource,
        ).first()

        if resource_amount is None:
            return Decimal("0.00")

        return resource_amount.quantity

    def get_carried_weight(self) -> Decimal:
        if self.stockpile.context != Stockpile.Context.CARAVAN:
            return Decimal("0.00")

        result = self.stockpile.resource_amounts.aggregate(
            total_weight=Sum(
                F("quantity") * F("resource__weight_per_unit"),
                output_field=DecimalField(
                    max_digits=14,
                    decimal_places=2,
                ),
            )
        )

        return result["total_weight"] or Decimal("0.00")

    def get_available_capacity(self) -> Decimal:
        if self.stockpile.context != Stockpile.Context.CARAVAN:
            return Decimal("0.00")

        carried_weight = self.get_carried_weight()
        carry_capacity = Decimal(
            self.stockpile.campaign.caravan.carry_capacity
        )

        return carry_capacity - carried_weight

    @transaction.atomic
    def add_resource(self, resource, quantity: Decimal) -> ResourceAmount:
        if quantity <= Decimal("0"):
            raise ValueError("Resource quantity must be greater than zero.")

        resource_amount, _ = ResourceAmount.objects.get_or_create(
            stockpile=self.stockpile,
            resource=resource,
            defaults={"quantity": Decimal("0.00")},
        )

        resource_amount.quantity += quantity
        resource_amount.save()

        return resource_amount

    @transaction.atomic
    def remove_resource(self, resource, quantity: Decimal) -> ResourceAmount:
        if quantity <= Decimal("0"):
            raise ValueError("Resource quantity must be greater than zero.")

        resource_amount = self.stockpile.resource_amounts.filter(
            resource=resource,
        ).first()

        if resource_amount is None:
            raise ValueError(
                f"{resource.name} is not stored in this stockpile."
            )

        if resource_amount.quantity < quantity:
            raise ValueError(
                f"Cannot remove {quantity} {resource.name}; "
                f"only {resource_amount.quantity} available."
            )

        resource_amount.quantity -= quantity
        resource_amount.save()

        return resource_amount

    @transaction.atomic
    def transfer_resource(
        self,
        destination_service: "ResourceService",
        resource,
        quantity: Decimal,
    ) -> None:
        if quantity <= Decimal("0"):
            raise ValueError("Resource quantity must be greater than zero.")

        if destination_service.stockpile.context == Stockpile.Context.CARAVAN:
            available_capacity = destination_service.get_available_capacity()

            resource_weight = quantity * resource.weight_per_unit

            if resource_weight > available_capacity:
                raise ValueError(
                    f"Cannot transfer {quantity} {resource.name}; "
                    f"it would exceed the caravan carry capacity."
                )

        self.remove_resource(resource, quantity)
        destination_service.add_resource(resource, quantity)


class ConsumptionService:
    def __init__(self, caravan: Caravan):
        self.caravan = caravan

    def consume_daily_supplies(self) -> None:
        caravan_stockpile = self.caravan.campaign.stockpiles.get(
            context=Stockpile.Context.CARAVAN,
        )

        caravan_service = ResourceService(caravan_stockpile)

        food = ResourceTemplate.objects.get(
            category=ResourceTemplate.Category.FOOD,
        )
        water = ResourceTemplate.objects.get(
            category=ResourceTemplate.Category.WATER,
        )

        required_quantity = Decimal(self.caravan.survivor_count)

        self._validate_required_supplies(
            caravan_service=caravan_service,
            food=food,
            water=water,
            required_quantity=required_quantity,
        )

        caravan_service.remove_resource(
            resource=food,
            quantity=required_quantity,
        )

        caravan_service.remove_resource(
            resource=water,
            quantity=required_quantity,
        )

    def _validate_required_supplies(
        self,
        caravan_service: ResourceService,
        food: ResourceTemplate,
        water: ResourceTemplate,
        required_quantity: Decimal,
    ) -> None:
        food_quantity = caravan_service.get_resource_quantity(food)
        water_quantity = caravan_service.get_resource_quantity(water)

        if food_quantity < required_quantity:
            raise ValueError(
                f"Cannot consume daily supplies; "
                f"requires {required_quantity} {food.name}, "
                f"but only {food_quantity} available."
            )

        if water_quantity < required_quantity:
            raise ValueError(
                f"Cannot consume daily supplies; "
                f"requires {required_quantity} {water.name}, "
                f"but only {water_quantity} available."
            )


class TimeService:
    BLOCKS_PER_DAY = 6

    def __init__(self, campaign: Campaign):
        self.campaign = campaign

    @transaction.atomic
    def advance_block(self) -> None:
        if self.campaign.current_block < self.BLOCKS_PER_DAY:
            self.campaign.current_block += 1
        else:
            self.campaign.current_day += 1
            self.campaign.current_block = 1

            self._consume_daily_supplies()

        self.campaign.save()

    def _consume_daily_supplies(self) -> None:
        caravan = self.campaign.caravan

        if caravan is None:
            return

        consumption_service = ConsumptionService(caravan)
        consumption_service.consume_daily_supplies()