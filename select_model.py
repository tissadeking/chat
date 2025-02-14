import csv
import os
import numpy as np, pandas as pd


#get ratings from user preferences
def get_ratings(important_cols):
    df = pd.read_csv('model_ratings.csv')
    ratings = {}
    for j in range(len(df)):
        #cols = df.columns.tolist()
        cols = important_cols
        arr = []
        #for i in range(1, len(cols)):
        for i in range(len(cols)):
            x = df[cols[i]]
            arr.append(x[j])
        ratings[df['model'][j]] = arr
    #print('ratings: ', ratings)
    return ratings


#normalize the ratings to be between 0 and 1
def normalize_ratings(ratings):
    ratings_array = np.array(list(ratings.values()))
    #print('ratings array: ', ratings_array)
    normalized = ratings_array / ratings_array.max(axis=0)
    #print('normalised: ', normalized)
    return dict(zip(ratings.keys(), normalized))

#normalized_ratings = normalize_ratings(ratings)
#print('normalised ratings: ', normalized_ratings)
#get user preferences and compute weights
def compute_weights(preferences):
    total = sum(preferences)
    return [p / total for p in preferences]

#calculate weighted scores
def calculate_scores(normalized_ratings, weights):
    scores = {}
    #for each model, multiply each weight by its corresponding normalised rating
    #ie weight of latency in user_preference weights * normalised latency rating for each model
    #do the sum of the entire results for all multiplications
    for model, model_ratings in normalized_ratings.items():
        scores[model] = np.dot(model_ratings, weights)
    return scores

#rank the models
def rank_models(scores):
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

#function to get the top 2 models based on user preferences,
#if the user needs to select from best 2 models
def find_best_models(user_preferences, important_cols):
    weights = compute_weights(user_preferences)
    #print('weights: ', weights)
    ratings = get_ratings(important_cols)
    normalized_ratings = normalize_ratings(ratings)
    scores = calculate_scores(normalized_ratings, weights)
    #print('scores: ', scores)
    ranked_models = rank_models(scores)
    #print('ranked models: ', ranked_models)
    #return ranked_models[:2]
    return ranked_models[:2]

# Example: User preferences
# User wants high recall, low latency, and low verbosity
#user_preferences = [5, 1, 1, 1, 5, 1, 5]  # Latency, Memory, Accuracy, Precision, Recall, Cross-lingual, No Verbosity

def select_model_fun(user_selection):
    metrics_str = ['memory', 'latency', 'accuracy', 'precision', 'recall', 'cross', 'verbosity', 'much_explanation']
    user_preferences = []
    important_cols = []
    '''for key in user_selection:
        if int(user_selection[key]) == 5:
            important_cols.append(key)
            user_preferences.append(int(user_selection[key]))'''
    for i in range(len(user_selection.keys())):
        selected_rating = (list(user_selection.values())[i])
        if int(selected_rating) == 5:
            important_cols.append(metrics_str[i])
            user_preferences.append(int(selected_rating))
    # Find the best models
    best_models = find_best_models(user_preferences, important_cols)
    selected_model = best_models[0][0]
    print(best_models[0][0])
    if os.path.isfile("model.txt"):
        f = open("model.txt", "r+")
        f.truncate()
        f.write(selected_model)
        f.close()
    else:
        f = open("model.txt", "a")
        f.write(selected_model)
        f.close()
    return selected_model

