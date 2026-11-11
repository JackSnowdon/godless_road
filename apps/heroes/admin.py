from django.contrib import admin

from .models import HeroTemplate


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