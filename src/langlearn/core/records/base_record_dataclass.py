"""Compatibility alias for BaseRecord/RecordType.

This module re-exports the canonical BaseRecord/RecordType definitions to
avoid duplicate Enum classes across legacy dataclass record modules.
"""

from .base_record import BaseRecord, RecordClassProtocol, RecordType

__all__ = ["BaseRecord", "RecordClassProtocol", "RecordType"]
