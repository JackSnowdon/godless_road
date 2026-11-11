from apps.heroes.content_validation import HeroContentValidator


class TestHeroContentValidator:
    def test_valid_hero_content_has_no_errors(self):
        raw_data = {
            "slug": "mara-veyra",
            "name": "Mara Veyra",
            "title": "The Last Warden",
            "primary_affinity": "verdant",
            "secondary_affinity": "aether",
            "abilities": [
                {
                    "slug": "rootbind",
                    "name": "Rootbind",
                    "description": "Roots nearby enemies.",
                    "ability_type": "active",
                    "unlock_level": 1,
                    "cooldown_ticks": 8,
                }
            ],
        }

        validator = HeroContentValidator()
        errors = validator.validate(raw_data)

        assert errors == []

    def test_missing_required_hero_fields_are_reported(self):
        raw_data = {}

        validator = HeroContentValidator()
        errors = validator.validate(raw_data)

        error_fields = {error.field for error in errors}

        assert "slug" in error_fields
        assert "name" in error_fields
        assert "title" in error_fields
        assert "primary_affinity" in error_fields

    def test_invalid_primary_affinity_is_reported(self):
        raw_data = {
            "slug": "broken-hero",
            "name": "Broken Hero",
            "title": "Invalid",
            "primary_affinity": "fire",
        }

        validator = HeroContentValidator()
        errors = validator.validate(raw_data)

        assert any(error.field == "primary_affinity" for error in errors)

    def test_invalid_ability_type_is_reported(self):
        raw_data = {
            "slug": "broken-hero",
            "name": "Broken Hero",
            "title": "Invalid",
            "primary_affinity": "verdant",
            "abilities": [
                {
                    "slug": "broken-ability",
                    "name": "Broken Ability",
                    "description": "Invalid ability.",
                    "ability_type": "explosion",
                    "unlock_level": 1,
                    "cooldown_ticks": 0,
                }
            ],
        }

        validator = HeroContentValidator()
        errors = validator.validate(raw_data)

        assert any(
            error.field == "abilities[0].ability_type"
            for error in errors
        )

    def test_negative_cooldown_is_reported(self):
        raw_data = {
            "slug": "broken-hero",
            "name": "Broken Hero",
            "title": "Invalid",
            "primary_affinity": "verdant",
            "abilities": [
                {
                    "slug": "broken-ability",
                    "name": "Broken Ability",
                    "description": "Invalid ability.",
                    "ability_type": "active",
                    "unlock_level": 1,
                    "cooldown_ticks": -1,
                }
            ],
        }

        validator = HeroContentValidator()
        errors = validator.validate(raw_data)

        assert any(
            error.field == "abilities[0].cooldown_ticks"
            for error in errors
        )