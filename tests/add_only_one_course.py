# main.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

from fastapi import FastAPI, HTTPException
from py2neo import Graph, Node, Relationship, ServiceUnavailable
from typing import List

app = FastAPI()

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))




class UpdateCourseModel(BaseModel):
    course_number: Optional[str]
    name: Optional[str]
    description: Optional[str]

class UpdateProgramWithCoursesModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    courses: Optional[List[UpdateCourseModel]]


class ProgramCourseModel(BaseModel):
    course_number: str = Field(nullable=False)
    name: str = Field(nullable=False)
    description: str


def create_course_node(course: ProgramCourseModel, program_node):
    course_node = Node("Course", course_number=course.course_number, name=course.name, description=course.description)
    contains_relationship = Relationship(program_node, "CONTAINS", course_node)
    graph.create(course_node)
    graph.create(contains_relationship)
    return course_node    

# Update function for program and its related course nodes
def update_program_and_courses(program_name: str, updated_data: UpdateProgramWithCoursesModel):
    # First, update the Program node
    program_update_query = """
    MATCH (p:Program {name: $program_name})
    SET p += $program_updates
    RETURN p
    """
    program_updates = updated_data.dict(exclude_unset=True, exclude={"courses"})
    result = graph.run(program_update_query, program_name=program_name, program_updates=program_updates).data()
    
    if not result:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Next, update or create the related courses
    if updated_data.courses:
        for course_data in updated_data.courses:
            course_query = """
            MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})
            SET c += $course_updates
            RETURN c
            """
            course_updates = course_data.dict(exclude_unset=True)
            course_result = graph.run(course_query, program_name=program_name, course_number=course_data.course_number, course_updates=course_updates).data()
            
            if not course_result:
                # If the course does not exist, create it
                create_course_node(course_data, program_node=result[0]["p"])
    
    return {"response": "Program and related courses updated successfully"}

# Updated route for handling the update
@app.put("/update_program_with_courses/{program_name}")
def update_program_with_courses(program_name: str, updated_data: UpdateProgramWithCoursesModel):
    result = update_program_and_courses(program_name, updated_data)
    return result

