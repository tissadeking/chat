#import pandas as pd
#from llama_index.llms.groq import Groq
from langchain_openai import ChatOpenAI
#import fitz, os
#from docx import Document

# Initialize Groq model
groq_api_key = "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"  # Replace with your Groq API key
#model = Groq(model="llama3-8b-8192", api_key=groq_api_key, temperature=0.0)
llama3 = ChatOpenAI(api_key=groq_api_key,
                    base_url="https://api.groq.com/openai/v1",
                    model="mixtral-8x7b-32768",
                    )

#open and read processed data file
f = open("processed_data.txt", "r")
#print(f.read())
df = f.read()

def llm_query_fun_mixtral(user_query):
    def query_dataset(user_query):
        prompt = f"""
        You are a data analyst. Given the following dataset, answer the user's query. Please, avoid mistakes.
        Answer only according to information you find in the dataset. If an information is not found in the dataset just say you don't know and stop there.

        Dataset:
        {df}

        User Query:
        "{user_query}"

        Return the answer in plain text.
        """
        response = llama3.invoke(prompt)

        return response.content

    answer = query_dataset(user_query)
    return answer
