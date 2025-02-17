#import csv
#import os
#from tf_idf_method import main_tf_idf
from llam3_8_rag import llm_query_fun_3_8
from llam3_70_rag import llm_query_fun_3_70
from mixtral_groq_rag import llm_query_fun_mixtral
from gemma2_groq_rag import llm_query_fun_gemma2
#import time
#import tracemalloc

#use_case = 'GREEN DEAL'
print("Welcome to the dataset info retrieval tool!")
print("Type 'exit' to quit.\n")

def start_fun(user_query, use_case):
    # open and read the file after the appending:
    f = open("model.txt", "r")
    #print(f.read())
    model = f.read()
    models = [model]
    #return selected_model
    # Get user query
    #user_query = input("Enter your query: ")
    #if user_query.lower() == "exit":
    #    print("Goodbye!")
    #    break
    global answer
    columns = ['use_case', 'time', 'memory', 'query', 'answer', 'length']
    #get answer from the dataset
    for model in models:
        #answer = ''
        #data_dict = {}
        #tracemalloc.start()
        #start = time.time()
        '''if model == 'tf_idf_method':
            answer = main_tf_idf(user_query)
        if model == 'knl_graph':
            #answer = main_tf_idf(user_query)
            continue'''
        if model == 'llama3-8b':
            answer = llm_query_fun_3_8(user_query)
        if model == 'mixtral-8x7b':
            answer = llm_query_fun_mixtral(user_query)
        if model == 'gemma2-9b':
            answer = llm_query_fun_gemma2(user_query)
        if model == 'llama-3.3-70b':
            answer = llm_query_fun_3_70(user_query)

        '''end = time.time()
        current_usage, peak_usage = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        file_name = model + '.csv'
        data_dict['use_case'] = use_case
        data_dict['time'] = end - start
        data_dict['memory'] = current_usage
        data_dict['query'] = user_query
        data_dict['answer'] = answer
        answer_main = answer
        answer = answer.replace(' ', '')
        data_dict['length'] = len(answer)
        print('data dict: ', data_dict)
        if os.path.exists(file_name) == True:
            with open(file_name, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writerow(data_dict)
        elif os.path.exists(file_name) == False:
            with open(file_name, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                writer.writerow(data_dict)'''
    return answer