"""German language implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from langlearn.core.protocols.tts_protocol import TTSConfig
from langlearn.core.records import BaseRecord
from langlearn.languages.german.models import (
    GERMAN_TO_ENGLISH_ADVERB_TYPE_MAP,
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


class GermanLanguage:
    """German language implementation satisfying the Language protocol."""

    @property
    def code(self) -> str:
        return "de"

    @property
    def name(self) -> str:
        return "German"

    def get_supported_record_types(self) -> list[str]:
        return GermanRecordFactory.get_supported_types()

    def get_csv_to_record_type_mapping(self) -> dict[str, str]:
        return {
            "nouns.csv": "noun",
            "adjectives.csv": "adjective",
            "adverbs.csv": "adverb",
            "negations.csv": "negation",
            "prepositions.csv": "preposition",
            "phrases.csv": "phrase",
            "verbs.csv": "verb",
            "verbs_unified.csv": "verb_conjugation",
            "verb_imperatives.csv": "verb_imperative",
            "articles.csv": "article",
            "articles_unified.csv": "unified_article",
            "indefinite_articles.csv": "indefinite_article",
            "negative_articles.csv": "negative_article",
        }

    def get_tts_config(self) -> TTSConfig:
        return TTSConfig(voice_id="Marlene", language_code="de-DE")

    def get_template_path(self, record_type: str, side: str) -> str:
        templates_dir = Path(__file__).parent / "templates"
        return str(templates_dir / f"{record_type}_DE_de_{side}.html")

    def get_template_filename(self, card_type: str, side: str) -> str:
        if side == "css":
            return f"{card_type}_DE_de.css"
        return f"{card_type}_DE_de_{side}.html"

    def get_template_directory(self) -> Path:
        return Path(__file__).parent / "templates"

    def create_domain_model(self, record_type: str, record: BaseRecord) -> Any:
        d = record.to_dict()

        if record_type == "noun":
            return Noun(
                noun=d["noun"],
                article=d["article"],
                english=d["english"],
                plural=d["plural"],
                example=d["example"],
                related=d.get("related", ""),
            )

        if record_type == "verb":
            return Verb(
                verb=d["verb"],
                english=d["english"],
                present_ich=d["present_ich"],
                present_du=d["present_du"],
                present_er=d["present_er"],
                perfect=d["perfect"],
                example=d["example"],
                classification=d.get("classification", ""),
                präteritum=d.get("präteritum", ""),
                auxiliary=d.get("auxiliary", ""),
                separable=d.get("separable", False),
            )

        if record_type == "adjective":
            return Adjective(
                word=d["word"],
                english=d["english"],
                example=d["example"],
                comparative=d.get("comparative", ""),
                superlative=d.get("superlative", ""),
            )

        if record_type == "adverb":
            raw_type = d.get("type", "")
            adverb_type = GERMAN_TO_ENGLISH_ADVERB_TYPE_MAP.get(
                raw_type, AdverbType.MANNER
            )
            return Adverb(
                word=d["word"],
                english=d["english"],
                type=adverb_type,
                example=d["example"],
            )

        if record_type == "negation":
            raw_type = d.get("type", "general")
            return Negation(
                word=d["word"],
                english=d["english"],
                type=NegationType(raw_type),
                example=d["example"],
            )

        if record_type == "phrase":
            return Phrase(
                phrase=d["phrase"],
                english=d["english"],
                context=d["context"],
                related=d["related"],
            )

        if record_type == "preposition":
            return Preposition(
                preposition=d["preposition"],
                english=d["english"],
                case=d["case"],
                example1=d.get("example1", ""),
                example2=d.get("example2", ""),
            )

        if record_type == "article":
            gender_map = {
                "masculine": "maskulin",
                "feminine": "feminin",
                "neuter": "neutral",
                "plural": "plural",
            }
            return Article(
                artikel_typ="bestimmt",
                geschlecht=gender_map.get(d["gender"]) or d["gender"],
                nominativ=d["nominative"],
                akkusativ=d["accusative"],
                dativ=d["dative"],
                genitiv=d["genitive"],
                beispiel_nom=d["example_nom"],
                beispiel_akk=d["example_acc"],
                beispiel_dat=d["example_dat"],
                beispiel_gen=d["example_gen"],
            )

        raise ValueError(
            f"Unsupported record type '{record_type}' for German language. "
            f"Supported: {self.get_supported_record_types()}"
        )

    def create_record_from_csv(self, record_type: str, fields: list[str]) -> BaseRecord:
        return GermanRecordFactory.create(record_type, fields)

    def get_note_type_mappings(self) -> dict[str, str]:
        return {
            "German Noun": "noun",
            "German Noun with Media": "noun",
            "German Adjective": "adjective",
            "German Adjective with Media": "adjective",
            "German Adverb": "adverb",
            "German Adverb with Media": "adverb",
            "German Negation": "negation",
            "German Negation with Media": "negation",
            "German Verb": "verb",
            "German Verb with Media": "verb",
            "German Phrase": "phrase",
            "German Phrase with Media": "phrase",
            "German Preposition": "preposition",
            "German Preposition with Media": "preposition",
            "German Artikel Gender with Media": "unified_article",
            "German Artikel Context with Media": "unified_article",
        }

    # --- Stubs for methods requiring downstream ports ---

    def get_card_builder(self) -> Any:
        raise NotImplementedError("Requires langlearn-anki-jyy")

    def get_card_processor(self) -> Any:
        raise NotImplementedError("Requires langlearn-anki-jyy")

    def get_record_mapper(self) -> Any:
        raise NotImplementedError("Requires langlearn-anki-jyy")

    def get_grammar_service(self) -> Any:
        raise NotImplementedError("Requires langlearn-zmf")

    def get_media_enricher(self) -> Any:
        raise NotImplementedError("Requires langlearn-zmf")

    def create_media_enricher(
        self,
        audio_service: Any,
        image_service: Any,
        anthropic_service: Any,
        audio_base_path: Any,
        image_base_path: Any,
    ) -> Any:
        raise NotImplementedError("Requires langlearn-zmf")

    def process_fields_for_anki(
        self,
        note_type_name: str,
        fields: list[str],
        media_enricher: Any,
    ) -> list[str]:
        raise NotImplementedError("Requires langlearn-anki-jyy")
