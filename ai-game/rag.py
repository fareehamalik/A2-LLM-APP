import os
import chromadb

#chromadb setuo 

#chroma db filder, data persistence

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_creat_collection(name="syllabus_lore")
DATA_FILE = "RAG-data/syllabus.md" #getting file from directory

#initialize rag, if no file checking for that
def initialize():
    if collection.count()>0:
        return
    
    if not os.path.exist(DATA_FILE):
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




    #w

#retrieve context 
def retrieve(query, top_n=2): #searching database for 2 most relevant lines
    results = collection.query( #misplaced, issue below
             query_texts=[query],
             top_n=1 #most accurate match
        )

#return txt or empty string if nothing founf 
    if results['documents'] and results['documents'][0]:
        return results['documents'][0][0]
    return""
  # temporary list to store (chunk, similarity) pairs
  


#note, changed syllabus.txt to .md, instructor req
#note online says md and txt the same 

initialize_rag()
'''
unused code
similarities = []
initialize_rag() #running when imported, check DB
'''
