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