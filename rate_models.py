import csv
import os

import numpy as np
import pandas as pd

def rate_models_fun():
    #define the models and their ratings
    models = ["llama3-8b", "mixtral-8x7b", "gemma2-9b", "llama-3.3-70b"]
    memory = [183885.96296296295, 40406.81481481482, 32422.777777777777, 32662.51851851852]
    latency = [0.7799112178661205, 5.557156015325476, 0.48837983166729965, 1.2431185333817094]
    accuracy = [0.55, 0.46, 0.61, 0.82]
    precision = [0.8, 0.769, 0.8, 1]
    recall = [0.533, 0.667, 0.533, 0.8]
    cross = [0.56, 0.46, 0.9, 0.88]
    verbosity = [369.8888888888889, 357.5925925925926, 62.629629629629626, 454.9259259259259]
    much_explanation = [369.8888888888889, 357.5925925925926, 62.629629629629626, 454.9259259259259]

    metrics_used = [memory, latency, accuracy, precision, recall, cross, verbosity, much_explanation]
    metrics_str = ['memory', 'latency', 'accuracy', 'precision', 'recall', 'cross', 'verbosity', 'much_explanation']
    metrics_dict = {}
    for i in range(len(metrics_used)):
        metric_rating = []
        metric = metrics_used[i]
        #print('metric: ', metric)
        metric_str = metrics_str[i]
        max_num = max(metric)
        #print('max: ', max_num)
        min_num = min(metric)
        #print('min: ', min_num)
        range_num = max_num - min_num
        for j in range(len(metric)):
            if metric_str == 'memory' or metric_str == 'latency' or metric_str == 'verbosity':
                rating = 5 - ((metric[j] - min_num)/range_num) * 4
            else:
                rating = 1 + ((metric[j] - min_num)/range_num) * 4
            metric_rating.append(rating)
        #print('metric_rating: ', metric_rating)
        metrics_dict[metric_str] = metric_rating
    #print('metrics dict:', metrics_dict)
    ratings = {}
    file_name = 'model_ratings.csv'
    columns = ['model', 'memory', 'latency', 'accuracy', 'precision', 'recall', 'cross', 'verbosity', 'much_explanation']

    for j in range(len(models)):
        data_dict = {}
        data_dict['model'] = models[j]
        arr = []
        #for i in range(len(metrics_dict.keys())):
        for i in range(len(metrics_str)):
            x = metrics_dict[metrics_str[i]]
            data_dict[metrics_str[i]] = x[j]
            arr.append(x[j])
        ratings[models[j]] = arr
        #print('data dict: ', data_dict)
        if os.path.exists(file_name) == True:
            with open(file_name, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writerow(data_dict)
        elif os.path.exists(file_name) == False:
            with open(file_name, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                writer.writerow(data_dict)
    print('ratings: ', ratings)
    print('models rating completed')
