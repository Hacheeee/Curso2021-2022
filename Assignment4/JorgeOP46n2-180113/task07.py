# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE

**Task 07: Querying RDF(s)**
"""

#!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)

#g.parse(github_storage+"/resources/example6.rdf", format="xml")
g.parse("../course_materials/rdf/example6.rdf", format="xml")

ns = Namespace("http://somewhere#")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""
print("TASK 7.1")
print("RDFLib")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s, p, o)
print("SPARQL")
q1 = prepareQuery("""
    SELECT ?subclase WHERE{
    ?subclase rdfs:subClassOf ns:Person.
    }
""", initNs={"ns":ns})

for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**"""
print("TASK 7.2")
print("RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    print(s)

for x, y, z in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s, p, o in g.triples((None, RDF.type, x)):
        print(s)

print("SPARQL")
q2 = prepareQuery('''
    SELECT DISTINCT ?p WHERE{
        {?p rdf:type ns:Person.}
        UNION
        {?aux rdfs:subClassOf ns:Person.
         ?p rdf:type ?aux.}
    }''',
    initNs={"ns": ns}
    )
for i in g.query(q2):
    print(i.p)



"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**"""
print("TASK 7.3")
print("RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    for s2, p2, o2 in g.triples((s, None, None)):
        print(s2, p2)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s2, p2, o2 in g.triples((None, RDF.type, s)):
        for s3, p3, o3 in g.triples((s2, None, None)):
            print(s3, p3)
print("SPARQL")
q3 = prepareQuery('''
    SELECT DISTINCT ?person ?properties WHERE{
        {?person rdf:type ns:Person.
         ?person ?properties ?a.}
        UNION{
        ?aux rdfs:subClassOf ns:Person.
        ?person rdf:type ?aux.
        ?person ?properties ?aux1.}
    }''',
    initNs={"ns": ns}
    )
for i in g.query(q3):
    print(i.person,i.properties)