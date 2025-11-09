import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from config import EMBEDDING_MODEL, LLM_MODEL, SUPABASE_URL, SUPABASE_KEY

@st.cache_resource
def initialize_rag_pipeline():
    """Initializes RAG pipeline using Supabase/pgvector as the retriever."""
    connection_string = f"postgresql://postgres:{'YOUR_DATABASE_PASSWORD'}@{SUPABASE_URL.split('@')[1]}"
    
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    
    vectorstore = PGVector(
        connection_string=connection_string,
        embedding_function=embeddings,
        collection_name='documents', # This is your table name
    )
    
    llm = Ollama(model=LLM_MODEL)

    prompt_template = "..." # Same prompt template as before
    PROMPT = PromptTemplate(...)

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT}
    )
    return rag_chain
# ... (rest of the file is the same as before) ...