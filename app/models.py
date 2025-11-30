from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class PassengerRaw(BaseModel):
    Name: str = Field(strict=True, description="Full name as in raw dataset, e.g. 'Bauer, Mr. John'")
    Age: int = Field(strict=True, ge=0, description="Age in years; must be non-negative")
    Pclass: int = Field(strict=True, description="Passenger class: 1, 2 or 3")
    Fare: float = Field(..., description="Passenger fare; must be positive")

    @field_validator("Name", mode="before")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Name must not be blank")
        return v

    @field_validator("Age", mode="before")
    @classmethod
    def validate_age(cls, v):
        if v<0:
            raise ValueError("age must >=0")
        return v

    @field_validator("Pclass", mode="before")
    @classmethod
    def validate_pclass(cls, v):
        if v not in {1,2,3}:
            raise ValueError("Pclass must be 1, 2, or 3")
        return v

    @field_validator("Fare", mode="before")
    @classmethod
    def validate_fare(cls, v):
        if v <= 0:
            raise ValueError("Fare must be positive")
        return v

class PassengerClean(BaseModel):
    Name: str
    Age: int
    Pclass: int
    Fare: float
    Title: Optional[str]
    Title_Normalized: Optional[str]

class CleaningStep(ABC):
    @abstractmethod
    def apply(self, passenger: PassengerClean) -> PassengerClean:
        """Return a new cleaned passenger instance (immutable-style)."""
        pass