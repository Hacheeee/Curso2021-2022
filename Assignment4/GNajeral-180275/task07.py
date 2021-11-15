# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fzywZ4EwNykCSoc5kjbwf7_KAb8NKSC-

**Task 07: Querying RDF(s)**
"""

#!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

from rdflib.plugins.sparql import prepareQuery
NS = Namespace("http://somewhere#")
q = prepareQuery('''
   SELECT ?x WHERE { 
     ?x rdfs:subClassOf ns:Person. 
   }
   ''',
   initNs = { "ns": NS}
 )
for r in g.query(q):
  print(r.x)

#RDFLIB
print("\nRDFlib")

for s, p, o in g.triples((None, RDFS.subClassOf, NS.Person)):
  print(s)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

from rdflib.plugins.sparql import prepareQuery
NS = Namespace("http://somewhere#")
q = prepareQuery('''
   SELECT ?s WHERE { 
     {?s rdf:type ns:Person}
     UNION
     {?x rdfs:subClassOf ns:Person.
       ?s rdf:type ?x}
   }
   ''',
   initNs = { "ns": NS}
 )
for r in g.query(q):
  print(r.s)

#RDFLIB

print("\nRDFlib")

subclass = g.value(subject = None, predicate = RDF.type, object = NS.Researcher) 
print(subclass)
for s, p, o in g.triples((None, RDF.type, NS.Person)):
  print(s)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

from rdflib.plugins.sparql import prepareQuery
NS = Namespace("http://somewhere#")
q = prepareQuery('''
   SELECT ?s ?p WHERE { 
     {?s rdf:type ns:Person.
       ?s ?p ?o} 
     UNION 
     {?s rdf:type ?x.
       ?s ?p ?o.
       ?x rdfs:subClassOf ns:p}
   }
   ''',
   initNs = { "ns": NS}
 )
for r in g.query(q):
  print(r.s, r.p)

#RDFLIB

print("\nRDFlib")

subclass = g.value(None, RDFS.subClassOf, NS.Person)
subperson = g.value(None, RDF.type, subclass)
for s,p,o in g.triples((None, RDF.type, NS.Person)):
  for a,b,c in g.triples((s, None, None)):
    print(a,b)

for s,p,o in g.triples((subperson, None, None)):
  print(s,p)