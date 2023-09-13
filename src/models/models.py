from typing import Optional, List
from pydantic import BaseModel


class CharacterState(BaseModel):
    name: Optional[str]
    physical_appearance: Optional[str]
    background: Optional[str]
    internal_motivation: Optional[str]
    unique_traits: Optional[str]


class WorldState(BaseModel):
    name: Optional[str]
    geography: Optional[str]
    history: Optional[str]
    cultures: Optional[str]
    magic_system: Optional[str]


class PlotDescription(BaseModel):
    context: Optional[str]
