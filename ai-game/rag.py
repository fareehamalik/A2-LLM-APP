import os
import chromadb #wrong??
#from chromadb.config import Settings
#from chromadb import Client
#client = Client() wrong??
#chromadb setuo 
import sys
print(sys.path) #major issues rag file testing

#chroma db filder, data persistence

client = chromadb.PersistentClient(path="./chroma_db")

#client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
collection = client.get_or_create_collection(name="syllabus_lore")
#DATA_FILE = "RAG-data/syllabus.md" #getting file from directory
DATA_FILE = os.path.join("RAG-data","syllabus.md") #exists no join


#initialize rag, if no file checking for that
def initialize():
    if collection.count()>0:
        return
    
    if not os.path.exists(DATA_FILE):
        print(f"RAG warning {DATA_FILE} not found")
        return
    
    print("RAG loading syllabus into memory!")
    with open(DATA_FILE, "r") as f:
        text=f.read()
    
    #each text as line being read md, txt dont matter
    documents = [line for line in text.split('\n') if line.strip()]
    #TODO: if more documents need way to organize!!
    ids = [str(i) for i in range(len(documents))]

    if documents: 
         collection.add(documents=documents, ids=ids) #chroma needs this

#retrieve context - not retrieve (causing issue from mismatch)
def retrieve_context(query, top_n=2): #searching database for 2 most relevant lines
    results = collection.query( #misplaced, issue below
             query_texts=[query],
             #top_n=1 #most accurate match
             n_results=top_n
        )

#return txt or empty string if nothing founf 
    if results['documents'] and results['documents'][0]:
        return results['documents'][0][0]
    return "" #return""
  # temporary list to store (chunk, similarity) pairs
  


#note, changed syllabus.txt to .md, instructor req
#note online says md and txt the same 

#initialize_rag() error coz mismatch 
initialize()
'''
unused code
similarities = []
initialize_rag() #running when imported, check DB
'''
