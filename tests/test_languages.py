"""Tests for language implementations and registry wiring."""

from __future__ import annotations

from pathlib import Path

import pytest

from langlearn.languages.german.language import GermanLanguage
from langlearn.languages.german.models import (
    Adjective,
    Adverb,
    AdverbType,
    Article,
    Negation,
    NegationType,
    Noun,
    Phrase,
    Preposition,
    Verb,
)
from langlearn.languages.german.records.factory import GermanRecordFactory
from langlearn.languages.korean.language import KoreanLanguage
from langlearn.languages.korean.models.noun import KoreanNoun
from langlearn.languages.russian.language import RussianLanguage
from langlearn.languages.russian.models.noun import RussianNoun

# ---------------------------------------------------------------------------
# German language
# ---------------------------------------------------------------------------


class TestGermanLanguageProperties:
    def test_code(self) -> None:
        assert GermanLanguage().code == "de"

    def test_name(self) -> None:
        assert GermanLanguage().name == "German"


class TestGermanRecordTypes:
    def test_supported_types_delegates_to_factory(self) -> None:
        lang = GermanLanguage()
        expected = GermanRecordFactory.get_supported_types()
        assert lang.get_supported_record_types() == expected

    def test_csv_mapping_has_13_entries(self) -> None:
        mapping = GermanLanguage().get_csv_to_record_type_mapping()
        assert len(mapping) == 13

    def test_csv_mapping_nouns(self) -> None:
        mapping = GermanLanguage().get_csv_to_record_type_mapping()
        assert mapping["nouns.csv"] == "noun"

    def test_csv_mapping_verbs_unified(self) -> None:
        mapping = GermanLanguage().get_csv_to_record_type_mapping()
        assert mapping["verbs_unified.csv"] == "verb_conjugation"


class TestGermanTTSConfig:
    def test_voice_and_language(self) -> None:
        config = GermanLanguage().get_tts_config()
        assert config.voice_id == "Marlene"
        assert config.language_code == "de-DE"


class TestGermanTemplates:
    def test_template_path(self) -> None:
        path = GermanLanguage().get_template_path("noun", "front")
        assert path.endswith("noun_DE_de_front.html")

    def test_template_filename(self) -> None:
        result = GermanLanguage().get_template_filename("noun", "front")
        assert result == "noun_DE_de_front.html"

    def test_template_filename_css(self) -> None:
        assert GermanLanguage().get_template_filename("noun", "css") == "noun_DE_de.css"

    def test_template_directory(self) -> None:
        directory = GermanLanguage().get_template_directory()
        assert isinstance(directory, Path)
        assert directory.name == "templates"


class TestGermanCreateRecordFromCSV:
    def test_noun_round_trip(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "noun", ["Haus", "das", "house", "Häuser", "Das Haus ist groß.", "Gebäude"]
        )
        assert record.to_dict()["noun"] == "Haus"
        assert record.to_dict()["article"] == "das"

    def test_verb_round_trip(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "verb",
            [
                "arbeiten",
                "to work",
                "regelmäßig",
                "arbeite",
                "arbeitest",
                "arbeitet",
                "arbeitete",
                "haben",
                "hat gearbeitet",
                "Er arbeitet in einer Bank.",
                "false",
            ],
        )
        assert record.to_dict()["verb"] == "arbeiten"

    def test_invalid_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown model type"):
            GermanLanguage().create_record_from_csv("invalid_type", ["a", "b"])


class TestGermanCreateDomainModel:
    def test_noun(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "noun", ["Katze", "die", "cat", "Katzen", "Die Katze schläft.", "Tier"]
        )
        model = lang.create_domain_model("noun", record)
        assert isinstance(model, Noun)
        assert model.noun == "Katze"
        assert model.article == "die"

    def test_verb(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "verb",
            [
                "gehen",
                "to go",
                "unregelmäßig",
                "gehe",
                "gehst",
                "geht",
                "ging",
                "sein",
                "ist gegangen",
                "Er geht nach Hause.",
                "false",
            ],
        )
        model = lang.create_domain_model("verb", record)
        assert isinstance(model, Verb)
        assert model.verb == "gehen"
        assert model.auxiliary == "sein"

    def test_adjective(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "adjective",
            ["schön", "beautiful", "Das ist schön.", "schöner", "am schönsten"],
        )
        model = lang.create_domain_model("adjective", record)
        assert isinstance(model, Adjective)
        assert model.word == "schön"

    def test_adverb(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "adverb", ["heute", "today", "Zeitadverb", "Heute regnet es."]
        )
        model = lang.create_domain_model("adverb", record)
        assert isinstance(model, Adverb)
        assert model.word == "heute"
        assert model.type == AdverbType.TIME

    def test_negation(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "negation", ["nicht", "not", "general", "Ich bin nicht müde."]
        )
        model = lang.create_domain_model("negation", record)
        assert isinstance(model, Negation)
        assert model.type == NegationType.GENERAL

    def test_phrase(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "phrase", ["Guten Morgen!", "Good morning!", "formal greeting", "Guten Tag"]
        )
        model = lang.create_domain_model("phrase", record)
        assert isinstance(model, Phrase)
        assert model.phrase == "Guten Morgen!"

    def test_preposition(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "preposition",
            [
                "auf",
                "on/onto",
                "Akkusativ/Dativ",
                "Das Buch liegt auf dem Tisch.",
                "Er legt das Buch auf den Tisch.",
            ],
        )
        model = lang.create_domain_model("preposition", record)
        assert isinstance(model, Preposition)
        assert model.preposition == "auf"

    def test_article(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "article",
            [
                "masculine",
                "der",
                "den",
                "dem",
                "des",
                "Der Mann liest.",
                "Ich sehe den Mann.",
                "Ich gebe dem Mann.",
                "Das Buch des Mannes.",
            ],
        )
        model = lang.create_domain_model("article", record)
        assert isinstance(model, Article)
        assert model.nominativ == "der"
        assert model.geschlecht == "maskulin"

    def test_unsupported_type_raises(self) -> None:
        lang = GermanLanguage()
        record = lang.create_record_from_csv(
            "noun", ["Haus", "das", "house", "Häuser", "Das Haus ist groß.", ""]
        )
        with pytest.raises(ValueError, match="Unsupported record type"):
            lang.create_domain_model("nonexistent", record)


