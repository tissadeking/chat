import pandas as pd
from groq import Groq
from llama_index.llms.groq import Groq
from langchain_openai import ChatOpenAI
# pip install openai pandas python-docx
import fitz, os
import openai
from docx import Document

# Initialize Groq model
groq_api_key = "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"  # Replace with your Groq API key
model = Groq(model="llama3-8b-8192", api_key=groq_api_key, temperature=0.0)
llama3 = ChatOpenAI(api_key=groq_api_key,
                    base_url="https://api.groq.com/openai/v1",
                    model="llama-3.3-70b-versatile",
                    )


#LOAD FILES
def load_csv_files(folder_path):
    data = {}
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(folder_path, file))
            data[file] = df
    return data

def load_txt_files(folder_path):
    data = {}
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                data[file] = f.read()
    return data

def load_word_files(folder_path):
    data = {}
    for file in os.listdir(folder_path):
        if file.endswith('.docx'):
            doc = Document(os.path.join(folder_path, file))
            text = "\n".join([para.text for para in doc.paragraphs])
            data[file] = text
    return data

def load_pdf_files(folder_path):
    data = {}
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            text = ""
            pdf_path = os.path.join(folder_path, file)
            pdf_document = fitz.open(pdf_path)
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text += page.get_text("text")
            data[file] = text
    return data

#preprocess the data
def preprocess_data(data):
    #flatten the data into a single string (for simplicity in querying)
    processed_data = []
    for filename, content in data.items():
        if isinstance(content, pd.DataFrame):  #for CSV data (tabular)
            content = content.to_string()
        #processed_data.append(f"File: {filename}\n{content}\n\n")
        # processed_data.append(f"File: {filename}\n{content}\n\n")
        processed_data.append(content)
    return "\n".join(processed_data)

#retrieve data from the files inside the folder
def retrieve():
    data_folder = 'data_folder'
    #load data from CSV, TXT, and DOCX files
    csv_data = load_csv_files(data_folder)
    txt_data = load_txt_files(data_folder)
    word_data = load_word_files(data_folder)
    pdf_data = load_pdf_files(data_folder)
    #combine all data into a single list of documents
    all_data = {**csv_data, **txt_data, **word_data, **pdf_data}
    context = preprocess_data(all_data)
    return context

df = retrieve()


def llm_query_fun_3_70(user_query):
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
