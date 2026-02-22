from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from langlearn.core.protocols.domain_model_protocol import LanguageDomainModel
from langlearn.core.protocols.media_generation_protocol import MediaGenerationCapable
from langlearn.exceptions import MediaGenerationError

if TYPE_CHECKING:
    from collections.abc import Callable

    from langlearn.core.protocols.image_query_generation_protocol import (
        ImageQueryGenerationProtocol,
    )

logger = logging.getLogger(__name__)

"""German Noun Domain Model.

This module contains the domain model for German nouns with specialized
logic for German language learning applications. The module is responsible
for:

CORE RESPONSIBILITIES:
    - Modeling German noun data (noun, article, English translation,
    plural, example)
    - Implementing MediaGenerationCapable protocol for media enrichment
    - Providing German-specific linguistic validation and gender
    classification
    - Contributing domain expertise for image search term generation
    - Supporting audio generation with proper article and plural pronunciation

DESIGN PRINCIPLES:
    - Domain model is SMART: Contains German noun expertise and linguistic
    knowledge
    - Services are DUMB: External services receive rich context, no domain
    logic
    - Single Responsibility: Noun logic stays in Noun model, not in services
    - Dependency Injection: Protocol-based design for loose coupling

GERMAN LINGUISTIC FEATURES:
    - Gender system with definite articles (der/die/das)
    - Plural formation patterns and irregular plurals
    - Concrete vs abstract noun classification for visualization strategies
    - Context-aware search term generation using linguistic domain knowledge
    - Audio generation combining singular and plural forms with articles

INTEGRATION POINTS:
    - MediaGenerationCapable protocol for image/audio media enrichment
    - ImageQueryGenerationProtocol for AI-powered search term generation
    - MediaEnricher service for coordinated media asset generation

Usage:
    Basic usage:
        >>> noun = Noun(
        ...     noun="Katze",
        ...     article="die",
        ...     english="cat",
        ...     plural="Katzen",
        ...     example="Die Katze schläft auf dem Sofa."
        ... )

    Media generation with dependency injection:
        >>> strategy = noun.get_image_search_strategy(anthropic_service)
        >>> search_terms = strategy()  # Returns context-aware search terms
        >>> audio_text = noun.get_combined_audio_text()  # Article + noun
        forms
"""


