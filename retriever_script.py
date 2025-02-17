from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SimpleNodeParser
import pickle
import warnings

warnings.filterwarnings("ignore")

# Load your dataset (e.g., text files, PDFs, etc.)
documents = SimpleDirectoryReader("data_folder").load_data()

# Convert dataset into nodes (chunks)
node_parser = SimpleNodeParser.from_defaults(chunk_size=512)
nodes = node_parser.get_nodes_from_documents(documents)

# Create VectorStoreIndex with the local embedding model
index = VectorStoreIndex.from_documents(documents, show_progress=True, embed_model=embed_model)

#to be able to retrieve most relevant chunks of data based on the query
retriever = index.as_retriever(similarity_top_k=3)

#print(retriever)

#save the retriever
with open("retriever.pkl", "wb") as f:
    pickle.dump(retriever, f, protocol=pickle.HIGHEST_PROTOCOL)
