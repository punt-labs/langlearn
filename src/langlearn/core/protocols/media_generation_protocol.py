"""Protocol for domain models that support media generation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable

    from langlearn.core.protocols.image_query_generation_protocol import (
        ImageQueryGenerationProtocol,
    )


@runtime_checkable
class MediaGenerationCapable(Protocol):
    """Protocol for domain models that can generate media search terms.

    This protocol defines the interface that domain models must implement
    to support media enrichment. It enables dependency injection and loose
    coupling between MediaEnricher and domain models.
    """

    def get_image_search_strategy(
        self, ai_service: ImageQueryGenerationProtocol
    ) -> Callable[[], str]:
        """Get a strategy for generating image search terms.

        The domain model constructs context-aware requests using its knowledge of
        which fields are most relevant and part-of-speech specific guidance.

        Args:
            ai_service: Service for context-aware search term generation.

        Returns:
            A callable that generates image search terms when invoked
        """
        ...

    def get_combined_audio_text(self) -> str:
        """Get the text to be used for audio generation.

        Returns the complete text that should be converted to speech,
        including any language-specific pronunciation guidance or formatting.

        Returns:
            Text string for audio generation
        """
        ...

    def get_audio_segments(self) -> dict[str, str]:
        """Get all audio segments needed for this word type.

        Returns all audio field names and their corresponding text content
        that should be generated for cards of this type.

        Returns:
            Dictionary mapping audio field names to text content.
            E.g., {"word_audio": "das Haus", "example_audio": "Das ist mein Haus"}
        """
        ...

    def get_primary_word(self) -> str:
        """Get the primary word for filename generation and identification.

        Returns:
            The primary vocabulary word/term
        """
        ...
