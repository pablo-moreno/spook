import re
from django.db.models import Model
from typing import Type


def pluralize(text: str) -> str:
    """
        Pluralizes a word depending on the last letter of the word
    """
    return f'{text}ies' if text[-1] == 'y' else f'{text}s'


def get_model_slug(model: Type[Model]) -> str:
    """
        Returns the model slug
    """
    slug = re.sub('(?<=.)([A-Z]+)', '-\\1', model.__name__).lower()
    return pluralize(slug)
