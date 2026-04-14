from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class ActivityLevelEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class GoalEnum(str, Enum):
    loss = "weight_loss"
    maintenance = "maintenance"
    gain = "weight_gain"

class FoodPreferenceEnum(str, Enum):
    veg = "veg"
    non_veg = "non_veg"

# Request models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DietInput(BaseModel):
    age: int
    gender: GenderEnum
    height: float  # in cm
    weight: float  # in kg
    activity_level: ActivityLevelEnum
    goal: GoalEnum
    food_preference: FoodPreferenceEnum

class DietPlanResponse(BaseModel):
    id: Optional[int]
    bmi: float
    bmr: float
    daily_calories: float
    breakfast: str
    lunch: str
    dinner: str
    snacks: str
    water_intake: str
    created_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

