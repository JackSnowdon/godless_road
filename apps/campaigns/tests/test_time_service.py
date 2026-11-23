from decimal import Decimal

import pytest

from apps.campaigns.models import (
    Campaign,
    Caravan,
    ResourceTemplate,
    Stockpile,
)
from apps.campaigns.services import (
    InsufficientSuppliesError,
    ResourceService, 
    TimeService, 
)

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


def test_time_advances_through_all_six_blocks(
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    time_service = TimeService(caravan.campaign)

    caravan_service.add_resource(food, Decimal("60.00"))
    caravan_service.add_resource(water, Decimal("60.00"))

    assert caravan.campaign.current_day == 1
    assert caravan.campaign.current_block == 1

    time_service.advance_block()
    assert caravan.campaign.current_day == 1
    assert caravan.campaign.current_block == 2

    time_service.advance_block()
    assert caravan.campaign.current_day == 1
    assert caravan.campaign.current_block == 3

    time_service.advance_block()
    assert caravan.campaign.current_day == 1
    assert caravan.campaign.current_block == 4

    time_service.advance_block()
    assert caravan.campaign.current_day == 1
    assert caravan.campaign.current_block == 5

    time_service.advance_block()
    assert caravan.campaign.current_day == 1
    assert caravan.campaign.current_block == 6

    time_service.advance_block()
    assert caravan.campaign.current_day == 2
    assert caravan.campaign.current_block == 1

    assert caravan_service.get_resource_quantity(food) == Decimal("30.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("30.00")


def test_time_moves_from_dusk_to_next_day_night(
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    time_service = TimeService(caravan.campaign)

    caravan_service.add_resource(food, Decimal("30.00"))
    caravan_service.add_resource(water, Decimal("30.00"))

    caravan.campaign.current_block = 6
    caravan.campaign.save()

    time_service.advance_block()

    assert caravan.campaign.current_day == 2
    assert caravan.campaign.current_block == 1


def test_consumption_occurs_only_when_day_advances(
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    time_service = TimeService(caravan.campaign)

    caravan_service.add_resource(food, Decimal("60.00"))
    caravan_service.add_resource(water, Decimal("60.00"))

    time_service.advance_block()

    assert caravan.campaign.current_day == 1
    assert caravan.campaign.current_block == 2

    assert caravan_service.get_resource_quantity(food) == Decimal("60.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("60.00")


def test_advancing_from_dusk_consumes_daily_supplies(
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    time_service = TimeService(caravan.campaign)

    caravan_service.add_resource(food, Decimal("40.00"))
    caravan_service.add_resource(water, Decimal("40.00"))

    caravan.campaign.current_block = 6
    caravan.campaign.save()

    time_service.advance_block()

    assert caravan.campaign.current_day == 2
    assert caravan.campaign.current_block == 1

    assert caravan_service.get_resource_quantity(food) == Decimal("10.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("10.00")


def test_day_does_not_advance_when_supplies_are_insufficient(
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)
    time_service = TimeService(caravan.campaign)

    caravan_service.add_resource(food, Decimal("30.00"))
    caravan_service.add_resource(water, Decimal("10.00"))

    caravan.campaign.current_block = 6
    caravan.campaign.save()

    with pytest.raises(InsufficientSuppliesError):
        time_service.advance_block()

    campaign = caravan.campaign
    campaign.refresh_from_db()

    assert campaign.current_day == 1
    assert campaign.current_block == 6

    assert caravan_service.get_resource_quantity(food) == Decimal("30.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("10.00")