from django.contrib import admin

from apps.campaigns.models import (
    Campaign,
    Caravan,
    ResourceAmount,
    ResourceTemplate,
    Stockpile,
)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "scenario_slug",
        "current_day",
        "current_block",
        "status",
        "user",
    )

    list_filter = (
        "status",
        "scenario_slug",
    )

    search_fields = (
        "scenario_slug",
        "user__username",
    )


@admin.register(Caravan)
class CaravanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "campaign",
        "survivor_count",
        "carry_capacity",
    )

    search_fields = (
        "name",
        "campaign__scenario_slug",
    )


@admin.register(ResourceTemplate)
class ResourceTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "name",
        "category",
        "tier",
        "weight_per_unit",
    )

    list_filter = (
        "category",
        "tier",
    )

    search_fields = (
        "slug",
        "name",
    )


@admin.register(Stockpile)
class StockpileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "campaign",
        "context",
        "capacity",
    )

    list_filter = (
        "context",
    )


@admin.register(ResourceAmount)
class ResourceAmountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "stockpile",
        "resource",
        "quantity",
    )

    list_filter = (
        "stockpile__context",
        "resource__category",
    )