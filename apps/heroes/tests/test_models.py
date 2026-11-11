import pytest
from django.db import IntegrityError

from apps.heroes.models import HeroTemplate, ResourceAffinity


pytestmark = pytest.mark.django_db


class TestHeroTemplate:
    def test_can_create_hero_template(self):
        hero = HeroTemplate.objects.create(
            slug="mara-veyra",
            name="Mara Veyra",
            title="The Last Warden",
            primary_affinity=ResourceAffinity.VERDANT,
            secondary_affinity=ResourceAffinity.AETHER,
            base_stats={"health": 120, "attack": 8},
            tags=["protector", "support"],
        )

        assert str(hero) == "Mara Veyra, The Last Warden"
        assert hero.primary_affinity == "verdant"
        assert hero.secondary_affinity == "aether"
        assert hero.is_playable is True
        assert hero.is_recruitable is False

    def test_slug_must_be_unique(self):
        HeroTemplate.objects.create(
            slug="mara-veyra",
            name="Mara Veyra",
            title="The Last Warden",
            primary_affinity=ResourceAffinity.VERDANT,
        )

        with pytest.raises(IntegrityError):
            HeroTemplate.objects.create(
                slug="mara-veyra",
                name="Duplicate Mara",
                title="Should Not Exist",
                primary_affinity=ResourceAffinity.VERDANT,
            )

    def test_secondary_affinity_can_be_blank(self):
        hero = HeroTemplate.objects.create(
            slug="cinder",
            name="Cinder",
            title="The Ashforged",
            primary_affinity=ResourceAffinity.EMBER,
        )

        assert hero.secondary_affinity == ""