class TestGermanNoteTypeMappings:
    def test_has_16_entries(self) -> None:
        assert len(GermanLanguage().get_note_type_mappings()) == 16

    def test_noun_mapping(self) -> None:
        mappings = GermanLanguage().get_note_type_mappings()
        assert mappings["German Noun"] == "noun"
        assert mappings["German Noun with Media"] == "noun"


class TestGermanStubs:
    def test_get_card_builder_raises(self) -> None:
        with pytest.raises(NotImplementedError, match="langlearn-anki-jyy"):
            GermanLanguage().get_card_builder()

    def test_get_card_processor_raises(self) -> None:
        with pytest.raises(NotImplementedError, match="langlearn-anki-jyy"):
            GermanLanguage().get_card_processor()

    def test_get_grammar_service_raises(self) -> None:
        with pytest.raises(NotImplementedError, match="langlearn-zmf"):
            GermanLanguage().get_grammar_service()

    def test_get_media_enricher_raises(self) -> None:
        with pytest.raises(NotImplementedError, match="langlearn-zmf"):
            GermanLanguage().get_media_enricher()

    def test_create_media_enricher_raises(self) -> None:
        with pytest.raises(NotImplementedError, match="langlearn-zmf"):
            GermanLanguage().create_media_enricher(None, None, None, None, None)

    def test_process_fields_for_anki_raises(self) -> None:
        with pytest.raises(NotImplementedError, match="langlearn-anki-jyy"):
            GermanLanguage().process_fields_for_anki("German Noun", [], None)

    def test_get_record_mapper_raises(self) -> None:
        with pytest.raises(NotImplementedError, match="langlearn-anki-jyy"):
            GermanLanguage().get_record_mapper()


# ---------------------------------------------------------------------------
# Korean language
# ---------------------------------------------------------------------------


class TestKoreanLanguageProperties:
    def test_code(self) -> None:
        assert KoreanLanguage().code == "ko"

    def test_name(self) -> None:
        assert KoreanLanguage().name == "Korean"


class TestKoreanRecordTypes:
    def test_supported_types(self) -> None:
        assert KoreanLanguage().get_supported_record_types() == ["korean_noun"]

    def test_csv_mapping(self) -> None:
        mapping = KoreanLanguage().get_csv_to_record_type_mapping()
        assert mapping == {"nouns.csv": "korean_noun"}


class TestKoreanTTSConfig:
    def test_voice_and_language(self) -> None:
        config = KoreanLanguage().get_tts_config()
        assert config.voice_id == "Seoyeon"
        assert config.language_code == "ko-KR"


class TestKoreanCreateRecordFromCSV:
    def test_noun_round_trip(self) -> None:
        lang = KoreanLanguage()
        record = lang.create_record_from_csv(
            "korean_noun",
            ["사과", "sagwa", "apple", "개", "food", "", "", "", ""],
        )
        assert record.to_dict()["hangul"] == "사과"

    def test_invalid_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported record type"):
            KoreanLanguage().create_record_from_csv("noun", ["a"])


class TestKoreanCreateDomainModel:
    def test_noun(self) -> None:
        lang = KoreanLanguage()
        record = lang.create_record_from_csv(
            "korean_noun",
            ["사과", "sagwa", "apple", "개", "food", "", "", "", ""],
        )
        model = lang.create_domain_model("korean_noun", record)
        assert isinstance(model, KoreanNoun)
        assert model.hangul == "사과"
        assert model.english == "apple"

    def test_unsupported_type_raises(self) -> None:
        lang = KoreanLanguage()
        record = lang.create_record_from_csv(
            "korean_noun",
            ["사과", "sagwa", "apple", "개", "food", "", "", "", ""],
        )
        with pytest.raises(ValueError, match="Unsupported record type"):
            lang.create_domain_model("noun", record)


