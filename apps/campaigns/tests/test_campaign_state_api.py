from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.campaigns.models import (
    Campaign,
    Caravan,
    ResourceTemplate,
    Stockpile,
)
from apps.campaigns.services import ResourceService


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


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


def test_campaign_state_endpoint_returns_campaign_and_caravan(
    api_client,
    campaign,
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)

    caravan_service.add_resource(food, Decimal("40.00"))
    caravan_service.add_resource(water, Decimal("20.00"))

    url = reverse(
        "campaign-state",
        kwargs={"pk": campaign.pk},
    )

    response = api_client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert data["campaign_id"] == campaign.pk
    assert data["current_day"] == 1
    assert data["current_block"] == 1
    assert data["current_phase"] == "Night"

    assert data["caravan"]["id"] == caravan.pk
    assert data["caravan"]["name"] == "The Last Road"
    assert data["caravan"]["survivor_count"] == 30
    assert data["caravan"]["carry_capacity"] == 100
    assert data["caravan"]["carried_weight"] == "60.00"
    assert data["caravan"]["available_capacity"] == "40.00"

    caravan_resources = {
        resource["slug"]: resource
        for resource in data["caravan_resources"]
    }

    assert caravan_resources["preserved-rations"]["quantity"] == "40.00"
    assert caravan_resources["drinking-water"]["quantity"] == "20.00"

    assert data["camp_resources"] == []

def test_campaign_state_handles_missing_camp_stockpile(
    api_client,
    campaign,
    caravan,
    caravan_stockpile,
):
    url = reverse(
        "campaign-state",
        kwargs={"pk": campaign.pk},
    )

    response = api_client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert data["camp_resources"] == []