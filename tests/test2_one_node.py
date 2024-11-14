from neo4j import GraphDatabase
from pydantic import BaseModel, Field
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from py2neo import Graph, Node, Relationship

### ========================= *****  ========================= ###

    # CONNECTION_URI="bolt://localhost:7687"
    # USERNAME="neo4j"
    # PASSWORD="password"

### ========================= *****  ========================= ###

# # Driver instantiation
# def connection():
#     driver = GraphDatabase.driver(CONNECTION_URI, auth=(USERNAME, PASSWORD))
#     return driver

### ========================= *****  ========================= ###


# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Pydantic model for input validation
class ProgramCourseModel(BaseModel):
    program_name: str = Field(nullable=False, description="program name")
    program_description: str = Field(nullable=True, description="program descriptio")
    course_number: str = Field(nullable=False, description="course name")
    course_name: str = Field(nullable=False, description="course name")
    course_description: str = Field(nullable=True, description="course description")

# Function to create and add nodes and relationships dynamically
def create_program_course(program_name, program_description, course_number, course_name, course_description):
    program = Node("Program", name=program_name, description=program_description)
    course = Node("Course", course_number=course_number, name=course_name, description=course_description)
    contains_program_course = Relationship(program, "CONTAINS", course)
    graph.create(program)
    graph.create(course)
    graph.create(contains_program_course)

app = FastAPI()

@app.get('/')
def get_root():
    return {"response": "EduSmart Schema"}

@app.post("/create_program_course")
def create_program_course_endpoint(data: ProgramCourseModel):
    create_program_course(
        program_name=data.program_name,
        program_description=data.program_description,
        course_number=data.course_number,
        course_name=data.course_name,
        course_description=data.course_description
    )
    return {"response": "Program and course nodes created and relationship added."}

