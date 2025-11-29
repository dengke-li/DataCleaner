from typing import Optional

from pydantic import BaseModel, Field, validator


class PassengerRaw(BaseModel):
    Name: str = Field(...)
    Age: Optional[float] = Field(None, ge=0)
    Pclass: int = Field(...)
    Fare: float = Field(...)

