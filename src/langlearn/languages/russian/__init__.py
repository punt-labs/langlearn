from langlearn.languages.registry import LanguageRegistry
from langlearn.languages.russian.language import RussianLanguage

LanguageRegistry.register("ru", RussianLanguage)

__all__ = ["RussianLanguage"]
