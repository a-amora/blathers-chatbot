## Blathers

Blathers is a prototype, web-based RAG chatbot build on the LangChain framework.  In its present implementation it is LLM-agnostic and utilize's the HuggingFace API to allow the user to test out a variety of LLMs.

Blathers provides a simple React frontend to it's Flask backend.  This Flask backend provides several simple REST endpoints which allow the user to ask questions and upload Word documents to a QDrant vector database.  When answering end user questions, Blathers uses uploaded documents as reference material and tries to answer questions based solely on relevant materials.

