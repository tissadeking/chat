#import pandas as pd
from langchain_openai import ChatOpenAI
#import fitz, os
#from docx import Document

#initialize model
groq_api_key = "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"  # Replace with your Groq API key
llama3 = ChatOpenAI(api_key=groq_api_key,
                    base_url="https://api.groq.com/openai/v1",
                    model="gemma2-9b-it",
                    )
#open and read processed data file
f = open("processed_data.txt", "r")
#print(f.read())
df = f.read()

#query with the LLM
def llm_query_fun_gemma2(user_query):

    def query_dataset(user_query):
        #generate prompt for LLM
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
