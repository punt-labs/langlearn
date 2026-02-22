"""Core protocol definitions."""

from .domain_model_protocol import LanguageDomainModel
from .image_query_generation_protocol import ImageQueryGenerationProtocol
from .language_protocol import Language
from .media_enricher_protocol import MediaEnricherProtocol
from .media_generation_protocol import MediaGenerationCapable
from .tts_protocol import TTSConfig

__all__ = [
    "ImageQueryGenerationProtocol",
    "Language",
    "LanguageDomainModel",
    "MediaEnricherProtocol",
    "MediaGenerationCapable",
    "TTSConfig",
]
