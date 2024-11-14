
from py2neo import Graph, Node, Relationship


# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Create nodes for Program, Course, and Class
program = Node("Program", 
               name="name", 
               description="description")

course = Node("Course", 
              course_number="course_number", 
              name="name", 
              description="description")

_class = Node("Class", 
              section_number="section_number", 
              start_date="start_date", 
              end_date="end_date", 
              class_days_of_week="class_days_of_week", 
              class_time="class_time", 
              class_duration="class_duration", 
              lab_days_of_week="lab_days_of_week", 
              lab_time="lab_time", 
              lab_duration="lab_duration")

# Create nodes for Person, Student, and Teacher
person = Node("Person", 
              name="name", 
              url="url", 
              givenName="givenName", 
              familyName="familyName", 
              birthDate="birthDate", 
              signupDate="signupDate")

student = Node("Student", 
               student_id="student_id")

teacher = Node("Teacher", 
               teacher_id="teacher_id")

# Create nodes for TextBook, Topic, and Interaction
textbook = Node("TextBook", 
                title="title", 
                author_name="author_name", 
                description="description")

topic = Node("Topic", 
             title="title", 
             url="url", details="details", 
             lastReviewed="lastReviewed", 
             creationDate="creationDate", 
             sequenceNumber="sequenceNumber")

interaction = Node("Interaction", 
                   title="title", 
                   author_name="author_name", 
                   description="description")

# Create relationships between nodes
contains_program_course = Relationship(program, "CONTAINS", course)
scheduled_course_class = Relationship(course, "SCHEDULED", _class)
admission_student_program = Relationship(student, "ADMISSION", program)
registers_student_class = Relationship(student, "REGISTERS", _class)
teaches_teacher_class = Relationship(teacher, "TEACHES", _class)
taught_course_textbook = Relationship(course, "TAUGHT", textbook)
contains_topic_textbook = Relationship(topic, "CONTAINS", textbook)
contains_topic_topic = Relationship(topic, "CONTAINS", topic)
knows_student_topic = Relationship(student, "KNOWS", topic, level=0, assesment_date="assesment_date")
covers_interaction_topic = Relationship(interaction, "COVERS", topic)

# Add nodes and relationships to the graph
graph.create(contains_program_course)
graph.create(scheduled_course_class)
graph.create(admission_student_program)
graph.create(registers_student_class)
graph.create(teaches_teacher_class)
graph.create(taught_course_textbook)
graph.create(contains_topic_textbook)
graph.create(contains_topic_topic)
graph.create(knows_student_topic)
graph.create(covers_interaction_topic)