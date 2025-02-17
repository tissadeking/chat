from langchain_openai import ChatOpenAI
import pickle

#initialize model
groq_api_key = "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"  
llama3 = ChatOpenAI(api_key=groq_api_key,
                    base_url="https://api.groq.com/openai/v1",
                    model="llama3-8b-8192"
                    )

def llm_query_fun_3_8(user_query):
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
