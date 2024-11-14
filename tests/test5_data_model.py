# main.py
from pydantic import BaseModel, Field
from typing import List
from datetime import date

# create schema
class ProgramModel(BaseModel):
    name: str = Field(nullable=False)
    description: str 

class ProgramCourseModel(BaseModel):
    course_number: str = Field(nullable=False)
    name: str = Field(nullable=False)
    description: str

class CourseTextBookModel(BaseModel):
    title: str =  Field(nullable=False)
    author_name: str = Field(nullable=False)
    description: str 

class CourseTopicModel(BaseModel):
    title: str = Field(nullable=False)
    url: str 
    details: str 
    lastReviewed: str = Field(nullable=False)
    creationDate: str = Field(default=date.today())
    sequenceNumber: int = Field(nullable=False)

class CourseClassModel(BaseModel):
    section_number: str = Field(nullable=False)
    start_date: str = Field(default=date.today())
    end_date: str = Field(default=date.today())
    class_days_of_week: str = Field(nullable=False)
    class_time: str = Field(nullable=False)
    class_duration: str = Field(nullable=False)
    lab_days_of_week: str = Field(nullable=False)
    lab_time: str = Field(nullable=False)
    lab_duration: str = Field(nullable=False) 