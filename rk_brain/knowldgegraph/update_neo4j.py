
import gensim 
from py2neo import authenticate, Graph, Node, Relationship

# set up authentication parameters
authenticate("localhost:7474", "neo4j", "password123")

# connect to authenticated graph database
graph = Graph("http://localhost:7474/db/data/")

tx = graph.begin()

tx.run("")

