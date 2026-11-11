from django.conf import settings
from django.db import models


class ResourceAffinity(models.TextChoices):
    EMBER = "ember", "Ember"
    VERDANT = "verdant", "Verdant"
    AETHER = "aether", "Aether"


class HeroTemplate(models.Model):
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Stable identifier used in code, APIs, and content files.",
    )
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    primary_affinity = models.CharField(
        max_length=20,
        choices=ResourceAffinity.choices,
    )
    secondary_affinity = models.CharField(
        max_length=20,
        choices=ResourceAffinity.choices,
        blank=True,
    )

    base_stats = models.JSONField(
        default=dict,
        blank=True,
        help_text="Initial combat and support stats for this Hero.",
    )
    growth = models.JSONField(
        default=dict,
        blank=True,
        help_text="Per-level stat progression rules.",
    )
    visual = models.JSONField(
        default=dict,
        blank=True,
        help_text="Front-end presentation data, such as colours or icon references.",
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Flexible design labels, such as protector, control, or siege.",
    )

    is_playable = models.BooleanField(default=True)
    is_recruitable = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "hero"
        verbose_name_plural = "heroes"

    def __str__(self):
        return f"{self.name}, {self.title}"


class AbilityType(models.TextChoices):
    ACTIVE = "active", "Active"
    PASSIVE = "passive", "Passive"
    AURA = "aura", "Aura"
    ULTIMATE = "ultimate", "Ultimate"


class HeroAbility(models.Model):
    hero_template = models.ForeignKey(
        HeroTemplate,
        on_delete=models.CASCADE,
        related_name="abilities",
    )

    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()

    ability_type = models.CharField(
        max_length=20,
        choices=AbilityType.choices,
        default=AbilityType.ACTIVE,
    )

    unlock_level = models.PositiveIntegerField(default=1)
    cooldown_ticks = models.PositiveIntegerField(default=0)
    resource_cost = models.JSONField(default=dict, blank=True)

    data = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Ability-specific parameters. Keep combat effects here until "
            "the ability system stabilises."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["hero_template__name", "unlock_level", "name"]
        verbose_name = "hero ability"
        verbose_name_plural = "abilities"
        constraints = [
            models.UniqueConstraint(
                fields=["hero_template", "slug"],
                name="unique_ability_slug_per_hero",
            )
        ]

    def __str__(self):
        return f"{self.hero_template.name}: {self.name}"


class PlayerHero(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="heroes",
    )

    template = models.ForeignKey(
        HeroTemplate,
        on_delete=models.PROTECT,
        related_name="player_instances",
    )

    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)

    current_stats = models.JSONField(default=dict, blank=True)
    unlocked_ability_ids = models.JSONField(default=list, blank=True)
    assignment = models.JSONField(default=dict, blank=True)
    condition = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "template"],
                name="unique_hero_template_per_user",
            )
        ]

    def __str__(self):
        return f"{self.user} — {self.template.name}"