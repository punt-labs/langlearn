"""Protocol for converting domain context into image search queries."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ImageQueryGenerationProtocol(Protocol):
    """Protocol for generating image search queries from domain context.

    This protocol defines the interface for services that can convert rich
    domain model context into optimized search queries for image APIs.
    """

    def generate_image_query(self, context: Any) -> str:
        """Generate an image search query from rich domain context.

        Args:
            context: Rich context string from domain model's _build_search_context()
                    containing linguistic expertise and visualization guidance

        Returns:
            Query string suitable for image search APIs (e.g., Pexels, Unsplash)
        """
        ...
