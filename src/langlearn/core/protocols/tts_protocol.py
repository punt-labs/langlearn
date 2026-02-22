"""TTS (Text-to-Speech) configuration protocol for language implementations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TTSConfig:
    """Configuration for Text-to-Speech audio generation.

    This dataclass encapsulates the TTS settings that each language
    implementation should provide for generating audio content.
    """

    voice_id: str
    """Voice identifier for the TTS provider (e.g., 'Marlene', 'Tatyana', 'Seoyeon')."""

    language_code: str
    """ISO language code (e.g., 'de-DE', 'ru-RU', 'ko-KR')."""

    engine: str = "standard"
    """Engine or model identifier for the TTS provider (default: 'standard')."""
