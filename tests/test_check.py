# # Example usage
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

### ========================= *****  ========================= ###

# # Function to update a Program node and its subnodes
# def update_program_node_and_subnodes(program_name: str, updated_data: UpdateNodeModel):
#     program_query = """
#     MATCH (p:Program {name: $program_name})
#     SET p += $updated_data
#     RETURN p
#     """
#     program_result = graph.run(program_query, program_name=program_name, updated_data=updated_data.dict(exclude_unset=True)).data()
#     if not program_result:
#         return None

#     # Update related subnodes (example for courses, similar updates can be done for other subnodes)
#     subnodes_query = """
#     MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course)
#     OPTIONAL MATCH (c)-[:CONTAINS]->(t:Topic)
#     OPTIONAL MATCH (c)-[:TAUGHT]->(tb:TextBook)
#     OPTIONAL MATCH (c)-[:SCHEDULED]->(cl:Class)
#     SET c += $updated_data, t += $updated_data, tb += $updated_data, cl += $updated_data
#     RETURN c, t, tb, cl
#     """
#     subnodes_result = graph.run(subnodes_query, program_name=program_name, updated_data=updated_data.dict(exclude_unset=True)).data()

#     return program_result, subnodes_result

# # Route to update a Program node and its subnodes
# @app.put("/update_program_and_subnodes/{program_name}")
# def update_program_and_subnodes(program_name: str, updated_data: UpdateNodeModel):
#     result = update_program_node_and_subnodes(program_name, updated_data)
#     if not result:
#         raise HTTPException(status_code=404, detail="Program or subnodes not found")
#     return {"response": "Program node and subnodes updated successfully", "details": result}


# # Function to update a Program node and its subnodes and return full details
# def update_program_node_and_subnodes(program_name: str, updated_data: UpdateNodeModel):
#     # Update the Program node
#     program_query = """
#     MATCH (p:Program {name: $program_name})
#     SET p += $updated_data
#     RETURN p
#     """
#     program_result = graph.run(program_query, program_name=program_name, updated_data=updated_data.dict(exclude_unset=True)).data()

#     if not program_result:
#         return None

#     # Update related subnodes (Courses, Topics, TextBooks, Classes)
#     subnodes_query = """
#     MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course)
#     OPTIONAL MATCH (c)-[:CONTAINS]->(t:Topic)
#     OPTIONAL MATCH (c)-[:TAUGHT]->(tb:TextBook)
#     OPTIONAL MATCH (c)-[:SCHEDULED]->(cl:Class)
#     SET c += $updated_data, t += $updated_data, tb += $updated_data, cl += $updated_data
#     RETURN c, collect(t) as topics, collect(tb) as textbooks, collect(cl) as classes
#     """
#     subnodes_result = graph.run(subnodes_query, program_name=program_name, updated_data=updated_data.dict(exclude_unset=True)).data()

#     return program_result, subnodes_result

# # Route to update a Program node and its subnodes
# @app.put("/update_program_and_subnodes/{program_name}")
# def update_program_and_subnodes(program_name: str, updated_data: UpdateNodeModel):
#     result = update_program_node_and_subnodes(program_name, updated_data)
    
#     if not result:
#         raise HTTPException(status_code=404, detail="Program or subnodes not found")
    
#     program_result, subnodes_result = result

#     # Format response to include details of the Program and its subnodes
#     response_data = {
#         "program": {
#             "name": program_result[0]['p']['name'],
#             "description": program_result[0]['p']['description']
#         },
#         "courses": []
#     }

#     # Iterate through the subnodes result and structure the response
#     for subnode in subnodes_result:
#         course = {
#             "course_number": subnode['c']['course_number'],
#             "name": subnode['c']['name'],
#             "description": subnode['c']['description'],
#             "topics": [],
#             "textbooks": [],
#             "classes": []
#         }

#         # Add topics
#         for topic in subnode['topics']:
#             course["topics"].append({
#                 "title": topic['title'],
#                 "url": topic['url'],
#                 "details": topic['details'],
#                 "lastReviewed": topic['lastReviewed'],
#                 "creationDate": topic['creationDate'],
#                 "sequenceNumber": topic['sequenceNumber']
#             })

#         # Add textbooks
#         for textbook in subnode['textbooks']:
#             course["textbooks"].append({
#                 "title": textbook['title'],
#                 "author_name": textbook['author_name'],
#                 "description": textbook['description']
#             })

#         # Add classes
#         for _class in subnode['classes']:
#             course["classes"].append({
#                 "section_number": _class['section_number'],
#                 "start_date": _class['start_date'],
#                 "end_date": _class['end_date'],
#                 "class_days_of_week": _class['class_days_of_week'],
#                 "class_time": _class['class_time'],
#                 "class_duration": _class['class_duration'],
#                 "lab_days_of_week": _class['lab_days_of_week'],
#                 "lab_time": _class['lab_time'],
#                 "lab_duration": _class['lab_duration']
#             })

