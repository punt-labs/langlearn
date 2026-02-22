from langlearn.languages.korean.language import KoreanLanguage
from langlearn.languages.registry import LanguageRegistry

LanguageRegistry.register("ko", KoreanLanguage)

__all__ = ["KoreanLanguage"]
