# main.py
from pydantic import BaseModel, Field
from typing import List

class ProgramModel(BaseModel):
    name: str = Field(..., description="Program name")
    description: str = Field(None, description="Program description")

class CourseModel(BaseModel):
    course_number: str = Field(..., description="Course number")
    name: str = Field(..., description="Course name")
    description: str = Field(None, description="Course description")

class ClassModel(BaseModel):
    section_number: str = Field(..., description="Section number")
    start_date: str = Field(..., description="Start date")
    end_date: str = Field(..., description="End date")
    class_days_of_week: str = Field(..., description="Class days of the week")
    class_time: str = Field(..., description="Class time")
    class_duration: str = Field(..., description="Class duration")
    lab_days_of_week: str = Field(..., description="Lab days of the week")
    lab_time: str = Field(..., description="Lab time")
    lab_duration: str = Field(..., description="Lab duration")

class PersonModel(BaseModel):
    name: str = Field(..., description="Person name")
    url: str = Field(None, description="URL")
    givenName: str = Field(None, description="Given name")
    familyName: str = Field(..., description="Family name")
    birthDate: str = Field(..., description="Birth date")
    signupDate: str = Field(..., description="Signup date")

class StudentModel(PersonModel):
    student_id: str = Field(..., description="Student ID")

class TeacherModel(PersonModel):
    teacher_id: str = Field(..., description="Teacher ID")

class TextBookModel(BaseModel):
    title: str = Field(..., description="Title")
    author_name: str = Field(..., description="Author name")
    description: str = Field(None, description="Description")

class TopicModel(BaseModel):
    title: str = Field(..., description="Title")
    url: str = Field(None, description="URL")
    details: str = Field(None, description="Details")
    lastReviewed: str = Field(..., description="Last reviewed")
    creationDate: str = Field(..., description="Creation date")
    sequenceNumber: int = Field(..., description="Sequence number")

class InteractionModel(BaseModel):
    title: str = Field(..., description="Title")
    author_name: str = Field(..., description="Author name")
    description: str = Field(None, description="Description")



### ========================= *****  ========================= ###

from fastapi import FastAPI
from py2neo import Graph, Node, Relationship
import uvicorn

app = FastAPI()

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

@app.post("/create_program")
def create_program(program: ProgramModel, courses: List[CourseModel]):
    # Create Program node
    program_node = Node("Program", name=program.name, description=program.description)
    graph.create(program_node)

    # Create Course nodes and relationships
    for course in courses:
        course_node = Node("Course", course_number=course.course_number, name=course.name, description=course.description)
        contains_relationship = Relationship(program_node, "CONTAINS", course_node)
        graph.create(course_node)
        graph.create(contains_relationship)
        
    return {"response": "Program and course nodes created, and relationships added."}

@app.get("/get_program/{name}")
def get_program(name: str):
    query = f"MATCH (p:Program)-[:CONTAINS]->(c:Course) WHERE p.name=$name RETURN p, c"
    results = graph.run(query, name=name).data()
    return {"data": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

### ========================= *****  ========================= ###


# nullable=False
# 

### ========================= *****  ========================= ###



### ========================= *****  ========================= ###



### ========================= *****  ========================= ###

# @app.post("/create")
# def createnode(node:nodemodel):
#     driver_neo4j=connection()
#     session=driver_neo4j.session()

#     q1="""
#     create(n:user{name:$name,name_id:$name_id}) return n.name as name
#     """

#     x={"name":node.name,"name_id":node.name_id}
#     results=session.run(q1,x)
#     data=[{"Name":row["name"]}for row in results][0]["Name"]
#     return {"response":"node created with course name as: "+data}

### ========================= *****  ========================= ###

