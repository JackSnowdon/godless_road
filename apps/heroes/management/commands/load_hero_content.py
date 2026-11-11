import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.heroes.services import HeroContentData, HeroContentService

CONTENT_DIR = Path("content") / "heroes"


class Command(BaseCommand):
    help = "Load Hero content definitions from the content directory."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default=str(CONTENT_DIR),
            help="Directory containing Hero content JSON files.",
        )

    def handle(self, *args, **options):
        content_path = Path(options["path"])

        if not content_path.exists():
            raise CommandError(f"Content directory does not exist: {content_path}")

        json_files = sorted(content_path.glob("*.json"))

        if not json_files:
            raise CommandError(f"No Hero content files found in: {content_path}")

        loaded = 0

        for json_file in json_files:
            try:
                raw_data = json.loads(json_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                raise CommandError(f"Invalid JSON in {json_file}: {error}")

            hero_data = HeroContentData(
                slug=raw_data["slug"],
                name=raw_data["name"],
                title=raw_data["title"],
                biography=raw_data.get("biography", ""),
                primary_affinity=raw_data["primary_affinity"],
                secondary_affinity=raw_data.get("secondary_affinity", ""),
                base_stats=raw_data.get("base_stats", {}),
                growth=raw_data.get("growth", {}),
                visual=raw_data.get("visual", {}),
                tags=raw_data.get("tags", []),
                is_playable=raw_data.get("is_playable", True),
                is_recruitable=raw_data.get("is_recruitable", False),
                abilities=raw_data.get("abilities", []),
            )

            service = HeroContentService(hero_data)
            hero = service.upsert()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Loaded {hero.name} with {hero.abilities.count()} abilities."
                )
            )

            loaded += 1

        self.stdout.write(
            self.style.SUCCESS(f"Loaded {loaded} Hero content file(s).")
        )