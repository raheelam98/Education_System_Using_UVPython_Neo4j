from neo4j import GraphDatabase

class EduSmartSchema:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_schema(self):
        with self.driver.session() as session:
            # Create Constraints for uniqueness and index on important fields
            session.write_transaction(self.create_constraints)

            # Create nodes and relationships (edges) as per schema
            session.write_transaction(self.create_program_node)
            session.write_transaction(self.create_course_node)
            session.write_transaction(self.create_class_node)
            session.write_transaction(self.create_person_node)
            session.write_transaction(self.create_student_node)
            session.write_transaction(self.create_teacher_node)
            session.write_transaction(self.create_textbook_node)
            session.write_transaction(self.create_topic_node)
            session.write_transaction(self.create_interaction_node)

            # Create Relationships (Edges)
            session.write_transaction(self.create_relationships)

    @staticmethod
    def create_constraints(tx):
        tx.run("CREATE CONSTRAINT program_name IF NOT EXISTS ON (p:Program) ASSERT p.name IS UNIQUE")
        tx.run("CREATE CONSTRAINT course_number IF NOT EXISTS ON (c:Course) ASSERT c.course_number IS UNIQUE")
        tx.run("CREATE CONSTRAINT student_id IF NOT EXISTS ON (s:Student) ASSERT s.student_id IS UNIQUE")
        tx.run("CREATE CONSTRAINT teacher_id IF NOT EXISTS ON (t:Teacher) ASSERT t.teacher_id IS UNIQUE")

    @staticmethod
    def create_program_node(tx):
        tx.run("""
        CREATE (:Program {
            name: 'Program Name',
            description: 'Program Description'
        })
        """)

    @staticmethod
    def create_course_node(tx):
        tx.run("""
        CREATE (:Course {
            course_number: 'CS101',
            name: 'Intro to Computer Science',
            description: 'This is an introductory course on computer science'
        })
        """)

    @staticmethod
    def create_class_node(tx):
        tx.run("""
        CREATE (:Class {
            section_number: '001',
            start_date: date('2024-01-10'),
            end_date: date('2024-05-10'),
            class_days_of_week: 'MWF',
            class_time: time('10:00:00'),
            class_duration: duration('P1H'),
            lab_days_of_week: 'T',
            lab_time: time('14:00:00'),
            lab_duration: duration('P2H')
        })
        """)

    @staticmethod
    def create_person_node(tx):
        tx.run("""
        CREATE (:Person {
            name: 'John Doe',
            givenName: 'John',
            familyName: 'Doe',
            birthDate: date('1990-01-01'),
            signupDate: datetime('2024-01-01T10:00:00')
        })
        """)

    @staticmethod
    def create_student_node(tx):
        tx.run("""
        CREATE (:Student {
            student_id: 'S12345',
            name: 'Jane Doe',
            givenName: 'Jane',
            familyName: 'Doe',
            birthDate: date('2000-01-01'),
            signupDate: datetime('2024-01-01T10:00:00')
        })
        """)

    @staticmethod
    def create_teacher_node(tx):
        tx.run("""
        CREATE (:Teacher {
            teacher_id: 'T98765',
            name: 'Dr. Smith',
            givenName: 'John',
            familyName: 'Smith',
            birthDate: date('1980-01-01'),
            signupDate: datetime('2024-01-01T10:00:00')
        })
        """)

    @staticmethod
    def create_textbook_node(tx):
        tx.run("""
        CREATE (:TextBook {
            title: 'Introduction to Computer Science',
            author_name: 'John Author',
            description: 'This is a textbook for introductory computer science'
        })
        """)

    @staticmethod
    def create_topic_node(tx):
        tx.run("""
        CREATE (:Topic {
            title: 'Basics of Algorithms',
            url: 'http://example.com/algorithms',
            details: 'Details about algorithms',
            lastReviewed: '2024-01-01',
            creationDate: date('2024-01-01'),
            sequenceNumber: 1
        })
        """)

    @staticmethod
    def create_interaction_node(tx):
        tx.run("""
        CREATE (:Interaction {
            title: 'Algorithm Tutorial',
            author_name: 'John Author',
            description: 'This is a tutorial about algorithms'
        })
        """)

    @staticmethod
    def create_relationships(tx):
        # Relationships between Program, Course, and Class
        tx.run("""
        MATCH (p:Program {name: 'Program Name'}), (c:Course {course_number: 'CS101'})
        CREATE (p)-[:contains]->(c)
        """)
        tx.run("""
        MATCH (c:Course {course_number: 'CS101'}), (cl:Class {section_number: '001'})
        CREATE (c)-[:scheduled]->(cl)
        """)
        
        # Relationships between Student, Program, and Class
        tx.run("""
        MATCH (s:Student {student_id: 'S12345'}), (p:Program {name: 'Program Name'})
        CREATE (s)-[:admission]->(p)
        """)
        tx.run("""
        MATCH (s:Student {student_id: 'S12345'}), (cl:Class {section_number: '001'})
        CREATE (s)-[:registers]->(cl)
        """)
        
        # Relationships between Teacher and Class
        tx.run("""
        MATCH (t:Teacher {teacher_id: 'T98765'}), (cl:Class {section_number: '001'})
        CREATE (t)-[:teaches]->(cl)
        """)

        # Relationships between Course and TextBook
        tx.run("""
        MATCH (c:Course {course_number: 'CS101'}), (tb:TextBook {title: 'Introduction to Computer Science'})
        CREATE (c)-[:taught]->(tb)
        """)

        # Relationships between Topic and TextBook
        tx.run("""
        MATCH (t:Topic {title: 'Basics of Algorithms'}), (tb:TextBook {title: 'Introduction to Computer Science'})
        CREATE (t)-[:contains]->(tb)
        """)

        # Relationships between Student and Topic (knows edge)
        tx.run("""
        MATCH (s:Student {student_id: 'S12345'}), (t:Topic {title: 'Basics of Algorithms'})
        CREATE (s)-[:knows {level: 3, assesment_date: datetime('2024-01-10T10:00:00')}]->(t)
        """)

        # Relationships between Interaction and Topic
        tx.run("""
        MATCH (i:Interaction {title: 'Algorithm Tutorial'}), (t:Topic {title: 'Basics of Algorithms'})
        CREATE (i)-[:covers]->(t)
        """)


# Example usage
if __name__ == "__main__":
    uri = "bolt://localhost:7687"  # Replace with your Neo4j URI
    user = "neo4j"  # Replace with your Neo4j username
    password = "password"  # Replace with your Neo4j password

    schema = EduSmartSchema(uri, user, password)
    schema.create_schema()
    schema.close()
