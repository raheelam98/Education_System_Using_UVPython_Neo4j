# main.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Define the Schema using Pydantic Models
class ProgramModel(BaseModel):
    name: str = Field(nullable=False)
    description: str

class ProgramCourseModel(BaseModel):
    course_number: str = Field(nullable=False)
    name: str = Field(nullable=False)
    description: str

class CourseTextBookModel(BaseModel):
    title: str = Field(nullable=False)
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

### ========================= *****  ========================= ###
### ========================= *****  ========================= ###  

# Pydantic model for input validation
class UpdateNodeModel(BaseModel):
    name: Optional[str] = Field(None, description="Name of the program")
    description: Optional[str] = Field(None, description="Description of the program")      

# Define the UpdateCourseMode
class UpdateCourseModel(BaseModel):
    course_number: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

# Define the Update Topic Model
class UpdateTopicModel(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    details: Optional[str] = None
    lastReviewed: Optional[str] = None
    creationDate: Optional[str] = Field(default=str(date.today()))
    sequenceNumber: Optional[int] = None

### ========================= *****  ========================= ###  
    
# Model to Update TextBook
class UpdateTextBookModel(BaseModel):
    title: Optional[str] = None
    author_name: Optional[str] = None
    description: Optional[str] = None    

### ========================= *****  ========================= ###  
### ========================= *****  ========================= ###

from fastapi import FastAPI, HTTPException
from py2neo import Graph, Node, Relationship, ServiceUnavailable
from typing import List

app = FastAPI()

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))


# Function to create nodes and relationships dynamically
def create_program_node(program: ProgramModel):
    program_node = Node("Program", name=program.name, description=program.description)
    graph.create(program_node)
    return program_node

def create_course_node(course: ProgramCourseModel, program_node):
    course_node = Node("Course", course_number=course.course_number, name=course.name, description=course.description)
    contains_relationship = Relationship(program_node, "CONTAINS", course_node)
    graph.create(course_node)
    graph.create(contains_relationship)
    return course_node

def create_topic_node(topic: CourseTopicModel, course_node):
    topic_node = Node("Topic", title=topic.title, url=topic.url, details=topic.details, lastReviewed=topic.lastReviewed, creationDate=topic.creationDate, sequenceNumber=topic.sequenceNumber)
    contains_relationship = Relationship(course_node, "CONTAINS", topic_node)
    graph.create(topic_node)
    graph.create(contains_relationship)
    return topic_node

def create_textbook_node(textbook: CourseTextBookModel, course_node):
    textbook_node = Node("TextBook", title=textbook.title, author_name=textbook.author_name, description=textbook.description)
    taught_relationship = Relationship(course_node, "TAUGHT", textbook_node)
    graph.create(textbook_node)
    graph.create(taught_relationship)
    return textbook_node

def create_class_node(_class: CourseClassModel, course_node):
    class_node = Node("Class", section_number=_class.section_number, start_date=_class.start_date, end_date=_class.end_date, class_days_of_week=_class.class_days_of_week, class_time=_class.class_time, class_duration=_class.class_duration, lab_days_of_week=_class.lab_days_of_week, lab_time=_class.lab_time, lab_duration=_class.lab_duration)
    scheduled_relationship = Relationship(course_node, "SCHEDULED", class_node)
    graph.create(class_node)
    graph.create(scheduled_relationship)
    return class_node

### ========================= *****  ========================= ###
### ========================= *****  ========================= ###

# Function to Update Program Node
def update_program_node(program_name: str, updated_data: UpdateNodeModel):
    query = f"MATCH (p:Program {{name: $program_name}}) SET p += $updated_data RETURN p"
    result = graph.run(query, program_name=program_name, updated_data=updated_data.dict(exclude_unset=True)).data()
    return result

### ========================= *****  ========================= ###

# Update a course corresponding to a specific program 

# Function to Update Course Node
def update_course_in_program(program_name: str, course_number: str, updated_data: UpdateCourseModel):
    # Query to update the course under the specified program
    update_query = """
    MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})
    SET c += $course_updates
    RETURN c
    """
    
    course_updates = updated_data.dict(exclude_unset=True)
    
    # Run the query
    result = graph.run(update_query, program_name=program_name, course_number=course_number, course_updates=course_updates).data()
    
    if not result:
        raise HTTPException(status_code=404, detail="Course not found under the specified program")
    
    return result[0]["c"]

