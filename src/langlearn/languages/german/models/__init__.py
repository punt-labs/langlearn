"""German language domain models.

Exports all German-specific domain model classes and enums for nouns, verbs,
adjectives, adverbs, articles, negations, phrases, and prepositions.
"""

from langlearn.languages.german.models.adjective import Adjective
from langlearn.languages.german.models.adverb import (
    GERMAN_ADVERB_TYPES,
    GERMAN_TO_ENGLISH_ADVERB_TYPE_MAP,
    Adverb,
    AdverbType,
)
from langlearn.languages.german.models.article import Article
from langlearn.languages.german.models.negation import Negation, NegationType
from langlearn.languages.german.models.noun import Noun
from langlearn.languages.german.models.phrase import Phrase
from langlearn.languages.german.models.preposition import Preposition
from langlearn.languages.german.models.verb import Verb

__all__ = [
    "GERMAN_ADVERB_TYPES",
    "GERMAN_TO_ENGLISH_ADVERB_TYPE_MAP",
    "Adjective",
    "Adverb",
    "AdverbType",
    "Article",
    "Negation",
    "NegationType",
    "Noun",
    "Phrase",
    "Preposition",
    "Verb",
]
