
# backend/app/services/rag_service.py
from app.db.pinecone_store import vector_db
from app.core.llm import llm
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

def add_to_vector_store(text: str, filename: str) -> int:
    """
    Chunks text and saves it to ChromaDB.
    Returns the number of chunks added.
    """
    # We chunk the text so the AI doesn't get overwhelmed by massive documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200 # Overlap prevents cutting sentences in half
    )
    chunks = text_splitter.split_text(text)
    
    # Convert chunks into LangChain Document objects with metadata
    docs = [Document(page_content=chunk, metadata={"source": filename}) for chunk in chunks]
    
    # Add to ChromaDB
    vector_db.add_documents(docs)
    return len(docs)

def query_rag_system(question: str) -> str:
    """
    Searches the vector store and uses Mistral to answer the question based on the documents.
    """
    # 1. Retrieve the top 3 most relevant chunks from ChromaDB
    docs = vector_db.similarity_search(question, k=3)
    
    # Combine the retrieved chunks into a single context string
    context = "\n\n".join([f"Source ({doc.metadata.get('source')}): {doc.page_content}" for doc in docs])
    
    # 2. Create the RAG prompt
    prompt = ChatPromptTemplate.from_template(
        "You are an expert document analysis AI. Answer the following question based ONLY on the provided context.\n"
        "If you cannot find the answer in the context, say 'I do not have enough information in the uploaded documents to answer that.'\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}"
    )
    
    # 3. Chain the prompt, the standard LLM (not the structured one), and a string parser
    chain = prompt | llm | StrOutputParser()
    
    # 4. Generate the final answer
    return chain.invoke({"context": context, "question": question})