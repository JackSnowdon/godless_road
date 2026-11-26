from django.core.management.base import BaseCommand

from apps.campaigns.models import (
    Campaign,
    Caravan,
    ResourceAmount,
    ResourceTemplate,
    Stockpile,
)


class Command(BaseCommand):
    help = "Create repeatable local demo data for browser testing."

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data…")

        resource_templates = self._create_resource_templates()
        campaign = self._create_demo_campaign(resource_templates)

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo campaign ready: Campaign {campaign.pk} — "
                f"{campaign.scenario_slug}"
            )
        )

    def _create_resource_templates(self):
        templates = {}

        definitions = [
            {
                "slug": "preserved-rations",
                "name": "Preserved Rations",
                "category": ResourceTemplate.Category.FOOD,
                "tier": 0,
                "weight_per_unit": "1.00",
            },
            {
                "slug": "drinking-water",
                "name": "Drinking Water",
                "category": ResourceTemplate.Category.WATER,
                "tier": 0,
                "weight_per_unit": "1.00",
            },
        ]

        for definition in definitions:
            template, _created = ResourceTemplate.objects.update_or_create(
                slug=definition["slug"],
                defaults=definition,
            )

            templates[template.slug] = template

            self.stdout.write(
                f"Resource template ready: {template.slug}"
            )

        return templates

    def _create_demo_campaign(self, resource_templates):
        campaign, _created = Campaign.objects.update_or_create(
            scenario_slug="act-0-the-broken-road",
            defaults={
                "current_day": 1,
                "current_block": 1,
                "status": Campaign.Status.ACTIVE,
            },
        )

        caravan, _created = Caravan.objects.update_or_create(
            campaign=campaign,
            defaults={
                "name": "The Last Road",
                "survivor_count": 30,
                "carry_capacity": 100,
            },
        )

        caravan_stockpile, _created = Stockpile.objects.update_or_create(
            campaign=campaign,
            context=Stockpile.Context.CARAVAN,
            defaults={
                "capacity": 100,
            },
        )

        camp_stockpile, _created = Stockpile.objects.update_or_create(
            campaign=campaign,
            context=Stockpile.Context.CAMP,
            defaults={
                "capacity": 0,
            },
        )

        ResourceAmount.objects.update_or_create(
            stockpile=caravan_stockpile,
            resource=resource_templates["preserved-rations"],
            defaults={
                "quantity": 60,
            },
        )

        ResourceAmount.objects.update_or_create(
            stockpile=caravan_stockpile,
            resource=resource_templates["drinking-water"],
            defaults={
                "quantity": 60,
            },
        )

        self.stdout.write(
            f"Demo campaign ready: {campaign.pk}"
        )

        return campaign