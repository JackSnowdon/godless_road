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
from apps.campaigns.serializers import CampaignStateSerializer
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


def test_advance_time_endpoint_advances_one_block(
    api_client,
    campaign,
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)

    caravan_service.add_resource(food, Decimal("40.00"))
    caravan_service.add_resource(water, Decimal("40.00"))

    url = reverse(
        "campaign-advance-time",
        kwargs={"pk": campaign.pk},
    )

    response = api_client.post(url)

    assert response.status_code == 200

    data = response.json()

    assert data["campaign_id"] == campaign.pk
    assert data["current_day"] == 1
    assert data["current_block"] == 2
    assert data["current_phase"] == "Dawn"

    assert data["caravan"]["carried_weight"] == "80.00"
    assert data["caravan"]["available_capacity"] == "20.00"

    caravan_resources = {
        resource["slug"]: resource
        for resource in data["caravan_resources"]
    }

    assert caravan_resources["preserved-rations"]["quantity"] == "40.00"
    assert caravan_resources["drinking-water"]["quantity"] == "40.00"


def test_advance_time_endpoint_consumes_supplies_at_day_boundary(
    api_client,
    campaign,
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)

    caravan_service.add_resource(food, Decimal("40.00"))
    caravan_service.add_resource(water, Decimal("40.00"))

    campaign.current_block = 6
    campaign.save()

    url = reverse(
        "campaign-advance-time",
        kwargs={"pk": campaign.pk},
    )

    response = api_client.post(url)

    assert response.status_code == 200

    data = response.json()

    assert data["current_day"] == 2
    assert data["current_block"] == 1
    assert data["current_phase"] == "Night"

    caravan_resources = {
        resource["slug"]: resource
        for resource in data["caravan_resources"]
    }

    assert caravan_resources["preserved-rations"]["quantity"] == "10.00"
    assert caravan_resources["drinking-water"]["quantity"] == "10.00"


def test_advance_time_endpoint_rejects_insufficient_supplies(
    api_client,
    campaign,
    caravan,
    caravan_stockpile,
    food,
    water,
):
    caravan_service = ResourceService(caravan_stockpile)

    caravan_service.add_resource(food, Decimal("30.00"))
    caravan_service.add_resource(water, Decimal("10.00"))

    campaign.current_block = 6
    campaign.save()

    url = reverse(
        "campaign-advance-time",
        kwargs={"pk": campaign.pk},
    )

    response = api_client.post(url)

    assert response.status_code == 400

    data = response.json()

    assert "Drinking Water" in data["detail"]

    campaign.refresh_from_db()

    assert campaign.current_day == 1
    assert campaign.current_block == 6

    caravan_resources = {
        resource["slug"]: resource["quantity"]
        for resource in CampaignStateSerializer(campaign).data[
            "caravan_resources"
        ]
    }

    assert caravan_resources["preserved-rations"] == "30.00"
    assert caravan_resources["drinking-water"] == "10.00"