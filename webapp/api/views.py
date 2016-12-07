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
        'Grammer Errors',
        'Sentiment Positive',
        'Watson Anger',
        'Watson Disgust',
        'Watson Fear',
        'Watson Joy',
        'Watson Openness',
        'Watson Conscientiousness',
        'Watson Extraversion',
        'Watson Agreeableness',
        'Watson Emotional Range',
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def askreddit(df):
    with open(os.path.join(module_dir, "./classifiers/AskReddit_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Word Count',
        'Time of Day',
        'watson cluster',
        'body cluster',
        'Grammer Errors',
        'Sentiment Negative',
        'Sentiment Positive',
        'Sentiment Neutral',
        'Watson Anger',
        'Watson Disgust',
        'Watson Fear',
        'Watson Joy',
        'Watson Sadness',
        'Watson Tenative',
        'Watson Openness',
        'Watson Conscientiousness',
        'Watson Extraversion',
        'Watson Agreeableness',
        'Watson Emotional Range'
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def funny(df):
    with open(os.path.join(module_dir, "./classifiers/funny_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Contains MD',
        'Word Count',
        'body cluster',
        'Grammer Errors',
        'Sentiment Neutral',
        'Watson Anger',
        'Watson Joy',
        'Watson Sadness',
        'Watson Extraversion',
        'Watson Agreeableness',
        'Watson Emotional Range',
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def news(df):
    with open(os.path.join(module_dir, "./classifiers/news_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Word Count',
        'Watson Openness'
    ]


    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def nfl(df):
    with open(os.path.join(module_dir, "./classifiers/nfl_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Contains MD',
        'Word Count',
        'Time of Day',
        'watson cluster',
        'body cluster',
        'Grammer Errors',
        'Sentiment Label',
        'Sentiment Negative',
        'Sentiment Positive',
        'Sentiment Neutral',
        'flair',
        'Watson Anger',
        'Watson Disgust',
        'Watson Fear',
        'Watson Joy',
        'Watson Sadness',
        'Watson Analytical',
        'Watson Confident',
        'Watson Tenative',
        'Watson Openness',
        'Watson Conscientiousness',
        'Watson Extraversion',
        'Watson Agreeableness',
        'Watson Emotional Range',
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def pics(df):
    with open(os.path.join(module_dir, "./classifiers/pics_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Contains MD',
        'Word Count',
        'Time of Day',
        'watson cluster',
        'body cluster',
        'Grammer Errors',
        'Sentiment Label',
        'Sentiment Negative',
        'Sentiment Positive',
        'Sentiment Neutral',
        'Watson Anger',
        'Watson Disgust',
        'Watson Fear',
        'Watson Joy',
        'Watson Sadness',
        'Watson Analytical',
        'Watson Confident',
        'Watson Tenative',
        'Watson Openness',
        'Watson Conscientiousness',
        'Watson Extraversion',
        'Watson Agreeableness',
        'Watson Emotional Range',
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def todayilearned(df):
    with open(os.path.join(module_dir, "./classifiers/todayilearned_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Word Count',
        'body cluster',
        'Sentiment Negative',
        'Sentiment Positive',
        'Sentiment Neutral',
        'Watson Fear',
        'Watson Joy',
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def videos(df):
    with open(os.path.join(module_dir, "./classifiers/videos_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Word Count',
        'body cluster',
        'Grammer Errors',
        'Watson Disgust',
        'Watson Fear',
        'Watson Joy',
        'Watson Sadness',
        'Watson Openness',
        'Watson Agreeableness'
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def worldnews(df):
    with open(os.path.join(module_dir, "./classifiers/worldnews_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Contains MD',
        'Word Count',
        'Time of Day',
        'watson cluster',
        'body cluster',
        'Grammer Errors',
        'Sentiment Label',
        'Sentiment Negative',
        'Sentiment Positive',
        'Sentiment Neutral',
        'flair',
        'Watson Anger',
        'Watson Disgust',
        'Watson Fear',
        'Watson Joy',
        'Watson Sadness',
        'Watson Analytical',
        'Watson Confident',
        'Watson Tenative',
        'Watson Openness',
        'Watson Conscientiousness',
        'Watson Extraversion',
        'Watson Agreeableness',
        'Watson Emotional Range'
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


def wtf(df):
    with open(os.path.join(module_dir, "./classifiers/WTF_classifier.pickle"),'rb') as f:
        forest = pickle.load(f) # imports classifier from file

    features = [
        'Score Bracket',
        'Word Count',
        'body cluster',
        'Grammer Errors',
        'Sentiment Positive',
        'Watson Anger',
        'Watson Disgust',
        'Watson Fear',
        'Watson Joy',
        'Watson Openness',
        'Watson Conscientiousness',
        'Watson Extraversion',
        'Watson Agreeableness',
        'Watson Emotional Range',
    ]

    return {'features': features, 'prediction': str(forest.predict(df[features])[0])}


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

    # Create datafram
    df = pd.DataFrame.from_dict({
        'body': [req.POST['comment']],
        'subreddit': [req.POST['subreddit']],
        'created_utc': [int(time.time())],
        'score': [int(req.POST['score'])],
        'author_flair_css_class': [str(req.POST['flair'])]
    })

    # Munge Data
    try:
        df = mg.munge_dataset(df, badwords, 'user', 'password')
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
        pred = adviceanimals(df)
    elif req.POST['subreddit'] == 'AskReddit':
        pred = askreddit(df)
    elif req.POST['subreddit'] == 'funny':
        pred = funny(df)
    elif req.POST['subreddit'] == 'news':
        pred = news(df)
    elif req.POST['subreddit'] == 'nfl':
        pred = nfl(df)
    elif req.POST['subreddit'] == 'pics':
        pred = pics(df)
    elif req.POST['subreddit'] == 'todayilearned':
        pred = todayilearned(df)
    elif req.POST['subreddit'] == 'videos':
        pred = videos(df)
    elif req.POST['subreddit'] == 'worldnews':
        pred = worldnews(df)
    elif req.POST['subreddit'] == 'WTF':
        pred = wtf(df)
    else:
        return HttpResponse('Not a valid subreddit')

    # Pull out prediction and relevant features
    for value in pred['features']:
        res[value] = str(df[value][0])
    res['prediction'] = pred['prediction']

    # Respond with our conclusion
    return HttpResponse(json.dumps(res), content_type="application/json")