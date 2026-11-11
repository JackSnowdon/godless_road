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
        verbose_name = "hero template"
        verbose_name_plural = "hero templates"

    def __str__(self):
        return f"{self.name}, {self.title}"