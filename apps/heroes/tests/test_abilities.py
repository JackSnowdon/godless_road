import pytest
from django.db import IntegrityError

from apps.heroes.models import AbilityType, HeroAbility, HeroTemplate, ResourceAffinity


pytestmark = pytest.mark.django_db


@pytest.fixture
def mara():
    return HeroTemplate.objects.create(
        slug="mara-veyra",
        name="Mara Veyra",
        title="The Last Warden",
        primary_affinity=ResourceAffinity.VERDANT,
    )


class TestHeroAbility:
    def test_can_create_active_ability(self, mara):
        ability = HeroAbility.objects.create(
            hero_template=mara,
            slug="rootbind",
            name="Rootbind",
            description="Roots nearby enemies in place.",
            ability_type=AbilityType.ACTIVE,
            unlock_level=1,
            cooldown_ticks=8,
            resource_cost={"verdant": 2},
            data={"radius": 2, "duration_ticks": 4},
        )

        assert ability.hero_template == mara
        assert ability.ability_type == "active"
        assert ability.resource_cost == {"verdant": 2}
        assert ability.data["radius"] == 2

    def test_ability_slug_unique_per_hero(self, mara):
        HeroAbility.objects.create(
            hero_template=mara,
            slug="rootbind",
            name="Rootbind",
            description="Roots nearby enemies in place.",
        )

        with pytest.raises(IntegrityError):
            HeroAbility.objects.create(
                hero_template=mara,
                slug="rootbind",
                name="Duplicate Rootbind",
                description="Should not be allowed.",
            )

    def test_same_slug_allowed_for_different_heroes(self, mara):
        cinder = HeroTemplate.objects.create(
            slug="cinder",
            name="Cinder",
            title="The Ashforged",
            primary_affinity=ResourceAffinity.EMBER,
        )

        HeroAbility.objects.create(
            hero_template=mara,
            slug="shared-slug",
            name="Mara Ability",
            description="Mara-specific ability.",
        )

        ability = HeroAbility.objects.create(
            hero_template=cinder,
            slug="shared-slug",
            name="Cinder Ability",
            description="Cinder-specific ability.",
        )

        assert ability.hero_template == cinder