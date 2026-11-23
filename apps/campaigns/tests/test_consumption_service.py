from decimal import Decimal

import pytest

from apps.campaigns.models import (
    Campaign,
    Caravan,
    ResourceTemplate,
    Stockpile,
)
from apps.campaigns.services import ConsumptionService, ResourceService


pytestmark = pytest.mark.django_db


@pytest.fixture
def campaign():
    return Campaign.objects.create(
        scenario_slug="act-0-the-broken-road",
    )


@pytest.fixture
def caravan(campaign):
    return Caravan.objects.create(
        campaign=campaign,
        name="The Last Road",
        survivor_count=30,
        carry_capacity=100,
    )


@pytest.fixture
def caravan_stockpile(caravan):
    return Stockpile.objects.create(
        campaign=caravan.campaign,
        context=Stockpile.Context.CARAVAN,
    )


@pytest.fixture
def camp_stockpile(campaign):
    return Stockpile.objects.create(
        campaign=campaign,
        context=Stockpile.Context.CAMP,
    )


@pytest.fixture
def food():
    return ResourceTemplate.objects.create(
        slug="preserved-rations",
        name="Preserved Rations",
        category=ResourceTemplate.Category.FOOD,
        tier=0,
        weight_per_unit=Decimal("1.00"),
    )


@pytest.fixture
def water():
    return ResourceTemplate.objects.create(
        slug="drinking-water",
        name="Drinking Water",
        category=ResourceTemplate.Category.WATER,
        tier=0,
        weight_per_unit=Decimal("1.00"),
    )


def test_daily_consumption_removes_food_and_water(
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    consumption_service = ConsumptionService(caravan)

    caravan_service.add_resource(food, Decimal("40.00"))
    caravan_service.add_resource(water, Decimal("40.00"))

    consumption_service.consume_daily_supplies()

    assert caravan_service.get_resource_quantity(food) == Decimal("10.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("10.00")


def test_consumption_uses_caravan_stockpile_not_camp_stockpile(
    caravan,
    caravan_stockpile,
    camp_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    camp_service = ResourceService(camp_stockpile)
    consumption_service = ConsumptionService(caravan)

    caravan_service.add_resource(food, Decimal("30.00"))
    caravan_service.add_resource(water, Decimal("30.00"))

    camp_service.add_resource(food, Decimal("100.00"))
    camp_service.add_resource(water, Decimal("100.00"))

    consumption_service.consume_daily_supplies()

    assert caravan_service.get_resource_quantity(food) == Decimal("0.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("0.00")

    assert camp_service.get_resource_quantity(food) == Decimal("100.00")
    assert camp_service.get_resource_quantity(water) == Decimal("100.00")


def test_consumption_fails_when_food_is_insufficient(
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    consumption_service = ConsumptionService(caravan)

    caravan_service.add_resource(food, Decimal("10.00"))
    caravan_service.add_resource(water, Decimal("30.00"))

    with pytest.raises(ValueError):
        consumption_service.consume_daily_supplies()

    assert caravan_service.get_resource_quantity(food) == Decimal("10.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("30.00")


def test_consumption_fails_when_water_is_insufficient(
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    consumption_service = ConsumptionService(caravan)

    caravan_service.add_resource(food, Decimal("30.00"))
    caravan_service.add_resource(water, Decimal("10.00"))

    with pytest.raises(ValueError):
        consumption_service.consume_daily_supplies()

    assert caravan_service.get_resource_quantity(food) == Decimal("30.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("10.00")