### ========================= *****  ========================= ###

# Update a topic corresponding to a specific program and course

# Function to Update Topic Node
def update_topic_in_course(program_name: str, course_number: str, title: str, updated_data: UpdateTopicModel):
    # Correct the relationship to ensure we're matching the right one
    update_query = """
    MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:CONTAINS]->(t:Topic {title: $title})
    SET t += $topic_updates
    RETURN t
    """
    
    # Debugging prints for verification
    print("Updating topic for:")
    print(f"Program Name: {program_name}, Course Number: {course_number}, Title: {title}")

    # Prepare the topic updates
    topic_updates = updated_data.model_dump(exclude_unset=True)
    print("Topic updates:", topic_updates)

    # Execute the query
    result = graph.run(update_query, 
                       program_name=program_name, 
                       course_number=course_number, 
                       title=title, 
                       topic_updates=topic_updates).data()
    
    # Debugging: Check the query result
    print("Query result ...", result)
    
    # If no result is found, raise an error
    if not result:
        print("No topic found for the given criteria.")
        raise HTTPException(status_code=404, detail="Topic not found under the specified course and program")
    
    print("Topic updated successfully:", result)
    return result[0]["t"]

### ========================= *****  ========================= ###

# Update a class corresponding to a specific program, course, and topic

# Function to Update Class Node

def update_class_in_course(program_name: str, course_number: str, section_number: str, updated_data: CourseClassModel):
    # Query to match the specific class node under a program and course
    update_query = """
    MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:SCHEDULED]->(cl:Class {section_number: $section_number})
    SET cl += $class_updates
    RETURN cl
    """
    
    # Prepare class updates dictionary excluding unset fields
    class_updates = updated_data.model_dump(exclude_unset=True)

    # Run the query
    result = graph.run(update_query, 
                       program_name=program_name, 
                       course_number=course_number, 
                       section_number=section_number, 
                       class_updates=class_updates).data()

    # Raise an error if no result is found
    if not result:
        raise HTTPException(status_code=404, detail="Class not found under the specified course and program")
    
    return result[0]["cl"]

### ========================= *****  ========================= ###

# To update a TextBook corresponding to a specific program, course, and topic
# Function to Update TextBook Node
def update_textbook_in_course(program_name: str, course_number: str, title: str, updated_data: UpdateTextBookModel):
    # Cypher query to find and update the textbook
    update_query = """
    MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:TAUGHT]->(tb:TextBook {title: $title})
    SET tb += $textbook_updates
    RETURN tb
    """
    
    # Prepare the updates, excluding any fields that are not provided
    textbook_updates = updated_data.dict(exclude_unset=True)

    # Run the query
    result = graph.run(update_query, 
                       program_name=program_name, 
                       course_number=course_number, 
                       title=title, 
                       textbook_updates=textbook_updates).data()

    # If no result is found, raise an error
    if not result:
        raise HTTPException(status_code=404, detail="Textbook not found under the specified course and program")

    return result[0]["tb"]

### ========================= *****  ========================= ###
### ========================= *****  ========================= ###

# Add a new sub-node Course under a specific main node Program, 
# along with its relevant relationships (i.e., the Course contains Topics, TextBooks, and Classes)

# Function to Create Sub-nodes (Course, Topics, TextBooks, and Classes)

def add_course_to_program(program_name: str, course: ProgramCourseModel, topics: List[CourseTopicModel], textbooks: List[CourseTextBookModel], classes: List[CourseClassModel]):
    # Find the program node
    program_node_query = f"MATCH (p:Program {{name: $program_name}}) RETURN p"
    program_node = graph.run(program_node_query, program_name=program_name).data()

    # If program node doesn't exist, raise an error
    if not program_node:
        raise HTTPException(status_code=404, detail="Program not found")

    # Get the program node reference
    program_node_ref = program_node[0]['p']

    # Create the Course node and relate it to the Program
    course_node = create_course_node(course, program_node_ref)

    # Create Topic nodes and establish relationships with the Course
    for topic in topics:
        create_topic_node(topic, course_node)

    # Create TextBook nodes and establish relationships with the Course
    for textbook in textbooks:
        create_textbook_node(textbook, course_node)

    # Create Class nodes and establish relationships with the Course
    for _class in classes:
        create_class_node(_class, course_node)

    return {"message": f"Course '{course.name}' added to Program '{program_name}' with its topics, textbooks, and classes"}



