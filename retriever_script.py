from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.vector_stores.faiss import FaissVectorStore
#from llama_index.core.storage.storage_context import StorageContext
#import faiss
#from langchain_openai import ChatOpenAI
from llama_index.core.node_parser import SimpleNodeParser
#import faiss
import pickle
#import cloudpickle
import warnings

warnings.filterwarnings("ignore")

# Load your dataset (e.g., text files, PDFs, etc.)
documents = SimpleDirectoryReader("data_folder").load_data()

# Convert dataset into nodes (chunks)
node_parser = SimpleNodeParser.from_defaults(chunk_size=512)
nodes = node_parser.get_nodes_from_documents(documents)

# Initialize Embedding Model (HuggingFace or OpenAI)
#embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
# loads BAAI/bge-small-en-v1.5
#embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
#embeddings = embed_model.get_text_embedding("Hello World!")
#print(len(embeddings))
# Create FAISS Index for fast similarity search
#faiss_index = faiss.IndexFlatL2(embed_model.get_text_embedding_dimension())
'''faiss_index = faiss.IndexFlatL2(len(embeddings))
vector_store = FaissVectorStore(faiss_index=faiss_index)
# Store vectors in a storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)
# Create VectorStoreIndex
index = VectorStoreIndex(nodes, storage_context=storage_context, embed_model=embed_model)
'''
# Create VectorStoreIndex with the local embedding model
index = VectorStoreIndex.from_documents(documents, show_progress=True, embed_model=embed_model)

#to be able to retrieve most relevant chunks of data based on the query
retriever = index.as_retriever(similarity_top_k=3)

#print(retriever)

#save the retriever
with open("retriever.pkl", "wb") as f:
    pickle.dump(retriever, f, protocol=pickle.HIGHEST_PROTOCOL)
