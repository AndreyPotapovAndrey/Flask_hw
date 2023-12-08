from abc import ABC
from typing import Optional, Type

import pydantic


class AbstractAds(pydantic.BaseModel, ABC):
    title: str
    description: str
    owner: str

    @pydantic.field_validator("title")
    @classmethod
    def ads_length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError("Maxima length of title is 100")
        return v


class CreateAds(AbstractAds):
    title: str
    description: str
    owner: str


class UpdateAds(AbstractAds):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None


SCHEMA_CLASS = Type[CreateAds | UpdateAds]  # Создаём тип данных для передачи классов
SCHEMA = CreateAds | UpdateAds
