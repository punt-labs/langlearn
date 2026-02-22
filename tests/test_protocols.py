"""Tests for core protocols, exceptions, and registry."""

from __future__ import annotations

import pytest

from langlearn.core.protocols.tts_protocol import TTSConfig
from langlearn.exceptions import (
    CardGenerationError,
    ConfigurationError,
    DataProcessingError,
    DomainError,
    LangLearnError,
    ProcessingError,
    ServiceError,
)
from langlearn.languages.registry import LanguageRegistry

# --- TTSConfig tests ---


def test_tts_config_defaults() -> None:
    config = TTSConfig(voice_id="Marlene", language_code="de-DE")
    assert config.engine == "standard"


def test_tts_config_custom_engine() -> None:
    config = TTSConfig(voice_id="Seoyeon", language_code="ko-KR", engine="neural")
    assert config.engine == "neural"


def test_tts_config_frozen() -> None:
    config = TTSConfig(voice_id="Tatyana", language_code="ru-RU")
    with pytest.raises(AttributeError):
        config.voice_id = "Other"  # type: ignore[misc]


# --- Exception hierarchy tests ---


def test_configuration_error_inherits_from_both() -> None:
    err = ConfigurationError("bad config")
    assert isinstance(err, LangLearnError)
    assert isinstance(err, ValueError)


def test_service_error_hierarchy() -> None:
    err = ServiceError("service down")
    assert isinstance(err, LangLearnError)
    assert not isinstance(err, ValueError)


def test_domain_error_hierarchy() -> None:
    assert issubclass(DomainError, LangLearnError)


def test_data_processing_error_hierarchy() -> None:
    assert issubclass(DataProcessingError, LangLearnError)


def test_card_generation_error_hierarchy() -> None:
    assert issubclass(CardGenerationError, LangLearnError)


def test_catch_all_with_langlearn_error() -> None:
    """All project exceptions are catchable via LangLearnError."""
    for exc_cls in [
        ConfigurationError,
        ServiceError,
        DomainError,
        DataProcessingError,
        CardGenerationError,
    ]:
        with pytest.raises(LangLearnError):
            raise exc_cls("test")


def test_processing_error_str() -> None:
    err = ProcessingError(record="noun:Haus", error=ValueError("bad"), context="row 3")
    assert "noun:Haus" in str(err)
    assert "bad" in str(err)
    assert "row 3" in str(err)


def test_processing_error_str_no_context() -> None:
    err = ProcessingError(record="noun:Haus", error=ValueError("bad"))
    result = str(err)
    assert "noun:Haus" in result
    assert "row 3" not in result


def test_processing_error_repr() -> None:
    err = ProcessingError(record="noun:Haus", error=ValueError("bad"), context="row 3")
    r = repr(err)
    assert "ProcessingError" in r
    assert "noun:Haus" in r


# --- LanguageRegistry tests ---


def test_registry_register_and_get() -> None:
    LanguageRegistry.clear()

    class FakeLang:
        code = "xx"
        name = "Fake"

    LanguageRegistry.register("xx", FakeLang)  # type: ignore[arg-type]
    lang = LanguageRegistry.get("xx")
    assert lang.code == "xx"
    LanguageRegistry.clear()


def test_registry_get_unregistered_raises() -> None:
    LanguageRegistry.clear()
    with pytest.raises(ValueError, match="not registered"):
        LanguageRegistry.get("zz")


def test_registry_list_available() -> None:
    LanguageRegistry.clear()

    class FakeLang:
        code = "xx"

    LanguageRegistry.register("xx", FakeLang)  # type: ignore[arg-type]
    LanguageRegistry.register("yy", FakeLang)  # type: ignore[arg-type]
    available = LanguageRegistry.list_available()
    assert "xx" in available
    assert "yy" in available
    LanguageRegistry.clear()


def test_registry_clear() -> None:
    class FakeLang:
        code = "xx"

    LanguageRegistry.register("xx", FakeLang)  # type: ignore[arg-type]
    LanguageRegistry.clear()
    assert LanguageRegistry.list_available() == []
