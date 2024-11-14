from neo4j import GraphDatabase
from pydantic import BaseModel
from fastapi import FastAPI
import os
from dotenv import load_dotenv

CONNECTION_URI="bolt://localhost:7687"
USERNAME="neo4j"
PASSWORD="password"

class nodemodel(BaseModel):
    name:str
    name_id:int

# Driver instantiation
def connection():
    driver = GraphDatabase.driver(CONNECTION_URI,auth=(USERNAME, PASSWORD))
    return driver

app=FastAPI()

@app.get('/')
def get_root():
    return {"response" : "EduSmart Scheema"}

# nullable=False
# 

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

# @app.put("/update")
# def update(node:nodemodel,inputname):
#     driver_neo4j=connection()
#     session=driver_neo4j.session()
#     q1="""
#     match(n:user{name:$inputname}) set n.name=$name ,n.user_id=$user_id return n.name as name
#     """
#     x={"inputname":inputname,"name":node.name,"user_id":node.user_id}
#     results=session.run(q1,x)
#     data=[{"Name":row["name"]}for row in results]
#     if (len(data)>0):
#         data=data[0]["Name"]
#         return {"response":"node updated with new name: "+data}
#     else:
#         return {"response":"your input name is not found in the graph!!"}

### ========================= *****  ========================= ###
    
# @app.delete("/delete/{user_id}")
# def delete(user_id:int):
#     driver_neo4j=connection()
#     session=driver_neo4j.session()
#     q1="""
#     match(n:user{user_id:$user_id}) delete n
#     """
#     x={"user_id":user_id}
#     results=session.run(q1,x)
#     response=results.consume().counters
#     deleted_nodes=response.nodes_deleted
#     if(deleted_nodes>0):
#         return {"Response":response}
#     else:
#         return {"Response":"Your Entered user_is Is Missing In The Graph"}    

### ========================= *****  ========================= ###

### ========================= *****  ========================= ###

# # Define a function to create nodes and relationships
# def create_data(tx):
#     tx.run("CREATE (a:Person {name: $name})", name="Alice")

# # Open a session and run your function
# with driver.session() as session:
#     session.write_transaction(create_data)

# # Close the driver connection when done
# driver.close()

### ========================= *****  ========================= ###


# class HelloWorldExample:

#     def __init__(self, uri, user, password):
#         self.driver = GraphDatabase.driver(uri, auth=(user, password))

#     def close(self):
#         self.driver.close()

#     def print_greeting(self, message):
#         with self.driver.session() as session:
#             greeting = session.execute_write(self._create_and_return_greeting, message)
#             print(greeting)

#     @staticmethod
#     def _create_and_return_greeting(tx, message):
#         result = tx.run("CREATE (a:Greeting) "
#                         "SET a.message = $message "
#                         "RETURN a.message + ', from node ' + id(a)", message=message)
#         return result.single()[0]


# if __name__ == "__main__":
#     greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "password")
#     greeter.print_greeting("hello, world")
#     greeter.close()

### ========================= *****  ========================= ###

# @app.delete("/delete")
# def delete_node(name: str):
#     driver_neo4j = connection()
#     session = driver_neo4j.session()
#     q2 = """
#     MATCH (n:Course {name: $name})
#     DETACH DELETE n
#     """
#     x = {"name": name}
#     session.run(q2, x)
#     session.close()
#     return {"response": f"Node with name '{name}' deleted"}

### ========================= *****  ========================= ###

# # Define your database connection parameters
# load_dotenv()
# CONNECTION_URI = os.getenv("CONNECTION_URI")
# USERNAME = os.getenv("neo4j")
# PASSWORD = os.getenv("password")