### ========================= *****  ========================= ###
### ========================= *****  ========================= ###

# Retrieve and display all programs

@app.get("/get_all_programs")
def get_all_programs():
    # Cypher query to match and return all Program nodes
    query = """
    MATCH (p:Program)
    RETURN p
    """
    # Execute the query and get the results
    results = graph.run(query).data()

    # Check if no results were found
    if not results:
        return {"response": "No programs found"}
 
    # Extract program details from the results
    programs = [{"name": record['p']['name'], "description": record['p']['description']} for record in results]
    return {"programs": programs}

### ========================= *****  ========================= ###

# Retrieves all relevant data for a program, including the courses, topics, textbooks, and classes

@app.get("/get_program/{name}")
def get_program(name: str):
    query = """
    MATCH (p:Program {name: $name})-[:CONTAINS]->(c:Course)
    OPTIONAL MATCH (c)-[:CONTAINS]->(t:Topic)
    OPTIONAL MATCH (c)-[:TAUGHT]->(tb:TextBook)
    OPTIONAL MATCH (c)-[:SCHEDULED]->(cl:Class)
    RETURN p, c, t, tb, cl
    """
    results = graph.run(query, name=name).data()

    if not results:
        raise HTTPException(status_code=404, detail="Program not found")

    # Create a dictionary to organize the data
    program_data = {
        "program": {"name": results[0]['p']['name'], "description": results[0]['p']['description']},
        "courses": []
    }

    # To avoid duplicate courses, track seen courses
    seen_courses = {}

    for record in results:
        course_data = {
            "course_number": record['c']['course_number'],
            "name": record['c']['name'],
            "description": record['c']['description'],
            "topics": [],
            "textbooks": [],
            "classes": []
        }

        # If the course hasn't been added yet, add it
        course_key = record['c']['course_number']
        if course_key not in seen_courses:
            seen_courses[course_key] = course_data
            program_data["courses"].append(seen_courses[course_key])

        # Add topics
        if record.get('t'):
            topic_data = {
                "title": record['t']['title'],
                "url": record['t']['url'],
                "details": record['t']['details'],
                "lastReviewed": record['t']['lastReviewed'],
                "creationDate": record['t']['creationDate'],
                "sequenceNumber": record['t']['sequenceNumber']
            }
            seen_courses[course_key]["topics"].append(topic_data)

        # Add textbooks
        if record.get('tb'):
            textbook_data = {
                "title": record['tb']['title'],
                "author_name": record['tb']['author_name'],
                "description": record['tb']['description']
            }
            seen_courses[course_key]["textbooks"].append(textbook_data)

        # Add classes
        if record.get('cl'):
            class_data = {
                "section_number": record['cl']['section_number'],
                "start_date": record['cl']['start_date'],
                "end_date": record['cl']['end_date'],
                "class_days_of_week": record['cl']['class_days_of_week'],
                "class_time": record['cl']['class_time'],
                "class_duration": record['cl']['class_duration'],
                "lab_days_of_week": record['cl']['lab_days_of_week'],
                "lab_time": record['cl']['lab_time'],
                "lab_duration": record['cl']['lab_duration']
            }
            seen_courses[course_key]["classes"].append(class_data)

    return {"data": program_data}


### ========================= *****  ========================= ###

# Route to add a new Topic under a specific Course within a Program
@app.post("/programs/{program_name}/courses/{course_number}/add_topic")
def add_topic_to_course_endpoint(
    program_name: str, 
    course_number: str, 
    topic: CourseTopicModel, 
    textbooks: List[CourseTextBookModel], 
    classes: List[CourseClassModel]
):
    # Find the program node
    program_node_query = f"MATCH (p:Program {{name: $program_name}}) RETURN p"
    program_node = graph.run(program_node_query, program_name=program_name).data()

    # If program node doesn't exist, raise an error
    if not program_node:
        raise HTTPException(status_code=404, detail="Program not found")

    # Find the course node
    course_node_query = f"MATCH (c:Course {{course_number: $course_number}})<-[:CONTAINS]-(p:Program {{name: $program_name}}) RETURN c"
    course_node = graph.run(course_node_query, program_name=program_name, course_number=course_number).data()

    # If course node doesn't exist, raise an error
    if not course_node:
        raise HTTPException(status_code=404, detail="Course not found under the specified program")

    # Get the course node reference
    course_node_ref = course_node[0]['c']

    # Create the new Topic node and relate it to the Course
    topic_node = create_topic_node(topic, course_node_ref)

    # Create TextBook nodes and establish relationships with the Topic
    for textbook in textbooks:
        create_textbook_node(textbook, topic_node)

    # Create Class nodes and establish relationships with the Topic
    for _class in classes:
        create_class_node(_class, topic_node)

    return {"message": f"Topic '{topic.title}' added to Course '{course_number}' under Program '{program_name}' with its textbooks and classes."}

