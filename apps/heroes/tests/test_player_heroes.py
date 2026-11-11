import pytest
from django.contrib.auth import get_user_model

from apps.heroes.models import HeroTemplate, PlayerHero, ResourceAffinity


pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="test_user",
        password="test-password-123",
    )


@pytest.fixture
def mara():
    return HeroTemplate.objects.create(
        slug="mara-veyra",
        name="Mara Veyra",
        title="The Last Warden",
        primary_affinity=ResourceAffinity.VERDANT,
    )


class TestPlayerHero:
    def test_can_create_player_hero(self, user, mara):
        player_hero = PlayerHero.objects.create(
            user=user,
            template=mara,
        )

        assert player_hero.user == user
        assert player_hero.template == mara
        assert player_hero.level == 1
        assert player_hero.experience == 0
        assert str(player_hero) == f"{user} — Mara Veyra"

    def test_user_cannot_own_duplicate_hero_template(self, user, mara):
        PlayerHero.objects.create(
            user=user,
            template=mara,
        )

        with pytest.raises(Exception):
            PlayerHero.objects.create(
                user=user,
                template=mara,
            )