#         # Add course to the response
#         response_data["courses"].append(course)

#     return {"response": "Program node and subnodes updated successfully", "details": response_data}


# # Example usage
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# # Define the Request Body Model
# class UpdateCourseModel(BaseModel):
#     course_number: Optional[str] = Field(None, description="Course number")
#     name: Optional[str] = Field(None, description="Course name")
#     description: Optional[str] = Field(None, description="Course description")

# class UpdateTopicModel(BaseModel):
#     title: Optional[str] = Field(None, description="Topic title")
#     url: Optional[str] = Field(None, description="Topic URL")
#     details: Optional[str] = Field(None, description="Topic details")
#     lastReviewed: Optional[str] = Field(None, description="Last reviewed date")
#     creationDate: Optional[str] = Field(None, description="Creation date")
#     sequenceNumber: Optional[int] = Field(None, description="Sequence number")

# class UpdateTextBookModel(BaseModel):
#     title: Optional[str] = Field(None, description="Title")
#     author_name: Optional[str] = Field(None, description="Author name")
#     description: Optional[str] = Field(None, description="Description")

# class UpdateClassModel(BaseModel):
#     section_number: Optional[str] = Field(None, description="Section number")
#     start_date: Optional[str] = Field(None, description="Start date")
#     end_date: Optional[str] = Field(None, description="End date")
#     class_days_of_week: Optional[str] = Field(None, description="Class days of the week")
#     class_time: Optional[str] = Field(None, description="Class time")
#     class_duration: Optional[str] = Field(None, description="Class duration")
#     lab_days_of_week: Optional[str] = Field(None, description="Lab days of the week")
#     lab_time: Optional[str] = Field(None, description="Lab time")
#     lab_duration: Optional[str] = Field(None, description="Lab duration")

# class UpdateProgramWithSubnodesModel(BaseModel):
#     program: UpdateNodeModel
#     courses: List[UpdateCourseModel] = []
#     topics: List[UpdateTopicModel] = []
#     textbooks: List[UpdateTextBookModel] = []
#     classes: List[UpdateClassModel] = []

# # Function to Update Program and Subnodes
# def update_program_and_subnodes(program_name: str, updated_data: UpdateProgramWithSubnodesModel):
#     program_query = """
#     MATCH (p:Program {name: $program_name})
#     SET p += $updated_data
#     RETURN p
#     """
#     program_result = graph.run(program_query, program_name=program_name, updated_data=updated_data.program.dict(exclude_unset=True)).data()
#     if not program_result:
#         return None

#     updated_subnodes = []

#     # Update Courses
#     for course in updated_data.courses:
#         course_query = """
#         MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})
#         SET c += $updated_course
#         RETURN c
#         """
#         course_result = graph.run(course_query, program_name=program_name, course_number=course.course_number, updated_course=course.dict(exclude_unset=True)).data()
#         updated_subnodes.extend(course_result)

#     # Update Topics
#     for topic in updated_data.topics:
#         topic_query = """
#         MATCH (p:Program {name: $program_name})-[:CONTAINS]->(:Course)-[:CONTAINS]->(t:Topic {title: $title})
#         SET t += $updated_topic
#         RETURN t
#         """
#         topic_result = graph.run(topic_query, program_name=program_name, title=topic.title, updated_topic=topic.dict(exclude_unset=True)).data()
#         updated_subnodes.extend(topic_result)

#     # Update TextBooks
#     for textbook in updated_data.textbooks:
#         textbook_query = """
#         MATCH (p:Program {name: $program_name})-[:CONTAINS]->(:Course)-[:TAUGHT]->(tb:TextBook {title: $title})
#         SET tb += $updated_textbook
#         RETURN tb
#         """
#         textbook_result = graph.run(textbook_query, program_name=program_name, title=textbook.title, updated_textbook=textbook.dict(exclude_unset=True)).data()
#         updated_subnodes.extend(textbook_result)

#     # Update Classes
#     for _class in updated_data.classes:
#         class_query = """
#         MATCH (p:Program {name: $program_name})-[:CONTAINS]->(:Course)-[:SCHEDULED]->(cl:Class {section_number: $section_number})
#         SET cl += $updated_class
#         RETURN cl
#         """
#         class_result = graph.run(class_query, program_name=program_name, section_number=_class.section_number, updated_class=_class.dict(exclude_unset=True)).data()
#         updated_subnodes.extend(class_result)

#     return program_result, updated_subnodes
    
# # Route to Update Program and Subnodes

