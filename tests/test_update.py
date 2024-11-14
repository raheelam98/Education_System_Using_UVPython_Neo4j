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


# Models for the input structure
class CourseModel(BaseModel):
    course_number: str
    name: str
    description: str

class TopicModel(BaseModel):
    title: str
    url: str
    details: str
    lastReviewed: Optional[str]
    creationDate: Optional[date]
    sequenceNumber: int

class TextBookModel(BaseModel):
    title: str
    author_name: str
    description: str

class ClassModel(BaseModel):
    section_number: str
    start_date: date
    end_date: date
    class_days_of_week: str
    class_time: str
    class_duration: str
    lab_days_of_week: str
    lab_time: str
    lab_duration: str

class UpdateNodeModel(BaseModel):
    courses: Optional[List[CourseModel]]
    topics: Optional[List[TopicModel]]
    textbooks: Optional[List[TextBookModel]]
    classes: Optional[List[ClassModel]]

# Function to update the Program and its subnodes
def update_program_node_and_subnodes(program_name: str, updated_data: UpdateNodeModel):
    # Update the Program node
    program_query = """
    MATCH (p:Program {name: $program_name})
    SET p += $updated_data
    RETURN p
    """
    program_result = graph.run(program_query, program_name=program_name, updated_data=updated_data.dict(exclude_unset=True)).data()

    if not program_result:
        return None, None, None

    # Update Courses related to the Program
    if updated_data.courses:
        for course in updated_data.courses:
            course_query = """
            MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})
            SET c += $course_data
            RETURN c
            """
            graph.run(course_query, program_name=program_name, course_number=course.course_number, course_data=course.dict(exclude_unset=True)).data()

            # Update Topics related to each Course
            if updated_data.topics:
                for topic in updated_data.topics:
                    topic_query = """
                    MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:CONTAINS]->(t:Topic {title: $topic_title})
                    SET t += $topic_data
                    RETURN t
                    """
                    graph.run(topic_query, program_name=program_name, course_number=course.course_number, topic_title=topic.title, topic_data=topic.dict(exclude_unset=True)).data()

            # Update TextBooks related to each Course
            if updated_data.textbooks:
                for textbook in updated_data.textbooks:
                    textbook_query = """
                    MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:TAUGHT]->(tb:TextBook {title: $textbook_title})
                    SET tb += $textbook_data
                    RETURN tb
                    """
                    graph.run(textbook_query, program_name=program_name, course_number=course.course_number, textbook_title=textbook.title, textbook_data=textbook.dict(exclude_unset=True)).data()

            # Update Classes related to each Course
            if updated_data.classes:
                for class_item in updated_data.classes:
                    class_query = """
                    MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:SCHEDULED]->(cl:Class {section_number: $section_number})
                    SET cl += $class_data
                    RETURN cl
                    """
                    graph.run(class_query, program_name=program_name, course_number=course.course_number, section_number=class_item.section_number, class_data=class_item.dict(exclude_unset=True)).data()

    return program_result


@app.put("/program/{program_name}/update")
def update_program(program_name: str, updated_data: UpdateNodeModel):
    # Call the update function
    program_result = update_program_node_and_subnodes(program_name, updated_data)

    if not program_result:
        raise HTTPException(status_code=404, detail="Program not found")

    return {
        "message": "Program and its subnodes updated successfully",
        "program": program_result
    }