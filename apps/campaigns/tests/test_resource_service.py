from decimal import Decimal

import pytest

from apps.campaigns.models import (
    Campaign,
    Caravan,
    ResourceAmount,
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
def caravan_stockpile(campaign):
    return Stockpile.objects.create(
        campaign=campaign,
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


@pytest.fixture
def food_cubes():
    return ResourceTemplate.objects.create(
        slug="food-cubes",
        name="Food Cubes",
        category=ResourceTemplate.Category.FOOD,
        tier=0,
        weight_per_unit=Decimal("0.50"),
    )


def test_empty_caravan_stockpile_has_zero_weight(
    caravan_stockpile,
):
    service = ResourceService(caravan_stockpile)

    assert service.get_carried_weight() == Decimal("0.00")


def test_carried_weight_includes_resource_weight(
    caravan_stockpile,
    water,
    food_cubes,
):
    ResourceAmount.objects.create(
        stockpile=caravan_stockpile,
        resource=water,
        quantity=Decimal("10.00"),
    )

    ResourceAmount.objects.create(
        stockpile=caravan_stockpile,
        resource=food_cubes,
        quantity=Decimal("20.00"),
    )

    service = ResourceService(caravan_stockpile)

    assert service.get_carried_weight() == Decimal("20.00")


def test_available_capacity_subtracts_carried_weight(
    caravan,
    caravan_stockpile,
    water,
):
    ResourceAmount.objects.create(
        stockpile=caravan_stockpile,
        resource=water,
        quantity=Decimal("30.00"),
    )

    service = ResourceService(caravan_stockpile)

    assert service.get_available_capacity() == Decimal("70.00")


def test_camp_stockpile_has_no_weight_limit(
    camp_stockpile,
    water,
):
    ResourceAmount.objects.create(
        stockpile=camp_stockpile,
        resource=water,
        quantity=Decimal("500.00"),
    )

    service = ResourceService(camp_stockpile)

    assert service.get_carried_weight() == Decimal("0.00")
    assert service.get_available_capacity() == Decimal("0.00")