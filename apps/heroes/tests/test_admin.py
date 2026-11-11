import pytest
from django.contrib.admin.sites import AdminSite

from apps.heroes.admin import HeroTemplateAdmin
from apps.heroes.models import HeroTemplate


pytestmark = pytest.mark.django_db


class TestHeroTemplateAdmin:
    def test_admin_lists_core_fields(self):
        site = AdminSite()
        admin = HeroTemplateAdmin(HeroTemplate, site)

        assert "name" in admin.list_display
        assert "primary_affinity" in admin.list_display
        assert "is_playable" in admin.list_display