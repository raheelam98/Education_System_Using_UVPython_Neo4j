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
    print("programa result...", result)

    if not result:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Next, update or return a message for the related courses
    if updated_data.courses:
        for course_data in updated_data.courses:
            course_query = """
            MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})
            SET c += $course_updates
            RETURN c
            """
            print("course query...", course_query)
            course_updates = course_data.dict(exclude_unset=True)
            course_result = graph.run(course_query, program_name=program_name, course_number=course_data.course_number, course_updates=course_updates).data()
            print("course result...", course_result)

            if not course_result:
                # If the course does not exist, raise an error or log a message
                raise HTTPException(status_code=404, detail=f"Course with course_number {course_data.course_number} not found under program {program_name}")
    
    return {"response": "Program and related courses updated successfully"}

# Updated route for handling the update
@app.put("/update_program_with_courses/{program_name}")
def update_program_with_courses(program_name: str, updated_data: UpdateProgramWithCoursesModel):
    result = update_program_and_courses(program_name, updated_data)
    return result
