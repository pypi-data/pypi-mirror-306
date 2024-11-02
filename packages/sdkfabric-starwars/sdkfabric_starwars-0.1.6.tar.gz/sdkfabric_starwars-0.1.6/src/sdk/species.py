"""
species automatically generated by SDKgen please do not edit this file manually
https://sdkgen.app
"""

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
import datetime


# A Species is a type of person or character within the Star Wars Universe
class Species(BaseModel):
    name: Optional[str] = Field(default=None, alias="name")
    classification: Optional[str] = Field(default=None, alias="classification")
    designation: Optional[str] = Field(default=None, alias="designation")
    average_height: Optional[str] = Field(default=None, alias="average_height")
    average_lifespan: Optional[str] = Field(default=None, alias="average_lifespan")
    eye_colors: Optional[str] = Field(default=None, alias="eye_colors")
    hair_colors: Optional[str] = Field(default=None, alias="hair_colors")
    skin_colors: Optional[str] = Field(default=None, alias="skin_colors")
    language: Optional[str] = Field(default=None, alias="language")
    homeworld: Optional[str] = Field(default=None, alias="homeworld")
    people: Optional[List[str]] = Field(default=None, alias="people")
    films: Optional[List[str]] = Field(default=None, alias="films")
    url: Optional[str] = Field(default=None, alias="url")
    created: Optional[datetime.datetime] = Field(default=None, alias="created")
    edited: Optional[datetime.datetime] = Field(default=None, alias="edited")
    pass