class TestKoreanNoteTypeMappings:
    def test_mappings(self) -> None:
        mappings = KoreanLanguage().get_note_type_mappings()
        assert mappings["Korean Noun"] == "korean_noun"
        assert mappings["Korean Noun with Media"] == "korean_noun"


class TestKoreanStubs:
    def test_get_card_builder_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            KoreanLanguage().get_card_builder()

    def test_get_grammar_service_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            KoreanLanguage().get_grammar_service()

    def test_process_fields_for_anki_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            KoreanLanguage().process_fields_for_anki("Korean Noun", [], None)


# ---------------------------------------------------------------------------
# Russian language
# ---------------------------------------------------------------------------


class TestRussianLanguageProperties:
    def test_code(self) -> None:
        assert RussianLanguage().code == "ru"

    def test_name(self) -> None:
        assert RussianLanguage().name == "Russian"


class TestRussianRecordTypes:
    def test_supported_types(self) -> None:
        assert RussianLanguage().get_supported_record_types() == ["noun"]

    def test_csv_mapping(self) -> None:
        mapping = RussianLanguage().get_csv_to_record_type_mapping()
        assert mapping == {"nouns.csv": "noun"}


class TestRussianTTSConfig:
    def test_voice_and_language(self) -> None:
        config = RussianLanguage().get_tts_config()
        assert config.voice_id == "Tatyana"
        assert config.language_code == "ru-RU"


class TestRussianCreateRecordFromCSV:
    def test_noun_round_trip(self) -> None:
        lang = RussianLanguage()
        fields = ["дом", "house", "masculine", "дома"]
        record = lang.create_record_from_csv("noun", fields)
        assert record.to_dict()["noun"] == "дом"

    def test_invalid_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported record type"):
            RussianLanguage().create_record_from_csv("verb", ["a"])


class TestRussianCreateDomainModel:
    def test_noun(self) -> None:
        lang = RussianLanguage()
        fields = ["дом", "house", "masculine", "дома"]
        record = lang.create_record_from_csv("noun", fields)
        model = lang.create_domain_model("noun", record)
        assert isinstance(model, RussianNoun)
        assert model.noun == "дом"
        assert model.english == "house"
        assert model.gender == "masculine"

    def test_unsupported_type_raises(self) -> None:
        lang = RussianLanguage()
        fields = ["дом", "house", "masculine", "дома"]
        record = lang.create_record_from_csv("noun", fields)
        with pytest.raises(ValueError, match="Unsupported record type"):
            lang.create_domain_model("verb", record)


class TestRussianNoteTypeMappings:
    def test_mappings(self) -> None:
        mappings = RussianLanguage().get_note_type_mappings()
        assert mappings["Russian Noun"] == "noun"
        assert mappings["Russian Noun with Media"] == "noun"


class TestRussianStubs:
    def test_get_card_builder_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            RussianLanguage().get_card_builder()

    def test_get_media_enricher_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            RussianLanguage().get_media_enricher()

    def test_process_fields_for_anki_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            RussianLanguage().process_fields_for_anki("Russian Noun", [], None)


# ---------------------------------------------------------------------------
# Registry integration
# ---------------------------------------------------------------------------


class TestLanguageRegistry:
    def test_all_languages_registered(self) -> None:
        # Importing langlearn.languages triggers registration
        import langlearn.languages  # noqa: F401  # pyright: ignore[reportUnusedImport]
        from langlearn.languages.registry import LanguageRegistry

        available = LanguageRegistry.list_available()
        assert "de" in available
        assert "ko" in available
        assert "ru" in available

    def test_get_german(self) -> None:
        import langlearn.languages  # noqa: F401  # pyright: ignore[reportUnusedImport]
        from langlearn.languages.registry import LanguageRegistry

        lang = LanguageRegistry.get("de")
        assert lang.code == "de"
        assert lang.name == "German"

    def test_get_korean(self) -> None:
        import langlearn.languages  # noqa: F401  # pyright: ignore[reportUnusedImport]
        from langlearn.languages.registry import LanguageRegistry

        lang = LanguageRegistry.get("ko")
        assert lang.code == "ko"
        assert lang.name == "Korean"

    def test_get_russian(self) -> None:
        import langlearn.languages  # noqa: F401  # pyright: ignore[reportUnusedImport]
        from langlearn.languages.registry import LanguageRegistry

        lang = LanguageRegistry.get("ru")
        assert lang.code == "ru"
        assert lang.name == "Russian"

    def test_get_unregistered_raises(self) -> None:
        from langlearn.languages.registry import LanguageRegistry

        with pytest.raises(ValueError, match="not registered"):
            LanguageRegistry.get("xx")
