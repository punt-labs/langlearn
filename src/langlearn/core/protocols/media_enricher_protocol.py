"""Media enricher protocol for language-agnostic media enrichment."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from langlearn.core.protocols.media_generation_protocol import (
        MediaGenerationCapable,
    )


@runtime_checkable
class MediaEnricherProtocol(Protocol):
    """Protocol for language-agnostic media enrichment.

    This protocol allows core components to work with media enrichers from
    any language without knowing their specific implementation details.
    """

    def enrich_with_media(self, domain_model: MediaGenerationCapable) -> dict[str, Any]:
        """Enrich domain model with media using its domain expertise.

        Args:
            domain_model: Domain model implementing MediaGenerationCapable

        Returns:
            Dictionary containing generated media data with keys like:
            - 'image': Image filename or reference
            - 'word_audio': Audio filename for word pronunciation
            - 'example_audio': Audio filename for example sentence

        Raises:
            MediaGenerationError: If media generation fails
        """
        ...
