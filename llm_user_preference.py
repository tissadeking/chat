import json
from llama_index.llms.groq import Groq
import config

groq_api_key = config.groq_api_key

def llm_preference_fun(ask):
    llama3 = Groq(model="llama3-8b-8192", api_key=groq_api_key, temperature=0.0)

    examples = """Respond only with valid JSON. Do not write an introduction or summary. 
    If the input starts with intent then the type will be intent otherwise it will be query.
    For intents, the default values of the parameters in the result dictionary are 1. 
    The values can be either 5 or 1 depending on what the user wants.
    If the input from the user needs a fast model or model with small latency then value of low_latency should be 5.
    If the input says the model should not consume much memory or space then low_memory will be 5.
    If the input is that the model goes straight to the point, the low_verbosity should be 5.
    If the input is that the model should not explain much, the low_verbosity should be 5.
    If the input says the model should be able to explain a lot then much_explanation should be 5.
    If the input says the model should have high verbosity then much_explanation should be 5.
    If the input is that the model should focus well on ground truth or be able to retrieve enough good answers from the true cases, then recall should be 5.
    If the input is that the model is very accurate or correct, then accuracy should be 5.
    If the input is that the model should be precise, then precision should be 5.
    If the input is that the user wants to query dataset in different language, then the cross_lingual should be 5.
    If the input is that the model should have ability to handle various languages, then the cross_lingual should be 5.
    Here is an example input:
    Intent: I want to use a fast model that goes straight to the point. 
    Here is an example output:
    {'type': 'intent', 'result': {'low_memory': '1', 'low_latency': '5', 'accuracy': '1', 
    'precision': '1', 'recall': '1', 'cross_lingual': '1', 'low_verbosity': '5', 'much_explanation': '1'}, 
    'text': 'Intent: I want to use a fast model that goes straight to the point.'}
    ###
    Here is an example input:
    intent: I want my model to be very accurate and also consider the ground truth very well.
    I don't care about whether it's fast or slow or any other thing. 
    Here is an example output:
    {'type': 'intent', 'result': {'low_memory': '1', 'low_latency': '1', 'accuracy': '5', 
    'precision': '1', 'recall': '5', 'cross_lingual': '1', 'low_verbosity': '1', 'much_explanation': '1'}, 
    'text': 'intent: I want my model to be very accurate and also consider the ground truth very well.
    I don't care about whether it's fast or slow or any other thing.'}
    ###
    Here is an example input:
    intent, I am interacting with dataset in Spanish but I can only speak English. Please select a good model for me.
    Here is an example output:
    {'type': 'intent', 'result': {'low_memory': '1', 'low_latency': '1', 'accuracy': '1', 
    'precision': '1', 'recall': '1', 'cross_lingual': '5', 'low_verbosity': '1', 'much_explanation': '1'}, 
    'text': 'intent, I am interacting with dataset in Spanish but I can only speak English. Please select a good model for me.'}
    ###
    Here is an example input:
    intent please give me a model that is precise, I also want it not to consume too much RAM memory. 
    Here is an example output:
    {'type': 'intent', 'result': {'low_memory': '5', 'low_latency': '1', 'accuracy': '1', 
    'precision': '5', 'recall': '1', 'cross_lingual': '1', 'low_verbosity': '1', 'much_explanation': '1'}, 
    'text': 'intent please give me a model that is precise, I also want it not to consume too much RAM memory.'}
    ###
    Here is an example input:
    Intent: do u have any model that explains very well? the model can consume too much resources, i don't care.
    also, can the model retrieve good answers well from the true cases?
    Here is an example output:
    {'type': 'intent', 'result': {'low_memory': '1', 'low_latency': '1', 'accuracy': '1', 
    'precision': '1', 'recall': '5', 'cross_lingual': '1', 'low_verbosity': '1', 'much_explanation': '5'}, 
    'text': 'Intent: do u have any model that explains very well? the model can consume too much resources, i don't care.
    also, can the model retrieve good answers well from the true datasets?'}
    ###
    Here is an example input:
    Intent: do u have any model with very high verbosity?
    Here is an example output:
    {'type': 'intent', 'result': {'low_memory': '1', 'low_latency': '1', 'accuracy': '1', 
    'precision': '1', 'recall': '1', 'cross_lingual': '1', 'low_verbosity': '1', 'much_explanation': '5'}, 
    'text': 'Intent: do u have any model with very high verbosity?'}
    ###
    Here is an example input:
    how many productions have defect status 1? 
    Here is an example output:
    {'type': 'query', 'result': {}, 
    'text': 'how many productions have defect status 1?'}
    ###
    Here is an example input:
    Did any supplier receive more that one consulting contract?
    Here is an example output:
    {'type': 'query', 'result': {}, 
    'text': 'Did any supplier receive more that one consulting contract?'}
    ###
    Here is an example input:
    Which country had the most suppliers, maybe it’s better for my company to target such country?
    Here is an example output:
    {'type': 'query', 'result': {}, 
    'text': 'Which country had the most suppliers, maybe it’s better for my company to target such country?'}
    ###
    Here is an example input:
    What is this project about “Heat recovery from the Defense cold network to supply the Courbevoie (92) heating network”? 
    Here is an example output:
    {'type': 'query', 'result': {}, 
    'text': 'What is this project about “Heat recovery from the Defense cold network to supply the Courbevoie (92) heating network”?'}
    ###
    Here is an example input:
    I am interested in how much methanization is encouraged, so I need the list of the projects involving methanization. 
    Here is an example output:
    {'type': 'query', 'result': {}, 
    'text': 'I am interested in how much methanization is encouraged, so I need the list of the projects involving methanization. '}
    ###

    Here is the real input: """

    completing = """
    Now write the real output. Do not write an introduction or summary.
    Do not write any other thing aside the output in json:

    '{"type": "", "result": {}, "text": ""}'
    """

    all_text = examples + ask + completing
    generation = llama3.complete(all_text)
    # print(generation)
    json_obj = json.loads(generation.text)
    # json_obj = json.loads(generation)
    # json_obj = generation.text
    # print(json_obj['type'])
    print(json_obj)
    # if json_obj['type'] == 'harmonise':
    #    data_harmonise_fun(json_obj['file'])
    # print('intent accepted')
    # print(type(json_obj))
    return json_obj


