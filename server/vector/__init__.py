
import os
from flask import current_app
from langchain_qdrant import Qdrant
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

def initialize_db(app):
    key = os.getenv('KEY')
    host =  os.getenv('QDRANT')
    collection = os.getenv('COLLECTION')
        
    if key and host and collection:
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en")
        app.config['EMBEDDINGS'] = embeddings

        qdrant = Qdrant.from_existing_collection(
            embedding=embeddings,
            collection_name=collection,
            api_key=key,
            url=host,
            path=None 
        )
    
        retriever = qdrant.as_retriever()
        
        if retriever:
            app.config['DB'] = qdrant
            app.config['RETRIEVER'] = retriever
  
    return None

def vectorize(data):
    #Unit test for memory overflow
    results = None

    if data:
        createCollection = False #Initial deployment only - needs refactor
        client = current_app.config['DB']
        
        if createCollection is True:
            print("Creating collection...")
            results = create_collection(data)
        else:
            try:
                client.add_documents(data)
                results =  True
            
            except Exception as e:
                print(str(e))

    return results

def create_collection(data):
    key = os.getenv('KEY')
    host =  os.getenv('QDRANT')
    collection = os.getenv('COLLECTION')
    embeddings = current_app.config['EMBEDDINGS']

    results = None

    try:
        Qdrant.from_documents(
            documents=data,
            embedding=embeddings,
            collection_name=collection,
            api_key=key,
            url=host,
            path=None 
        )

        results = True

    except Exception as e:
        print(str(e))

    return results