"""
Pydantic Schemas Module

This module defines the data validation schemas using Pydantic.
These schemas ensure that incoming data matches the expected format
and types before processing.
"""

from pydantic import BaseModel, Field


class StudentData(BaseModel):
    """
    Student Data Schema
    
    This schema defines the structure of input data for predictions.
    All fields are required and must match the types specified below.
    
    Attributes:
        attendance: Student's attendance percentage (0-100)
        study_hours: Number of hours studied per week
        assignments_completed: Number of assignments completed
        quiz_score: Average quiz score (0-100)
        midterm_score: Midterm exam score (0-100)
        internet_access: Whether student has internet access (0 or 1)
        past_failures: Number of past course failures
    """
    
    attendance: float = Field(..., description="Student's attendance percentage", ge=0, le=100)
    study_hours: float = Field(..., description="Number of hours studied per week", ge=0)
    assignments_completed: int = Field(..., description="Number of assignments completed", ge=0)
    quiz_score: float = Field(..., description="Average quiz score", ge=0, le=100)
    midterm_score: float = Field(..., description="Midterm exam score", ge=0, le=100)
    internet_access: int = Field(..., description="Internet access (0=No, 1=Yes)", ge=0, le=1)
    past_failures: int = Field(..., description="Number of past course failures", ge=0)
    
    class Config:
        """Pydantic configuration."""
        # Example values for API documentation
        json_schema_extra = {
            "example": {
                "attendance": 85.5,
                "study_hours": 10.0,
                "assignments_completed": 8,
                "quiz_score": 75.0,
                "midterm_score": 80.0,
                "internet_access": 1,
                "past_failures": 0
            }
        }

