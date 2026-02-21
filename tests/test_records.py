from __future__ import annotations

from langlearn.languages.german.records.noun_record import NounRecord
from langlearn.languages.german.records.verb_record import VerbRecord
from langlearn.languages.korean.records.noun_record import KoreanNounRecord
from langlearn.languages.russian.records.noun_record import RussianNounRecord


def test_german_noun_from_csv_fields() -> None:
    record = NounRecord.from_csv_fields(
        ["Haus", "das", "house", "Hauser", "Das Haus ist gross.", ""]
    )
    assert record.noun == "Haus"
    assert record.article == "das"
    assert record.plural == "Hauser"


def test_german_verb_separable_flag() -> None:
    record = VerbRecord.from_csv_fields(
        [
            "aufstehen",
            "to get up",
            "regular",
            "stehe auf",
            "stehst auf",
            "steht auf",
            "stand auf",
            "sein",
            "ist aufgestanden",
            "Ich stehe früh auf.",
            "true",
        ]
    )
    assert record.separable is True


def test_korean_noun_particles_generated() -> None:
    record = KoreanNounRecord.from_csv_fields(
        [
            "사과",
            "sagwa",
            "apple",
            "개",
            "food",
            "",
            "",
            "",
            "",
        ]
    )
    assert record.topic_particle.endswith("는")
    assert record.subject_particle.endswith("가")
    assert record.object_particle.endswith("를")


def test_russian_noun_defaults() -> None:
    record = RussianNounRecord.from_csv_fields(
        ["dom", "house", "masculine", "doma"]
    )
    assert record.nominative == "dom"
    assert record.accusative == "dom"
