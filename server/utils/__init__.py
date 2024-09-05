import mimetypes
import os
from flask import current_app
from server.vector import vectorize
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.prompts import PromptTemplate

conversion_handlers = {
    "application/msword": "word",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "word"
}


def inspect(state):
    print(state)
    return state

def ask(query):
    answer = ""
    llm = current_app.config["LLM"]
    retriever = current_app.config["RETRIEVER"]

    if llm and retriever:
        #You can't use chat memory here, since it reinitializes with each post request

        template = """Your name is Blathers and you are a chatbot.  
        Your job is to provide an answer to the question below, using the context below.
        If you cannot find an answer to the user's question using the context below, please say "I am sorry, I couldn't find the answer to that."
        Please try to keep your answer as concise and close to the context as possible.
        Respond with nothing but your Helpful Answer.

        Context: {context}

        Question: {question}

        Helpful Answer:"""

        prompt = PromptTemplate.from_template(template)

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            #| RunnableLambda(inspect) #Prints retrieved context
            | llm
            | StrOutputParser()
        )
        response = rag_chain.invoke({"question": query})
        
        if response:
            answer = response.strip()

    return answer

def validate_file(file):
    file_type = None
    filename = file.filename
    file_type, _ = mimetypes.guess_type(filename)

    if file_type in conversion_handlers.keys():
        return conversion_handlers[file_type]
    else:
        print("No file handler found")

    return file_type

def process_word(name, path):
    #Convert to Azure AI Document Intelligence?
    results = None
    loader = Docx2txtLoader(path)

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n","\n", "  "],
        chunk_size = 1000,
        chunk_overlap = 200
    )

    data = loader.load_and_split(splitter)

    if data and len(data) > 0:
        #print(data)
        results = vectorize(data)
    else:
        print("No document data.")

    #Delete local copy of file
    os.remove(path)

    return results

def load_llm(app):
    key = os.getenv('HGF')
    #repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id, 
        max_new_tokens=512,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=0.01,
        return_full_text=False,
        repetition_penalty=1.03,
        huggingfacehub_api_token=key
    )

    if llm:
        app.config['LLM'] = llm
        print("Connected to LLM.")
