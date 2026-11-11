import pytest
from dataclasses import replace

from apps.heroes.models import HeroAbility, HeroTemplate
from apps.heroes.services import HeroContentData, HeroContentService


pytestmark = pytest.mark.django_db


@pytest.fixture
def mara_content():
    return HeroContentData(
        slug="mara-veyra",
        name="Mara Veyra",
        title="The Last Warden",
        biography="A survivor who believes protection is rebuilding.",
        primary_affinity="verdant",
        secondary_affinity="aether",
        base_stats={"health": 120},
        growth={"health_per_level": 8},
        visual={"colour": "#4f7942"},
        tags=["protector"],
        is_playable=True,
        is_recruitable=False,
        abilities=[
            {
                "slug": "rootbind",
                "name": "Rootbind",
                "description": "Roots nearby enemies.",
                "ability_type": "active",
                "unlock_level": 1,
                "cooldown_ticks": 8,
                "resource_cost": {"verdant": 2},
                "data": {"radius": 2},
            }
        ],
    )



class TestHeroContentService:
    def test_creates_hero_and_ability(self, mara_content):
        service = HeroContentService(mara_content)
        hero = service.upsert()

        assert HeroTemplate.objects.count() == 1
        assert HeroAbility.objects.count() == 1
        assert hero.abilities.first().slug == "rootbind"

    def test_updates_existing_hero_without_duplicates(self, mara_content):
        initial_service = HeroContentService(mara_content)
        initial_service.upsert()

        updated_content = replace(
            mara_content,
            name="Mara Veyra Updated",
        )

        assert mara_content.name == "Mara Veyra"
        assert updated_content.name == "Mara Veyra Updated"

        updated_service = HeroContentService(updated_content)
        hero = updated_service.upsert()

        assert HeroTemplate.objects.count() == 1
        assert HeroAbility.objects.count() == 1
        assert hero.name == "Mara Veyra Updated"

    def test_no_changes_returns_empty_dict(self, mara_content):
        service = HeroContentService(mara_content)
        hero = service.upsert()

        changes = service.get_changes(hero)

        assert changes == {}

    def test_detects_changed_hero_field(self, mara_content):
        service = HeroContentService(mara_content)
        hero = service.upsert()

        updated_content = replace(
            mara_content,
            name="Mara Veyra Updated",
        )

        updated_service = HeroContentService(updated_content)
        changes = updated_service.get_changes(hero)

        assert changes["hero"]["name"] == {
            "current": "Mara Veyra",
            "proposed": "Mara Veyra Updated",
        }

    def test_detects_added_ability(self, mara_content):
        service = HeroContentService(mara_content)
        hero = service.upsert()

        updated_content = replace(
            mara_content,
            abilities=[
                *mara_content.abilities,
                {
                    "slug": "thorn-guard",
                    "name": "Thorn Guard",
                    "description": "Creates a protective barrier.",
                    "ability_type": "active",
                    "unlock_level": 2,
                    "cooldown_ticks": 10,
                    "resource_cost": {"verdant": 3},
                    "data": {"shield": 20},
                },
            ],
        )

        updated_service = HeroContentService(updated_content)
        changes = updated_service.get_changes(hero)

        assert changes["abilities"]["thorn-guard"]["action"] == "added"

    def test_detects_changed_ability_data(self, mara_content):
        service = HeroContentService(mara_content)
        hero = service.upsert()

        updated_content = replace(
            mara_content,
            abilities=[
                {
                    "slug": "rootbind",
                    "name": "Rootbind",
                    "description": "Roots nearby enemies.",
                    "ability_type": "active",
                    "unlock_level": 1,
                    "cooldown_ticks": 8,
                    "resource_cost": {"verdant": 2},
                    "data": {"radius": 3},
                }
            ],
        )

        updated_service = HeroContentService(updated_content)
        changes = updated_service.get_changes(hero)

        assert changes["abilities"]["rootbind"]["action"] == "changed"
        assert changes["abilities"]["rootbind"]["changes"]["data"] == {
            "current": {"radius": 2},
            "proposed": {"radius": 3},
        }

    def test_detects_removed_ability(self, mara_content):
        service = HeroContentService(mara_content)
        hero = service.upsert()

        updated_content = replace(
            mara_content,
            abilities=[],
        )

        updated_service = HeroContentService(updated_content)
        changes = updated_service.get_changes(hero)

        assert changes["abilities"]["rootbind"]["action"] == "removed"