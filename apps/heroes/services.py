from dataclasses import dataclass

from django.db import transaction

from .models import HeroAbility, HeroTemplate


@dataclass(frozen=True)
class HeroContentData:
    slug: str
    name: str
    title: str
    biography: str
    primary_affinity: str
    secondary_affinity: str
    base_stats: dict
    growth: dict
    visual: dict
    tags: list
    is_playable: bool
    is_recruitable: bool
    abilities: list


class HeroContentService:
    def __init__(self, hero_data: HeroContentData):
        self.hero_data = hero_data

    def get_changes(self, existing_hero: HeroTemplate) -> dict:
        hero_changes = self._get_hero_field_changes(existing_hero)
        ability_changes = self._get_ability_changes(existing_hero)

        changes = {}

        if hero_changes:
            changes["hero"] = hero_changes

        if ability_changes:
            changes["abilities"] = ability_changes

        return changes

    @transaction.atomic
    def upsert(self) -> HeroTemplate:
        hero, _ = HeroTemplate.objects.update_or_create(
            slug=self.hero_data.slug,
            defaults={
                "name": self.hero_data.name,
                "title": self.hero_data.title,
                "biography": self.hero_data.biography,
                "primary_affinity": self.hero_data.primary_affinity,
                "secondary_affinity": self.hero_data.secondary_affinity,
                "base_stats": self.hero_data.base_stats,
                "growth": self.hero_data.growth,
                "visual": self.hero_data.visual,
                "tags": self.hero_data.tags,
                "is_playable": self.hero_data.is_playable,
                "is_recruitable": self.hero_data.is_recruitable,
            },
        )

        self._upsert_abilities(hero)

        return hero

    def _get_hero_field_changes(
        self,
        existing_hero: HeroTemplate,
    ) -> dict:
        proposed_fields = {
            "name": self.hero_data.name,
            "title": self.hero_data.title,
            "biography": self.hero_data.biography,
            "primary_affinity": self.hero_data.primary_affinity,
            "secondary_affinity": self.hero_data.secondary_affinity,
            "base_stats": self.hero_data.base_stats,
            "growth": self.hero_data.growth,
            "visual": self.hero_data.visual,
            "tags": self.hero_data.tags,
            "is_playable": self.hero_data.is_playable,
            "is_recruitable": self.hero_data.is_recruitable,
        }

        changes = {}

        for field, proposed_value in proposed_fields.items():
            current_value = getattr(existing_hero, field)

            if current_value != proposed_value:
                changes[field] = {
                    "current": current_value,
                    "proposed": proposed_value,
                }

        return changes

    def _get_ability_changes(
        self,
        existing_hero: HeroTemplate,
    ) -> dict:
        existing_abilities = {
            ability.slug: ability
            for ability in existing_hero.abilities.all()
        }

        proposed_abilities = {
            ability["slug"]: ability
            for ability in self.hero_data.abilities
        }

        changes = {}

        for slug, proposed_ability in proposed_abilities.items():
            existing_ability = existing_abilities.get(slug)

            if existing_ability is None:
                changes[slug] = {
                    "action": "added",
                    "proposed": proposed_ability,
                }
                continue

            ability_changes = self._get_ability_field_changes(
                existing_ability,
                proposed_ability,
            )

            if ability_changes:
                changes[slug] = {
                    "action": "changed",
                    "changes": ability_changes,
                }

        for slug, existing_ability in existing_abilities.items():
            if slug not in proposed_abilities:
                changes[slug] = {
                    "action": "removed",
                    "current": {
                        "name": existing_ability.name,
                        "description": existing_ability.description,
                    },
                }

        return changes

    
    def _get_ability_field_changes(
        self,
        existing_ability: HeroAbility,
        proposed_ability: dict,
    ) -> dict:
        proposed_fields = {
            "name": proposed_ability["name"],
            "description": proposed_ability["description"],
            "ability_type": proposed_ability["ability_type"],
            "unlock_level": proposed_ability["unlock_level"],
            "cooldown_ticks": proposed_ability["cooldown_ticks"],
            "resource_cost": proposed_ability.get("resource_cost", {}),
            "data": proposed_ability.get("data", {}),
        }

        changes = {}

        for field, proposed_value in proposed_fields.items():
            current_value = getattr(existing_ability, field)

            if current_value != proposed_value:
                changes[field] = {
                    "current": current_value,
                    "proposed": proposed_value,
                }

        return changes

    def _upsert_abilities(self, hero: HeroTemplate) -> None:
        for ability_data in self.hero_data.abilities:
            HeroAbility.objects.update_or_create(
                hero_template=hero,
                slug=ability_data["slug"],
                defaults={
                    "name": ability_data["name"],
                    "description": ability_data["description"],
                    "ability_type": ability_data["ability_type"],
                    "unlock_level": ability_data["unlock_level"],
                    "cooldown_ticks": ability_data["cooldown_ticks"],
                    "resource_cost": ability_data.get("resource_cost", {}),
                    "data": ability_data.get("data", {}),
                },
            )