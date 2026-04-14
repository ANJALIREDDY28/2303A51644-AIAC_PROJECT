from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# SQLite database URL
DATABASE_URL = "sqlite:///./meals_db.sqlite"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    diet_plans = relationship("DietPlan", back_populates="user")

class DietPlan(Base):
    __tablename__ = "diet_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    activity_level = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    food_preference = Column(String, nullable=False)
    bmi = Column(Float)
    bmr = Column(Float)
    daily_calories = Column(Float)
    breakfast = Column(String)
    lunch = Column(String)
    dinner = Column(String)
    snacks = Column(String)
    water_intake = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="diet_plans")

# Create tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")