@dataclass
class Noun(LanguageDomainModel, MediaGenerationCapable):
    """German noun domain model with linguistic expertise and media
    generation.

    Represents a German noun with its properties, German linguistic knowledge,
    and specialized logic for media enrichment. German nouns are characterized
    by their grammatical gender (reflected in articles), plural formation
    patterns, and case declension system.

    This model implements MediaGenerationCapable protocol to contribute domain
    expertise for image and audio generation, using concrete/abstract
    classification strategies for appropriate visual representation.

    Attributes:
        noun: The German noun (e.g., "Katze", "Haus")
        article: Definite article indicating gender ("der", "die", "das")
        english: English translation (e.g., "cat", "house")
        plural: Plural form (e.g., "Katzen", "Häuser")
        example: German example sentence demonstrating usage
        related: Related words or phrases (optional)

    Note:
        This model follows the design principle that domain models are SMART
        (contain expertise) while services are DUMB (execute instructions).
    """

    noun: str
    article: str
    english: str
    plural: str
    example: str
    related: str = field(default="")

    def __post_init__(self) -> None:
        """Validate the noun data after initialization."""
        # Validate core required fields - 'plural' and 'related' can be empty
        required_fields = ["noun", "article", "english", "example"]
        for field_name in required_fields:
            value = getattr(self, field_name)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"Required field '{field_name}' cannot be empty")

        # Validate German article (only when non-empty)
        if (
            self.article
            and self.article.strip()
            and self.article not in {"der", "die", "das"}
        ):
            raise ValueError(
                f"Invalid German article: {self.article}. Must be 'der', "
                f"'die', or 'das'"
            )

    def get_combined_audio_text(self) -> str:
        """Get combined text for German noun audio generation.

        Combines the noun with its article in both singular and plural forms
        to provide proper pronunciation context for German language learners.
        This helps learners associate nouns with their grammatical gender and
        plural formation patterns.

        Returns:
            Formatted string: "{article} {noun}, {plural_with_article}" for
            audio.

        Example:
            >>> noun = Noun(noun="Katze", article="die", english="cat",
            ...             plural="Katzen", example="Die Katze schläft.")
            >>> noun.get_combined_audio_text()
            'die Katze, die Katzen'
        """
        # Check if plural already includes article
        if self.plural.startswith(("der ", "die ", "das ")):
            return f"{self.article} {self.noun}, {self.plural}"
        else:
            return f"{self.article} {self.noun}, die {self.plural}"

    def get_audio_segments(self) -> dict[str, str]:
        """Get all audio segments needed for noun cards.

        Nouns require two audio segments:
        - word_audio: The noun with its article and plural form
        - example_audio: The example sentence demonstrating usage

        Returns:
            Dictionary mapping audio field names to text content
        """
        return {
            "word_audio": self.get_combined_audio_text(),
            "example_audio": self.example,
        }

    def get_primary_word(self) -> str:
        """Get the primary word for filename generation and identification.

        Returns the German noun that identifies this domain model.

        Returns:
            The German noun (e.g., "Haus", "Katze")
        """
        return self.noun

    def is_concrete(self) -> bool:
        """Classify German nouns as concrete or abstract based on linguistic patterns.

        Uses German morphological patterns and word lists to determine concreteness:
        - Abstract suffixes: -heit, -keit, -ung, -ion, -schaft
        - Abstract word list: common abstract concepts (emotions, ideas, etc.)
        - Concrete indicators: -chen, -zeug
        - Default: concrete (most German nouns are concrete)

        Returns:
            True for concrete nouns that can be visualized
            False for abstract concepts that cannot be directly depicted
        """
        # Abstract noun suffixes
        abstract_suffixes = ("heit", "keit", "ung", "ion", "schaft")
        if any(self.noun.endswith(suffix) for suffix in abstract_suffixes):
            return False

        # Common abstract nouns without typical suffixes
        abstract_words = {
            "Liebe",  # love
            "Angst",  # fear
            "Hoffnung",  # hope (actually has -ung but worth including)
            "Glaube",  # faith
            "Zeit",  # time
            "Glück",  # happiness/luck
            "Mut",  # courage
        }
        if self.noun in abstract_words:
            return False

        # Concrete noun indicators
        concrete_indicators = ("chen", "zeug")
        if any(self.noun.endswith(indicator) for indicator in concrete_indicators):
            return True

        # Default to concrete for other nouns
        return True

    def get_image_search_strategy(
        self, ai_service: ImageQueryGenerationProtocol
    ) -> Callable[[], str]:
        """Get strategy for generating image search terms with domain
        expertise.

        Creates a callable that uses this noun's domain knowledge to generate
        context-aware image search terms. The noun contributes German
        linguistic
        expertise (concrete vs abstract classification, gender context) while
        the anthropic service executes the actual AI processing.

        Design: Domain model is SMART (provides rich context), service is DUMB
        (processes whatever context it receives).

        Args:
            ai_service: Service implementing ImageQueryGenerationProtocol for
                AI-powered search term generation.

        Returns:
            Callable that when invoked returns image search terms as string.

        Raises:
            MediaGenerationError: When AI service returns empty result or fails.

        Example:
            >>> noun = Noun(noun="Katze", article="die", english="cat",
            ...             plural="Katzen", example="Die Katze schläft.")
            >>> strategy = noun.get_image_search_strategy(ai_service)
            >>> search_terms = strategy()  # Returns context-aware search terms
        """

        def generate_search_terms() -> str:
            """Execute search term generation strategy with noun context.

            Raises:
                MediaGenerationError: When AI service fails or returns empty result.
            """
            logger.info(
                f"🔄 AI CHAIN STEP 1: Starting search term generation for "
                f"German noun: '{self.noun}'"
            )

            try:
                # Use domain expertise to build rich context for the service
                context = self._build_search_context()
                logger.info(
                    f"📝 AI CHAIN INPUT: Context sent to AI service: '{context}'"
                )

                result = ai_service.generate_image_query(context)
                logger.info(f"🤖 AI CHAIN OUTPUT: Raw AI service response: '{result}'")

                if result and result.strip():
                    ai_generated_terms = result.strip()
                    logger.info(
                        f"✅ AI CHAIN STEP 1 COMPLETE: '{self.noun}' → "
                        f"'{ai_generated_terms}'"
                    )
                    return ai_generated_terms

                # AI service returned empty result - this is a service failure
                logger.error(
                    f"❌ AI CHAIN STEP 1 FAILED: Empty result from AI service for "
                    f"'{self.noun}'"
                )
                raise MediaGenerationError(
                    f"AI service returned empty image search query for noun "
                    f"'{self.noun}'"
                )
            except MediaGenerationError:
                # Re-raise our own exceptions
                raise
            except Exception as e:
                # Convert any other exception to MediaGenerationError
                raise MediaGenerationError(
                    f"Failed to generate image search for noun '{self.noun}': {e}"
                ) from e

        return generate_search_terms

    def _build_search_context(self) -> str:
        """Build simple context for image search."""
        return (
            f"German word: {self.noun} means {self.english}. "
            f"Generate a simple search term."
        )
