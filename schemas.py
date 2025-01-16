from pydantic import BaseModel, EmailStr, validator, constr
from typing import List
import re
from email_validator import validate_email, EmailNotValidError

class UserBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    age: int
    gender: str
    email: str
    city: constr(min_length=1, max_length=50)
    interests: List[str]

    @validator('email')
    def validate_email(cls, v):
        try:
            # Validate and normalize the email
            email_info = validate_email(v, check_deliverability=True)
            # Get the normalized form of the email
            normalized_email = email_info.normalized
            return normalized_email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {str(e)}")

    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 100:
            raise ValueError('Age must be between 18 and 100')
        return v

    @validator('gender')
    def validate_gender(cls, v):
        valid_genders = ['male', 'female']
        if v.lower() not in valid_genders:
            raise ValueError('Gender must be either "male" or "female"')
        return v.lower()

    @validator('interests')
    def validate_interests(cls, v):
        if not v:  # Check if empty
            raise ValueError('At least one interest is required')
        
        # Clean and validate each interest
        cleaned = []
        for interest in v:
            if isinstance(interest, str):
                # Remove special characters and extra spaces
                cleaned_interest = re.sub(r'[^\w\s-]', '', interest).strip()
                if cleaned_interest and len(cleaned_interest) <= 30:  # Max length for each interest
                    cleaned.append(cleaned_interest.lower())
        
        if not cleaned:
            raise ValueError('No valid interests provided')
        return cleaned

    @validator('interests', pre=True)
    def split_interests(cls, v):
        if isinstance(v, str):
            # Handle empty string case
            return v.split(',') if v else []
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: constr(min_length=1, max_length=50) | None = None
    age: int | None = None
    gender: str | None = None
    email: str | None = None
    city: constr(min_length=1, max_length=50) | None = None
    interests: List[str] | None = None

    @validator('email')
    def validate_email(cls, v):
        if v is not None:
            try:
                # Validate and normalize the email
                email_info = validate_email(v, check_deliverability=True)
                # Get the normalized form of the email
                return email_info.normalized
            except EmailNotValidError as e:
                raise ValueError(f"Invalid email address: {str(e)}")
        return v

    @validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 18 or v > 100):
            raise ValueError('Age must be between 18 and 100')
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v is not None:
            valid_genders = ['male', 'female']
            if v.lower() not in valid_genders:
                raise ValueError('Gender must be either "male" or "female"')
            return v.lower()
        return v

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

