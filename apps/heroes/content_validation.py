from dataclasses import dataclass

from apps.heroes.models import AbilityType, ResourceAffinity


@dataclass(frozen=True)
class ContentValidationError:
    field: str
    message: str


class HeroContentValidator:
    REQUIRED_HERO_FIELDS = ("slug", "name", "title", "primary_affinity")
    REQUIRED_ABILITY_FIELDS = ("slug", "name", "description", "ability_type")

    def validate(self, raw_data: dict) -> list[ContentValidationError]:
        errors = []

        errors.extend(self._validate_required_fields(raw_data))
        errors.extend(self._validate_affinities(raw_data))
        errors.extend(self._validate_abilities(raw_data))

        return errors

    def _validate_required_fields(
        self,
        raw_data: dict,
    ) -> list[ContentValidationError]:
        errors = []

        for field in self.REQUIRED_HERO_FIELDS:
            if not raw_data.get(field):
                errors.append(
                    ContentValidationError(
                        field=field,
                        message="This field is required.",
                    )
                )

        return errors

    def _validate_affinities(
        self,
        raw_data: dict,
    ) -> list[ContentValidationError]:
        errors = []
        valid_affinities = ResourceAffinity.values

        primary_affinity = raw_data.get("primary_affinity")
        secondary_affinity = raw_data.get("secondary_affinity", "")

        if primary_affinity and primary_affinity not in valid_affinities:
            errors.append(
                ContentValidationError(
                    field="primary_affinity",
                    message=f"Unknown affinity: {primary_affinity}",
                )
            )

        if secondary_affinity and secondary_affinity not in valid_affinities:
            errors.append(
                ContentValidationError(
                    field="secondary_affinity",
                    message=f"Unknown affinity: {secondary_affinity}",
                )
            )

        return errors

    def _validate_abilities(
        self,
        raw_data: dict,
    ) -> list[ContentValidationError]:
        errors = []
        valid_ability_types = AbilityType.values

        for index, ability in enumerate(raw_data.get("abilities", [])):
            prefix = f"abilities[{index}]"

            for field in self.REQUIRED_ABILITY_FIELDS:
                if not ability.get(field):
                    errors.append(
                        ContentValidationError(
                            field=f"{prefix}.{field}",
                            message="This field is required.",
                        )
                    )

            ability_type = ability.get("ability_type")

            if ability_type and ability_type not in valid_ability_types:
                errors.append(
                    ContentValidationError(
                        field=f"{prefix}.ability_type",
                        message=f"Unknown ability type: {ability_type}",
                    )
                )

            unlock_level = ability.get("unlock_level", 1)

            if not isinstance(unlock_level, int) or unlock_level < 1:
                errors.append(
                    ContentValidationError(
                        field=f"{prefix}.unlock_level",
                        message="Must be a positive integer.",
                    )
                )

            cooldown_ticks = ability.get("cooldown_ticks", 0)

            if not isinstance(cooldown_ticks, int) or cooldown_ticks < 0:
                errors.append(
                    ContentValidationError(
                        field=f"{prefix}.cooldown_ticks",
                        message="Must be zero or a positive integer.",
                    )
                )

        return errors