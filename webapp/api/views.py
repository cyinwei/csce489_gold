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
import sys
from scripts import Munger as mg

'''
Global variable, such as classifiers that will not change.
'''
module_dir = os.path.dirname(__file__)  # get current directory

badwords = pd.read_csv(os.path.join(module_dir, 'etc/Terms-to-Block.csv'))['Word']

with open(os.path.join(module_dir, "./classifiers/tfidf_vectorizer.pickle"),'rb') as f:
    tfloaded = pickle.load(f) # imports classifier from file

with open(os.path.join(module_dir, "./classifiers/watson_clusterer.pickle"),'rb') as f:
    watsonloaded = pickle.load(f) # imports classifier from file

with open(os.path.join(module_dir, "./classifiers/body_clusterer.pickle"),'rb') as f:
    kmloaded = pickle.load(f) # imports classifier from file


'''
Subreddit specific functions
'''

def adviceanimals(df):
    with open(os.path.join(module_dir, "./classifiers/AdviceAnimals_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Word Count',
        'body cluster',
        'Watson Disgust',
        'Watson Joy',
        'Watson Agreeableness'
    ]

    return str(forest.predict(df[features])[0])


def askreddit(df):
    with open(os.path.join(module_dir, "./classifiers/AskReddit_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Word Count',
        'Sentiment Neutral',
        'Watson Disgust',
        'Watson Sadness',
        'Watson Agreeableness'
    ]

    return str(forest.predict(df[features])[0])


def funny(df):
    with open(os.path.join(module_dir, "./classifiers/funny_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
    ]

    return str(forest.predict(df[features])[0])


def news(df):
    with open(os.path.join(module_dir, "./classifiers/news_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
    ]

    return str(forest.predict(df[features])[0])


def nfl(df):
    with open(os.path.join(module_dir, "./classifiers/nfl_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
    ]

    return str(forest.predict(df[features])[0])


def pics(df):
    with open(os.path.join(module_dir, "./classifiers/pics_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
    ]

    return str(forest.predict(df[features])[0])


def todayilearned(df):
    with open(os.path.join(module_dir, "./classifiers/todayilearned_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
    ]

    return str(forest.predict(df[features])[0])


def videos(df):
    with open(os.path.join(module_dir, "./classifiers/videos_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
    ]

    return str(forest.predict(df[features])[0])


def worldnews(df):
    with open(os.path.join(module_dir, "./classifiers/worldnews_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
    ]

    return str(forest.predict(df[features])[0])


def wtf(df):
    with open(os.path.join(module_dir, "./classifiers/WTF_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
    ]

    return str(forest.predict(df[features])[0])


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

    # Create datafram
    df = pd.DataFrame.from_dict({'body': [res['comment']], 'created_utc': [int(time.time())], 'score': [int(req.POST['score'])]})

    # Munge Data
    try:
        df = mg.munge_dataset(df, badwords, 'a9b99375-b559-4e7e-a033-25c8ae178c6e', 'RRSUytaQ3nMz')
    except:
        return HttpResponse(content="Unexpected error:" + str(sys.exc_info()[0]))

    # Create TFIDF vector from body
    tfidf = tfloaded.transform(df['body'])

    # Cluster from TFIDF and put into dataframe
    df['body cluster'] = kmloaded.predict(tfidf)

    # Cluster Watson analysis and put into dataframe
    watson = ['Watson Anger', 'Watson Disgust', 'Watson Fear',
            'Watson Joy', 'Watson Sadness', 'Watson Analytical',
            'Watson Confident', 'Watson Tenative', 'Watson Openness',
            'Watson Conscientiousness', 'Watson Extraversion',
            'Watson Agreeableness', 'Watson Emotional Range']
    df['watson cluster'] = watsonloaded.predict(df[watson].values)

    # Determine which classifiers to use
    if req.POST['subreddit'] == 'AdviceAnimals':
        res['gilded?'] = adviceanimals(df)
    elif req.POST['subreddit'] == 'AskReddit':
        res['gilded?'] = askreddit(df)
    elif req.POST['subreddit'] == 'funny':
        res['gilded?'] = funny(df)
    elif req.POST['subreddit'] == 'news':
        res['gilded?'] = news(df)
    elif req.POST['subreddit'] == 'nfl':
        res['gilded?'] = nfl(df)
    elif req.POST['subreddit'] == 'pics':
        res['gilded?'] = pics(df)
    elif req.POST['subreddit'] == 'todayilearned':
        res['gilded?'] = todayilearned(df)
    elif req.POST['subreddit'] == 'videos':
        res['gilded?'] = videos(df)
    elif req.POST['subreddit'] == 'worldnews':
        res['gilded?'] = worldnews(df)
    elif req.POST['subreddit'] == 'WTF':
        res['gilded?'] = wtf(df)
    else:
        return HttpResponse('Not a valid subreddit')

    # Respond with our conclusion
    return HttpResponse(json.dumps(res), content_type="application/json")