### ========================= *****  ========================= ###

# Create a program and all its subnodes
@app.post("/create_program")
def create_program(program: ProgramModel, courses: List[ProgramCourseModel], topics: List[CourseTopicModel], textbooks: List[CourseTextBookModel], classes: List[CourseClassModel]):
    program_node = create_program_node(program)
    
    for course in courses:
        course_node = create_course_node(course, program_node)
        
        for topic in topics:
            create_topic_node(topic, course_node)
        
        for textbook in textbooks:
            create_textbook_node(textbook, course_node)
        
        for _class in classes:
            create_class_node(_class, course_node)

    return {"response": "Program, courses, topics, textbooks, and classes nodes created and relationships added."}

### ========================= *****  ========================= ###

# Add a new sub-node Course under a specific main node Program, 
# along with its relevant relationships (i.e., the Course contains Topics, TextBooks, and Classes)

# Route to add a Course to a specific Program, along with its related nodes.
@app.post("/programs/{program_name}/creat_course")
def add_course_to_program_endpoint(program_name: str, course: ProgramCourseModel, topics: List[CourseTopicModel], textbooks: List[CourseTextBookModel], classes: List[CourseClassModel]):
    result = add_course_to_program(program_name, course, topics, textbooks, classes)
    return result

### ========================= *****  ========================= ###
### ========================= *****  ========================= ###

# Route to update a Program node
@app.put("/update_program/{program_name}")
def update_program(program_name: str, updated_data: UpdateNodeModel):
    result = update_program_node(program_name, updated_data)
    if not result:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"response": "Program node updated successfully"}

### ========================= *****  ========================= ###

# Set Up the Route for updating program node
@app.put("/programs/{program_name}/courses/{course_number}")
def update_course(program_name: str, course_number: str, updated_data: UpdateCourseModel):
    updated_course = update_course_in_program(program_name, course_number, updated_data)
    return {"message": "Course updated successfully", "course": updated_course}

### ========================= *****  ========================= ###

# Route for Updating a Topic
# Set up the route for updating a topic
@app.put("/programs/{program_name}/courses/{course_number}/topics/{title}")
def update_topic(program_name: str, course_number: str, title: str, updated_data: UpdateTopicModel):
    updated_topic = update_topic_in_course(program_name, course_number, title, updated_data)
    return {"message": "Topic updated successfully", "topic": updated_topic}

### ========================= *****  ========================= ###

# Route for Updating a Class
@app.put("/programs/{program_name}/courses/{course_number}/classes/{section_number}")
def update_class(program_name: str, course_number: str, section_number: str, updated_data: CourseClassModel):
    updated_class = update_class_in_course(program_name, course_number, section_number, updated_data)
    return {"message": "Class updated successfully", "class": updated_class}

### ========================= *****  ========================= ###

# Route for Updating a TextBook
@app.put("/programs/{program_name}/courses/{course_number}/textbooks/{title}")
def update_textbook(program_name: str, course_number: str, title: str, updated_data: UpdateTextBookModel):
    updated_textbook = update_textbook_in_course(program_name, course_number, title, updated_data)
    return {"message": "Textbook updated successfully", "textbook": updated_textbook}

### ========================= *****  ========================= ###
### ========================= *****  ========================= ###

# Delete a program and all its subnodes
@app.delete("/delete_program/{program_name}")
def delete_program(program_name: str):
    query = """
    MATCH (p:Program {name: $program_name})
    OPTIONAL MATCH (p)-[r*0..]-(sub)
    DETACH DELETE p, sub
    """
    result = graph.run(query, program_name=program_name).data()
    
    if not result:
        raise HTTPException(status_code=404, detail="Program not found")
    
    return {"response": "Program and related subnodes deleted successfully"}

### ========================= *****  ========================= ###
### ========================= *****  ========================= ###
### ========================= *****  ========================= ###

#To update a class corresponding to a specific program, course, and topic



