from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from database import init_connection
from config import MANUALS_DIR, EMBEDDING_MODEL
import os

def embed_and_store():
    """Reads manuals, creates embeddings, and stores them in Supabase."""
    print("Starting manual embedding process...")
    db_client = init_connection()
    
    # 1. Load Documents
    docs_content = []
    for filename in os.listdir(MANUALS_DIR):
        with open(os.path.join(MANUALS_DIR, filename), 'r') as file:
            docs_content.append(file.read())
    
    # 2. Split documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text('\n\n'.join(docs_content))
    
    # 3. Create Embeddings
    print(f"Creating embeddings using '{EMBEDDING_MODEL}'...")
    embeddings_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    embeddings = embeddings_model.embed_documents(texts)
    
    # 4. Store in Supabase
    print(f"Storing {len(texts)} chunks in Supabase...")
    db_client.table('documents').delete().neq('id', 0).execute() # Clear old documents
    
    for i, text in enumerate(texts):
        db_client.table('documents').insert({
            'content': text,
            'embedding': embeddings[i]
        }).execute()
        
    print("Embedding process complete!")

if __name__ == '__main__':
    embed_and_store()