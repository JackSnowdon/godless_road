import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.heroes.content_validation import HeroContentValidator
from apps.heroes.models import HeroTemplate
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
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show proposed changes without writing to the database.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Create or overwrite Heroes without prompting.",
        )

    def handle(self, *args, **options):
        content_path = Path(options["path"])

        if not content_path.exists():
            raise CommandError(f"Content directory does not exist: {content_path}")

        json_files = sorted(content_path.glob("*.json"))

        if not json_files:
            raise CommandError(f"No Hero content files found in: {content_path}")

        created_count = 0
        updated_count = 0
        unchanged_count = 0
        skipped_count = 0

        for json_file in json_files:
            raw_data = self._load_json(json_file)
            self._validate_content(json_file, raw_data)

            hero_data = self._build_hero_data(raw_data)
            service = HeroContentService(hero_data)
            existing_hero = HeroTemplate.objects.filter(
                slug=hero_data.slug,
            ).first()

            if existing_hero is None:
                if options["dry_run"]:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Would create {hero_data.name}."
                        )
                    )
                    created_count += 1
                    continue

                hero = service.upsert()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {hero.name} with "
                        f"{hero.abilities.count()} abilities."
                    )
                )

                created_count += 1
                continue

            changes = service.get_changes(existing_hero)

            if not changes:
                self.stdout.write(
                    self.style.WARNING(
                        f"No changes for {existing_hero.name}."
                    )
                )

                unchanged_count += 1
                continue

            self._write_change_summary(existing_hero, changes)

            if options["dry_run"]:
                self.stdout.write(
                    self.style.WARNING(
                        f"Dry run: no changes written for {existing_hero.name}."
                    )
                )
                skipped_count += 1
                continue

            if options["force"] or self._confirm_overwrite(existing_hero):
                hero = service.upsert()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Updated {hero.name} with "
                        f"{hero.abilities.count()} abilities."
                    )
                )

                updated_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipped {existing_hero.name}."
                    )
                )

                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Hero content load complete: "
                f"{created_count} created, "
                f"{updated_count} updated, "
                f"{unchanged_count} unchanged, "
                f"{skipped_count} skipped."
            )
        )

    def _load_json(self, json_file: Path) -> dict:
        try:
            return json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise CommandError(f"Invalid JSON in {json_file}: {error}")

    def _validate_content(self, json_file: Path, raw_data: dict) -> None:
        validator = HeroContentValidator()
        validation_errors = validator.validate(raw_data)

        if not validation_errors:
            return

        error_messages = [
            f"{error.field}: {error.message}"
            for error in validation_errors
        ]

        raise CommandError(
            f"Invalid Hero content in {json_file}:\n"
            + "\n".join(error_messages)
        )

    def _build_hero_data(self, raw_data: dict) -> HeroContentData:
        return HeroContentData(
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

    def _write_change_summary(
        self,
        existing_hero: HeroTemplate,
        changes: dict,
    ) -> None:
        self.stdout.write(
            self.style.WARNING(
                f"Changes proposed for {existing_hero.name}:"
            )
        )

        hero_changes = changes.get("hero", {})

        for field, change in hero_changes.items():
            self.stdout.write(
                f"  {field}: {change['current']} -> {change['proposed']}"
            )

        ability_changes = changes.get("abilities", {})

        for slug, change in ability_changes.items():
            action = change["action"]

            if action == "added":
                self.stdout.write(
                    f"  ability/{slug}: would be added"
                )
            elif action == "removed":
                self.stdout.write(
                    f"  ability/{slug}: would be removed"
                )
            else:
                self.stdout.write(
                    f"  ability/{slug}: would be changed"
                )

                for field, field_change in change["changes"].items():
                    self.stdout.write(
                        f"    {field}: "
                        f"{field_change['current']} -> "
                        f"{field_change['proposed']}"
                    )

    def _confirm_overwrite(self, existing_hero: HeroTemplate) -> bool:
        answer = input(
            f"Overwrite {existing_hero.name}? [y/N]: "
        ).strip().lower()

        return answer == "y"