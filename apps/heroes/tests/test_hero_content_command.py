import json
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.heroes.models import HeroAbility, HeroTemplate


pytestmark = pytest.mark.django_db


@pytest.fixture
def valid_hero_content():
    return {
        "slug": "mara-veyra",
        "name": "Mara Veyra",
        "title": "The Last Warden",
        "primary_affinity": "verdant",
        "secondary_affinity": "aether",
        "base_stats": {"health": 120},
        "growth": {"health_per_level": 8},
        "visual": {"colour": "#4f7942"},
        "tags": ["protector"],
        "is_playable": True,
        "is_recruitable": False,
        "abilities": [
            {
                "slug": "rootbind",
                "name": "Rootbind",
                "description": "Roots nearby enemies.",
                "ability_type": "active",
                "unlock_level": 1,
                "cooldown_ticks": 8,
                "resource_cost": {"verdant": 2},
                "data": {"radius": 2},
            }
        ],
    }


@pytest.fixture
def content_directory(tmp_path):
    def _write_content(filename: str, content: dict) -> Path:
        content_path = tmp_path / filename
        content_path.write_text(
            json.dumps(content),
            encoding="utf-8",
        )

        return tmp_path

    return _write_content


def test_creates_new_hero(
    valid_hero_content,
    content_directory,
):
    content_path = content_directory(
        "mara_veyra.json",
        valid_hero_content,
    )
    stdout = StringIO()

    call_command(
        "load_hero_content",
        path=str(content_path),
        stdout=stdout,
    )

    output = stdout.getvalue()
    hero = HeroTemplate.objects.get(slug="mara-veyra")

    assert hero.name == "Mara Veyra"
    assert hero.primary_affinity == "verdant"
    assert hero.abilities.count() == 1
    assert "Created Mara Veyra" in output
    assert "1 created" in output


def test_skips_unchanged_hero(
    valid_hero_content,
    content_directory,
):
    content_path = content_directory(
        "mara_veyra.json",
        valid_hero_content,
    )

    call_command(
        "load_hero_content",
        path=str(content_path),
    )

    stdout = StringIO()

    call_command(
        "load_hero_content",
        path=str(content_path),
        stdout=stdout,
    )

    output = stdout.getvalue()

    assert HeroTemplate.objects.count() == 1
    assert HeroAbility.objects.count() == 1
    assert "No changes for Mara Veyra" in output
    assert "1 unchanged" in output


def test_dry_run_does_not_create_hero(
    valid_hero_content,
    content_directory,
):
    content_path = content_directory(
        "mara_veyra.json",
        valid_hero_content,
    )
    stdout = StringIO()

    call_command(
        "load_hero_content",
        path=str(content_path),
        dry_run=True,
        stdout=stdout,
    )

    output = stdout.getvalue()

    assert HeroTemplate.objects.count() == 0
    assert HeroAbility.objects.count() == 0
    assert "Would create Mara Veyra" in output
    assert "1 would create" in output


def test_force_overwrites_changed_hero(
    valid_hero_content,
    content_directory,
):
    content_path = content_directory(
        "mara_veyra.json",
        valid_hero_content,
    )

    call_command(
        "load_hero_content",
        path=str(content_path),
    )

    changed_content = {
        **valid_hero_content,
        "name": "Mara Veyra Updated",
    }

    content_path = content_directory(
        "mara_veyra.json",
        changed_content,
    )

    stdout = StringIO()

    call_command(
        "load_hero_content",
        path=str(content_path),
        force=True,
        stdout=stdout,
    )

    output = stdout.getvalue()
    hero = HeroTemplate.objects.get(slug="mara-veyra")

    assert hero.name == "Mara Veyra Updated"
    assert HeroTemplate.objects.count() == 1
    assert "Updated Mara Veyra Updated" in output
    assert "1 updated" in output


def test_prompts_before_overwriting_changed_hero(
    monkeypatch,
    valid_hero_content,
    content_directory,
):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "y",
    )

    content_path = content_directory(
        "mara_veyra.json",
        valid_hero_content,
    )

    call_command(
        "load_hero_content",
        path=str(content_path),
    )

    changed_content = {
        **valid_hero_content,
        "name": "Mara Veyra Updated",
    }

    content_path = content_directory(
        "mara_veyra.json",
        changed_content,
    )

    stdout = StringIO()

    call_command(
        "load_hero_content",
        path=str(content_path),
        stdout=stdout,
    )

    output = stdout.getvalue()
    hero = HeroTemplate.objects.get(slug="mara-veyra")

    assert hero.name == "Mara Veyra Updated"
    assert "Updated Mara Veyra Updated" in output


def test_declining_prompt_skips_overwrite(
    monkeypatch,
    valid_hero_content,
    content_directory,
):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "n",
    )

    content_path = content_directory(
        "mara_veyra.json",
        valid_hero_content,
    )

    call_command(
        "load_hero_content",
        path=str(content_path),
    )

    changed_content = {
        **valid_hero_content,
        "name": "Mara Veyra Updated",
    }

    content_path = content_directory(
        "mara_veyra.json",
        changed_content,
    )

    stdout = StringIO()

    call_command(
        "load_hero_content",
        path=str(content_path),
        stdout=stdout,
    )

    output = stdout.getvalue()
    hero = HeroTemplate.objects.get(slug="mara-veyra")

    assert hero.name == "Mara Veyra"
    assert HeroTemplate.objects.count() == 1
    assert "Skipped Mara Veyra" in output
    assert "1 skipped" in output


def test_invalid_content_raises_command_error(
    content_directory,
):
    invalid_content = {
        "slug": "broken-hero",
        "name": "Broken Hero",
        "title": "Invalid Hero",
        "primary_affinity": "fire",
    }

    content_path = content_directory(
        "broken_hero.json",
        invalid_content,
    )

    with pytest.raises(CommandError) as error:
        call_command(
            "load_hero_content",
            path=str(content_path),
        )

    assert "Invalid Hero content" in str(error.value)
    assert "primary_affinity" in str(error.value)
    assert HeroTemplate.objects.count() == 0