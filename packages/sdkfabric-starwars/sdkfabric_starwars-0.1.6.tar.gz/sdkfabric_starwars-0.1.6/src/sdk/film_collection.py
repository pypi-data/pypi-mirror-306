"""
film_collection automatically generated by SDKgen please do not edit this file manually
https://sdkgen.app
"""

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from .collection import Collection
from .film import Film
class FilmCollection(Collection):
    results: Optional[List[Film]] = Field(default=None, alias="results")
    pass