# @app.put("/update_program_and_subnodes/{program_name}")
# def update_program_and_subnodes(program_name: str, updated_data: UpdateProgramWithSubnodesModel):
#     result = update_program_and_subnodes(program_name, updated_data)
#     if not result:
#         raise HTTPException(status_code=404, detail="Program or subnodes not found")
#     program_result, subnodes_result = result

#     # Format response to include details of the Program and its subnodes
#     response_data = {
#         "program": {
#             "name": program_result[0]['p']['name'],
#             "description": program_result[0]['p']['description']
#         },
#         "subnodes": subnodes_result
#     }
#     return {"response": "Program node and subnodes updated successfully", "details": response_data}

# # Example usage
# if __name__ == "__main__":
#     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)

# # Define the Request Body Model
# class UpdateCourseModel(BaseModel):
#     course_number: Optional[str] = Field(None, description="Course number")
#     name: Optional[str] = Field(None, description="Course name")
#     description: Optional[str] = Field(None, description="Course description")

# class UpdateTopicModel(BaseModel):
#     title: Optional[str] = Field(None, description="Topic title")
#     url: Optional[str] = Field(None, description="Topic URL")
#     details: Optional[str] = Field(None, description="Topic details")
#     lastReviewed: Optional[str] = Field(None, description="Last reviewed date")
#     creationDate: Optional[str] = Field(None, description="Creation date")
#     sequenceNumber: Optional[int] = Field(None, description="Sequence number")

# class UpdateTextBookModel(BaseModel):
#     title: Optional[str] = Field(None, description="Title")
#     author_name: Optional[str] = Field(None, description="Author name")
#     description: Optional[str] = Field(None, description="Description")

# class UpdateClassModel(BaseModel):
#     section_number: Optional[str] = Field(None, description="Section number")
#     start_date: Optional[str] = Field(None, description="Start date")
#     end_date: Optional[str] = Field(None, description="End date")
#     class_days_of_week: Optional[str] = Field(None, description="Class days of the week")
#     class_time: Optional[str] = Field(None, description="Class time")
#     class_duration: Optional[str] = Field(None, description="Class duration")
#     lab_days_of_week: Optional[str] = Field(None, description="Lab days of the week")
#     lab_time: Optional[str] = Field(None, description="Lab time")
#     lab_duration: Optional[str] = Field(None, description="Lab duration")

# class UpdateProgramWithSubnodesModel(BaseModel):
#     program: UpdateNodeModel
#     courses: List[UpdateCourseModel] = []
#     topics: List[UpdateTopicModel] = []
#     textbooks: List[UpdateTextBookModel] = []
#     classes: List[UpdateClassModel] = []

# def update_program_and_subnodes(program_name: str, updated_data: UpdateProgramWithSubnodesModel):
#     program_query = """
#     MATCH (p:Program {name: $program_name})
#     SET p += $updated_data
#     RETURN p
#     """
#     program_result = graph.run(program_query, program_name=program_name, updated_data=updated_data.program.dict(exclude_unset=True)).data()
#     if not program_result:
#         return None

#     updated_subnodes = []

#     # Update Courses
#     for course in updated_data.courses:
#         course_query = """
#         MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})
#         SET c += $updated_course
#         RETURN c
#         """
#         course_result = graph.run(course_query, program_name=program_name, course_number=course.course_number, updated_course=course.dict(exclude_unset=True)).data()
#         updated_subnodes.extend(course_result)

#     # Update Topics
#     for topic in updated_data.topics:
#         topic_query = """
#         MATCH (p:Program {name: $program_name})-[:CONTAINS]->(:Course)-[:CONTAINS]->(t:Topic {title: $title})
#         SET t += $updated_topic
#         RETURN t
#         """
#         topic_result = graph.run(topic_query, program_name=program_name, title=topic.title, updated_topic=topic.dict(exclude_unset=True)).data()
#         updated_subnodes.extend(topic_result)

#     # Update TextBooks
#     for textbook in updated_data.textbooks:
#         textbook_query = """
#         MATCH (p:Program {name: $program_name})-[:CONTAINS]->(:Course)-[:TAUGHT]->(tb:TextBook {title: $title})
#         SET tb += $updated_textbook
#         RETURN tb
#         """
#         textbook_result = graph.run(textbook_query, program_name=program_name, title=textbook.title, updated_textbook=textbook.dict(exclude_unset=True)).data()
#         updated_subnodes.extend(textbook_result)

#     # Update Classes
#     for _class in updated_data.classes:
#         class_query = """
#         MATCH (p:Program {name: $program_name})-[:CONTAINS]->(:Course)-[:SCHEDULED]->(cl:Class {section_number: $section_number})
#         SET cl += $updated_class
#         RETURN cl
#         """
#         class_result = graph.run(class_query, program_name=program_name, section_number=_class.section_number, updated_class=_class.dict(exclude_unset=True)).data()
#         updated_subnodes.extend(class_result)

