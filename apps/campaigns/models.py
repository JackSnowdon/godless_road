from django.conf import settings
from django.db import models


class Campaign(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="campaigns",
    )

    scenario_slug = models.SlugField()
    current_day = models.PositiveIntegerField(default=1)
    current_block = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Campaign {self.pk} — Day {self.current_day}"


class Caravan(models.Model):
    campaign = models.OneToOneField(
        Campaign,
        on_delete=models.CASCADE,
        related_name="caravan",
    )

    name = models.CharField(max_length=100)
    survivor_count = models.PositiveIntegerField(default=0)
    carry_capacity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ResourceTemplate(models.Model):
    class Category(models.TextChoices):
        WATER = "water", "Water"
        FOOD = "food", "Food"
        MATERIAL = "material", "Material"
        EMBER = "ember", "Ember"
        VERDANT = "verdant", "Verdant"
        AETHER = "aether", "Aether"

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )
    tier = models.PositiveSmallIntegerField(default=0)
    weight_per_unit = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=1,
    )
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "tier", "name"]

    def __str__(self) -> str:
        return self.name


class Stockpile(models.Model):
    class Context(models.TextChoices):
        CARAVAN = "caravan", "Caravan"
        CAMP = "camp", "Camp"

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="stockpiles",
    )

    context = models.CharField(
        max_length=20,
        choices=Context.choices,
    )
    capacity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "context"],
                name="unique_stockpile_per_campaign_context",
            )
        ]

    def __str__(self) -> str:
        return f"{self.get_context_display()} stockpile — Campaign {self.campaign_id}"


class ResourceAmount(models.Model):
    stockpile = models.ForeignKey(
        Stockpile,
        on_delete=models.CASCADE,
        related_name="resource_amounts",
    )

    resource = models.ForeignKey(
        ResourceTemplate,
        on_delete=models.PROTECT,
        related_name="stock_amounts",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stockpile", "resource"],
                name="unique_resource_per_stockpile",
            )
        ]

    def __str__(self) -> str:
        return f"{self.resource.name}: {self.quantity}"