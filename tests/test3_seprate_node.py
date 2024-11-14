from neo4j import GraphDatabase
from pydantic import BaseModel, Field
from fastapi import FastAPI
from typing import List
from py2neo import Graph, Node, Relationship

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Pydantic model for input validation
class CourseModel(BaseModel):
    course_number: str = Field(nullable=False, description="Course number")
    course_name: str = Field(nullable=False, description="Course name")
    course_description: str = Field(None, description="Course description")

class ProgramCourseModel(BaseModel):
    program_name: str = Field(nullable=False, description="Program name")
    program_description: str = Field(None, description="Program description")
    courses: List[CourseModel] = Field(nullable=False, description="List of courses")

# Function to create and add nodes and relationships dynamically
def create_program_courses(program_name, program_description, courses):
    # Create Program node
    program = Node("Program", name=program_name, description=program_description)
    graph.create(program)
    
    # Create Course nodes and relationships
    for course in courses:
        course_node = Node("Course", course_number=course.course_number, name=course.course_name, description=course.course_description)
        contains_relationship = Relationship(program, "CONTAINS", course_node)
        graph.create(course_node)
        graph.create(contains_relationship)

app = FastAPI()

@app.get('/')
def get_root():
    return {"response": "EduSmart Schema"}

@app.post("/create_program_courses")
def create_program_courses_endpoint(data: ProgramCourseModel):
    create_program_courses(
        program_name=data.program_name,
        program_description=data.program_description,
        courses=data.courses
    )
    return {"response": "Program and course nodes created and relationships added."}

