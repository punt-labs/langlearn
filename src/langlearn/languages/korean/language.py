"""Korean language implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from langlearn.core.protocols.tts_protocol import TTSConfig
from langlearn.core.records import BaseRecord
from langlearn.languages.korean.models.noun import KoreanNoun
from langlearn.languages.korean.records.noun_record import KoreanNounRecord


class KoreanLanguage:
    """Korean language implementation satisfying the Language protocol."""

    @property
    def code(self) -> str:
        return "ko"

    @property
    def name(self) -> str:
        return "Korean"

    def get_supported_record_types(self) -> list[str]:
        return ["korean_noun"]

    def get_csv_to_record_type_mapping(self) -> dict[str, str]:
        return {"nouns.csv": "korean_noun"}

    def get_tts_config(self) -> TTSConfig:
        return TTSConfig(voice_id="Seoyeon", language_code="ko-KR")

    def get_template_path(self, record_type: str, side: str) -> str:
        templates_dir = Path(__file__).parent / "templates"
        return str(templates_dir / f"{record_type}_KO_ko_{side}.html")

    def get_template_filename(self, card_type: str, side: str) -> str:
        if side == "css":
            return f"{card_type}_KO_ko.css"
        return f"{card_type}_KO_ko_{side}.html"

    def get_template_directory(self) -> Path:
        return Path(__file__).parent / "templates"

    def create_domain_model(self, record_type: str, record: BaseRecord) -> Any:
        if record_type == "korean_noun":
            d = record.to_dict()
            return KoreanNoun(**d)

        raise ValueError(
            f"Unsupported record type '{record_type}' for Korean language. "
            f"Supported: {self.get_supported_record_types()}"
        )

    def create_record_from_csv(self, record_type: str, fields: list[str]) -> BaseRecord:
        if record_type == "korean_noun":
            return KoreanNounRecord.from_csv_fields(fields)

        raise ValueError(
            f"Unsupported record type '{record_type}' for Korean language. "
            f"Supported: {self.get_supported_record_types()}"
        )

    def get_note_type_mappings(self) -> dict[str, str]:
        return {
            "Korean Noun": "korean_noun",
            "Korean Noun with Media": "korean_noun",
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
