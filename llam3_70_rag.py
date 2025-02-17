'''from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.storage.storage_context import StorageContext
import faiss'''
from langchain_openai import ChatOpenAI
#from llama_index.core.node_parser import SimpleNodeParser
import pickle

'''# Load your dataset (e.g., text files, PDFs, etc.)
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
#faiss_index = faiss.IndexFlatL2(embed_model.get_text_embedding_dimension())'''
'''faiss_index = faiss.IndexFlatL2(len(embeddings))
vector_store = FaissVectorStore(faiss_index=faiss_index)
# Store vectors in a storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)
# Create VectorStoreIndex
index = VectorStoreIndex(nodes, storage_context=storage_context, embed_model=embed_model)
'''
'''# Create VectorStoreIndex with the local embedding model
index = VectorStoreIndex.from_documents(documents, show_progress=True, embed_model=embed_model)

#to be able retrieve most relevant chunks of data based on the query
retriever = index.as_retriever(similarity_top_k=3)'''

# Load the index
#with open("index.pkl", "rb") as f:
#    index = pickle.load(f)

#user_query = "what are the sous-domane?"
#print(retrieve_relevant_data(user_query))

# Initialize Groq model
groq_api_key = "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"  # Replace with your Groq API key
#model = Groq(model="llama3-8b-8192", api_key=groq_api_key, temperature=0.0)
llama3 = ChatOpenAI(api_key=groq_api_key,
                    base_url="https://api.groq.com/openai/v1",
                    model="llama-3.3-70b-versatile",
                    )
def llm_query_fun_3_70(user_query):
    #load the retriever
    with open("retriever.pkl", "rb") as f:
        retriever = pickle.load(f)

    #retrieve most relevant information
    def retrieve_relevant_data(user_query):
        retrieved_nodes = retriever.retrieve(user_query)
        retrieved_text = "\n".join([node.text for node in retrieved_nodes])
        return retrieved_text

    def query_dataset(user_query):
        prompt = f"""
        You are a data analyst. Given the following dataset, answer the user's query. Please, avoid mistakes.
        Answer only according to information you find in the dataset. If an information is not found in the dataset just say you don't know and stop there.

        Dataset:
        {retrieve_relevant_data(user_query)}

        User Query:
        "{user_query}"

        Return the answer in plain text.
        """
        response = llama3.invoke(prompt)

        return response.content

    answer = query_dataset(user_query)

    return answer

#query = "what things have been done in biogas?"
#print(llm_query_fun_3_70(query))


