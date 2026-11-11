from django.contrib import admin

from .models import HeroAbility, HeroTemplate

class HeroAbilityInline(admin.StackedInline):
    model = HeroAbility
    extra = 0
    prepopulated_fields = {"slug": ("name",)}


@admin.register(HeroTemplate)
class HeroTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "title",
        "primary_affinity",
        "secondary_affinity",
        "is_playable",
        "is_recruitable",
    )
    list_filter = (
        "primary_affinity",
        "secondary_affinity",
        "is_playable",
        "is_recruitable",
    )
    search_fields = ("name", "title", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(HeroAbility)
class HeroAbilityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "hero_template",
        "ability_type",
        "unlock_level",
        "cooldown_ticks",
    )
    list_filter = ("ability_type", "hero_template")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}