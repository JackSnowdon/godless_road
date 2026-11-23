from decimal import Decimal

import pytest

from apps.campaigns.models import (
    Campaign,
    Caravan,
    ResourceTemplate,
    Stockpile,
)
from apps.campaigns.services import ResourceService


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
def water():
    return ResourceTemplate.objects.create(
        slug="drinking-water",
        name="Drinking Water",
        category=ResourceTemplate.Category.WATER,
        tier=0,
        weight_per_unit=Decimal("1.00"),
    )

def test_transfer_moves_resource_from_camp_to_caravan(
    camp_stockpile,
    caravan_stockpile,
    water,
):
    camp_service = ResourceService(camp_stockpile)
    caravan_service = ResourceService(caravan_stockpile)

    camp_service.add_resource(water, Decimal("20.00"))

    camp_service.transfer_resource(
        destination_service=caravan_service,
        resource=water,
        quantity=Decimal("10.00"),
    )

    assert camp_service.get_resource_quantity(water) == Decimal("10.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("10.00")


def test_transfer_rejects_quantity_above_carry_capacity(
    camp_stockpile,
    caravan_stockpile,
    water,
):
    camp_service = ResourceService(camp_stockpile)
    caravan_service = ResourceService(caravan_stockpile)

    camp_service.add_resource(water, Decimal("150.00"))

    with pytest.raises(
        ValueError,
        match="exceed the caravan carry capacity",
    ):
        camp_service.transfer_resource(
            destination_service=caravan_service,
            resource=water,
            quantity=Decimal("120.00"),
        )

    assert camp_service.get_resource_quantity(water) == Decimal("150.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("0.00")


def test_transfer_rejects_removing_more_than_available(
    camp_stockpile,
    caravan_stockpile,
    water,
):
    camp_service = ResourceService(camp_stockpile)
    caravan_service = ResourceService(caravan_stockpile)

    camp_service.add_resource(water, Decimal("5.00"))

    with pytest.raises(ValueError, match="Cannot remove"):
        camp_service.transfer_resource(
            destination_service=caravan_service,
            resource=water,
            quantity=Decimal("10.00"),
        )

    assert camp_service.get_resource_quantity(water) == Decimal("5.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("0.00")


def test_transfer_updates_both_stockpiles(
    camp_stockpile,
    caravan_stockpile,
    water,
):
    camp_service = ResourceService(camp_stockpile)
    caravan_service = ResourceService(caravan_stockpile)

    camp_service.add_resource(water, Decimal("40.00"))

    camp_service.transfer_resource(
        destination_service=caravan_service,
        resource=water,
        quantity=Decimal("25.00"),
    )

    assert camp_service.get_resource_quantity(water) == Decimal("15.00")
    assert caravan_service.get_resource_quantity(water) == Decimal("25.00")
    assert caravan_service.get_carried_weight() == Decimal("25.00")