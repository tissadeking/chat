from llam3_8 import llm_query_fun_3_8
from llam3_70 import llm_query_fun_3_70
from mixtral_groq import llm_query_fun_mixtral
from gemma2_groq import llm_query_fun_gemma2

#use_case = 'GREEN DEAL'
print("Welcome to the dataset info retrieval tool!")
print("Type 'exit' to quit.\n")

def start_fun(user_query, use_case):
    #open and read the model file:
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
    
    #get answer from the dataset
    for model in models:
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

    return answer
