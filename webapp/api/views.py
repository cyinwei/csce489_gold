from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import os
import json
import re
import pickle
import pandas as pd
import time


'''
Global variable, such as classifiers that will not change.
Will need to load all 3 for each subreddit (30 in total)
Yikes!
'''
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'baz.txt')

# TODO: Update location of classifiers after they are complete
with open(os.path.join(module_dir, "./classifiers/tfidf_vectorizer.pickle"),'rb') as f:
    tfloaded = pickle.load(f) # imports classifier from file

with open(os.path.join(module_dir, "./classifiers/kmeans_clustering.pickle"),'rb') as f:
    kmloaded = pickle.load(f) # imports classifier from file

with open(os.path.join(module_dir, "./classifiers/forest_classifier.pickle"),'rb') as f:
    frloaded = pickle.load(f) # imports classifier from file


# Create your views here.

def index(req):
    res = '''You\'ve  reached the API. Congrats!
             This is where we would do our classifier calculation and just return the answer for the website to display.
             Super simple, huh?'''
    return HttpResponse(content=res, status=200)

@require_POST
@csrf_exempt
def analyze(req):
    # Read in inputs from request
    res = {}
    res['comment'] = req.POST['comment']
    res['subreddit'] = req.POST['subreddit']
    res['datetime'] = int(time.time())
    res['wordcount'] = len(re.findall("\S+", req.POST['comment']))

    # Create datafram
    # TODO: Remove hard coded data (such as 'Contains MD') and let munger infer it
    df = pd.DataFrame.from_dict({'body': [res['comment']], 'created_utc': [int(time.time())], 'Word Count': [res['wordcount']], 'Time of Day': [1], 'Contains MD': True})

    # Munge Data
    # TODO: Need to import munger package after completion
    # df = mg.munge_dataset(df)
    # df['Time of Day'] = df['Time of Day'].map({'Afternoon': 1,'Evening': 2,'Night': 3,'Morning': 4})

    # Create TFIDF vector from body
    tfidf = tfloaded.transform(df['body'])

    # Cluster from TFIDF and put into dataframe
    df['cluster'] = kmloaded.predict(tfidf)

    # Calssify with forest classifier
    res['gilded?'] = str(frloaded.predict(df[['Contains MD', 'Word Count', 'Time of Day', 'cluster']])[0])

    # Respond with our conclusion
    return HttpResponse(json.dumps(res), content_type="application/json")