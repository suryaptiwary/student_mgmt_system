from pydantic import BaseModel, Field
from typing import Optional


class Address(BaseModel):
    city: str
    country: str


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the student")
    age: int = Field(..., ge=0, description="Age of the student (must be >= 0)")
    address: Address


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, ge=0)
    address: Optional[Address] = None

class StudentResponse(StudentCreate):
    id: str
