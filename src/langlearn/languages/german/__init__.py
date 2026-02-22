from langlearn.languages.german.language import GermanLanguage
from langlearn.languages.registry import LanguageRegistry

LanguageRegistry.register("de", GermanLanguage)

__all__ = ["GermanLanguage"]
