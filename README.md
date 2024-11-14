
### EduSmart Schema using Neo4j (a graph database management system)
Py2neo is a client library and toolkit for working with Neo4j from within Python applications


**Install Packages**

* `pip install neo4j` :- interact with the Neo4j database
* `pip install py2neo` :- client library and toolkit for working with Neo4j from within Python.
* `poetry add py2neo`  :- dependency management tool for Python.

**Structure of Neo4j**

* **`Node`**: An entity, like a person, place, or thing.

* **`Relationship`**: Connections between nodes.

* **`Properties`**: Key-value pairs attached to nodes and relationships; store data like names and dates.

* **`Labels`**: Tags or categories assigned to nodes.

* **`Indexing`**: Neo4j allows indexing on node properties to speed up query performance.

* **`Cypher Query Language`**: A powerful and intuitive query language used by Neo4j.

### Commands used for manipulating data in Neo4j

**`MATCH` Command in Neo4j** 

**`MATCH`** is used to find specific parts of the graph in Neo4j. When retrieving, updating, or deleting data, start with `MATCH` to set the scope. Without it, navigating the graph would be challenging.

Counts all nodes in the database
```bash
MATCH (n)
RETURN COUNT(n) AS total_nodes
```

Delete all nodes and relationship
```bash
MATCH (n)
DETACH DELETE n
```

Deletes the node n along with all its relationships
```bash
MATCH (n:user {name: 'my-name', name_id: 1})
DETACH DELETE n
```
`DETACH DELETE n:` This deletes the node n along with all its relationships.

Delete specific properties from all nodes
```bash
MATCH (n)
REMOVE n.course_number, n.description, n.name, n.name_id 
```
Removes the specified properties from all nodes matched by m without deleting the nodes themselves.

### Tutorials

[Connection - neo4j](https://neo4j.com/docs/python-manual/current/connect/)

[NODES 2023 - Building Your Python API on Top of Neo4j with neomodel](https://www.youtube.com/watch?v=v4CgjiVist4)

[Neo4j with Python [Upload data into Neo4j with Python]](https://www.youtube.com/watch?v=yluHRteVBNI)

https://neo4j.com/blog/py2neo-2-0-unleashed/

https://stackoverflow.com/questions/41356886/importing-neo4j-with-py2neo

[Creating Neo4J Graphs using Pytho](https://medium.com/@herambh/creating-neo4j-graphs-using-python-bd59662cbad6)

[How to create label on py2neo object using Object-Graph-Mapping before saved in Neo4j database](https://stackoverflow.com/questions/24832013/how-to-create-label-on-py2neo-object-using-object-graph-mapping-before-saved-in)


[Introduction to Property Graphs Using Python With Neo4j](https://sease.io/2023/08/introduction-to-property-graphs-using-python-with-neo4j.html)


[Using Neo4j from Python](https://neo4j.com/docs/getting-started/languages-guides/neo4j-python/)
   

[NEO4J TUTORIAL|Neo4j Python|Create Rest Api Using Neo4j & FastApi From Python|PART:105](https://www.youtube.com/watch?v=L_OOTp7fd1g)

[NEO4J_PYTHON](https://github.com/ronidas39/NEO4J_PYTHON/tree/main)

`**`
COALESCE


# Education_System_Using_UVPython_Neo4j