#     return program_result, updated_subnodes


# @app.put("/update_program_and_subnodes/{program_name}")
# def update_program_and_subnodes(program_name: str, updated_data: UpdateProgramWithSubnodesModel):
#     result = update_program_and_subnodes(program_name, updated_data)
#     if not result:
#         raise HTTPException(status_code=404, detail="Program or subnodes not found")
#     program_result, subnodes_result = result

#     # Format response to include details of the Program and its subnodes
#     response_data = {
#         "program": {
#             "name": program_result[0]['p']['name'],
#             "description": program_result[0]['p']['description']
#         },
#         "subnodes": subnodes_result
#     }
#     return {"response": "Program node and subnodes updated successfully", "details": response_data}

# # Example usage
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

### ========================= *****  ========================= ###
### ========================= *****  ========================= ###
### ========================= *****  ========================= ###


# class UpdateNodeModel(BaseModel):
#     courses: Optional[List[CourseModel]]
#     topics: Optional[List[TopicModel]]
#     textbooks: Optional[List[TextBookModel]]
#     classes: Optional[List[ClassModel]]

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import date

# app = FastAPI()

# # Models for the input structure
# class CourseModel(BaseModel):
#     course_number: str
#     name: str
#     description: str

# class TopicModel(BaseModel):
#     title: str
#     url: str
#     details: str
#     lastReviewed: Optional[str]
#     creationDate: Optional[date]
#     sequenceNumber: int

# class TextBookModel(BaseModel):
#     title: str
#     author_name: str
#     description: str

# class ClassModel(BaseModel):
#     section_number: str
#     start_date: date
#     end_date: date
#     class_days_of_week: str
#     class_time: str
#     class_duration: str
#     lab_days_of_week: str
#     lab_time: str
#     lab_duration: str

# class UpdateNodeModel(BaseModel):
#     courses: Optional[List[CourseModel]]
#     topics: Optional[List[TopicModel]]
#     textbooks: Optional[List[TextBookModel]]
#     classes: Optional[List[ClassModel]]

# # Function to update the Program and its subnodes
# def update_program_node_and_subnodes(program_name: str, updated_data: UpdateNodeModel):
#     # Update the Program node
#     program_query = """
#     MATCH (p:Program {name: $program_name})
#     SET p += $updated_data
#     RETURN p
#     """
#     program_result = graph.run(program_query, program_name=program_name, updated_data=updated_data.dict(exclude_unset=True)).data()

#     if not program_result:
#         return None, None, None

#     # Update Courses related to the Program
#     if updated_data.courses:
#         for course in updated_data.courses:
#             course_query = """
#             MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})
#             SET c += $course_data
#             RETURN c
#             """
#             graph.run(course_query, program_name=program_name, course_number=course.course_number, course_data=course.dict(exclude_unset=True)).data()

#             # Update Topics related to each Course
#             if updated_data.topics:
#                 for topic in updated_data.topics:
#                     topic_query = """
#                     MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:CONTAINS]->(t:Topic {title: $topic_title})
#                     SET t += $topic_data
#                     RETURN t
#                     """
#                     graph.run(topic_query, program_name=program_name, course_number=course.course_number, topic_title=topic.title, topic_data=topic.dict(exclude_unset=True)).data()

#             # Update TextBooks related to each Course
#             if updated_data.textbooks:
#                 for textbook in updated_data.textbooks:
#                     textbook_query = """
#                     MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:TAUGHT]->(tb:TextBook {title: $textbook_title})
#                     SET tb += $textbook_data
#                     RETURN tb
#                     """
#                     graph.run(textbook_query, program_name=program_name, course_number=course.course_number, textbook_title=textbook.title, textbook_data=textbook.dict(exclude_unset=True)).data()

#             # Update Classes related to each Course
#             if updated_data.classes:
#                 for class_item in updated_data.classes:
#                     class_query = """
#                     MATCH (p:Program {name: $program_name})-[:CONTAINS]->(c:Course {course_number: $course_number})-[:SCHEDULED]->(cl:Class {section_number: $section_number})
#                     SET cl += $class_data
#                     RETURN cl
#                     """
#                     graph.run(class_query, program_name=program_name, course_number=course.course_number, section_number=class_item.section_number, class_data=class_item.dict(exclude_unset=True)).data()

#     return program_result


# @app.put("/program/{program_name}/update")
# def update_program(program_name: str, updated_data: UpdateNodeModel):
#     # Call the update function
#     program_result = update_program_node_and_subnodes(program_name, updated_data)

#     if not program_result:
#         raise HTTPException(status_code=404, detail="Program not found")

#     return {
#         "message": "Program and its subnodes updated successfully",
#         "program": program_result
#     }