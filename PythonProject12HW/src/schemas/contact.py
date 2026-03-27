from typing import Optional
import re
from datetime import datetime

from src.schemas.user import UserResponse

from pydantic import BaseModel, EmailStr, Field, field_validator

class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=70)
    last_name: str = Field(min_length=3, max_length=70)
    email: str = Field(min_length=3, max_length=120)
    phone: str = Field(min_length=3, max_length=120)
    birthday: str = Field(min_length=3, max_length=120)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

class ContactUpdateSchema(ContactSchema):
    first_name: Optional[str] = Field(None, min_length=1, max_length=70)
    last_name: Optional[str] = Field(None, min_length=1, max_length=70)
    email: Optional[str] = Field(None, min_length=1, max_length=120)
    phone: Optional[str] = Field(None, min_length=1, max_length=120)
    birthday: Optional[str] = Field(None, min_length=1, max_length=120)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

class ContactResponseSchema(ContactSchema):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    class Config:
        from_attributes = True