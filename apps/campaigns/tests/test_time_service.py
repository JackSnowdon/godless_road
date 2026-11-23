import pytest

from apps.campaigns.models import Campaign
from apps.campaigns.services import TimeService


pytestmark = pytest.mark.django_db


@pytest.fixture
def campaign():
    return Campaign.objects.create(
        scenario_slug="act-0-the-broken-road",
    )


def test_time_advances_through_all_six_blocks(campaign):
    time_service = TimeService(campaign)

    assert campaign.current_day == 1
    assert campaign.current_block == 1

    time_service.advance_block()
    assert campaign.current_day == 1
    assert campaign.current_block == 2

    time_service.advance_block()
    assert campaign.current_day == 1
    assert campaign.current_block == 3

    time_service.advance_block()
    assert campaign.current_day == 1
    assert campaign.current_block == 4

    time_service.advance_block()
    assert campaign.current_day == 1
    assert campaign.current_block == 5

    time_service.advance_block()
    assert campaign.current_day == 1
    assert campaign.current_block == 6

    time_service.advance_block()
    assert campaign.current_day == 2
    assert campaign.current_block == 1


def test_time_moves_from_dusk_to_next_day_night(campaign):
    campaign.current_block = 6
    campaign.save()

    time_service = TimeService(campaign)

    time_service.advance_block()

    assert campaign.current_day == 2
    assert campaign.current_block == 1